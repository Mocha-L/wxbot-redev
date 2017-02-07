基于wxBot(https://github.com/liuwons/wxBot) 项目实现一些微信的小功能开发

1.微信自动回复（可配置回复内容和状态）
2.支持图灵机器人聊天

配置

在bot.py同级目录创建文件conf.ini包含：
1.需要申请图灵机器人账号
2.配置图灵机器人apikey
3.加入master信息。
conf.ini示例如下：
[main]    
key=41040614f**********d3a777561204f
[master]
name=pengbo
tel=186*****590
