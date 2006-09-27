#!/usr/bin/python2.4

import re
import readline
import os
import sys
import shutil
from optparse import OptionParser
import datetime
from fetcher import py_tvm_fetcher

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
			

# get the tvmovie date string for today
def getTvmDateString():
	if (datetime.date.today().month < 10):
       	 	monthStr = `0`+`datetime.date.today().month`
	else:
		monthStr = `datetime.date.today().month`

	if (datetime.date.today().day < 10):
       		 dayStr = `0`+`datetime.date.today().day`
	else:
		dayStr = `datetime.date.today().day`

	todayString = `datetime.date.today().year`+monthStr+dayStr
	
	return todayString

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
	
	if options.channelid_file:
		channel_file=options.channelid_file		
	else:
		channel_file="./channel_ids"

	if not os.path.isfile(channel_file):
		print "channel ids file not found: "+channel_file
		sys.exit(1)

	all_channels = getChannelIDs(channel_file)

	pytvHome = os.environ["HOME"]+os.sep+".xmltv"+os.sep+"pytv"+os.sep
	userConfig = pytvHome+"tv_grab_de_tvmovie.conf"
	downloadFolder = pytvHome+os.sep+"grabedTvms"+os.sep

	if options.run_configure:
		print "running channel configuration"
		runConfigure(userConfig,all_channels)
		sys.exit(0)

	tvmDate = getTvmDateString()
	tvmExtension = ".xml.tvm"
	tvmXmlUrl = "http://tvmovie.kunde.serverflex.info/onlinedata/xml-gz5/"		

	user_configured_channels = getUserChannels(userConfig)
	print user_configured_channels
		






if __name__=='__main__': main()
