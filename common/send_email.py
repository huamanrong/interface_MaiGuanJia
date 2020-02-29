__author__ = '10336'
import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class SendEmail:
    def __init__(self,send, pwd, receiver, message, Subject):
        self.send = send
        self.pwd = pwd
        self.receiver = receiver
        self.message = message
        self.Subject = Subject

    def send_email_just_message(self):
        msg=MIMEText(self.message)
        msg["Subject"] = self.Subject
        msg["From"] = self.send
        msg["To"] = self.receiver
        send=smtplib.SMTP_SSL('smtp.qq.com',465)
        send.login(self.send,self.pwd)
        send.sendmail(self.send,self.receiver,msg.as_string())
        send.close()

    def send_email_with_file(self,file_path):
        #发送HTML等格式的附件，在邮箱中预览会出现显示问题，会以文本的形式展示，要下载到本地再打开！！！
        msg = MIMEMultipart()
        msg["Subject"] = self.Subject
        msg["From"] = self.send
        msg["To"] = self.receiver
        #---这是文字部分---
        part = MIMEText(self.message, _charset='utf-8')
        msg.attach(part)
        #---这是附件部分---
        # filename=os.path.split(file_path)[1]
        basename=os.path.basename(file_path)
        part = MIMEApplication(open(file_path,'rb').read())
        part['Content_Type'] = 'application/octet_stream'
        part.add_header('Content-Disposition', 'attachment', filename='%s' % basename.encode('gb2312'))
        msg.attach(part)
        #发送邮件部分
        send = smtplib.SMTP_SSL("smtp.qq.com", port=465,timeout=30)#连接smtp邮件服务器,端口默认是25
        send.login(self.send, self.pwd)#登录服务器
        send.sendmail(self.send, self.receiver, msg.as_string())#发送邮件
        send.close()

if __name__ == '__main__':
    send='1033674932@qq.com'
    pwd=''
    receiver='1033674932@qq.com'
    message='测试报告'
    Subject='发送html的邮件'
    file_path=r'D:\Backup\我的文档\GitHub\interface_automation\interface\test_result\html_report\test2018-11-06_14_06_33.html'
    SendEmail(send,pwd,receiver,message,Subject).send_email_with_file(file_path)
