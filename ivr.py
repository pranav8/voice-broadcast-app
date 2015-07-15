import os
from flask import url_for
from flask import Flask
from flask import Response
from flask import request
from flask import render_template
from twilio import twiml
from twilio.rest import TwilioRestClient


# Pull in configuration from system environment variables
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')

# create an authenticated client that can make requests to Twilio for your
# account.
#client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Create a Flask web app
app = Flask(__name__)


# Route for the IVR application
@app.route('/ivr', methods=['GET','POST'])
def ivr():
    # Start IVR
    resp = twiml.Response()

    resp.pause(length="0.2")

    resp.say("Thanks for calling.")

    with resp.gather(action="/play") as g:
        # Ask for input
        g.say("To talk to sales press 1")
        g.say("To talk to support press 2")

    resp.pause(length='1')
    path = url_for('.ivr')
    resp.redirect(path)

    # Return control to Twilio
    return str(resp)

# Route for playback
@app.route('/play', methods=['GET', 'POST'])
def play():
    # Parse user input
    resp = twiml.Response()

    digit = request.form['Digits']

    if digit == '1':
        resp.say("Connecting you to the agent")
        resp.dial(number = "+16142718890", action = "/callback")
    elif digit == '2':
        resp.say("Stop being cheap and pay full price")
    else:
        resp.say("You entered an invalid request")
        path = url_for('.ivr')
        resp.redirect(path, method = 'GET')
    return str(resp)

@app.route('/callback', methods=['GET', 'POST'])
def callback():

    resp = twiml.Response()

    resp.say("Incoming call")
    with resp.gather(action= "/whisper") as g:
        g.say("To accept the call press 1")
        g.say("To reject the call press 2")

    resp.pause(length='0.5')
    resp.redirect('.callback')
    return str(resp)

@app.route('/whisper', methods=['GET', 'POST'])
def whisper():

    resp = twiml.Response()

    digit = request.form['Digits']

    if digit == '1':
        resp.say("Connecting you to the caller")
    else:
        resp.say("Hanging up")
        resp.hangup()

    return str(resp)

if __name__ == '__main__':
    # Note that in production, you would want to disable debugging
    app.run(debug=True)