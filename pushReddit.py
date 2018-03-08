#!/usr/bin/python3

"""
PushReddit

Bot that pushs a notification of new posts on Reddit to an Android device using pushover
"""

import praw
import re
import time
import pushover
import syslog
import pymysql
import json
import sys

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
db = pymysql.connect(db_host,db_user,db_pass,db_database)
cursor = db.cursor()

# Database insert function
def insert(ID, name, url, date):
    try:
        stripped_name = db.escape(name)
        cursor.execute("INSERT INTO Done values ({},{},{},{})".format(ID,stripped_name,url,date))
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
    # iterate through them
    for x in submissions:
        # Discard all Wanting to Trade/Wanting to Buy posts, leaving only Wanting to Sell or untagged posts
        match = re.search('WT[TB]', str(x.title))
        # Pull the list of ids from the database
        already_done = getExisting()
        if x.id not in already_done and not match:
            # strip title of post and assemble message
            stripped_title = str(re.sub(r'([0-9]+\s::\s)', '', str(x.title), flags=re.IGNORECASE))
            short_link = 'http://redd.it/{}'.format(x.id)
            message = stripped_title + ' - ' + short_link
            # print out to stdout
            print('Message sent:  New r/pipetobaccomarket Post - {}'.format(message))
            # send message via Pushover
            client.send_message(message, title="New r/pipetobaccomarket Post", priority=1)
            # Log to syslog for documentation sake (will be replaced by logger at some point)
            syslog.syslog('PushReddit - Message sent:  New r/pipetobaccomarket Post - ' + message)
            # Add post ID to the database
            insert(x.id, stripped_title, short_link, x.created_utc)

def main_loop():
    while 1:
        main()
        time.sleep(600)

# Run main_loop
if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        db.close()
        sys.stderr.write('\nExiting by user request.\n')
        sys.exit(0)
    except:
        db.close()
        sys.stderr.write('\nExiting due to unknown cause.\n')
        print(sys.exc_info()[0])
        sys.exit(0)
