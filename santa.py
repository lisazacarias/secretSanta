from random import shuffle
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import csv
from getpass import getpass

name2email = {}
name2request = {}
names = []

with open("secretSantaInterest2018.tsv") as f:
    tsvreader = csv.reader(f, delimiter='\t')

    for row in tsvreader:
        names.append(row[3])
        name2email[row[3]] = row[2]
        name2request[row[3]] = row[5]

shuffle(names)

assignment = {}

for i in xrange(0, len(names)):
   assignment[names[i]] = names[(i+1) % len(names)]

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
username = raw_input("gmail username: ")
try:
    server.login(username, getpass(prompt="gmail password: "))
except smtplib.SMTPAuthenticationError:
    print "Gmail authentication error. Please try again."

fromaddr = username + "@gmail.com"

for giver, receiver in assignment.iteritems():

    toaddr = name2email[giver]
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Secret Santa Result!"

    body = ("Congratulations " + giver + ", you are " + receiver
            + "'s Secret Santa! If your recipient has a message for you, "
              "it'll be listed below. Gentle reminder that it's a $25 limit, "
              "but that is by no means the target! The best gifts are often"
              " inexpensive yet creative(: \n"
              "\nAt some point next week, a box will magically appear in "
              "the touchdown room for you to deposit your gift and pick up your "
              "own! You can open yours whenever you'd like, but for anyone who'd"
              " like to have a more formal \'opening party\', we're planning on"
              " having a get together at 4:30PM on Tuesday Dec. 18th in the "
              "ACR! There's also talk of turning this into a big holiday "
              "potluck, so stay posted! Word has it that Matt has volunteered "
              "his world famous mac n cheese, so if that doesn't sway you, "
              "I don't know what will.\n"
              "\nHappy shopping!\n"
            + "\nMessage from your Santee: " + name2request[receiver])

    msg.attach(MIMEText(body, 'plain'))

    try:
        server.sendmail(fromaddr, toaddr, msg.as_string())
    except smtplib.SMTPSenderRefused, SMTPServerDisconnected:
        print "Sender refused or server disconnected - might be two factor " \
              "authentication. Try again with app password?"
