# Sao_Title_Bot
一个生成骚论文题目的机器人

# 使用说明
如果您只是想体验一下，只需要:

1. 安装python
2. 通过pip安装numpy: `pip install numpy`
3. `python SaoLanguageBot.py`

如果您希望使用到完整的功能，包括词库爬虫，那么除了以上的步骤之外您还需要:

4. 安装Google Chrome浏览器
5. 下载适合您的系统及Google Chrome版本的[ChromeDriver](https://chromedriver.chromium.org/)并把可执行文件放到同一目录下
6. 通过pip安装selenium: `pip install selenium`
7. `python SaoLanguageBotFullVer.py`

# 功能介绍
自动根据词库生成一些无厘头的但是看起来却很骚的论文题目。例如:
```
（默认参数，不自动添加英文单词，骚程度=0）
关于新时代决策树上语义特征的中国产业国际竞争力分析与进一步精确量化

（自动添加英文单词，骚程度=0）
论一体化FRAVO资本属性中IiiofzWebGIS的地理信息系统及其线路故障定位优化矩阵算法

（自动添加英文单词，骚程度=2）
面向一体化Zhpl行业面板数据与故障树最小割集中XJCPL灰色模糊综合评判和Zhkd思与LqumlTsj权限管理的案例分析
```

词库可控。例如能够手动添加、手动删除、自动通过爬虫添加，包括自动分析百度学术及谷歌学术上搜索到的论文题目并添加词汇到词库中。词库越大，生成的题目就会有更多变化。

# 命令帮助 ~~（如果觉得程序里的帮助太难理解可以看这个）~~
## help
显示帮助

## input industry/noun text
把text输入到词库里。如：

`input industry 数学` 把“数学”添加到工业类型词库里

`input noun 实验` 把“实验”添加到名词词库里

## remove industry/noun text
把text从词库中移除。如：

`remove industry 数学` 把“数学”从工业类型词库里移除

`remove noun 实验` 把“实验”从名词词库里移除

## check industry/noun
查看词库内容。如：

`check industry` 查看工业类型词库

`check noun` 查看名词词库

## get [add_eng_word] [sao_degree]
获取一个骚标题。

`add_eng_word`: 可选参数。只能是0或者1。0说明不要自动添加英语单词；1说明要自动添加英语单词。0为默认值。

`sao_degree`: 可选参数。为非负整数。指定标题有多骚，越高越骚。0为默认值。

如:

`get` 按照默认参数生成一个标题

`get 1` 生成一个自动添加单词的，骚程度为0的标题

`get 1 2` 生成一个自动添加单词的，骚程度为2的标题

## update keyword start end
从百度学术搜索指定的内容，并从指定的页面范围分析并获取词汇。

`keyword`: 需要搜索的关键字。（推荐试一下“的”还有“基于”，能爬到不少词汇）

`start`: 开始页面

`end`: 结束页面

如:

`update 基于 1 10` 将自动从百度学术搜索“基于”并从第1到10页获取词汇。

## update_google keyword start end
从谷歌学术搜索指定的内容，并从指定的页面范围分析并获取词汇。

`keyword`: 需要搜索的关键字。（推荐试一下“的”还有“基于”，能爬到不少词汇）

`start`: 开始页面

`end`: 结束页面

_注意: 谷歌很烦，遇到疑似自动化程序会弹出人机验证。遇到这种情况，需要用户手动完成验证即可继续爬虫进程。_

如:

`update_google 基于 1 10` 将自动从谷歌学术搜索“基于”并从第1到10页获取词汇。

## 空白输入
相当于`get 0 0`

## exit
退出。

# 文件说明
`SaoLanguageBot.py` 去掉了爬虫部分的代码，减少了所依赖的库。

`SaoLanguageBotFullVer.py` 完整版的代码，包括了爬虫部分。

`chromedriver.exe` ChromeDriver 79.0.3945.36，支持我电脑上的Google Chrome 79.0.3945.130。您可以自行下载适合您的系统及Google Chrome版本的ChromeDriver可执行文件并将其替换掉。

`Industry_dict.npy`和`NounList_dict.npy` 分别是以文件形式存储的工业类型词库和名词词库。

# 为啥写这个东西
不知道，大概是太无聊？

当然，生成的东西完全不能作为论文题目（23333333

受到“狗屁不通文章生成器”的启发而编写。（这个比它差得远喽！

# 开原协议
MIT License. 请见[LICENSE](LICENSE)