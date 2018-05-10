import re
# import nltk
import nltk as nltk

from .title_word_list import title_map, profile_words, category_map
from .feature_pattern_utils import get_feature_pattern
from .split_utils import split_by_font_style

def _preprocessing_text(text):
    text = text.upper()
    text = text.replace(".", " ")
    text = text.replace("/", " ")
    text = text.replace("(", "")
    text = text.replace(")", "")
    text = text.replace(":", " ")
    text = text.replace("-", " ")
    text = text.replace(",", " ")
    text = text.replace("<", " ")
    text = text.replace(">", " ")
    text = text.replace("&", " ")
    text = text.replace("[", " ")
    text = text.replace("]", " ")
    text = text.replace("!", " ")
    text = text.strip()
    return text

def title_percent(text):
    text = _preprocessing_text(text)
    words = text.split()
    percent_dict = dict()
    for category, group_words in title_map.items():
        not_important_words = []
        num_words = 0
        for word in words:
            if word in ["AND", "OR", "OF", ""] or word.isnumeric() is True:
                not_important_words.append(word)
                continue
            if word in group_words:
                num_words += 1 * group_words[word]
        for word in not_important_words:
            words.remove(word)
        if len(words) == 0:
            return dict()
        else:
            percent = (num_words * 100) / len(words)
        percent_dict[category] = percent
    return percent_dict

def _get_max_key(a_dict):
    key, _ = max(a_dict.items(), key=lambda x:x[1])
    return key

def _get_x_y(line):
    x = line.get('cen')[0]
    y = line.get('cen')[1]
    return x, y 

def _get_font_style(line):
    full_text = line.get('full_text')
    if "__BoldStart__" in full_text:
        return "bold"
    if "__ItalicStart__" in full_text:
        return "italic"
    if "__BoldItalicStart__" in full_text:
        return "bolditalic"
    return "normal"

def detect_title(line_objs):
    result = []
    title_lines = {}
    chosen_line_marg=[]
    for line in line_objs:
        is_lower = False
        text = line.get('text')
        words = text.split()
        for word in words:
            if word.islower():
                is_lower = True
        if is_lower:
            continue
        text = _preprocessing_text(text)
        text = text.replace(":", " ").strip()
        text = ' '.join(text.split())
        is_text_lower = text.islower()
        is_text_upper = text.isupper()
        is_text_title = text.istitle()



        if text.upper() in category_map['experience'] and not is_text_lower:
            line['label'] = 'title'
            line['category'] = 'experience'
            result.append('experience')
            title_lines['experience'] = line
            chosen_line_marg.append((line.get('cen')[0],line.get('cen')[0] + line.get('wh')[0]//2))
            continue
        if text.upper() in category_map['education'] and not is_text_lower:
            line['label'] = 'title'
            line['category'] = 'education'
            result.append('education')
            title_lines['education'] = line
            chosen_line_marg.append((line.get('cen')[0], line.get('cen')[0] + line.get('wh')[0] // 2))
            continue
        if text.upper() in category_map['skill'] and not is_text_lower:
            line['label'] = 'title'
            line['category'] = 'skill'
            result.append('skill')
            continue

        # Fix case word split by blank space
        fix_text = text.replace(" ", "")
        if fix_text.upper() in [line.replace(" ", "") for line in category_map['experience']] and not fix_text.islower():
            print(fix_text)
            line['label'] = 'title'
            line['category'] = 'experience'
            result.append('experience')
            title_lines['experience'] = line
            chosen_line_marg.append((line.get('cen')[0],line.get('cen')[0] + line.get('wh')[0]//2))
            continue
        if fix_text.upper() in [line.replace(" ", "") for line in category_map['education']] and not fix_text.islower():
            line['label'] = 'title'
            line['category'] = 'education'
            result.append('education')
            title_lines['education'] = line
            chosen_line_marg.append((line.get('cen')[0], line.get('cen')[0] + line.get('wh')[0] // 2))
            continue
        if fix_text.upper() in [line.replace(" ", "") for line in category_map['skill']] and not fix_text.islower():
            line['label'] = 'title'
            line['category'] = 'skill'
            result.append('skill')
            continue

        font_style = _get_font_style(line)
        percent_dict = title_percent(text)
        if not percent_dict:
            continue
        category = _get_max_key(percent_dict)
        if category == 'experience' or category == 'education':
            score = 0
            percent = percent_dict[category]
            if percent < 100:
                continue
            if percent >= 100:
                score += 1
            if percent >= 150:
                score += 1
            if percent >= 200:
                score += 1
            if is_text_lower:
                score -= 1
            if is_text_upper:
                score += 1
            if font_style != 'normal':
                score += 1
            if score >= 2 and text.upper() not in category_map['other']: # and pass_marg:
                line['label'] = 'title'
                line['category'] = category
                if category not in title_lines:
                    title_lines[category] = line
                result.append(category)
    
    # Fix title have content
    for line in line_objs:
        is_split = False
        text = line.get('text')
        full_text = line.get('full_text')
        label = line.get('label')
        if label == 'title':
            continue
        for c in [": ", "   "]:
            parts = text.split(c)
            if len(parts) > 1:
                part_text = parts[0].strip()
                for category in ['experience', 'education', 'skill']:
                    if part_text.upper() in category_map[category] and not part_text.islower():
                        print("TITLE in line ", text, category)
                        line['label'] = 'title-in-line'
                        line['category'] = category
                        line['text'] = text.replace(part_text, "")
                        for i in split_by_font_style(full_text):
                            if part_text in i:
                                line['full_text'] = full_text.replace(part_text, '')
                        result.append(category)
                        is_split = True
                        break
                if is_split:
                    continue

    
    exp_left_margin, exp_height, exp_font_style, exp_center, is_exp_upper = None, None, None, None, False
    edu_left_margin, edu_height, edu_font_style, edu_center, is_edu_upper = None, None, None, None, False
    exp_title_lines = title_lines.get('experience')
    if exp_title_lines:
        exp_text = exp_title_lines.get('text')
        is_exp_upper = exp_text.isupper()
        #exp_line = exp_title_lines[0]
        exp_left_margin = exp_title_lines.get('cen')[0]
        exp_height = exp_title_lines.get('wh')[1]
        exp_center = exp_left_margin + exp_title_lines.get('wh')[0] // 2
        exp_font_style = _get_font_style(exp_title_lines)
    edu_title_lines = title_lines.get('education')
    if edu_title_lines:
        edu_text = edu_title_lines.get('text')
        is_edu_upper = edu_text.isupper()
        #edu_line = edu_title_lines[0]
        edu_left_margin = edu_title_lines.get('cen')[0]
        edu_height = edu_title_lines.get('wh')[1]
        edu_center = edu_left_margin + edu_title_lines.get('wh')[0] // 2
        edu_font_style = _get_font_style(edu_title_lines)

    for line in line_objs:
        text = line.get('text')
        parts = text.split()
        if parts[0] in ["&", "-", "/"]:
            continue
        label = line.get('label')
        if label:
            continue
        percent_dict = title_percent(text)
        if not percent_dict:
            continue
        category = _get_max_key(percent_dict)
        if category != 'experience' and category != 'education':
            score = 0
            percent = percent_dict[category]
            if percent >= 100:
                score += 1
            if percent >= 150:
                score += 1
            if percent >= 200:
                score += 1
            if percent < 100:
                continue
            is_text_upper = text.isupper()
            if is_edu_upper:
                if is_text_upper == is_edu_upper:
                    score += 1
            if is_exp_upper:
                if is_text_upper == is_exp_upper:
                    score += 1
            if text.islower():
                continue
            left_margin, _ = _get_x_y(line)
            height = line.get('wh')[1]
            center = left_margin + line.get('wh')[0]
            if exp_left_margin:
                if abs(left_margin - exp_left_margin) < 2:
                    score += 1
            if edu_left_margin:
                if abs(left_margin - edu_left_margin) < 2:
                    score += 1
            if exp_center:
                if abs(center - exp_center) < 2:
                    score += 1
            if edu_center:
                if abs(center - edu_center) < 2:
                    score += 1
            font_style = _get_font_style(line)
            if exp_font_style:
                if font_style == exp_font_style:
                    score += 1
            if edu_font_style:
                if font_style == edu_font_style:
                    score += 1
            if font_style != exp_font_style and font_style != edu_font_style:
                if font_style != 'normal':
                    score += 1
                else:
                    score -= 1
            if exp_height:
                if height >= exp_height:
                    score += 1
            if edu_height:
                if height >= edu_height:
                    score += 1
            if score > 5:
                line['label'] = 'title'
                line['category'] = category
                result.append(category)

    for title in result:
        if title not in ['experience', 'education', 'skill'] and result.count(title) > 1:
            track = []
            texts = []
            for idx, line in enumerate(line_objs):
                text = line.get('text')
                label = line.get('label')
                category = line.get('category')
                if label == 'title' and category == title:
                    track.append(idx)
                    texts.append(text)
            track2 = track[:]
            for idx, text in zip(track, texts):
                if texts.count(text) > 1:
                    del line_objs[idx]['label']
                    del line_objs[idx]['category']
                    print("Unlabel title", text)
                    track2.remove(idx)
                    result.remove(title)
            

    if "personal_info" not in result:
        result.append("personal_info")
    print("======== ALL TITLES", result)
    for line in line_objs:
        text = line.get('text')
        label = line.get('label')
        category = line.get('category')
        if label == 'title' or label == 'title-in-line':
            print(text, label, category)
    return result

def get_personal_info(line_objs):
    """
    Return all lines about personal info
    """
    result = []
    start = True
    for line in line_objs:
        line_label = line.get('label')
        line_category = line.get('category')
        if line_label == 'title':
            if line_category == 'personal_info':
                start = True
                continue
            else:
                start = False
        if start:
            result.append(line)
    try:
        max_height = max([line.get('wh')[1] for line in result])
    except:
        max_height = max([line.get('wh')[1] for line in line_objs])
    track_candicate_name = False
    for line in result:
        height = line.get('wh')[1]
        if height == max_height and not track_candicate_name:
            for word in profile_words.keys():
                if word in line.get("text"):
                    continue
                line['label'] = 'candicate_name'
                track_candicate_name = True
        else:
            line['label'] = 'description'
        line['category'] = 'personal_info'
    return result

def get_experience_data(line_objs):
    """
    Return all lines in category
    """
    result = []
    tmp = []
    start = False
    title_in_line = False
    for idx, line in enumerate(line_objs):
        if line.get('footer'):
            print("ignore footer line")
            continue
        line_label = line.get('label')
        line_category = line.get('category')
        if line_label == 'title':
            if line_category == 'experience':
                start = True
                continue
            else:
                start = False
        if line_label == 'title-in-line':
            if line_category == 'experience':
                start = True
            else:
                start = False
        if start:
            tmp.append(line)
        else:
            if tmp:
                result.append(tmp)
                tmp = []
        if idx == len(line_objs) - 1:
            if tmp:
                result.append(tmp)

    for tmp in result:
        for idx, line in enumerate(tmp):
            if idx > 0:
                prev_line = tmp[idx-1]
            else:
                prev_line = None
            if prev_line:
                line_x, line_y = _get_x_y(line)
                prev_line_x, prev_line_y = _get_x_y(prev_line)
                if line_y == prev_line_y:
                    line['cen'] = [prev_line_x, line_y]
                    print("changed x")

    for tmp in result:
        sorted_x = sorted([line.get('cen')[0] for line in tmp])
        min_left_margin = sorted_x[0]
        max_left_margin = sorted_x[-1]
        for line in tmp:
            pattern_feature = get_feature_pattern(line, min_left_margin, max_left_margin)
            line['pattern_feature'] = pattern_feature
    return result


def get_education_data(line_objs):
    """
    Return all lines in category
    """
    result = []
    tmp = []
    start = False
    for idx, line in enumerate(line_objs):
        if line.get('footer'):
            print("ignore footer line")
            continue
        line_label = line.get('label')
        line_category = line.get('category')
        if line_label == 'title':
            if line_category == 'education':
                start = True
                continue
            else:
                start = False
        if line_label == 'title-in-line':
            if line_category == 'education':
                start = True
            else:
                start = False
        if start:
            tmp.append(line)
        else:
            if tmp:
                result.append(tmp)
                tmp = []
    if idx == len(line_objs) - 1:
        if tmp:
            result.append(tmp)

    for tmp in result:
        for idx, line in enumerate(tmp):
            if idx > 0:
                prev_line = tmp[idx-1]
            else:
                prev_line = None
            if prev_line:
                line_x, line_y = _get_x_y(line)
                prev_line_x, prev_line_y = _get_x_y(prev_line)
                if line_y == prev_line_y:
                    line['cen'] = [prev_line_x, line_y]
                    print("changed x")

    for tmp in result:
        sorted_x = sorted([line.get('cen')[0] for line in tmp])
        min_left_margin = sorted_x[0]
        max_left_margin = sorted_x[-1]
        for line in tmp:
            pattern_feature = get_feature_pattern(line, min_left_margin, max_left_margin)
            line['pattern_feature'] = pattern_feature
    return result


def get_category_data(line_objs, category):
    """
    Return all lines in category
    """
    result = []
    start = False
    for line in line_objs:
        line_label = line.get('label')
        line_category = line.get('category')
        if line_label == 'title':
            if line_category == category:
                start = True
                continue
            else:
                start = False
        if start:
            line['label'] = 'description'
            line['category'] = category
            result.append(line)
    return result

def extract_document(line_objs):
    result = dict()
    all_titles = set(detect_title(line_objs))
    line_objs, _ = _merge_lines(line_objs)
    for title in all_titles:
        if title == 'personal_info':
            data = get_personal_info(line_objs)
        elif title == 'experience':
            data = get_experience_data(line_objs)
        elif title == 'education':
            data = get_education_data(line_objs)
        else:
            data = get_category_data(line_objs, title)
        result[title] = data
    return result

def have_time(text):
    time_patterns = [
        r'\d{1,2}[\/\-., \(]?\d{1,2}[\/\-., \)]?\d{2,4}',
        r'\d{0,4}[\/\-., \(]?(Jan|Feb|Mar|Apr|May|June|July|Aug|Sep|Oct|Nov|Dec)\S{0,6}[\/\-., \)]?\d{0,4}'
    ]
    for pattern in time_patterns:
        m = re.search(pattern, text)
        if m:
            return True
    return False

def _merge_lines(line_objs):
    def is_bullet(char):
        return ord(char) >= 128 or char in ["-","*", "#", "!", "@", "$", "%", "^", "&", "(", ")", "+", ":", ";", "<", ">", ","]
    pdf_lines = line_objs[:]
    merge_lines_idx = []
    tmp  = []
    last_char_tag_prev_line = ""
    prev_label = None
    last_char_prev_line = ""
    for idx, line in enumerate(pdf_lines):
        text = line.get('bullet') + ' ' + line.get('text')
        text = text.strip()
        text_length = len(text.split())
        first_char = text[:1]
        if is_bullet(first_char) is False and (first_char.islower() or last_char_tag_prev_line in ['CC','DT','IN','MD','TO',',']) \
            and text_length < 7 and prev_label != 'title' \
            and last_char_prev_line in ['am', 'is', 'are', 'was', 'were', 'be', 'being', 'been']:
            tmp.append(idx)
        else:
            if len(tmp) == 0:
                tmp.append(idx)
            else:
                merge_lines_idx.append(tmp)
                tmp = [idx]

        tokens = nltk.word_tokenize(text)
        pos_tags = nltk.pos_tag(tokens)
        last_char_tag_prev_line = pos_tags[-1:][0][1]
        last_char_prev_line = text.split()[-1].strip()
        prev_label = line.get('label')

    if len(tmp) > 0:
        merge_lines_idx.append(tmp)

    result = []
    for idx_list in merge_lines_idx:
        if len(idx_list) == 1:
            idx = idx_list[0]
            result.append(pdf_lines[idx])
        else:
            first_idx = idx_list[0]
            first_line = pdf_lines[first_idx]
            text = ' '.join([pdf_lines[i].get('text') for i in idx_list])
            full_text = ' '.join([pdf_lines[i].get('full_text') for i in idx_list])
            first_line['text'] = text
            first_line['full_text'] = full_text
            result.append(first_line)
    
    return result, merge_lines_idx

