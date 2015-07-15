from flask import Flask, request, redirect
from twilio import twiml
 
app = Flask(__name__)
 
 
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond and greet the caller by name."""
 
    body = request.values.get('Body', None)

    r = twiml.Response()

    if body == "hours":
        r.message(" 9 to 5")
    elif body == "location":
        r.message("FC Road")
    else:
    	r.message("Invalid")
    	
    return str(r)
 
if __name__ == "__main__":
    app.run(debug=True)
