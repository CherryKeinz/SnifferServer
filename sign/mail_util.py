# -*- coding: utf-8 -*-

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
from smtplib import SMTP_SSL

from_addr = "kai_keinz@163.com"
password = "AIYUN1010"
to_addr = "553636890@qq.com"
smtp_server = "smtp.163.com"


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

class my_mail(object):
    def __init__(self, to_addr):
        self.to_addr = to_addr

    def send_mail(self, text):
        msg = MIMEText(text, 'plain', 'utf-8')
        msg['From'] = _format_addr(u'我的服务器 <%s>' % from_addr)
        msg['To'] = _format_addr(u'知名不具 <%s>' % self.to_addr)
        msg['Subject'] = Header(u'今天没有签到呀', 'utf-8').encode()

#        server = smtplib.SMTP(smtp_server, 25)
	server = SMTP_SSL(smtp_server)
	server.ehlo(smtp_server)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [self.to_addr], msg.as_string())
        server.quit()

#mail = my_mail("kai_keinz@163.com")
#mail.send_mail("teststet")
