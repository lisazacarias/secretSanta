from __future__ import print_function
from random import shuffle
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv
from getpass import getpass

nameCol = "Name"
emailCol = "Email"
suggestionCol = "Any special requests/suggestions/factoids/jokes for your Santa?"

name2email = {}
name2request = {}
names = []

with open("test.csv") as f:
    csvReader = csv.reader(f)
    header = next(csvReader)

    nameColIdx = header.index(nameCol)
    emailColIdx = header.index(emailCol)
    suggestionColIdx = header.index(suggestionCol)

    for row in csvReader:
        names.append(row[nameColIdx])
        name2email[row[nameColIdx]] = row[emailColIdx]
        name2request[row[nameColIdx]] = row[suggestionColIdx]

shuffle(names)

assignment = {}

for i in range(0, len(names)):
    assignment[names[i]] = names[(i + 1) % len(names)]

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
username = input("gmail username: ")
try:
    server.login(username, getpass(prompt="gmail password: "))
except smtplib.SMTPAuthenticationError:
    print("Gmail authentication error. Please try again.")

fromaddr = username + "@gmail.com"

for giver, receiver in assignment.items():

    toaddr = name2email[giver]
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Secret Santa Result!"

    body = ("Congratulations " + giver + ", you are " + receiver
            + "'s Secret Santa! If your recipient has a message for you, "
              "it'll be listed below. It's a $25 limit, "
              "but that is by no means the target! The best gifts are often"
              " inexpensive yet creative(: \n"
              "\nAt some point this week, a box will magically appear in "
              "the ACR for you to deposit your gift and pick up your "
              "own! You can open yours whenever you'd like, but for anyone who'd"
              " like to have a more formal \'opening party\', we're planning on"
              " having a holiday potluck at 3:30PM on Wednesday Dec. 18th in the "
              "ACR.\n"
              "\nHappy shopping/crafting! "
              "And remember that I don't know any of the assignments!"
              " I wrote a script so that I could be as suprised as everyone else(:\n"
            + ("\nSpecial requests/suggestions/factoids/jokes from your santee: "
               + name2request[receiver]) if name2request[receiver] else "")

    msg.attach(MIMEText(body, 'plain'))

    try:
        server.sendmail(fromaddr, toaddr, msg.as_string())
    except smtplib.SMTPSenderRefused as SMTPServerDisconnected:
        print("Sender refused or server disconnected - might be two factor "
              "authentication. Try again with app password?")
