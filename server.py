import os
from flask import Flask, Response, request
from highfive.newpr import new_comment, new_pr

app = Flask(__name__)

# Throwaway root server
@app.route('/')
def app_root():
    return 'Highfive server for Tessel'

# Check for Dokku
@app.route('/check.txt')
def app_check():
    return 'simple_check'


# Highfive endpoint
@app.route('/highfive', methods=['POST'])
def app_highfive_newpr():
    secret = request.args.get('secret')
    if secret != os.environ.get('HIGHFIVE_WEBHOOK_SECRET'):
        return ('Invalid secret', 400, [])

    user = os.environ.get('HIGHFIVE_USERNAME')
    token = os.environ.get('HIGHFIVE_ACCESS_KEY')

    payload = request.get_json()
    print(request.get_data())
    if payload and payload.get('action') == "opened":
        new_pr(payload, user, token)
    elif payload and payload.get('action') == "created":
        new_comment(payload, user, token)
    else:
        return ('Invalid payload', 500, [])

    return Response('all good', mimetype='text/html;charset=utf-8')
