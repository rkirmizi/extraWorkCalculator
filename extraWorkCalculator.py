#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Inspired by http://blog.lost-theory.org/post/how-to-parse-git-log-output
"""

from subprocess import *
import datetime
import sys
import os

GIT_COMMIT_FIELDS = ['id', 'author_name', 'author_email', 'date', 'message']
GIT_LOG_FORMAT = ['%H', '%an', '%ae', '%ad', '%s']
GIT_LOG_FORMAT = '%x1f'.join(GIT_LOG_FORMAT) + '%x1e'

p = Popen('git log --format="%s"' % GIT_LOG_FORMAT, shell=True, stdout=PIPE)
(log, _) = p.communicate()
log = log.strip('\n\x1e').split("\x1e")
log = [row.strip().split("\x1f") for row in log]
log = [dict(zip(GIT_COMMIT_FIELDS, row)) for row in log]

short_months = ["Jan","Feb" ,"Mar","Apr","May" ,"June","Jul","Aug","Sep","Oct" ,"Nov","Dec"]

def calculateExtraWork(gitDir="."):
	os.chdir(gitDir)
	email = raw_input('Commiter email address:\t')
	month = raw_input('Month to calculate (in format): %s\n' %(", ".join(short_months)))
	work_start = int(raw_input('Work hour starts at:\nPlease Choose in range: %s\n' %range(0,24)))
	work_end = int(raw_input('Work hour ends at:\nPlease Choose in range: %s\n' %range(0,24)))
	print 'Calculating extra work for %s at month: %s. Excluded hours: %s' %(email, month,range(work_start,work_end))
	for i in log:
	    if i['author_email'] == email:
	        if i['date'].find(month) != -1:
	            tarih = i['date'].split('+')[0].strip()
	            tarih = datetime.datetime.strptime(tarih, '%a %b %d %H:%M:%S %Y')
	            if tarih.hour not in range(work_start,work_end):
	            	output = 'Extra Work: %s' %(i['date'].split('2013')[0].strip())
	            	if tarih.weekday() in (5,6):#cumartesi pazar
	            		print '{} (Weekend)'.format(output)
	            	else:
	            		print output


if __name__ == '__main__':
	if len(sys.argv) < 2:
		try:
			print "Git directory not given.\nTrying current path as git directory (%s)" %os.getcwd()
			if os.path.exists('.git'):
				calculateExtraWork()
			else:
				print "Given directory is not a git directory\nExiting app.."
				sys.exit()

		except KeyboardInterrupt:
			print "\nCtrl+C detected..\nExiting app.."
	else:
		try:
			print "Working on dir %s" %sys.argv[1]
			if os.path.exists('%s/.git'%sys.argv[1]):
				calculateExtraWork(sys.argv[1])
			else:
				print "Given directory is not a git directory\nExiting app.."
				sys.exit()
		except KeyboardInterrupt:
			print "\nCtrl+C detected..\nExiting app.."
