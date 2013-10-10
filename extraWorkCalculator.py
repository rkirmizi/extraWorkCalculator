#!/usr/bin/env python
#-*- coding: utf-8 -*-

from subprocess import *
import datetime

GIT_COMMIT_FIELDS = ['id', 'author_name', 'author_email', 'date', 'message']
GIT_LOG_FORMAT = ['%H', '%an', '%ae', '%ad', '%s']
GIT_LOG_FORMAT = '%x1f'.join(GIT_LOG_FORMAT) + '%x1e'

p = Popen('git log --format="%s"' % GIT_LOG_FORMAT, shell=True, stdout=PIPE)
(log, _) = p.communicate()
log = log.strip('\n\x1e').split("\x1e")
log = [row.strip().split("\x1f") for row in log]
log = [dict(zip(GIT_COMMIT_FIELDS, row)) for row in log]

short_months = ["Jan","Feb" ,"Mar","Apr","May" ,"June","Jul","Aug","Sep","Oct" ,"Nov","Dec"]

def calculateExtraWork():
	email = raw_input('Commiter email address:\t')
	month = raw_input('Month to calculate (in format):%s\n' %(", ".join(short_months)))
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
	try:
		calculateExtraWork()
	except KeyboardInterrupt:
		print "\nCtrl+C detected..\nExiting app.."