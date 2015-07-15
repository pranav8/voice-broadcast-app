import twilio
import os
from flask import url_for
from flask import Flask
from flask import Response
from flask import request
from flask import render_template
from flask import session
from twilio import twiml
from twilio.rest import TwilioRestClient

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')

# Create a Flask web app
app = Flask(__name__)

app.secret_key = 'XEqnUY76sZRyPcmCagW'

# Route for Recording the Voice Message

@app.route('/broadcast', methods=['GET'])
def broadcast():
	#Start start
	resp = twiml.Response()

	resp.pause(length = "0.2")

	resp.say("Welcome to your Voice Broadcast System")

	with resp.gather(action='/record') as g:

		g.say("Press 1 to start recording voice message")
		g.say("Press 2 to quit")

	resp.pause(length='1')
	path = url_for('.broadcast')
	resp.redirect(path)

	# Return control to Twilio
	return str(resp)

@app.route('/record', methods=['GET','POST'])
def record():
	#Start record
	resp = twiml.Response()

	digit = request.form['Digits']

	if digit == '1':
		resp.say("Recording will start after the beep. Press the pound key to stop recording")
		resp.redirect(method='GET',url='message')
	elif digit == '2':
		resp.say("Hanging up")
		resp.hangup()
	else:
		resp.say("Invalid entry")

	resp.pause(length='1')
	path = url_for('.record')
	resp.redirect(path)

	# Return control to Twilio
	return str(resp)

@app.route('/message', methods=['GET','POST'])
def message():
	#Start message

	resp = twiml.Response()
	resp.record(action='/dial', timeout=10, finishOnKey='#',playBeep='true')

	# Return control to Twilio
	return str(resp)

@app.route('/dial', methods=['GET','POST'])
def dial():
	#Start dial
	resp = twiml.Response()
	session['record_url'] = request.values.get('RecordingUrl')

	with resp.gather(action="/send") as g:

		g.say("Press 1 to hear recording again")
		g.say("Press 2 to broadcast")
		g.say("Press 3 to abort")

	resp.pause(length='1')
	path = url_for('.dial')
	resp.redirect(path)

	# Return control to Twilio
	return str(resp)

@app.route('/send', methods=['GET','POST'])
def send():
	#Start send

	resp = twiml.Response()

	digit = request.form['Digits']

	if digit == '1':
		resp.play(url=session['record_url'])
		resp.hangup()
	elif digit == '2':
		resp.dial(number='+16142718890')
	elif digit == '3':
		resp.hangup()

	resp.pause(length='1')
	path = url_for('.send')
	resp.redirect(path)

	return str(resp)

if __name__ == '__main__':
    # Note that in production, you would want to disable debugging
    app.run(debug=True)
