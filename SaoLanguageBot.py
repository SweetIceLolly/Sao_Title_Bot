import random

# 开头
BeginningList = ["基于", "关于", "探究", "促进", "一种", "讨论", "试论", "论", "试探究", "建基于", "面向", "评述"]

# 介词
PrepList = ["里", "中", "上", "的", "与", "和"]

# 形容词
AdjList = ["现代", "宏观", "微观", "当代", "新时代", "现代化", "国际化", "先进", "二十一世纪"]

# 工业类型
IndustryList = ["农业", "经济学", "技术", "产业", "管理学", "物理", "化学", "制药", "医学", "环境学", "计算机",
                "大数据", "生物学", "数学", "语言学习", "国民经济", "房地产市场", "土地利用", "投资", "企业",
                "生态学", "股市", "低碳经济"]

# 名词
NounList = ["技术", "方案", "功能", "产品", "方法", "工艺", "措施", "技能", "能力", "模型"]

# 结尾
EndingList = ["探究", "研究", "分析", "设计", "应用", "思考", "开发", "考察", "实践", "算法", "实证分析", "成因",
              "治理", "决策", "潜在问题", "效应", "贡献", "发展", "反思", "证据", "回顾", "展望", "处理", "深化"]

# 随机生成一段字母
def GetSomeLetters():
    rtn = ""
    IsAbbr = random.randint(1, 10) < 4
    if IsAbbr:                                      # 缩写式
        for i in range(random.randint(2, 5)):
            rtn += chr(random.randint(65, 90))
    else:                                           # 驼峰式
        for i in range(random.randint(1, 2)):           # 随机字母段数 (大写字母开头的为一段)
            rtn += chr(random.randint(65, 90))              # 弄一个大写字母
            for j in range(random.randint(2, 5)):           # 跟着一堆小写字母
                rtn += chr(random.randint(97, 122))
    return rtn

# 从source里面抽取一段文本，其中包含连接词的概率是(possibility_of_and/10)，force_use_and: 必须用“与”连接
def SelectItem(source, possibility_of_and = 5, force_use_and = False):
    data = source[:]
    index = random.randint(0, len(data) - 1)

    if len(data) > 2:
        if random.randint(1, 10) <= possibility_of_and:
            tmp = data[index]
            del data[index]
            if force_use_and:
                tmp += "与"
            else:
                if random.randint(1, 10) <= 5:          # 两个词换着来，不会这么枯燥
                    tmp += "与"
                else:
                    tmp += "及其"
            tmp += data[random.randint(0, len(data) - 1)]
            return tmp
    return data[index]

# 来点骚话吧！SaoDegree不宜过高，否则会太骚。3已经非常非常骚了
def GetSaoSentence(SaoDegree = 1):
    # 先抽取一个开头
    sentence = SelectItem(BeginningList, 0)

    sentence += SelectItem(AdjList, 0)
    sentence += GetSomeLetters()
    sentence += SelectItem(IndustryList, 3, True)
    sentence += SelectItem(PrepList, 0)
    for i in range(SaoDegree):
        sentence += GetSomeLetters()
        sentence += SelectItem(NounList, 0)
        sentence += SelectItem(PrepList, 0)
    
    sentence += GetSomeLetters()
    sentence += SelectItem(NounList, 0)
    sentence += "的"
    sentence += SelectItem(EndingList, 6)

    return sentence

if __name__ == '__main__':
    random.seed()

    while True:
        print(GetSaoSentence(random.randint(0, 2)))
        input()