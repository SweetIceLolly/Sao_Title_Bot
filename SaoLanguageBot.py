# 用于存储物件
import numpy as np

# 用于随机数生成
import random

# 用于异常处理
import sys

# 开头
BeginningList = ("基于", "关于", "探究", "促进", "一种", "讨论", "试论", "论", "试探究", "建基于", "面向", "评述")

# 介词
PrepList = ("里", "中", "上", "的", "与", "和")

# 形容词
AdjList = ("现代", "宏观", "微观", "当代", "新时代", "现代化", "国际化", "先进", "二十一世纪", "一体化")

# 工业类型词典
IndustryList = {"农业":0, "经济学":0, "技术":0, "产业":0, "管理学":0, "物理":0, "化学":0, "制药":0, "医学":0, "环境学":0, "计算机":0,
                "大数据":0, "生物学":0, "数学":0, "语言学习":0, "国民经济":0, "房地产市场":0, "土地利用":0, "投资":0, "企业":0,
                "生态学":0, "股市":0, "低碳经济":0}

# 名词词典
NounList_dict = {"技术":0, "方案":0, "功能":0, "产品":0, "方法":0, "工艺":0, "措施":0, "技能":0, "能力":0, "模型":0}

# 说明:   把NounList_dict储存到文件
def save_noun_dict():
    try:
        np.save('NounList_dict.npy', NounList_dict)
        print("名词词典已保存！")
    except:
        print("保存名词词典失败！")
        pass

# 说明:   把Industry_dict储存到文件
def save_industry_dict():
    try:
        np.save('Industry_dict.npy', Industry_dict)
        print("工业类型词典已保存！")
    except:
        print("保存工业类型词典失败！")
        pass

# 说明:   生成一个随机英文字符串
def get_some_letters():
    rtn = ""
    IsAbbr = random.randint(1, 10) < 4
    if IsAbbr:                                      # 缩写（全大写）
        for i in range(random.randint(2, 5)):
            rtn += chr(random.randint(65, 90))
    else:                                           # 驼峰式
        for i in range(random.randint(1, 2)):           # 单词块数（每个块由大写字母开始）
            rtn += chr(random.randint(65, 90))              # 生成一个大写字母
            for j in range(random.randint(2, 5)):           # 后面跟着一堆小写字母
                rtn += chr(random.randint(97, 122))
    return rtn

# 说明:   从source随机抽取一个字符串
# 参数:   source: 用来抽取文本的list
#         possibility_of_and: 出现连接词的几率 (possibility_of_and / 10)
#         force_use_and: 强制使用"与"作为连接词
# 返回:   随机抽取的字符串
def select_item(source, possibility_of_and = 5, force_use_and = False):
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

# 说明:   来点骚标题吧！
# 参数:   sao_degree: 骚的程度。不要太高！3就挺骚的了
#         need_letters: 是否在名词中间加入一些英语单词
# 返回:   骚标题
def get_sao_sentence(need_letters = False, sao_degree = 0):
    # Get a beginning
    sentence = select_item(BeginningList, 0)

    sentence += select_item(AdjList, 0)
    if need_letters:
        sentence += get_some_letters()
    sentence += select_item(list(Industry_dict.keys()), 3, True)
    sentence += select_item(PrepList, 0)
    for i in range(sao_degree):
        if need_letters:
            sentence += get_some_letters()
        sentence += select_item(list(NounList_dict.keys()), 0)
        sentence += select_item(PrepList, 0)
    
    if need_letters:
        sentence += get_some_letters()
    sentence += select_item(list(NounList_dict.keys()), 0)
    sentence += "的"
    sentence += select_item(list(NounList_dict.keys()), 6)

    return sentence

# 说明:   显示帮助
def show_help():
    print("基于当前脚本语言程序所能实现的功能而提供的可用人机交互命令:\n\n"
          "help : 通过基于键盘的人机互动方式显示该基于控制台输出的帮助指令\n\n"
          "input industry/noun text : 基于用户键盘输入与用户更新意向(industry: 更新工业类型词典; noun: 更新名词词典)以及有意愿新增的文本(text)的手动词典词库更新的功能实践\n"
          "例如: input noun 实验 会把“实验”添加到名词词典中\n\n"
          "remove industry/noun text : 基于用户键盘输入与用户更新意向(industry: 更新工业类型词典; noun: 更新名词词典)以及有意向要删除的文本(text)的手动词典词库更新的功能实践\n"
          "例如: remove industry 数学 会把“数学”从工业类型词典中移除\n\n"
          "check industry/noun : 通过现代化脚本语言内置的高效词典算法并基于控制台输出的方式进行人机互动从而使用户能够查看工业类型词典(industry)或者名词词典(noun)里的内容的过程的实现\n"
          "例如: check noun 会把名词词典中的内容输出，并告诉用户词条的数量\n\n"
          "get [自动添加英语单词(0/1)] [骚程度] : 获取基于现代电脑编程技术及其应用和新时代互联网技术的词库获取及语言分析的计算机程序自动生成的骚论文题目\n"
          "[自动添加英语单词]: 可选的。自动在名词中间添加看起来非常高大上的英语单词，默认为0(不自动添加); [骚程度]: 可选的。生成的题目有多骚，默认为0(已经挺骚了，除非您觉得不够骚)\n"
          "例如: get 1 2 会生成一个自动添加英语单词的、骚程度2的标题\n\n"
          "空白输入 : 相同于 get 0 0\n\n"
          "exit : 基于用户键盘输入的计算机程序退出的实践"
         )

# 说明:   显示错误信息
def show_error():
    print("此基于脚本语言的菜鸡程序未能处理刚才出现的异常，需要劳烦用户另行重新进行输入以取得期望中的计算机程序的执行结果。\n"
          "Exception: ", end='')
    print(sys.exc_info()[1])

# 程序入口点
if __name__ == '__main__':
    try:
        NounList_dict = np.load("NounList_dict.npy", allow_pickle=True).item()
        print("名词词典已加载！条目数: " + str(len(NounList_dict)))
    except:
        print("加载名词词典NounList_dict.npy失败！")

    try:
        Industry_dict = np.load("Industry_dict.npy", allow_pickle=True).item()
        print("工业类型词典已加载！条目数: " + str(len(Industry_dict)))
    except:
        print("加载工业类型词典Industry_dict.npy失败！")
    print("")

    random.seed()
    show_help()
    while True:
        userinput = input('\n').lower().strip()
        while userinput.find("  ") != -1:                   # 去掉多余的空格
            userinput = userinput.replace("  ", " ")

        if userinput == '':                                 # 获取骚标题
            print(get_sao_sentence())
        else:
            userinput = userinput.split(" ")
            if userinput[0] == 'help':                      # 显示帮助
                show_help()
            elif userinput[0] == 'get':                     # 获取骚标题（带参数）
                need_letters = False
                if len(userinput) == 1:                         # 没有参数
                    print(get_sao_sentence())
                elif len(userinput) >= 2:
                    if userinput[1].isnumeric():
                        if int(userinput[1]) == 1:                      # 指定了要加入英语单词
                            need_letters = True
                        elif int(userinput[1]) != 0:
                            show_error()
                            continue
                    else:
                        show_error()
                    if len(userinput) >= 3:
                        if userinput[2].isnumeric():
                            if int(userinput[2]) >= 0:                  # 指定了骚程度
                                print(get_sao_sentence(need_letters, int(userinput[2])))
                            else:
                                show_error()
                        else:
                            show_error()
                    else:
                        print(get_sao_sentence(need_letters))
            elif userinput[0] == 'input':                   # 手动输入词典
                try:
                    if userinput[1] == 'industry':              # 工业类型词典
                        if userinput[2] in Industry_dict:
                            print("您要输入的条目已存在！")
                        else:
                            Industry_dict.update({' '.join(userinput[2:]):0})
                            print("成功添加！")
                            save_industry_dict()
                    elif userinput[1] == 'noun':                # 名词词典
                        if userinput[2] in NounList_dict:
                            print("您要输入的条目已存在！")
                        else:
                            NounList_dict.update({' '.join(userinput[2:]):0})
                            print("成功添加！")
                            save_noun_dict()
                    else:
                        show_error()
                except:
                    show_error()
            elif userinput[0] == 'remove':                  # 手动删除词典
                try:
                    if userinput[1] == 'industry':              # 工业类型词典
                        if userinput[2] in Industry_dict:
                            print("您要移除的条目不存在！")
                        else:
                            del Industry_dict[' '.join(userinput[2:])]
                            print("成功移除！")
                            save_industry_dict()
                    elif userinput[1] == 'noun':                # 名词词典
                        if userinput[2] in NounList_dict:
                            print("您要输入的条目已存在！")
                        else:
                            del Industry_dict[' '.join(userinput[2:])]
                            print("成功移除！")
                            save_noun_dict()
                    else:
                        show_error()
                except:
                    show_error()
            elif userinput[0] == 'check':                   # 查看词典
                try:
                    if userinput[1] == 'industry':              # 工业类型词典
                        print(list(Industry_dict.keys()))
                        print("工业类型词典条目数: " + str(len(Industry_dict)))
                    elif userinput[1] == 'noun':                # 名词词典
                        print(list(NounList_dict.keys()))
                        print("名词词典条目数: " + str(len(NounList_dict)))
                    else:
                        show_error()
                except:
                    show_error()
            elif userinput[0] == 'exit':                    # 退出
                break
            else:                                           # 未知命令
                print("用户刚才通过人机交互的方式给这个基于脚本语言的垃圾程序输入了其不能理解的内容，需要劳烦用户另行重新进行输入以取得期望中的计算机程序的执行结果。")
