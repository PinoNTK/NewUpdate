from pdfminer.pdfparser import PDFParser, PDFDocument
# from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTLayoutContainer
import pdfminer.layout as lt
import numpy as np
import os
import codecs
from sklearn.cluster import DBSCAN
from binascii import b2a_hex
from recruitment_recommender_system.settings import BASE_DIR, MEDIA_ROOT

from . import utils_nlp
from .utils_opencv import detect_face
from .title_word_list import category_map
from .utils_nlp import preprocessing_text
from .title_list import title_list


dir_temp = os.path.join(MEDIA_ROOT, 'images')


class PDFObject(object):
    '''Creates a point on a coordinate plane with values x and y.'''

    def __init__(self, type, x0, y0, x1, y1, text='', font_style=None, font_size=None, font_name=None, margin=[5,5,5,5],neighbours=['pad','pad','pad','pad']):
        '''Defines x and y variables'''
        if x0 > x1:
            t = x0
            x0 = x1
            x1 = t
        if y0 > y1:
            t = y0
            y0 = y1
            y1 = t
        self.type = type
        self.x0 = round(x0)
        self.y0 = round(y0)
        self.x1 = round(x1)
        self.y1 = round(y1)
        self.w = self.x1-self.x0
        self.h = self.y1-self.y0
        self.x_cen = round((x0 + x1) / 2)
        self.y_cen = round((y0 + y1) / 2)
        self.text = text
        self.font_style = font_style
        self.font_size = font_size
        self.font_name = font_name
        self.margin=margin
        self.neighbours = neighbours
        self.is_title = False
        if text != None:
            self.title = title_list.get(utils_nlp.clean_title(text), None)
            if self.title != None:
                self.is_title = True
        else:
            self.title = None
        self.is_vertical = self.x1 - self.x0 < self.y1 - self.y0

    def __str__(self):
        return ""+'_'.join(self.text.split())

    def check(self, x, y):
        return (abs(self.x0 - x) < 2 and abs(self.y0 - y) < 2) or (abs(self.x1 - x) < 2 and abs(self.y1 - y) < 2)


def get_font(textline):
    assert isinstance(textline, lt.LTTextLine)
    for o in textline._objs:
        return o.fontname


def get_size(textline):
    assert isinstance(textline, lt.LTTextLine)
    for o in textline._objs:
        return o.size


def get_textbox_font_size(textbox):
    assert isinstance(textbox, lt.LTTextBox)
    for o in textbox._objs:
        return [get_font(o), get_size(o)]


def is_upper(text):
    for c in text:
        if c.islower():
            return False
    return True


def is_int(text):
    try:
        int(text)
        return True
    except:
        return False


def is_index_page(textline):
    assert isinstance(textline, lt.LTTextLine)
    if textline.y0 < 50 and is_int(textline.get_text()):
        return True
    return False


def get_text_from_textline(textline):
    assert isinstance(textline, lt.LTTextLine)
    txt = ''
    for c in textline._objs:
        if isinstance(c, lt.LTChar) and c.fontname.split(',')[0].lower() != 'symbol':
            txt += c.get_text()
    return txt


def parse_textline(textline):
    assert isinstance(textline, lt.LTTextLine)
    text = get_text_from_textline(textline).strip()
    font = get_font(textline).split(',')
    if len(font) > 1:
        style = font[1]
    else:
        style = 'Normal'
    font = font[0]
    size = get_size(textline)
    x0 = round(textline.x0)
    x1 = round(textline.x1)
    y0 = round(textline.y0)
    y1 = round(textline.y1)

    return PDFObject('TextLine', x0, y0, x1, y1, text=text, font_name=font, font_size=size,
                     font_style=style)  # [text, font, style, size, x0, x1, y0, y1]


def histogram(_objs, width, height):
    max_x = width
    max_y = height
    for obj in _objs:
        if obj.x1 > max_x:
            max_x = obj.x1
        if obj.y1 > max_y:
            max_y = obj.y1
    hx = np.zeros(max_x + 2)
    hy = np.zeros(max_y + 2)
    for obj in _objs:
        for i in range(obj.x0, obj.x1):
            hx[i] += 1
        for i in range(obj.y0, obj.y1):
            hy[i] += 1
    return hx, hy


def find_threshold(histogram, n=2):
    t = n
    x = []
    for i in range(len(histogram)):
        if histogram[i] < t:
            x.append([i])
    #     print(x)
    _dbscan = DBSCAN(eps=5, min_samples=10)
    _dbscan.fit(x)
    lb = _dbscan.labels_
    cluster = []
    for i in range(max(lb) + 1):
        c = 0
        s = 0
        for j in range(len(x)):
            if lb[j] == i:
                c += 1
                s += j
        if c > 0:
            cluster.append(s / c)
    return cluster


def find_threshold_y(histogram):
    x = []
    for i in range(len(histogram)):
        if histogram[i] < 1:
            x.append(i)
    threshold = [0]
    pre_y = 0
    w = 0
    for i in range(1, len(x)):
        if x[i] - x[i - 1] < 2:
            w += x[i] - x[i - 1]
        else:
            if (x[i] - x[i - 1] + pre_y) / 2 < 1.2 * w:
                w = 0
                threshold.append(x[i - 1] + 1)
                pre_y = x[i] - x[i - 1]
            else:
                w = 0
    return threshold


def get_obj_rectange(lts, x0, x1, y0, y1):
    inside = []
    outside = []
    for obj in lts:
        if x0 < obj.x_cen and x1 > obj.x_cen and y0 < obj.y_cen and y1 > obj.y_cen:
            inside.append(obj)
        else:
            outside.append(obj)
    return inside, outside  # [x for x in lts if x0< (x[4]+x[5])/2 and x1> (x[4]+x[5])/2 and y0 < (x[6]+x[7])/2 and y1 > (x[6]+x[7])/2]


def get_text(lts):
    lts = sorted(lts, key=lambda obj: obj.y_cen * 700 - obj.x_cen, reverse=True)
    return ' '.join([obj.text for obj in lts])


def find_line(lines, x0, y0):
    return [line for line in lines if
            (abs(line.x0 - x0) < 3 and abs(line.y0 - y0) < 3) or (abs(line.x1 - x0) < 3 and abs(line.y1 - y0) < 3)]


def is_line(obj):
    return (obj.height < 2 or obj.width < 2) and (obj.height > 8 or obj.width > 8)


def obj_to_line(obj):
    if obj.height < 2:
        return PDFObject('Line', obj.x0, (obj.y0 + obj.y1) / 2, obj.x1, (obj.y0 + obj.y1) / 2)
    else:
        return PDFObject('Line', (obj.x0 + obj.x1) / 2, obj.y0, (obj.x0 + obj.x1) / 2, obj.y1)


def get_rect(line, lines):
    if line.is_vertical:
        up = [l for l in lines if (not l.is_vertical) and l.check(line.x0, line.y0)]
        down = [l for l in lines if (not l.is_vertical) and l.check(line.x1, line.y1)]
        for u in up:
            for d in down:
                if abs(u.x0 - d.x0) < 2 and abs(u.x1 - d.x1) < 2:
                    return PDFObject('Rect', u.x0, line.y0, u.x1, line.y1)
    else:
        left = [l for l in lines if (l.is_vertical) and l.check(line.x0, line.y0)]
        right = [l for l in lines if (l.is_vertical) and l.check(line.x1, line.y1)]
        for u in left:
            for d in right:
                if abs(u.y0 - d.y0) < 2 and abs(u.y1 - d.y1) < 2:
                    return PDFObject('Rect', line.x0, u.y0, line.x1, u.y1)
    return None


def dect_rect(lines):
    lines = sorted(lines, key=lambda x: (x.y0 + x.y1) * 700 + (x.x0 + x.x1))
    rects = []
    count = 1
    for line in lines:
        rect = get_rect(line, lines[count:])
        if rect != None:
            rects.append(rect)
        count += 1

    return rects


def write_file(folder, filename, filedata, flags='w'):
    """Write the file data to the folder and filename combination
    (flags: 'w' for write text, 'wb' for write binary, use 'a' instead of 'w' for append)"""
    result = False
    if os.path.isdir(folder):
        try:
            file_obj = open(os.path.join(folder, filename), flags)
            file_obj.write(filedata)
            file_obj.close()
            result = True
        except IOError:
            pass
    return result


def determine_image_type(stream_first_4_bytes):
    """Find out the image file type based on the magic number comparison of the first 4 (or 2) bytes"""
    file_type = None
    bytes_as_hex = b2a_hex(stream_first_4_bytes)
    if bytes_as_hex.startswith(b'ffd8'):
        file_type = '.jpeg'
    elif bytes_as_hex == b'89504e47':
        file_type = '.png'
    elif bytes_as_hex == b'47494638':
        file_type = '.gif'
    elif bytes_as_hex.startswith(b'424d'):
        file_type = '.bmp'
    return file_type


def save_image(lt_image, page_number, images_folder):
    """Try to save the image data from this LTImage object, and return the file name, if successful"""
    result = None
    if lt_image.stream:
        file_stream = lt_image.stream.get_rawdata()
        if file_stream:
            file_ext = determine_image_type(file_stream[0:4])
            if file_ext:
                file_name = ''.join([str(page_number), '_', lt_image.name, file_ext])
                if write_file(images_folder, file_name, file_stream, flags='wb'):
                    result = file_name
    return result


def is_newsentence(textline, before):
    if textline.text == None:
        return False
    if len(textline.text) == 0:
        return False
    if textline.y1 > before.y0:
        return False
    if (textline.text.strip()[0] in ['+', '-', '*']) and before.x1 > textline.x0:
        return True
    if textline.is_title:
        return True
    if before.is_title:
        return True
    return False


def parse_page(page, before=None):
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    # I changed the following 2 parameters to get rid of white spaces inside words:
    laparams.char_margin = 1.0
    laparams.word_margin = 1.0
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    all_lines = []
    list_textline = []
    count_textline = 0
    interpreter.process_page(page)

    layout = device.get_result()
    width = 700
    height = 700
    # histogram_x = np.zeros([1200])
    # histogram_y = np.zeros([1200])
    images = []

    for lt_obj in layout:
        # print(lt_obj)
        if isinstance(lt_obj, lt.LTFigure):
            for lt_image in lt_obj:
                if isinstance(lt_image, lt.LTImage):
                    saved_file = save_image(lt_image, page.pageid, dir_temp)
                    if saved_file:
                        if detect_face(os.path.join(dir_temp, saved_file)):
                            images.append(os.path.join(dir_temp, saved_file))
                        else:
                            os.remove(os.path.join(dir_temp, saved_file))
        if isinstance(lt_obj, lt.LTTextBox):  # or isinstance(lt_obj, LTTextLine) :
            for obj in lt_obj:
                if isinstance(obj, LTTextLine) and len(obj.get_text().strip()) > 0 and not is_index_page(obj):
                    p = parse_textline(obj)
                    #                     for i in range(p[4],p[5]):
                    #                         histogram_x[i]+=1
                    #                     for i in range(p[6],p[7]):
                    #                         histogram_y[i]+=1
                    list_textline.append(p)
                    if p.x1 > width:
                        width = p.x1
                    if p.y1 > height:
                        height = p.y1
                    count_textline += 1
        elif isinstance(lt_obj, LTTextLine) and len(lt_obj.get_text().strip()) > 0 and not is_index_page(lt_obj):
            p = parse_textline(lt_obj)
            #                     for i in range(p[4],p[5]):
            #                         histogram_x[i]+=1
            #                     for i in range(p[6],p[7]):
            #                         histogram_y[i]+=1
            list_textline.append(p)
            if p.x1 > width:
                width = p.x1
            if p.y1 > height:
                height = p.y1
            count_textline += 1
        elif is_line(lt_obj):
            #             print(lt_obj)
            #             print(obj_to_line(lt_obj))
            line = obj_to_line(lt_obj)
            all_lines.append(line)
            if line.x1 > width:
                width = line.x1
            if line.y1 > height:
                height = line.y1
    #             for i in range(round(lt_obj.x0),round(lt_obj.x1)):
    #                 histogram_x[i]+=2
    #             for i in range(round(lt_obj.y0)+3,round(lt_obj.y1)-3):
    #                 histogram_y[i]+=2
    #     print(len(all_lines))
    histogram_x, histogram_y = histogram(list_textline, width, height)
    # for line in all_lines:
    #     if line.is_vertical:
    #         for i in range(line.y0+5,line.y1-2):
    #             histogram_y[i]+=1
    width = len(histogram_x)
    table_texts = []
    rects = dect_rect(all_lines)
    # for rect in rects:
    #     for i in range(rect.y0+2,rect.y1-2):
    #         histogram_y[i] += 1
    #     print(len(rects))
    rects = sorted(rects, key=lambda rect: rect.y_cen * 700 - rect.x_cen, reverse=True)

    for rect in rects:
        i, list_textline = get_obj_rectange(list_textline, rect.x0 - 1, rect.x1 + 1, rect.y0 - 1, rect.y1 + 1)
        table_texts.append(get_text(i))
        list_textline.append(PDFObject('TextRect', rect.x_cen, rect.y_cen, rect.x1 - 5, rect.y1 - 5, get_text(i)))
        # list_textline.append(
        #     [get_text(i), 'font', 'style', 'size', (rect.x0 + rect.x1) / 2, rect.x1 - 5, (rect.y0 + rect.y1) / 2,
        #      rect.y1 - 5])

    list_textline = sorted(list_textline, key=lambda obj: obj.y_cen * width - obj.x_cen, reverse=True)
    #     print(get_text(get_obj_rectange(list_textline,0,700,500,900)))
    # cluster_x = find_threshold(histogram_x, n=5)
    cluster_y = find_threshold_y(histogram_y)
    for line in all_lines:
        if not line.is_vertical and line.x1 - line.x0 > 0.4 * width:
            # print(line.y_cen)
            cluster_y.append(line.y_cen)
    cluster_y = sorted(cluster_y, reverse=True)
    # print(cluster_y)
    # cluster_y = list(reversed(cluster_y))
    # cluster_y.append(2000)
    iy = 0
    listtext = []
    cluster_obj = []
    text = ''
    objs = []
    # before = None
    for i, obj in enumerate(list_textline):
        if i == 0 or before == None:
            text = obj.text
            objs = [obj]

        elif is_newsentence(obj, before):
            if len(text.strip()) > 0:
                listtext.append(text.strip())
                cluster_obj.append(objs)
            text = obj.text
            objs = [obj]
        elif obj.y_cen >= cluster_y[iy] - 1:  # and not is_newsentence(x,before):
            text += ' ' + obj.text
            objs.append(obj)
        else:
            if len(text.strip()) > 0:
                listtext.append(text.strip())
                cluster_obj.append(objs)
            text = obj.text
            objs = [obj]
            iy += 1
        if before != None and not obj.is_title:
            obj.title = before.title
        before = obj
    if len(text.strip()) > 0:
        listtext.append(text.strip())
        cluster_obj.append(objs)
    #     for text in listtext:
    #         print('+++',text)
    #     print(list_textline)
    return listtext, cluster_obj, table_texts, images, before


def parse(_pathfile, _rate=1, _show=False):
    with open(_pathfile, 'rb') as file_content:
        parser = PDFParser(file_content)
        doc = PDFDocument(parser)
        parser.set_document(doc)
        doc.set_parser(parser)
        doc.initialize('')

        list_page = []
        height = 0
        width = 0
        count_textline = 0
        all_text = []
        table = []
        images = []
        cluster_obj = []
        # Process each page contained in the document.
        # import pdb; pdb.set_trace()
        before = None
        for page in doc.get_pages():
            #             print('Page ... \n\n')
            print(page.cropbox)
            list_text, list_obj, table_text, image, before = parse_page(page, before)
            all_text.extend(list_text)
            table.extend(table_text)
            images.extend(image)
            cluster_obj.extend(list_obj)
        #

        file_content.close()
    #         all_text = ' '.join([' '.join([(x[0]) for x in sort_list if  x[3].split(',')[0] != 'Symbol' ]) for sort_list in all_textobj])
    # sort_list = sorted(list_page[0],key=lambda x:x[2]*width-x[1],reverse=True)
    # print(' '.join([x[0] for x in sort_list if len(x[0].strip())>1]))
    return all_text, cluster_obj, table, images  # ,width,dy,count_textline


if __name__ == "__main__":
    path_cv = '../data/cv/en/done/ITSOL_CV_IOS_ Ta Cuong.pdf'
    _,objs,_,_ = parse(path_cv,1,False)
    print(objs)
