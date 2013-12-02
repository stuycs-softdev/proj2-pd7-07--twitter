proj2-pd7-07-#twitter
==================

Give #Twitter any hashtag you want. It will search Twitter for that hashtag, take some tweets containing the hashtag, take a random (different!) hashtag from one of those tweets, and then repeat the cycle, finally choosing another hashtag. Your job is to find a path between the two hashtags as quickly as possible using the same method as the program.

The minimum number of possible clicks to get from the start hashtag to the end hashtag is (typically) 3. However, our leaderboard goes primarily by speed: how quickly can you find the end hashtag? 

Team:
* Christopher Burke
* Jeremy Karson
* Maia Ezratty
* Shaan Sheikh

Requirements to Run:
* flask_oauth
* pymongo
* mongodb
* you must run mongod in another terminal 

Bugs/Notes:
* The minimum number of steps from start to end hashtag is three. However, it is conceivable that you could get there in two or even one step. Our program burrows two levels down, but this does not ensure that the same hashtag cannot be found one or zero levels down.
* Clicking on certain hashtags causes a "UnicodeEncodeError". We believe this occurs when you click on a hashtag containing an emoji.
* It is the user's job to strategize. We don't recommend "burrowing more than two levels down," but our program does allow it.
* When you click on a hashtag, the "previous" hashtag (whose page you were just on) is always listed as one of the hashtags you can click on. In this way, there is a built-in "back" button.
* Ideally, you can always find your way back to the starting hashtag. The tweet that links #money to #philosophy will also link #philosophy to #money.
* However, our program pulls the information directly from twitter. As such, it is conceivable that during the course of the user's playing of our game, their path could get "obstructed" by a flurry of new tweets. In this way, the user might not have an easy path back to the starting hashtag. If this happens: good luck.
* Typically, the program gives a choice of 5 tweets, plus the "previous" tweet when available. However, inconsistencies to this arise when: a) there are not enough results to produce 5 possible tweets and b) there is an inaccuracy in the search. For instance, a search for #football will match #football!!!. Our program deals with this as well as possible, but it does not exclude #football!!! from being one of the tweets that you can click on (IN ADDITION, IT IS POSSIBLE THAT THE END HASHTAG WILL INVOLVE A PATH THROUGH THIS HASHTAG!). The result is that it is possible to have six possible options for tweets you could click on.