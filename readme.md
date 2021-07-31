#### 简单图片文字识别 ###
+ 基于百度的 <code>baidu-aip</code> sdk 进行简单封装
+ 支持 <font color='blue'>本地</font>、<font color='blue'>网络图片</font> 内容识别
+ 服务端 api 基于 <code>flask</code>进行编写
#### 项目结构说明 ####
+ img 目录 测试的图片
+ orc_test_case.py 测试文件
+ orc_utils.py 图片文字识别的核心类
+ server.py api接口
+ Pipfile pip 环境配置文件
#### 项目启动 ####
1. 启动服务端
~~~python
执行命令: python server.py
~~~~
2. 执行测试用例
~~~python
执行命令: python ocr_test_case.py
~~~