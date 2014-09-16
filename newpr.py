#!/usr/bin/python

import base64
import urllib, urllib2
import cgi
import cgitb
import simplejson as json
import random
import sys
import ConfigParser
from StringIO import StringIO
import gzip
cgitb.enable()

def is_new_contributor(username, stats):
    for contributor in stats:
        if contributor['login'] == username:
            return False
    return True

contributors_url = "https://api.github.com/repos/%s/%s/contributors?per_page=400"
collaborators_url = "https://api.github.com/repos/%s/%s/collaborators"
post_comment_url = "https://api.github.com/repos/%s/%s/issues/%s/comments"

welcome_msg = "Thanks for the pull request, and welcome! The Rust team is excited to review your changes, and you should hear from @%s (or someone else) soon."
warning_summary = '<img src="http://www.joshmatthews.net/warning.svg" alt="warning" height=20> **Warning** <img src="http://www.joshmatthews.net/warning.svg" alt="warning" height=20>\n\n%s'
unsafe_warning_msg = 'These commits modify **unsafe code**. Please review it carefully!'

def api_req(method, url, data=None, username=None, token=None, media_type=None):
	data = None if not data else json.dumps(data)
	headers = {} if not data else {'Content-Type': 'application/json'}
	req = urllib2.Request(url, data, headers)
	req.get_method = lambda: method
	if token:
        	base64string = base64.standard_b64encode('%s:x-oauth-basic' % (token)).replace('\n', '')
        	req.add_header("Authorization", "Basic %s" % base64string)

	if media_type:
		req.add_header("Accept", media_type)
	f = urllib2.urlopen(req)
	if f.info().get('Content-Encoding') == 'gzip':
	    buf = StringIO(f.read())
	    f = gzip.GzipFile(fileobj=buf)
	return f.read()

print "Content-Type: text/html;charset=utf-8"
print

config = ConfigParser.RawConfigParser()
config.read('./config')
user = config.get('github', 'user')
token = config.get('github', 'token')

post = cgi.FieldStorage()
payload_raw = post.getfirst("payload",'')
payload = json.loads(payload_raw)
if payload["action"] != "opened":
	sys.exit(0)

owner = payload['pull_request']['base']['repo']['owner']['login']
repo = payload['pull_request']['base']['repo']['name']
stats_raw = api_req("GET", contributors_url % (owner, repo), None, user, token)
stats = json.loads(stats_raw)

author = payload["pull_request"]['user']['login']
issue = str(payload["number"])

def post_comment(body, owner, repo, issue, user, token):
    global post_comment_url
    try:
        result = api_req("POST", post_comment_url % (owner, repo, issue), {"body": body}, user, token)
    except urllib2.HTTPError, e:
        if e.code == 201:
                pass
	else:
		raise e

if is_new_contributor(author, stats):
	collaborators = ['brson', 'nikomatsakis', 'pcwalton', 'alexcrichton', 'aturon', 'huonw'] if repo == 'rust' and owner == 'rust-lang' else ['test_user_selection_ignore_this']
        random.seed()
        to_notify = random.choice(collaborators)
	post_comment(welcome_msg % to_notify, owner, repo, issue, user, token)

warn_unsafe = False
diff = api_req("GET", payload["pull_request"]["diff_url"])
for line in diff.split('\n'):
    if line.startswith('+') and not line.startswith('+++') and line.find('unsafe') > -1:
        warn_unsafe = True

warnings = []
if warn_unsafe:
    warnings += [unsafe_warning_msg]

if warnings:
    post_comment(warning_summary % '\n'.join(map(lambda x: '* ' + x, warnings)), owner, repo, issue, user, token)
