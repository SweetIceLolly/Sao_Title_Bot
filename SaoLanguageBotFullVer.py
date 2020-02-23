# -*- coding:utf-8 -*-

# For browser manipulations
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# For object storage
import numpy as np

# For random numbers
import random

# For exception handling
import sys

# Beginnings
BeginningList = ("基于", "关于", "探究", "促进", "一种", "讨论", "试论", "论", "试探究", "建基于", "面向", "评述")

# Prepositions
PrepList = ("里", "中", "上", "的", "与", "和")

# Adjectives
AdjList = ("现代", "宏观", "微观", "当代", "新时代", "现代化", "国际化", "先进", "二十一世纪", "一体化")

# Industry types
IndustryList = {"农业":0, "经济学":0, "技术":0, "产业":0, "管理学":0, "物理":0, "化学":0, "制药":0, "医学":0, "环境学":0, "计算机":0,
                "大数据":0, "生物学":0, "数学":0, "语言学习":0, "国民经济":0, "房地产市场":0, "土地利用":0, "投资":0, "企业":0,
                "生态学":0, "股市":0, "低碳经济":0}

# --------------------------------------------------------------------------
# For dictionary update
# Ignore text after "的" when meeting these symbols
special_characters = ("《", "》", "-", "—", "(", ")", "|")

# Split text after "的" by these conjunctions
split_strings = ("及其", "与", "和", "、", "以及", "及")

# Skip current string if these strings are found in the text after "的"
ignore_strings = ("?", "？", "吗", "...")

# Noun dictionary
NounList_dict = {"技术":0, "方案":0, "功能":0, "产品":0, "方法":0, "工艺":0, "措施":0, "技能":0, "能力":0, "模型":0}
# --------------------------------------------------------------------------

# Purpose:  Check if any ignore strings are in title
# Args:     title: Title
# Return:   True if this title is OK. False otherwise
def check_ignore_list(title):
    for i in range(len(ignore_strings)):
        if title.find(ignore_strings[i]) != -1:
            return False
    return True

# Purpose:  Split text by conjunctions (split_strings)
# Args:     text: The string to be splitted
# Return:   A list that contains splitted items
def split_by_list(text):
    rtn_list = []
    prev_pos = 0
    prev_len = 0
    for i in range(len(text)):
        for j in range(len(split_strings)):
            if text[i:i+len(split_strings[j])] == split_strings[j]:
                rtn_list.append(text[prev_pos + prev_len:i].strip())
                prev_pos = i
                prev_len = len(split_strings[j])
                break
    rtn_list.append(text[prev_pos + prev_len:].strip())
    return rtn_list

# Purpose:  Analyze the title and add strings to our dictionaries
# Args:     title: Title
def analyze_and_add(title):
    begin_pos = title.find('基于')
    if begin_pos != -1:
        begin_pos += 2
        end_pos = title.find('的', begin_pos + 2)
    else:
        end_pos = title.rfind('的')

    if end_pos != -1:
        if begin_pos != -1:                                 # Try to get string between '基于' and '的'
            added_count = 0
            vocab_list = split_by_list(title[begin_pos:end_pos])
            for i in vocab_list:
                if not i in Industry_dict:
                    Industry_dict.update({i:0})
                    added_count += 1
            print("工业类型词典新增条目数:\t" + str(added_count), end = '\t')
            print(vocab_list)

        split_tmp = title.split('的')
        split_tmp = split_tmp[len(split_tmp) - 1]
        if check_ignore_list(split_tmp):                     # Check if title should be ignored
            for i in range(len(special_characters)):             # Cut title by special characters 
                pos = split_tmp.rfind(special_characters[i])
                if pos != -1:
                    split_tmp = split_tmp[0:pos - 1]
        
            added_count = 0
            vocab_list = split_by_list(split_tmp)
            for i in vocab_list:
                if not i in NounList_dict:
                    NounList_dict.update({i:0})
                    added_count += 1
            print("名词词典新增条目数:\t" + str(added_count), end='\t')
            print(vocab_list)
        
# Purpose:  Save NounList_dict to file
def save_noun_dict():
    try:
        np.save('NounList_dict.npy', NounList_dict)
        print("名词词典已保存！")
    except:
        print("保存名词词典失败！")
        pass

# Purpose:  Save Industry_dict to file
def save_industry_dict():
    try:
        np.save('Industry_dict.npy', Industry_dict)
        print("工业类型词典已保存！")
    except:
        print("保存工业类型词典失败！")
        pass

# Purpose:  Update dictionaries
# Args:     use_google: True: Use Google Scholar; False: Use Baidu Scholar
#           keyword: The keyword you want to search
#           start_pn: Start page
#           end_pn: End page
def update_dictionaries(use_google, keyword, start_pn, end_pn):
    initial_noun_items = len(NounList_dict)
    initial_industry_items = len(Industry_dict)

    print("正在初始化基于Chrome的浏览器自动化程序...\n")
    chrome_options = Options()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--log-level=3')
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(7)                     # Reduce timeout to increase speed
    print("基于Chrome的浏览器自动化程序初始化完成\n")

    if use_google:
        link = 'https://scholar.google.com/scholar?&q=' + keyword + '&hl=zh-CN&as_sdt=0,5&as_vis=1&start='
    else:
        link = 'http://xueshu.baidu.com/s?wd=' + keyword + '&pn='
    first_round = True
    for pn in range(start_pn - 1, end_pn):              # 'pn' (or 'start' for Google Scholar) argument in the request
        try:
            # Search
            print("正在获取页面: " + str(pn + 1) + "/" + str(end_pn))
            driver.get(link + str(pn * 10))
        except TimeoutException:                        # Ignore timeout
            pass
        finally:
            try:
                # Try to locate left navigation pane as an indication of page loaded
                try:
                    if use_google:
                        WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="gs_bdy_sb"]')
                            ))
                    else:
                        WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="leftnav"]')
                            ))
                except TimeoutException:                        # Timeout, increase time limit and try again
                    print("加载当前页面超时！正在重试...")
                    driver.set_page_load_timeout(5)
                    try:
                        driver.get(link + str(pn * 10))
                        if use_google:
                            WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                                (By.XPATH, '//*[@id="gs_bdy_sb"]')
                                ))
                        else:
                            WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                                (By.XPATH, '//*[@id="leftnav"]')
                                ))
                    except:
                        print("仍然超时！放弃加载当前网页。 pn = " + str(pn))
                        pass
                    finally:
                        driver.set_page_load_timeout(2)
                except:
                    pass

                # Try to get titles of all results (10 results per page)
                if use_google:          # Using Google Scholar
                    try:
                        # Try to locate reCAPTCHA
                        driver.find_element_by_xpath('//*[@id="gs_captcha_ccl"]')
                        print("检测到谷歌学术极其恼人的人机认证！劳烦您手动完成它... :(")

                        # Wait until reCAPTCHA is done by user
                        WebDriverWait(driver, 0xffffffff).until(EC.presence_of_element_located(
                                    (By.XPATH, '//*[@id="gs_nm"]')
                                    ))
                    except:
                        pass

                    # reCAPTCHA not located, continue the job
                    for i in range(1, 10):
                        try:
                            # Try to find the item
                            title = driver.find_element_by_xpath('//*[@id="gs_res_ccl_mid"]/div[' + str(i) + ']/div/h3').text
                            analyze_and_add(title)
                        except NoSuchElementException:
                            try:
                                # A pdf link might be given together with the item, so try another xpath
                                title = driver.find_element_by_xpath('//*[@id="gs_res_ccl_mid"]/div[' + str(i) + ']/div[2]/h3').text
                                analyze_and_add(title)
                            except:
                                pass
                        except:
                            pass
                else:                   # Using Baidu Scholar
                    for i in range(pn * 10 + 1, pn * 10 + 11):
                        try:
                            title = driver.find_element_by_xpath('//*[@id="' + str(i) + '"]/div[1]/h3/a').text
                            analyze_and_add(title)
                        except NoSuchElementException:
                            pass
                        except:
                            pass
                        
                # After the first round, reduce timeout to improve speed
                if first_round:
                    driver.set_page_load_timeout(2)
                    first_round = False
            except NoSuchElementException:
                print("加载页面失败: pn = " + str(pn) + " Exception: ", end='')
                print(sys.exc_info()[1])
            except:
                print("加载页面出错: pn = " + str(pn) + " Exception: ", end='')
                print(sys.exc_info()[1])
    
    driver.close()
    print("当前总计名词词典条目数: " + str(len(NounList_dict)) + " 新增条目数: " + str(len(NounList_dict) - initial_noun_items))
    print("当前总计工业类型词典条目数: " + str(len(Industry_dict)) + " 新增条目数: " + str(len(Industry_dict) - initial_industry_items))
    save_noun_dict()
    save_industry_dict()

# Purpose:  Generate a random string
def get_some_letters():
    rtn = ""
    IsAbbr = random.randint(1, 10) < 4
    if IsAbbr:                                      # Abbreviation
        for i in range(random.randint(2, 5)):
            rtn += chr(random.randint(65, 90))
    else:                                           # CamelCaps
        for i in range(random.randint(1, 2)):           # Random letter segments (Starts by upper case letters)
            rtn += chr(random.randint(65, 90))              # Get a upper case letter
            for j in range(random.randint(2, 5)):           # Following by a series of lower case letters
                rtn += chr(random.randint(97, 122))
    return rtn

# Purpose:  Randomly select a text from source
# Args:     source: The list to select text from
#           possibility_of_and: The possibility of the occurence of conjunction words (possibility_of_and / 10)
#           force_use_and: Force using "与" as conjunction word
# Return:   Randomly selected string
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
                if random.randint(1, 10) <= 5:          # Switch the word to make it fancy
                    tmp += "与"
                else:
                    tmp += "及其"
            tmp += data[random.randint(0, len(data) - 1)]
            return tmp
    return data[index]

# Purpose:  Get a Sao sentence!
# Args:     sao_degree: Degree of Sao. Should not be too high! 3 is Sao enough
#           need_letters: Add letters between nouns
# Return:   A Sao sentence
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

# Purpose:  Show help
def show_help():
    print("基于当前脚本语言程序所能实现的功能而提供的可用人机交互命令:\n\n"
          "help : 通过基于键盘的人机互动方式显示该基于控制台输出的帮助指令\n\n"
          "update keyword start end : 基于百度学术搜索的现代互联网技术以及客户输入的搜索内容(keyword)、开始页面(start)和结束页面(end)范围进行的在线大数据搜索、数据分析以及更新用户词库的功能实现\n"
          "例如: update 冰棍 1 10 会分析百度学术上以“冰棍”为关键字的1-10页搜索结果的标题并添加词汇到字典中\n\n"
          "update_google keyword start end : 基于谷歌学术搜索的现代互联网技术以及客户输入的搜索内容(keyword)、开始页面(start)和结束页面(end)范围进行的在线大数据搜索、数据分析以及更新用户词库的功能实现\n"
          "例如: update_google 冰棍 1 10 会分析谷歌学术上以“冰棍”为关键字的1-10页搜索结果的标题并添加词汇到字典中\n\n"
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

# Purpose:  Show error message
def show_error():
    print("此基于脚本语言的菜鸡程序未能处理刚才出现的异常，需要劳烦用户另行重新进行输入以取得期望中的计算机程序的执行结果。\n"
          "Exception: ", end='')
    print(sys.exc_info()[1])

# Entry point
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
        while userinput.find("  ") != -1:                   # Remove redundant spaces in the input
            userinput = userinput.replace("  ", " ")

        if userinput == '':                                 # Get Sao sentence
            print(get_sao_sentence())
        else:
            userinput = userinput.split(" ")
            if userinput[0] == 'help':                      # Show help
                show_help()
            elif userinput[0] == 'get':                     # Get Sao sentence (with arguments)
                need_letters = False
                if len(userinput) == 1:                         # No arguments
                    print(get_sao_sentence())
                elif len(userinput) >= 2:
                    if userinput[1].isnumeric():
                        if int(userinput[1]) == 1:                      # Need letters specified
                            need_letters = True
                        elif int(userinput[1]) != 0:
                            show_error()
                            continue
                    else:
                        show_error()
                    if len(userinput) >= 3:
                        if userinput[2].isnumeric():
                            if int(userinput[2]) >= 0:                  # Sao degree specified
                                print(get_sao_sentence(need_letters, int(userinput[2])))
                            else:
                                show_error()
                        else:
                            show_error()
                    else:
                        print(get_sao_sentence(need_letters))
            elif userinput[0] == 'update':                  # Update dictionaries via Baidu Scholar
                try:
                    if userinput[2].isnumeric() and userinput[3].isnumeric():
                        update_dictionaries(False, userinput[1], int(userinput[2]), int(userinput[3]))
                    else:
                        show_error()
                except:
                    show_error()
            elif userinput[0] == 'update_google':           # Update dictionaries via google scholar
                try:
                    if userinput[2].isnumeric() and userinput[3].isnumeric():
                        update_dictionaries(True, userinput[1], int(userinput[2]), int(userinput[3]))
                    else:
                        show_error()
                except:
                    show_error()
            elif userinput[0] == 'input':                   # Manually input dictionary
                try:
                    if userinput[1] == 'industry':              # For industry dictionary
                        if userinput[2] in Industry_dict:
                            print("您要输入的条目已存在！")
                        else:
                            Industry_dict.update({' '.join(userinput[2:]):0})
                            print("成功添加！")
                            save_industry_dict()
                    elif userinput[1] == 'noun':                # For noun dictionary
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
            elif userinput[0] == 'remove':                  # Manually remove
                try:
                    if userinput[1] == 'industry':              # For industry dictionary
                        if not userinput[2] in Industry_dict:
                            print("您要移除的条目不存在！")
                        else:
                            del Industry_dict[' '.join(userinput[2:])]
                            print("成功移除！")
                            save_industry_dict()
                    elif userinput[1] == 'noun':                # For noun dictionary
                        if not userinput[2] in NounList_dict:
                            print("您要移除的条目不存在！")
                        else:
                            del NounList_dict[' '.join(userinput[2:])]
                            print("成功移除！")
                            save_noun_dict()
                    else:
                        show_error()
                except:
                    show_error()
            elif userinput[0] == 'check':                   # Check dictionary
                try:
                    if userinput[1] == 'industry':              # For industry dictionary
                        print(list(Industry_dict.keys()))
                        print("工业类型词典条目数: " + str(len(Industry_dict)))
                    elif userinput[1] == 'noun':                # For noun dictionary
                        print(list(NounList_dict.keys()))
                        print("名词词典条目数: " + str(len(NounList_dict)))
                    else:
                        show_error()
                except:
                    show_error()
            elif userinput[0] == 'exit':                    # Exit
                break
            else:                                           # Unknown command
                print("用户刚才通过人机交互的方式给这个基于脚本语言的垃圾程序输入了其不能理解的内容，需要劳烦用户另行重新进行输入以取得期望中的计算机程序的执行结果。")
