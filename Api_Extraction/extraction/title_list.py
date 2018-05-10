from . import utils_nlp
from . import title_word_list
title_raw={
    u'SƠ YẾU LÝ LỊCH CÁ NHÂN':'title',
    u'Học vấn/Ngoại ngữ':'education',
    u'Thông tin cá nhân':'person_detail',
    u'LÝ LỊCH ỨNG VIÊN':'title',
    u'Kinh nghiệm làm việc':'experience',
    u'Kỹ năng':'skill',
    u'Mục Tiêu Nghề Nghiệp':'objective',
    u'Mục Tiêu':'objective',
    u'Học Vấn Và Bằng Cấp':'education',
    u'QUÁ TRÌNH CÔNG TÁC':'experience',
    u'DỰ ÁN ĐÃ THAM GIA':'project',
    u'BẰNG CẤP CHUYÊN MÔN':'education',
    u'THÔNG TIN KHÁC':'other',
    u'THÔNG TIN THAM KHẢO':'other',
    u'CHỨNG CHỈ KHÁC':'other',
    u'Trình độ học vấn':'education',
    u'Quá trình công tác':'experience',
    u'CÁC DỰ ÁN TIÊU BIỂU':'project',
    u'Kỹ năng làm việc':'skill',
    u'Sở thích':'other',
    u'Nguyện vọng':'objective',
    u'VỀ BẢN THÂN':'person_detail',
    u'TRÌNH ĐỘ CHUYÊN MÔN':'education',
    u'CÁC CHỨNG CHỈ ĐÀO TẠO KHÁC':'education',
    u'Công việc':'experience',
    u'QUÁ TRÌNH HỌC TẬP':'education',
    u'MỤC TIÊU NGHỀ NGHIỆP':'objective',
    u'HỌC VẤN':'education',
    u'HOẠT ĐỘNG':'other',
    u'THÔNG TIN ỨNG TUYỂN':'objective',
    u'HỒ SƠ ỨNG VIÊN':'title',
    u'KINH NGHIỆM BẢN THÂN':'experience',
    u'THÔNG TIN BỔ SUNG':'other',
    u'DỰ ÁN THỰC TẾ':'project',
    u'CHỨNG CHỈ':'education',
    u'TÍNH CÁCH':'other',
    u'CÁC KỸ NĂNG':'skill',
    u'SỞ THÍCH':'other',
    u'GIỚI THIỆU BẢN THÂN':'person_detail',
    u'NGƯỜI THAM CHIẾU':'other',
    u'Career Objective':'objective',
    u'Educational Background':'education',
    u'TECHNOLOGY AND SOFTWARE DEVELOPMENT SKILLS':'skill',
    u'PROFESSIONAL SUMMARY':'other',
    u'OBJECTIVE':'objective',
    u'EDUCATION & CERTIFICATIONS':'education',

}
en_list ={}
for k,titles in title_word_list.category_map.items():
    for title in titles:
        en_list[utils_nlp.clean_title(title)] = k
title_list =({utils_nlp.clean_title(k):v for k,v in title_raw.items()})
en_list.update(title_list)
title_list=en_list