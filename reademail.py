import imaplib
import os
SERVER='imap.gmail.com'
USER='miguelangeldiazmejia79'
PASS='ylbpmwgzdtsjovpl'
Mail='miguelangeldiazmejia79@gmail.com'

#Conectar al servidor gmail
server=imaplib.IMAP4_SSL(SERVER,993)

#Login
server.login(USER,PASS)

#seleccionar la bandeja inbox
status, count=server.select('Inbox')
status, data=server.fetch(count[0],'(UID BODY[TEXT])')

flag=str((data[0] [1]))
print(flag)
server.close()
server.logout()
