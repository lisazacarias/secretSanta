from __future__ import print_function
from random import shuffle
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv
from getpass import getpass
from typing import List


TEST_MODE = True


class Participant:
    def __init__(self, name, email, office, address, onSite, suggestion):
        # type: (str, str, str, str, bool, str) -> None
        self.name = name
        self.email = email
        self.office = office
        self.address = address
        self.onSite = onSite
        self.santee = None  # type: Participant
        self.suggestion = suggestion

    def assignSantee(self, santee):
        # type: (Participant) -> None
        self.santee = santee


def main():

    nameCol = "Name"
    emailCol = "Email"
    suggestionCol = "Any special requests/suggestions/factoids/jokes for your Santa?"
    officeCol = "Office Location"
    mailingCol = "Mailing Address"
    onSiteCol = "Would you be able to pick up your gift on site?"

    participants = []  # type: List[Participant]

    with open("test.csv" if TEST_MODE else "Secret Santa 2020(1-15).csv") as f:
        csvReader = csv.reader(f)
        header = next(csvReader)

        nameColIdx = header.index(nameCol)
        emailColIdx = header.index(emailCol)
        suggestionColIdx = header.index(suggestionCol)
        officeColIdx = header.index(officeCol)
        mailingColIdx = header.index(mailingCol)
        onSiteColIdx = header.index(onSiteCol)

        for row in csvReader:
            name = row[nameColIdx]
            onSite = (row[onSiteColIdx] == "Yes")
            participant = Participant(name=name, email=row[emailColIdx],
                                      office=row[officeColIdx],
                                      address=row[mailingColIdx], onSite=onSite,
                                      suggestion=row[suggestionColIdx])
            participants.append(participant)

    shuffle(participants)

    for i in range(0, len(participants)):
        participants[i].assignSantee(participants[(i + 1) % len(participants)])

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    username = input("gmail username: ")

    try:
        server.login(username, getpass(prompt="gmail password: "))
    except smtplib.SMTPAuthenticationError:
        print("Gmail authentication error. Please try again.")

    fromaddr = username + "@gmail.com"

    for participant in participants:
        toaddr = participant.email
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Secret Santa Result!"
        body = ("Dear {SANTA},\n\n"
                "Congratulations! you are {SANTEE}'s Secret Santa! The dollar limit for this year"
                " is $25 before shipping, but that is by no means the target. "
                "The best gifts are often inexpensive yet creative(:\n\n"
                "Given that things have been so incredibly bananas, we're gonna do "
                "things a little bit differently this year. If your santee is able "
                "to pick up their gift on site, there will be an office location at "
                "the end of this email. If not, you will see only a mailing address. "
                "If you decide to drop it off in person, you have the option of "
                "leaving it at their desk or leaving it at mine (B52/246 in case "
                "they're floating around inconveniently and would see you. Whatever "
                "you do, you will need to fill out another form ({LINK}) when you've "
                "successfully dropped/mailed it off so that I can tell them to go "
                "look for it (it will be anonymous submission, so I'll have no idea"
                "who's telling me they did the thing!). On that note, remember that "
                "this whole thing is automated, so I don't know the assignments "
                "either! That makes it more fun for me(:\n\n"
                "Happy Secretive Gift Giving!\n"
                "Lisa\n\n"
                "{SUGGESTION}\n\n"
                "{OFFICE}\n\n"
                "Mailing Address: {ADDRESS}")

        santee = participant.santee

        suggestion = ("Requests/Suggestions/Factoids/Jokes: {SUGGESTION}"
                      .format(SUGGESTION=santee.suggestion)
                      if santee.suggestion else "")

        office = ("Office Location: {OFFICE}".format(OFFICE=santee.office)
                  if santee.onSite else "")

        link = ("https://forms.office.com/Pages/ResponsePage.aspx?"
                "id=Wq7yzmYmFkebYOiOKuv0mjsMAgZabqZBtA-ff3Sz3pVUQkRWV0IyWFhLRVc1V1RWQ0Y3S1BDRjU1RC4u")

        msg.attach(MIMEText(body.format(SANTA=participant.name, SANTEE=santee.name,
                                        LINK=link, SUGGESTION=suggestion,
                                        OFFICE=office, ADDRESS=santee.address)))

        try:
            server.sendmail(fromaddr, toaddr, msg.as_string())
        except smtplib.SMTPSenderRefused as SMTPServerDisconnected:
            print("Sender refused or server disconnected - might be two factor "
                  "authentication. Try again with app password?")


if __name__ == '__main__':
    main()
