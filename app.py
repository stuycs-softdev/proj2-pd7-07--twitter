from flask_oauth import OAuth
from flask import Flask, Markup
from flask import session, url_for, redirect, render_template, request, flash
import urllib2
import json
from pymongo import MongoClient
from time import time
from random import choice


app = Flask(__name__)
oauth = OAuth()

client = MongoClient()
db = client['highscores']
scores = db['scores']

username = ""
start = ""
previous = ""
current = ""
end = ""
numClicks = 0
numSeconds = 0
startingTime = 0

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
    global previous
    global current
    global end
    global numClicks
    global numSeconds
    global startingTime
    start = end = previous = current = ""
    numClicks = numSeconds = startingTime = 0
    if request.method == "GET":
        return render_template("home.html")
    else:
        start = str(request.form['start'])
        current = start
        startingTime = time()
        return redirect(url_for('game'))

@app.route("/error", methods = ['GET','POST'])
def error():
    global start
    global previous
    global current
    global end
    global numClicks
    global numSeconds
    global startingTime
    start = end = previous = current = ""
    numClicks = numSeconds = startingTime = 0
    if request.method == "GET":
        return "ERROR: No results. Please try a new search!<br>" + render_template("home.html")
    else:
        start = str(request.form['start'])
        current = start
        startingTime = time()
        return redirect(url_for('game'))

@app.route("/game", methods = ['GET','POST'])
def game():
    global start
    global previous
    global current
    global end
    global numClicks
    global numSeconds
    global startingTime

    result = twitter.request("https://api.twitter.com/1.1/search/tweets.json?q=%23{0}&lang=en&count=100".format(current),data="",headers=None,format='urlencoded',method='GET',content_type=None,token=get_twitter_token()).raw_data
    nicedata = json.loads(result)
    
    tweets = []
    numhashtags = 0
    i = 0
    allhashtags = []

    if len(nicedata['statuses']) == 0:
        return redirect(url_for('error'))

    if end == "":
        end = generateEnd()

    while numhashtags < 5 and i < len(nicedata['statuses']):
        hashtags = separateHashtags(nicedata['statuses'][i]['text'])
        if len(hashtags) <= 1:
            i+=1
        elif (numhashtags + len(hashtags) - 1) <= 5:
            addTweet = True
            for x in range (0, len(hashtags)):
                if hashtags[x].lower() in allhashtags:
                    addTweet = False
            if addTweet == False:
                i+=1
            else:
                tweets.append(nicedata['statuses'][i]['text'])
 #               numhashtags += (len(hashtags) - 1)
                for tag in hashtags:
                    if tag.lower() != current.lower() and tag.lower() != previous.lower():
                        numhashtags += 1
                        allhashtags.append(tag.lower())
        else:
            i+=1
            
    tweets = '<br><br>'.join(tweets)
    tweets = Markup(tweets)
    if previous != "":
        allhashtags.append(previous)
    
    if request.method == "GET":
        return render_template("game.html", data = tweets, start = start, current = current, end = end, hashtags = allhashtags, numClicks = numClicks)
    else:
        button = request.form['button']
        if button == "restart":
            return redirect(url_for("home"))
        else:
            previous = current
            current = button
            numClicks += 1
            if current.lower() == end.lower():
                numSeconds = int(time() - startingTime)
                return redirect(url_for('highscore'))
            else:
                return redirect(url_for('game'))

@app.route("/highscore", methods = ['GET','POST'])
def highscore():
    global numSeconds
    global numClicks
    if scores.count() > 20:
        cursor = db.scores.find(limit=20).sort([("time", -1), ("numclicks",-1)])
        results = [line for line in cursor]
        dictWorst = results[0]
        if (numSeconds > int(dictWorst["time"])):
            return redirect(url_for("home"))
        elif (numSeconds == int(dictWorst["time"])) and (numClicks >= int(dictWorst["numclicks"])):
            return redirect(url_for("home"))
        else:
            return highscoreHelper()
    else:
        return highscoreHelper()

def highscoreHelper():
    global numSeconds
    global numClicks
    if request.method == "GET":
        return render_template("username.html",time=numSeconds,clicks=numClicks)
    else:
        username = request.form["username"]
        score = {"user": username, "numclicks": numClicks, "time": numSeconds}
        scores.insert(score)
        return redirect(url_for("leaderboard"))

@app.route("/leaderboard", methods = ['GET','POST'])
def leaderboard():
    cursor = db.scores.find(limit=20).sort([("time",1), ("numclicks",1)])
    results = [line for line in cursor]
    print results
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


def generateEnd():
    global start
    global current
    search = start
    for j in range(0,3):
        result = twitter.request("https://api.twitter.com/1.1/search/tweets.json?q=%23{0}&lang=en&count=100".format(search),data="",headers=None,format='urlencoded',method='GET',content_type=None,token=get_twitter_token()).raw_data
        nicedata = json.loads(result)


        numhashtags = 0
        i = 0
        allhashtags = []

        while numhashtags < 5 and i < len(nicedata['statuses']):
            hashtags = separateHashtags(nicedata['statuses'][i]['text'])
            if len(hashtags) <= 1:
                i+=1
            elif (numhashtags + len(hashtags) - 1) <= 5:
                addTweet = True
                for x in range (0, len(hashtags)):
                    if hashtags[x].lower() in allhashtags:
                        addTweet = False
                if addTweet == False:
                    i+=1
                else:
                    #numhashtags += (len(hashtags) - 1)
                    for tag in hashtags:
                        if tag.lower() != current.lower() and tag.lower() != previous.lower():
                            allhashtags.append(tag.lower())
                            numhashtags += 1
            else:
                i+=1

        search = choice(allhashtags)
    return search


if __name__=="__main__":
    app.debug=True
    app.secret_key = 'super secret'
    app.run(host='0.0.0.0',port=7007)
