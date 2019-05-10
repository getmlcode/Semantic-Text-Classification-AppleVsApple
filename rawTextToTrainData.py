import os
from nltk.corpus import stopwords

stopList = list(stopwords.words('english')) # Stopwords
spclCharList  = ['#','^','!','(',')','`','~','%','/','\\' ,'{','}',']','[','.',',',':',';','"','-','°','@']

fruit_file = os.path.join(os.getcwd(),"TrainData\\apple-fruit.txt")
company_file = os.path.join(os.getcwd(),"TrainData\\apple-computers.txt")
trainDataText = open(os.path.join(os.getcwd(),"TrainData\\TrainData.txt"),'w')

with open(fruit_file,'r',encoding="utf-8") as input:
    paragraphs = input.read().split("\n\n")

datum =''
for para in paragraphs:
    for ch in spclCharList:
        para = para.replace(ch,'')
    para = ''.join([i for i in para if not i.isdigit()])
    para = para.lower().strip().split()
    para = list(filter(lambda x: x != '', para))
    para = [word for word in para if word not in stopList]
    para = ' '.join(str(w) for w in para)
    datum += para +'\t'+'fruit'+'\n'

with open(company_file,'r',encoding="utf-8") as input:
    paragraphs = input.read().split("\n\n")

for para in paragraphs:
    for ch in spclCharList:
        para = para.replace(ch,'')
    para = ''.join([i for i in para if not i.isdigit()])
    para = para.lower().strip().split()
    para = list(filter(lambda x: x != '', para))
    para = [word for word in para if word not in stopList]
    para = ' '.join(str(w) for w in para)
    datum += para +'\t'+'company'+'\n'

trainDataText.write(datum)
trainDataText.close()