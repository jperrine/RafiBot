from ircBase import *
import httplib
from bs4 import BeautifulSoup

redditConnection = httplib.HTTPConnection('www.reddit.com')
lastPostedLink = ''

def main(irc):
	message = irc.lastMessage()

	#If no room activity for 10 mins link the top rated carPorn picture if it hasn't already been linked
	if noRoomActivityForTime(irc, 600):
		try:
			urlFormat = '/r/carporn'
			redditConnection.request('GET', urlFormat)
			responseBody = redditConnection.getresponse()
			responseBodyString = responseBody.read()

			#Find all of the links
			soup = BeautifulSoup(responseBodyString)
			anchors = soup.find_all('a', "title")

			#Show the top link if it hasn't already been posted
			global lastPostedLink
			topRedditLink = anchors[0]['href']
			if topRedditLink != lastPostedLink:
				lastPostedLink = topRedditLink
				irc.sendMessage(topRedditLink)
		except:
			#Recreate the reddit connection, this should only happen in a timeout
			global redditConnection
			redditConnection = httplib.HTTPConnection('www.reddit.com')