from . import utils_nlp

class Dictionary(object):
    def __init__(self):
        self.dict=set()
    def build_dictionary(self,list):
        self.dict = self.dict.union([' '+utils_nlp.clean_string(s).lower()+' ' for s in list])

        # print(self.dict)
        # self.dict.
    def find(self,text):
        text = ' '+utils_nlp.clean_string(text)+' '
        lower = text.lower()
        result = []
        l = len(lower)
        for i in range(l):
            if(lower[i]==' '):
                for t in self.dict:
                    if len(t) < l - i - 1:
                        if t== lower[i:i+len(t)]:
                            result.append(text[i:i+len(t)].strip())
                        # flag = True
                        # for j in range(len(t)):
                        #     if t[j] != lower[i + j]:
                        #         flag = False
                        #         break
                        # if flag:
                        #     result.append(' '.join(text[i:i + len(t)]))

        return list(set(result))

    # def find(self,text):
    #     text = utils_nlp.clean_string(text).split()
    #     lower = [t.lower() for t in text]
    #     result=[]
    #     l = len(lower)
    #     for i in range(l):
    #         for t in self.dict:
    #             if len(t)<l-i-1:
    #                 flag = True
    #                 for j in range(len(t)):
    #                     if t[j]!= lower[i+j]:
    #                         flag =False
    #                         break
    #                 if flag:
    #                     result.append(' '.join(text[i:i+len(t)]))
    #
    #     return list(set(result))