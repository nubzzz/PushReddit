Pushreddit
=========

Once a new submission is noticed this script will send a push notification through Pushover
to every phone setup under the account. This allows the watching of marketplace like subreddits
such as <a href="http://www.reddit.com/r/pipetobaccomarket/">/r/pipetobaccomarket</a> for new submissions.

Requirements:

A Pushover Account - https://pushover.net/

The Python Reddit API wrapper - https://github.com/praw-dev/praw

The Pushover API wrapper - http://pythonhosted.org/python-pushover/

MySQLdb - http://mysql-python.sourceforge.net/


Set up:

1. Open file in your favorite text editor
2. Modify the values for the pushover keys
3. Modify the values for your database information
4. Modify the useragent
5. Create the required table with the following:
```CREATE TABLE IF NOT EXISTS `Done` (`id` varchar(100) COLLATE utf8_bin NOT NULL,`name` varchar(100) COLLATE utf8_bin NOT NULL,`url` varchar(100) COLLATE utf8_bin NOT NULL,`date`  varchar(100) COLLATE utf8_bin NOT NULL PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;```
6. Modify the subreddit you wish to pull from
7. Modify what you are looking for with regards to the regex
8. Run the script and watch for Pushover notifications
