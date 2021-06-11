
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header

def send_email(body):
    # SMTP服务器,这里使用企业邮箱
    mail_host = "smtp.300.cn"
    # 发件人邮箱
    mail_sender = "wuhaoyu@300.cn"
    # 邮箱授权码,注意这里不是邮箱密码,如何获取邮箱授权码,请看本文最后教程
    mail_license = "wuhaoyu@300"
    # 收件人邮箱，可以为多个收件人
    mail_receivers = ["1165951374@qq.com"]

    mm = MIMEMultipart('related')

    # 邮件主题
    subject_content = """自动化测试异常"""
    # 设置发送者,注意严格遵守格式,里面邮箱为发件人邮箱
    mm["From"] = "异常监控<wuhaoyu@300.com>"
    # 设置接受者,注意严格遵守格式,里面邮箱为接受者邮箱
    mm["To"] = "receiver_1_name<1165951374@qq.com>"
    # 设置邮件主题
    mm["Subject"] = Header(subject_content,'utf-8')

    # 邮件正文内容
    body_content = body
    # 构造文本,参数1：正文内容，参数2：文本格式，参数3：编码方式
    message_text = MIMEText(body_content,"plain","utf-8")
    # 向MIMEMultipart对象中添加文本对象
    mm.attach(message_text)


    # 创建SMTP对象
    stp = smtplib.SMTP()
    # 设置发件人邮箱的域名和端口，端口地址为25
    stp.connect(mail_host, 25)
    # set_debuglevel(1)可以打印出和SMTP服务器交互的所有信息
    stp.set_debuglevel(1)
    # 登录邮箱，传递参数1：邮箱地址，参数2：邮箱授权码
    stp.login(mail_sender,mail_license)
    # 发送邮件，传递参数1：发件人邮箱地址，参数2：收件人邮箱地址，参数3：把邮件内容格式改为str
    stp.sendmail(mail_sender, mail_receivers, mm.as_string())
    print("邮件发送成功")
    # 关闭SMTP对象
    stp.quit()


