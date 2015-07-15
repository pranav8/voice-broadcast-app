from twilio.rest.lookups import TwilioLookupsClient
 
# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "ACd3dc8a02a92dd0cb1ccf73b9aece2475"
auth_token = "3871c53d73bd5f4478109de6486c18e1"
client = TwilioLookupsClient(account_sid, auth_token)
 
number = client.numbers.get("+15108675309")
print number.carrier['name']