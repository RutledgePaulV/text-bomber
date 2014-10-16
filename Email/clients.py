import smtplib
import time

def send(host, port, username, password, rate, payload):

	# getting a connection to the smtp server
	server = smtplib.SMTP(host, port)
	server.ehlo_or_helo_if_needed()
	server.starttls()
	server.ehlo_or_helo_if_needed()

	# logging in under the particular user
	server.login(username, password)

	# sending the message
	server.send_message(payload)

	# closing connection to the server
	server.quit()

	# sleeping to avoid rate limits imposed by email providers
	time.sleep(rate)