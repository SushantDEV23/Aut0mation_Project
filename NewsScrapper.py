#importing several packages
import requests     #https requests

from bs4 import BeautifulSoup     #web scrapping
import smtplib
#emailBody
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime   #system date and time manipulation

now=datetime.datetime.now()

#email content placeholder

content=" "

#Script to extract the news

def extract_news(url):
    print("EXTRACTING Economic Times Top Headlines.....")
    cnt=''
    cnt +=('<b>ET TOP STORIES:</b>\n'+'<br'+'-'*50+'<br>')
    response=requests.get(url)
    content=response.content
    soup=BeautifulSoup(content,'html.parser')
    for i,tag in enumerate(soup.find_all('ul',attrs={'href':'','valign':''})):
        cnt+=((str(i+1)+' :: '+tag.text + "\n" + '<br>') if tag.text!='Follow Us On' else'')
    return cnt
cnt=extract_news('https://economictimes.indiatimes.com/')
content+=cnt
content+=('<br>------<br>')
content+=('<br><br>End of Message')

#updating the email address
SERVER='smtp.gmail.com'
PORT=587
FROM='***************'
TO='*****************'   #this can contain multiple gmail id contained in a list
PAS='******'  #password of the FROM ID

msg=MIMEMultipart()

msg['Subject']='Top News Stories of Todays in ET [AUTOMATED EMAIL]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(now.year)
msg['FROM']=FROM
msg['TO']=TO

msg.attach(MIMEText(content,'html'))

print('Initiating Server')
server=smtplib.SMTP(SERVER, PORT)
server.set_debuglevel(1)   #To print any error message if the server fails to connect
server.ehlo()
server.starttls()
server.login(FROM, PAS)
server.sendmail(FROM, TO, msg.as_string())

print('Email has been sent...')
server.quit()

