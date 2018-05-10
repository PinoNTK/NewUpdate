import pandas as pd
from googletrans import Translator
df = pd.read_excel('topic_train.xlsx')
translator = Translator()
df['vi'] = [translator.translate(text,dest='vi').text for text in df['text']]
df.to_excel('topic_train_vi.xlsx')
# print(df['vi'])
