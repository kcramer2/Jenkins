import smtplib
import subprocess

# List of users to notify
userList = ["turatsinze","kcramer3"]

userNames = [u for u in userList]

# Users email list
emailList = [name +  "@wisc.edu" for name in userNames]

# Submit server running the script
proc = subprocess.Popen("hostname", shell=True, stdout=subprocess.PIPE, )
submitserver = proc.communicate()[0]

SERVER = "chtc.wisc.edu"
FROM = "aaaaaa@example.com"
TO = emailList
SUBJECT = ("issue with" + " " + submitserver)
MSG = "These test jobs are not being successully submitted"

# Prepare actual message

message = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, MSG)

# Send the mail

server = smtplib.SMTP(SERVER)
server.sendmail(FROM, TO, message)
server.quit()
