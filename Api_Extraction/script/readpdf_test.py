from Api_Extraction.extraction.pdf_reader_v2 import parse

if __name__ == "__main__":
    path_cv = '../../../../Machine Learning/ReadPDF/data/cv/en/done/ITSOL_CV_IOS_LEPHUONG.pdf'
    _,c_objs,_,_ = parse(path_cv,1,False)
    for objs in c_objs:
        for obj in objs:
            print(obj)
