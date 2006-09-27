#!/usr/bin/python2.4

import re
import readline
import os
import sys
import shutil
from optparse import OptionParser
#import datetime
from mx.DateTime import *



def printVersion():
	print "version 0.0.1 - basic script handling stuff."

def getUserChannels(user_channels_file):
	uchfile = open(user_channels_file, 'r')

	userchids = []

	while 1:
		lineStr = uchfile.readline()
		
		if not (lineStr):
			break

		lineStr = re.sub("\n$","",lineStr)

		userchids.append(lineStr)

	uchfile.close()
	return userchids



# suck in the channel_ids file into a dictionary
def getChannelIDs(channel_file):
	chidfile = open(channel_file, 'r')

	count = 0
	chids = {}
	splitter = re.compile(":")

	while 1:
		lineStr = chidfile.readline()

		if not (lineStr):
			break


		lineStr = re.sub("\n$","",lineStr)


		if re.search(":", lineStr):

			lineStrArr = splitter.split(lineStr)
			
			if len(lineStrArr[1]) == 1:
				chids["00"+lineStrArr[1]] = lineStrArr[0]
			elif len(lineStrArr[1]) == 2:
				chids["0"+lineStrArr[1]] = lineStrArr[0]
			else:
				chids[lineStrArr[1]] = lineStrArr[0]			
			count = count + 1
	chidfile.close()
	return chids

# run configure to write users channel config file
def runConfigure(userConfig,all_channels):
	print "writing config file: "+userConfig

	try:

	 userConfig_file = open(userConfig, 'w')

	 for channel_id in all_channels.keys():



		print "add channel "+all_channels[channel_id]+"? [yes,no,all,none (default=yes)]"

		answer = sys.stdin.readline()
		answer = re.sub("\n$","",answer)

		if answer == "yes":
			userConfig_file.write(channel_id+"\n")
			print "channel "+all_channels[channel_id]+" added."

		elif answer == "all":
		 	for chid in all_channels.keys():		
				userConfig_file.write(chid+"\n")
			print "all channels added."
			break

		elif answer == "no":
			print "channel "++all_channels[channel_id]+ " skipped."
			break

	 userConfig_file.close()

	except KeyboardInterrupt:
		print "Ctrl+C recognized."
		userConfig_file.close()
			

def getTvmDateString(dayOffset):
	#print "new date func"
	todaysDate = now() + RelativeDateTime(days=dayOffset)

	if (todaysDate.day < 10):
		dayStr = `0`+`todaysDate.day`
	else:
		dayStr = todaysDate.day

	if (todaysDate.month < 10):
		monthStr = `0`+`todaysDate.month`
	else:
		monthStr = todaysDate.month

	return `todaysDate.year`+str(monthStr)+str(dayStr)

def getTvms(daysToGrab, user_configured_channels, todaysDate, tvmXmlUrl, tvmExtension):
	print "get tvms"
	count = 0

	for user_channel in user_configured_channels:
		while count < int(daysToGrab):
			downloadUrl = tvmXmlUrl+getTvmDateString(count)+"_"+user_channel+tvmExtension
			print downloadUrl
				
			count = count + 1		

def main():

	parser = OptionParser()
	parser.add_option("-C", "--configure", action="store_true", dest="run_configure", default=False, help="configure your channel list")
	parser.add_option("-D", "--days", dest="days", help="set number of days to grab. max 7 default 1")
	parser.add_option("-f", "--config-file", dest="config_file", help="set the config file to use")
	parser.add_option("-o", "--output-file", dest="output_file", help="set the output file")
	parser.add_option("-c", "--channelid-file", dest="channelid_file", help="set location of the channel_ids file")
	parser.add_option("-v", "--version", action="store_true", dest="show_version", default=False, help="show version")

	(options, args) = parser.parse_args()

	if options.show_version:
		printVersion()
		sys.exit(0)

	if int(options.days) > 7 or int(options.days) < 1:
		print "invalid days value, grabing 1 day."
		daysToGrab = 1
	else:
		daysToGrab = options.days
	
	
	if options.channelid_file:
		channel_file=options.channelid_file		
	else:
		channel_file="./channel_ids"

	if not os.path.isfile(channel_file):
		print "channel ids file not found: "+channel_file
		sys.exit(1)

	all_channels = getChannelIDs(channel_file)

	pytvHome = os.environ["HOME"]+os.sep+".xmltv"+os.sep+"pytv"+os.sep

	if not os.path.exists(pytvHome):
		os.makedirs(pytvHome)

	userConfig = pytvHome+"tv_grab_de_tvmovie.conf"
	downloadFolder = pytvHome+os.sep+"grabedTvms"+os.sep

	if not os.path.exists(downloadFolder):
		os.makedirs(downloadFolder)

	if options.run_configure:
		print "running channel configuration"
		runConfigure(userConfig,all_channels)
		sys.exit(0)
	
	tvmDate = getTvmDateString(0)
	tvmExtension = ".xml.tvm"
	tvmXmlUrl = "http://tvmovie.kunde.serverflex.info/onlinedata/xml-gz5/"		

	print "grabing "+`daysToGrab`+" days."
	user_configured_channels = getUserChannels(userConfig)

	getTvms(daysToGrab, user_configured_channels, tvmDate, tvmXmlUrl, tvmExtension)
		






if __name__=='__main__': main()
