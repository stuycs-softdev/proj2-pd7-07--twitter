from flask_oauth import OAuth
from flask import Flask
from flask import session, url_for, redirect, render_template, request, flash
import urllib2
import json

app = Flask(__name__)
oauth = OAuth()


twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key='zBxQ4c3ywctjoghjEtOn0Q',
    consumer_secret='16ODAwbjnKWv5S86vqzQxeaktQW1bZJxttIynwdZzBs'
)


@twitter.tokengetter
def get_twitter_token(token=None):
    #return session.get('twitter_token')
    return ("2208115477-sB8ldFSXBf9c3tSLgh0fSsiwTNOVdi84hZWUeft","NmYOFDYfeHq9qe7El8FH9i0QPrU3bufiTRjvXLWEnTEdp")

@app.route('/login')
def login():
    return twitter.authorize(callback=url_for('oauth_authorized',
        next=request.args.get('next') or request.referrer or None))


@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']

    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)


@app.route("/")
def index():
    result = twitter.request("https://api.twitter.com/1.1/search/tweets.json?q=%23blah&lang=en",data="",headers=None,format='urlencoded',method='GET',content_type=None,token=get_twitter_token()).raw_data
    nicedata = json.loads(result)
    
    return render_template("home.html", data = nicedata['statuses'][0]['text'])



if __name__=="__main__":
    app.debug=True
    app.secret_key = 'super secret'
    app.run(host='0.0.0.0',port=5000)
