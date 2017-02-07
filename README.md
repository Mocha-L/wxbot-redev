
#基于[wxBot](https://github.com/liuwons/wxBot) 项目实现一些微信的小功能开发
![python](https://img.shields.io/badge/python-2.7-ff69b4.svg)

##依赖

此版本只能运行于Python 2环境 。

**wxBot-redev** 用到了Python **requests** , **pypng** , **Pillow** 以及 **pyqrcode** 库。

使用之前需要所依赖的库:

```bash
pip install requests
pip install pyqrcode
pip install pypng
pip install Pillow
```

##功能

    1.微信自动回复（可配置回复内容和状态）
    2.支持图灵机器人聊天
    
##配置

在bot.py同级目录创建文件conf.ini包含：
    
    1.需要申请图灵机器人账号
    
    2.配置图灵机器人apikey
    
    3.加入master信息。
    
conf.ini示例如下：

```txt
[main]
key=41040614f**********d3a777561204f
[master]
name=pengbo
tel=186*****590
```

