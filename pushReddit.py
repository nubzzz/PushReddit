#!/usr/bin/env python

"""
PushReddit

Bot that pushs a notification of new posts on Reddit to an Android device using pushover
"""

import praw
import re
import time
import pushover

#Declare variables
application = ##application
user = ##user

# Setup pushover and the useragent for praw
pushover.init(application)
client = pushover.Client(user)
r = praw.Reddit(user_agent='New post checker by /u/nubzzz1836')

# Init the list of completed post ids
already_done = []

while True:
	# get your subreddit's newest 20 posts
	submissions = r.get_subreddit('pipetobaccomarket').get_new(limit=20)
	# iterate through them
	for x in submissions:
		# Pull out all 'For Sale' posts 
		match = re.search('WT[TB]', str(x))
		if x.id not in already_done and not match:
			# strip and send a push notification for all posts
			stripped_title = str(re.sub(r'([0-9]\s::\s)', '', str(x), flags=re.IGNORECASE))
			message = stripped_title + ' - ' + x.short_link
			print 'Message sent:  New r/pipetobaccomarket Post - ' + message
			client.send_message(message, title="New r/pipetobaccomarket Post", priority=1)
			already_done.append(x.id)
	time.sleep(300) #sleep for 5 minutes and do it all over again
