from email.mime.text import MIMEText
import smtplib
import time


# constructing the message.
payload = MIMEText(message)
payload['Subject'] = subject
payload['From'] = sender_info.email
payload['To'] = recipient_address

def send(sender_info, recipient_address, subject, message, count=1, rate_in_seconds=5):

	# getting a connection to the smtp server
	server = smtplib.SMTP(sender_info.domain.host,sender_info.domain.port)
	server.ehlo_or_helo_if_needed()
	server.starttls()
	server.ehlo_or_helo_if_needed()

	# logging in under the particular user
	server.login(sender_info.username, sender_info.password)

	# sending the message
	server.send_message(payload)

	# closing connection to the server
	server.quit()

	#
	time.sleep(rate_in_seconds)