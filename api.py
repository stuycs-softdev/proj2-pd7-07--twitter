from flask_oauth import OAuth
from flask import Flask, Markup
from flask import session, url_for, redirect, render_template, request, flash
import urllib2
import json
from pymongo import MongoClient
import datetime

app = Flask(__name__)
oauth = OAuth()

client = MongoClient()
db = client['highscores']
scores = db['scores']

username = ""
start = ""
current = ""
end = ""
numClicks = 0
numSeconds = 0

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

@app.route("/", methods = ['GET','POST'])
def home():
    global start
    global current
    if request.method == "GET":
        return render_template("home.html")
    else:
        start = str(request.form['start'])
        current = start
        return redirect(url_for('game'))
    

@app.route("/game", methods = ['GET','POST'])
def game():
    global start
    global current
    global end
    global numClicks
    result = twitter.request("https://api.twitter.com/1.1/search/tweets.json?q=%23{0}&lang=en&count=100".format(current),data="",headers=None,format='urlencoded',method='GET',content_type=None,token=get_twitter_token()).raw_data
    nicedata = json.loads(result)
    
    tweets = []
    numhashtags = 0
    i = 0
    allhashtags = []

    while numhashtags < 10 and i < len(nicedata['statuses']):
        hashtags = separateHashtags(nicedata['statuses'][i]['text'])
        if len(hashtags) <= 1:
            i+=1
        elif (numhashtags + (len(hashtags) - 1)) <= 10:
            tweets.append(nicedata['statuses'][i]['text'])
            numhashtags += (len(hashtags) - 1)
            i+=1

            for tag in hashtags:
                if tag.lower() != current.lower():
                    allhashtags.append(tag)
        else:
            i+=1
            
    tweets = '<br><br>'.join(tweets)
    tweets = Markup(tweets)
    
    if request.method == "GET":
        return render_template("game.html", data = tweets, start = start, current = current, end = end, hashtags = allhashtags)
    else:
        current = request.form['button']
        numClicks += 1
        return redirect(url_for('game'))

@app.route("/highscore", methods = ['GET','POST'])
def highscore():
    cursor = db.scores.find(limit=50).sort("time", -1)
    dictWorst = cursor[0]
    if (numSeconds > dictWorst["time"]) and scores.count() >= 50:
        return redirect(url_for("home"))
    else:
        if request.method == "GET":
            return render_template("username.html")
        else:
            username = request.form["username"]
            score = {"user": username, "numclicks": numClicks, "time": numSeconds, "date": datetime.datetime.utcnow()}
            scores.insert(score)
            return redirect(url_for("leaderboard"))

@app.route("/leaderboard", methods = ['GET','POST'])
def leaderboard():
    cursor = db.scores.find(limit=50).sort("time")
    results = [line for line in cursor]
    if request.method == "GET":
        return render_template("highscores.html", scores=results)
    else:
        return redirect(url_for("home"))


def separateHashtags(tweet):
    copy = tweet.split('#')
    for i in range(1,len(copy)):
        j = copy[i].split(' ')
        copy[i] = j[0]

    return copy[1:]


if __name__=="__main__":
    app.debug=True
    app.secret_key = 'super secret'
    app.run(host='0.0.0.0',port=5000)
