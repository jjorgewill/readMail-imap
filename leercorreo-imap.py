import poplib,imaplib
import string,random
from io import StringIO,BytesIO
import logging
import socks
import socket
import email
#from email import parser
import mailparser

proxy_ip = "localhost"
port = 8091

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,proxy_ip,port,True)
socket.socket = socks.socksocket

SERVER = "imap.gmail.com"
USER = ""
PASSWORD = ""

# connect to server
#print ("iniciando conexion...")
server = imaplib.IMAP4_SSL(SERVER,993)
#print ("conectado...")

# log in
server.login(USER,PASSWORD)
#print("logueado")

server.select('INBOX') 
status,response = server.uid('search',None, '(UNSEEN)')
email_ids = response[0].decode().split()
unread_msg_number=len(email_ids) 

data_list = []
for e_id in email_ids: 
  data_dict = {}
  e_id = e_id #.decode('utf-8')
  _, response = server.uid('fetch',e_id,'(RFC822)')
  html = response[0][1].decode('utf-8')
  email_msg = email.message_from_string(html)
  email1 = mailparser.parse_from_string(html)   
  data_dict['id'] = str(e_id)
  data_dict['to'] = email_msg['To']
  data_dict['subject'] = email_msg['Subject']
  data_dict['from'] = email.utils.parseaddr(email_msg['From'])
  #data_dict['body'] = email_msg.get_payload(decode=True)
  data_dict['text'] = email1.text_plain
  data_list.append(data_dict)
 

new_mails_count = len(data_list)

if new_mails_count > 0 :
 for i in range(new_mails_count):
  temp=data_list[i]
  eid=temp['id']
  filename="Message "+str(eid)+".html"
  file = open(filename, "w")
  message="From: "+ str(temp['from']) 
  message+=" --- To: "+str(temp['to'])
  message+=" --- Subject: " +str(temp['subject'])
  message+=" --- Text: " +str(temp['text'])
  file.write(str(message))
  print("Finished download message " +str(eid))
else:
 print("You don't have any new mail")

