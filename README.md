Pushreddit
=========

Once a new submission is noticed this script will send a push notification through Pushover
to every phone setup under the account. This allows the watching of marketplace like subreddits
such as <a href="http://www.reddit.com/r/pipetobaccomarket/">/r/pipetobaccomarket</a> for new submissions.

Requirements:

A Pushover Account - https://pushover.net/

The Python Reddit API wrapper - https://github.com/praw-dev/praw

The Pushover API wrapper - http://pythonhosted.org/python-pushover/

pymysql - https://github.com/PyMySQL/PyMySQL


Set up:

1. Copy config.json.example to config.json and modify values
2. Run `pip install -r requirements.txt` to install the python requirements
3. Create database
4. Create the required table with the following:
```CREATE TABLE IF NOT EXISTS `Done` (`id` varchar(100) COLLATE utf8_bin NOT NULL PRIMARY KEY,`name` varchar(65353) COLLATE utf8_bin NOT NULL,`url` varchar(100) COLLATE utf8_bin NOT NULL,`date`  varchar(100) COLLATE utf8_bin NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;```
5. Run the script and watch for Pushover notifications
