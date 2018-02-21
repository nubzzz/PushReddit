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
import json

# Read in config file
with open('config.json') as data_file:
    data = json.load(data_file)

# Declare variables
application = data["keys"]["application"]
user = data["keys"]["user"]
db_user = data["database"]["username"]
db_pass = data["database"]["password"]
db_database = data["database"]["database"]
db_host = data["database"]["host"]
praw_useragent = data["praw"]["useragent"]
praw_client_id = data["praw"]["client_id"]
praw_client_secret = data["praw"]["client_secret"]

# Database connection init
db = MySQLdb.connect(db_host,db_user,db_pass,db_database)
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
r = praw.Reddit(user_agent=praw_useragent,
                client_id=praw_client_id,
                client_secret=praw_client_secret)

# Main Function
def main():
        submissions = r.subreddit('pipetobaccomarket').new(limit=20)
	#submissions = r.get_subreddit('pipetobaccomarket').get_new(limit=20)
	# iterate through them
	for x in submissions:
		# Discard all Wanting to Trade/Wanting to Buy posts, leaving only Wanting to Sell or untagged posts
		match = re.search('WT[TB]', str(x.title))
		# Pull the list of ids from the database
		already_done = getExisting()
		if x.id not in already_done and not match:
			# strip title of post and assemble message
			stripped_title = str(re.sub(r'([0-9]+\s::\s)', '', str(x.title), flags=re.IGNORECASE))
			short_link = 'http://redd.it/%s' % (x.id)
			message = stripped_title + ' - ' + short_link
                        escaped_title = MySQLdb.escape_string(stripped_title)
			# print out to stdout
			print 'Message sent:  New r/pipetobaccomarket Post - ' + message
			# send message via Pushover
			client.send_message(message, title="New r/pipetobaccomarket Post", priority=1)
			# Log to syslog for documentation sake (will be replaced by logger at some point)
			syslog.syslog('PushReddit - Message sent:  New r/pipetobaccomarket Post - ' + message)
			# Add post ID to the database
			insert(x.id, escaped_title, short_link, x.created_utc)
	# Run every 300 seconds (5 minutes)
	s.enter(300, 1, main, ())

# Run main
if __name__ == '__main__':
	try:
		main()
		s.enter(300, 1, main, ())
		s.run()
	except:
		db.close()
