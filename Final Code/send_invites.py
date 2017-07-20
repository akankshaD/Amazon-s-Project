import datetime
import time
import datetime
import time
import smtplib
from flask import make_response
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

#### Sends invites to the interviewers based on matched_list as input
def send_invites(matched_list):
	CRLF = "\r\n"
	login = "chanandler.bong19@outlook.com"
	password = "janice19"
	organizer = "ORGANIZER;CN=Chanandler:mailto:chanandler.bong19"+CRLF+" @outlook.com"
	fro = "Chanandler Bong <chanandler.bong19@outlook.com>"

	utc_mins = datetime.timedelta(minutes = 330)

	for match in matched_list:
		print(match)
		start_time = datetime.datetime.strptime(match["start_time"], '%d-%m-%Y %H:%M')
		start_time = start_time - utc_mins
		end_time = datetime.datetime.strptime(match["end_time"], '%d-%m-%Y %H:%M')
		end_time = end_time - utc_mins
		room = match["room"]
		interviewer = match["login_name"]
		attendees = []
		attendees.append(interviewer)

		dtstamp = datetime.datetime.now().strftime("%d%m%YT%H%M%SZ")
		dtstart = start_time.strftime("%d%m%YT%H%M%SZ")
		
		dtend = end_time.strftime("%d%m%YT%H%M%SZ")
		
		description = "DESCRIPTION: Meeting invitation"+CRLF
		
		attendee = "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE"+CRLF+" ;CN="+interviewer+";X-NUM-GUESTS=0:"+CRLF+" mailto:"+interviewer+CRLF
		ical = "BEGIN:VCALENDAR"+CRLF+"PRODID:pyICSParser"+CRLF+"VERSION:2.0"+CRLF+"CALSCALE:GREGORIAN"+CRLF
		ical+="METHOD:REQUEST"+CRLF+"BEGIN:VEVENT"+CRLF+"DTSTART:"+dtstart+CRLF+"DTEND:"+dtend+CRLF+"DTSTAMP:"+dtstamp+CRLF+organizer+CRLF
		ical+= "UID:FIXMEUID"+dtstamp+CRLF
		ical+= attendee+"CREATED:"+dtstamp+CRLF+description+"LAST-MODIFIED:"+dtstamp+CRLF+"LOCATION:"+CRLF+"SEQUENCE:0"+CRLF+"STATUS:CONFIRMED"+CRLF
		ical+= "SUMMARY:Meeting in " + room +" on "+start_time.strftime("%d%m%Y @ %H:%M")+CRLF+"TRANSP:OPAQUE"+CRLF+"END:VEVENT"+CRLF+"END:VCALENDAR"+CRLF



		eml_body = "Test interview invite in " + room + " on " + match["start_time"]
		msg = MIMEMultipart('mixed')
		msg['Reply-To']=fro
		msg['Date'] = formatdate(localtime=True)
		msg['Subject'] = "You know,we know!!"
		msg['From'] = fro
		msg['To'] = ",".join(attendees)

		part_email = MIMEText(eml_body,"html")
		part_cal = MIMEText(ical,'calendar;method=REQUEST')

		msgAlternative = MIMEMultipart('alternative')
		msg.attach(msgAlternative)

		ical_atch = MIMEBase('application/ics',' ;name="%s"'%("invite.ics"))
		ical_atch.set_payload(ical)
		Encoders.encode_base64(ical_atch)
		ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"'%("invite.ics"))

		eml_atch = MIMEBase('text/plain','')
		Encoders.encode_base64(eml_atch)
		eml_atch.add_header('Content-Transfer-Encoding', "")

		msgAlternative.attach(part_email)
		msgAlternative.attach(part_cal)

		mailServer = smtplib.SMTP('smtp.live.com', 587)
		mailServer.ehlo()
		mailServer.starttls()
		mailServer.ehlo()
		mailServer.login(login, password)
		try:
			mailServer.sendmail(fro, attendees, msg.as_string())
		except(SMTPRecipientsRefused, SMTPHeloError, SMTPSenderRefused, SMTPDataError) as err:
			return -1
		finally:
			mailServer.close()