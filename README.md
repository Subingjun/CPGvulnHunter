# CPGvulnhunter
一个利用cpg和llm去进行漏洞挖掘任务的框架。

# workflow
除了初始化核心类cpg之外，所有的任务被抽象为pass。
initpass负责去读取目标源码中的所有外部函数，并传递给llm来判断senmantics（这里可以理解为外部函数的数据流传播规则，如memcpy的数据流是第二个参数传递给第一个参数，用来服务污点分析任务的）
basepass是一个污点类型漏洞的基本任务，现在实现的漏洞只有命令注入，如果要针对其他类型的漏洞，则只需要继承basepass，然后重写source、sink、santzier以及污点链条判断的提示词即可。

# 一些使用上的问题
joern下载需要使用git-lfs：<br>
<code>sudo apt install git-lfs</code><br>
<code>git lfs install</code>#初始化<br>
<code>git lfs pull</code>#拉取<br>
使用<code>pip install -r requirement.txt</code>文件时，需要删除-e .(因为没有setup.py)，不会影响运行，但是需要把run.py放在src中。
