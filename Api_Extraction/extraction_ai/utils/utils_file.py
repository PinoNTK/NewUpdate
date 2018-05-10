import glob
import os
import shutil
from .utils_nlp import remove_accents

# import comtypes.client
def doc_to_pdf(doc_file):
    # wdFormatPDF = 17
    #
    # if doc_file.endswith('.doc'):
    #     out_file = (doc_file[:-4] + '.pdf')
    # elif doc_file.endswith('.docx'):
    #     out_file = doc_file[:-5] + '.pdf'
    # elif doc_file.endswith('.pdf'):
    #     return doc_file
    # else:
    #     return None
    # word = comtypes.client.CreateObject('Word.Application',dynamic = True)
    #
    # print(word)
    # doc = word.Documents.Open(doc_file)
    # doc.SaveAs(out_file, FileFormat=wdFormatPDF)
    # doc.Close()
    # word.Quit()
    # return out_file
    return doc_file

def create_folder(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
def cluster_file(dir_root,dir_pdf,dir_doc):
    create_folder(dir_pdf)
    create_folder(dir_doc)
    for root, dir, files in os.walk(dir_root):
        for filename in files:
            if filename.endswith('pdf'):
                shutil.copy(os.path.join(root,filename),os.path.join(dir_pdf,remove_accents(u''+filename.replace(' ','_'))))
            if filename.split('.')[-1] in ['doc','docx']:
                shutil.copy(os.path.join(root,filename),os.path.join(dir_doc,remove_accents(u''+filename.replace(' ','_'))))

def list_file(dir):

    all_file = []
    for file in glob.glob(dir):
        a = os.path.split(file)
        all_file.append(a[-1])
        print(a[-1])

    # df = pd.DataFrame({'file_name': all_file})
    # df.to_excel('../../ITSOL/data/pdf/en/list_file.xls')
    # print(df.describe())
    return all_file


if __name__ == '__main__':
    cluster_file('../cv','../cv/pdf','../cv/doc')
