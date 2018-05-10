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
    # # word.Visible = True
    # print(word)
    # doc = word.Documents.Open(doc_file)
    # doc.SaveAs(out_file, FileFormat=wdFormatPDF)
    # doc.Close()
    # word.Quit()
    # return out_file
    return doc_file

# doc_to_pdf('../cv/pham_van_tien.docx')
