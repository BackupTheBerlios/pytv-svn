#!/usr/bin/python2.4
# -*- coding: iso-8859-1 -*-

# Copyright (C) 2006  Stefan Nistelberger (scuq@kages.at)
#		      Hans-Peter Schadler (blade.runner@gmx.at)
#		      Daniel Schrammel (nowx@gmx.at)
# tv_grab_de_siehferninfo.py - tv grabber

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.


import re
import readline
import os
import sys
from optparse import OptionParser
#from dl_tvtoday import dl_tvtoday
from mx.DateTime import *



def printVersion():
	print "version  - see svn log"

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
			userConfig_file.write(channel_id+":"+all_channels[channel_id]+"\n")
			print "channel "+all_channels[channel_id]+" added."

		elif answer == "":
			userConfig_file.write(channel_id+":"+all_channels[channel_id]+"\n")
			print "channel "+all_channels[channel_id]+" added."
	
		elif answer == "all":
		 	for chid in all_channels.keys():		
				userConfig_file.write(chid+":"+all_channels[chid]+"\n")
			print "all channels added."
			break

		elif answer == "no":
			print "channel "+all_channels[channel_id]+ " skipped."
		
		elif answer == "none":
			print "all channels skipped."
			break

		else:
			print "channel "+all_channels[channel_id]+ " skipped."

	 userConfig_file.close()

	except KeyboardInterrupt:
		print "Ctrl+C recognized."
		userConfig_file.close()
			

def getTvmDateString(dayOffset,dayStartOffset):
	todaysDate = now() + RelativeDateTime(days=dayOffset+int(dayStartOffset))

	if (todaysDate.day < 10):
		dayStr = `0`+`todaysDate.day`
	else:
		dayStr = todaysDate.day

	if (todaysDate.month < 10):
		monthStr = `0`+`todaysDate.month`
	else:
		monthStr = todaysDate.month

	#return `todaysDate.year`+str(monthStr)+str(dayStr)
	return str(dayStr)+"."+str(monthStr)+"."+`todaysDate.year`

def runFetcher(daysToGrab, daysOffset, user_configured_channels, downloadFolder, MainUrl, InfoStr, ChannelStr, DateStr):

	#fetcher = dl_tvtoday(tvtNextPageStr, tvtNextPageStrStep, tvtMoreShowsStr)
	for user_channel in user_configured_channels.keys():
		count = 0
		while count < int(daysToGrab):
			#tempTimeStr = getTvmDateString(count, daysOffset)
			tempTimeStr = getTvmDateString(count, daysOffset)
	# "http://programm.tvtoday.de/tv/programm/programm.php?ztag=0&sparte=alle&uhrzeit=00%3A00%3A00&sender=ARD&von=12"

			downloadUrl = MainUrl+"?"+ChannelStr+user_configured_channels[user_channel]+"&"+DateStr+str(tempTimeStr)
			print "fetcher should download: "+downloadUrl
	#		fetcher.download(downloadUrl, downloadFolder+user_channel+"_"+getTvmDateString(count, daysOffset)+".nohtml")
			
			count = count + 1		

def runConverter(downloadFolder, tvmExtension, gzExtension, xmlExtension, gzsFolder, xmlTvmFolder):

	print "reading files in "+downloadFolder

	if not os.path.exists(gzsFolder):
                os.makedirs(gzsFolder)

	if not os.path.exists(xmlTvmFolder):
		os.makedirs(xmlTvmFolder)


	for filename in os.listdir(downloadFolder):
		if re.search(tvmExtension+"$", filename):
			tvmfilename = downloadFolder+filename
			gzfilename = gzsFolder+filename
			gzfilename = re.sub(tvmExtension,gzExtension,gzfilename)	
			xmlfilename = xmlTvmFolder+filename
			xmlfilename = re.sub(tvmExtension,xmlExtension,xmlfilename)

			print "starting converter for: "+tvmfilename
			tvmconverter = convert_tvm_gz_xml(tvmfilename, gzfilename, xmlfilename)

			
			if tvmconverter.tvm2gz() == 0:
				print "successfully converted to gzip format."
			else:
				print "conversion to gzip format failed."
				sys.exit(1)

			if tvmconverter.extract_gz() == 0:
				print "successfully created xml file: "+xmlfilename
			else:
				print "xml file creation failed."
				sys.exit(1)

			os.remove(tvmfilename)
			os.remove(gzfilename)



def main():

	parser = OptionParser()
	parser.add_option("-C", "--configure", action="store_true", dest="run_configure", default=False, help="configure your channel list")
	parser.add_option("-D", "--days", dest="days", help="set number of days to grab. max 7 default 7")
	parser.add_option("-O", "--offset", dest="days_offset", help="start with day offset form today")
	parser.add_option("-s", "--share", dest="share_dir", help="share dir e.g. /usr/share/xmltv/")
	parser.add_option("-f", "--config-file", dest="config_file", help="set the config file to use")
	parser.add_option("-o", "--output", dest="output_file", help="set the output file")
	parser.add_option("-c", "--channelid-file", dest="channelid_file", help="set location of the channel_ids file")
	parser.add_option("-v", "--version", action="store_true", dest="show_version", default=False, help="show version")
	parser.add_option("-b", "--capabilities", action="store_true", dest="show_capabilities", default=False, help="show capabilities")
	parser.add_option("-q", "--quiet", action="store_true", dest="be_quiet", default=False, help="only error msgs")
	parser.add_option("-a", "--cache", action="store_true", dest="cache_mode", default=False, help="use cached xml files")

	(options, args) = parser.parse_args()


	if options.show_capabilities:
		print "baseline"
		print "manualconfig"
		print "share"
		print "cache"
		sys.exit(0)


		



	if options.show_version:
		printVersion()
		sys.exit(0)

	if not options.days:
		daysToGrab = 7
	else:
		if int(options.days) > 7 or int(options.days) < 1:
			print "invalid days value, grabing 1 day."
			daysToGrab = 7
		else:
			daysToGrab = options.days


	if not options.days_offset:
		daysOffset = 0
	else:
		daysOffset = options.days_offset
	
	
	if options.share_dir:
		shareDirectory = options.share_dir
		if shareDirectory[-1] != os.sep:
			shareDirectory = shareDirectory+os.sep
	else:
		shareDirectory = "./" 
	
	if options.channelid_file:
		channel_file=shareDirectory+options.channelid_file		
	else:
		channel_file=shareDirectory+"channel_ids"

	if not os.path.isfile(channel_file):
		print "channel ids file not found: "+channel_file
		sys.exit(1)

	all_channels = getChannelIDs(channel_file)

	pytvHome = os.environ["HOME"]+os.sep+".xmltv"+os.sep+"pytv"+os.sep

	if not os.path.exists(pytvHome):
		os.makedirs(pytvHome)

	userConfig = pytvHome+"pytv.conf"
	downloadFolder = pytvHome+"fetchedPages"+os.sep

	if not os.path.exists(downloadFolder):
		os.makedirs(downloadFolder)

	if options.run_configure:
		print "running channel configuration"
		runConfigure(userConfig,all_channels)
		sys.exit(0)

	print "grabing "+`daysToGrab`+" days with an offset of: "+`daysOffset`

	try:
		user_configured_channels = getChannelIDs(userConfig)

	except IOError:
		print "no config file found. please run --configure."
	
	
	MainUrl = "http://www.siehferninfo.de/"
	InfoStr = "textinfo="
	ChannelStr = "sender="
	DateStr = "viewdatum="

	#runFetcher(daysToGrab, daysOffset, user_configured_channels, downloadFolder, tvtMainUrl, tvtCategoryStr, tvtTimeStartStr, tvtDayOffsetStr, tvtChannelStr, tvtNextPageStr, tvtMoreShowsStr, tvtNextPageStrStep)
	runFetcher(daysToGrab, daysOffset, user_configured_channels, downloadFolder, MainUrl, InfoStr, ChannelStr, DateStr)
	







if __name__=='__main__': main()
