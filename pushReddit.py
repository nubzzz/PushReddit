#!/usr/bin/env python

"""
PushReddit

Bot that pushs a notification of new posts on Reddit to an Android device using pushover
"""

import praw
import re
import time
import pushover
import syslog
import MySQLdb
import sched

# Declare variables
application = ##application##
user = ##user##

# Database connection init
db = MySQLdb.connect("localhost",##username##,##password##,"pushReddit")
cursor = db.cursor()

# Setup the scheduler
s = sched.scheduler(time.time, time.sleep)

# Database insert function
def insert(ID, name, url, date):
	try:
		cmd = "INSERT INTO Done values (%s,%s,%s,%s)"
		cursor.execute(cmd,(ID, name, url, date))
		db.commit()
	except:
		db.rollback()
		
# Database id function - returns list of ids
def getExisting():
	cursor.execute("SELECT id from Done")
	data = cursor.fetchall()
	dataList = []
	for i in data:
		for a in i:
			dataList.append(a)
	return dataList

# Setup pushover and the useragent for praw
pushover.init(application)
client = pushover.Client(user)
r = praw.Reddit(user_agent='New post checker by /u/#yourusernamehere#')

# Main Function
def main():
	submissions = r.get_subreddit('pipetobaccomarket').get_new(limit=20)
	# iterate through them
	for x in submissions:
		# Pull out all 'For Sale' posts 
		match = re.search('WT[TB]', str(x))
		# Create the finished list
		already_done = getExisting()
		if x.id not in already_done and not match:
			# strip title of post and assemble message
			stripped_title = str(re.sub(r'([0-9]\s::\s)', '', str(x), flags=re.IGNORECASE))
			message = stripped_title + ' - ' + x.short_link
			# print out to stdout
			print 'Message sent:  New r/pipetobaccomarket Post - ' + message
			# send message via Pushover
			client.send_message(message, title="New r/pipetobaccomarket Post", priority=1)
			# Log to syslog for documentation sake (will be replaced by logger at some point)
			syslog.syslog('PushReddit - Message sent:  New r/pipetobaccomarket Post - ' + message)
			# Add post ID to the database
			insert(x.id, stripped_title, x.short_link, x.created_utc)
	# Run every 300 seconds (5 minutes)
	s.enter(300, 1, main, ())

# Run main
if __name__ == '__main__':
	try:
		while True:
			main()
			s.enter(300, 1, main, ())
			s.run()
	except:
		db.close()
