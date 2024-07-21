import xlrd  # xlrd是读excel，xlwt是写excel的库，这两个适用于.xls格式
import re
import jieba
import math
import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer


# from sklearn.feature_extraction.text import TfidfTransformer
# from sklearn import feature_extraction

def coreword(path):
    wordlist = []  # Q
    labellist = []  # A
    ExcelFile = xlrd.open_workbook(path)
    sheet = ExcelFile.sheet_by_index(0)  # 通过索引顺序获取工作表sheet
    rownum = sheet.nrows  # 获取sheet中的有效行数
    # print('sheet中的有效行数:',rownum)
    r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~“”！，：＋+、。；？ 〈\s\d]+'
    for i in range(0, rownum):
        row = sheet.row_values(i)  # 返回由该行中所有单元格的数据组成的列表
        wordstr = re.sub(r, '', row[0])  # 正则表达式，把匹配到r符号的替换空
        seg_list = jieba.cut(wordstr, cut_all=False)  # 精确模式,得到generator类
        wordlist.append(" ".join(seg_list))  # 词语之间加上空格
        labellist.append(row[1])
    # print(wordlist,'\n',labellist,'\n')
    return wordlist, labellist


def groupwordtfdif(list_q):
    count_list = CountVectorizer()
    count_a1ist = count_list.fit_transform(list_q)  # 计算各个词语出现的次数
    word = count_list.get_feature_names()  # 返回特征名称列表，即为所有文档的关键词
    # tg_wordcountarray=count_a1ist.toarray().tolist()
    # print(tg_wordcountarray)#查看词频结果
    groupransformer = TfidfVectorizer()
    groupransformer.fit(list_q)  # 用X_train数据来fit
    groupfidf = groupransformer.transform(list_q)  # 将词频矩阵X统计成TF-IDF值，词频（TF）和逆文档频率(IDF)的积
    group_wordtfdif = groupfidf.toarray().tolist()
    # print('多文档TFIDF矩阵:',group_wordtfdif)
    return group_wordtfdif


def dealword(str1):
    wordlist = []
    r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~“”！，：＋+、。；？ 〈\s\d]+'
    str1 = str1.strip()  # 删除头尾空字符
    linestr = re.sub(r, '', str1)
    seg_list = jieba.cut(linestr, cut_all=False)
    wordlist.append(" ".join(seg_list))
    return wordlist


def singlewordtfdif(user_q, list_q):
    groupransformer = TfidfVectorizer()
    groupransformer.fit(list_q)
    singlefidf = groupransformer.transform(user_q)  # 得到TF-IDF矩阵
    single_wordtfdif = singlefidf.toarray().tolist()
    # print('新文档TFIDF矩阵:',single_wordtfdif)
    return single_wordtfdif


def cosAB(listA, listB):
    resulttfdif = []
    listA = listA[0]
    for i in range(len(listB)):
        # print(listA,'\n',listB[i])
        if len(listA) != len(listB[i]) or len(listA) < 1:
            return False
        Molecular, denominatorA, denominatorB, denominator = 0, 1, 1, 0
        for j in range(len(listA)):
            listA[j] = float(listA[j])
            listB[i][j] = float(listB[i][j])
            # print('A和B',listA[j],listB[i][j])
            Molecular = Molecular + (listA[j] * listB[i][j])
            # print(Molecular,'\n')
            denominatorA += listA[j] * listA[j]
            denominatorB += listB[i][j] * listB[i][j]
        denominator = Molecular / (math.sqrt(denominatorA) * math.sqrt(denominatorB))
        # print('分子分母',Molecular,denominatorA,denominatorB)
        # print(denominator,'\n')
        resulttfdif.append(denominator)  # 与listB[i]的匹配度
    # print('cos-result:',resulttfdif)
    return resulttfdif


def QA(something):
    list_q, list_a = coreword("FAQ_data.xls")
    grouplist = groupwordtfdif(list_q)  # 库问题词频矩阵TF-IDF值
    user_q = dealword(something)  # 用户问题分词
    newlist = singlewordtfdif(user_q, list_q)  # 用户问题词频矩阵TF-IDF值
    resultlist = cosAB(newlist, grouplist)  # 库问题匹配度
    for r in resultlist:
        if r != 0:
            maxindex = resultlist.index(max(resultlist))
            q = re.sub(' ', '', list_q[maxindex])
            a = list_a[maxindex]
            return q, a
    q = '未找到相关问题，请重试'
    a = 'false'
    return q, a


def main():
    while True:
        something = input("请提问：")
        # start=time.time()
        q, a = QA(something)
        print("问题", q)
        print("回答", a)
        # end=time.time()
        # print('用时:',end-start,'s')


if __name__ == '__main__':
    main()
