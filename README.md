# WeChatRobot 微信自动回复机器人
## 利用wxpy框架+图灵机器人+MUI框架
## 特性：运行在服务器的版本，可以通过网页访问，扫码二维码登录启动并管理机器人
需要的python package:flask MySQLdb 
需要预装mysql环境，mysql账户、密码配置在DataBase.py文件内,mysql数据库配置文件为robot.sql
因为懒得写密码加密，表单传输过程使用明文![avatar](https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=372837488,2096860054&fm=27&gp=0.jpg)
为保证私密，不保存微信缓存文件
不提供百度OCR的APIKey 和图灵机器人的APIKey