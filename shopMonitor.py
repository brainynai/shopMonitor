import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import requests
import re
from bs4 import BeautifulSoup
from time import sleep
import ctypes


#Function to send emails 
def send_email(email_recipient,
               email_subject,
               email_message,
               attachment_location = '',
               pw = 'senderpassword_notanactualpwdontworry'):

    email_sender = 'scriptemail_notarealemailofc@gmail.com'

    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = ';'.join(email_recipient)
    msg['Subject'] = email_subject

    msg.attach(MIMEText(email_message, 'plain'))

    if attachment_location != '':
        filename = os.path.basename(attachment_location)
        attachment = open(attachment_location, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part)

    #Will require gmail option to allow "less secure apps" for the sender account
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(email_sender, pw)
        text = msg.as_string()
        server.sendmail(email_sender, email_recipient, text)
        print('email sent')
        server.quit()
    except IndexError:
        print("SMPT server connection error")

    return True


def main():
    newproducts, knownproducts = [], []

    #Using a text file to store the products seen last time
    with open('products.txt', 'r') as f:
        for line in f:
            knownproducts.append(line.strip())

    #Get the html of the hardware sale page        
    page = requests.get('https://myshop.senecacollege.ca/collections/its-used-hardware-sale').content

    #Soouuuup
    soup = BeautifulSoup(page, 'lxml')

    #Find all the anchor tags to filter down. Probably could've easily done the filtering in this regex.
    alla = soup.find_all(href=re.compile('.*\/collections\/its-used-hardware-sale.*'))

    #Pick out just the href value/url
    urls = [str(a)[str(a).find('href="') + 6 : str(a).find('"', str(a).find('href="')+6)] for a in alla]

    #Filters irrelevant tags because I didn't want to play with regex anymore
    urls = [url for url in urls if url.startswith('/collections') and not url.endswith('atom')]

    #Pick out just the product name (was on the end of the url)
    products = [url[url.rfind('/')+1:] for url in urls]


    with open('products.txt', 'w') as f:
        for product in products:
            if product not in knownproducts:
                newproducts.append(product)
            f.write(product + '\n')

    if len(newproducts) > 0:
        #print(newproducts)

        #Makes a popup messagebox
        ctypes.windll.user32.MessageBoxW(0, 'Just found these things:\n' + '\n'.join(newproducts), "Shop Monitor Alert", 8192)

        #send_email(['myemailforreceiving@gmail.com'], 'New things found on ITS Sale', 'Just found these things:\n' + '\n'.join(newproducts))
    else:
        print('Nothing yet.\n')

while(True):
    main()
    sleep(60*5) #Going to check the site every 5 minutes

