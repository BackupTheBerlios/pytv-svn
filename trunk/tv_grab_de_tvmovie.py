#!/usr/bin/python2.4
# -*- coding: iso-8859-1 -*-

# Copyright (C) 2006  Stefan Nistelberger (scuq@kages.at)
#		      Hans-Peter Schadler (blade.runner@gmx.at)
#		      Daniel Schrammel (nowx@gmx.at)
# tv_grab_de_tvmovie.py - tv movie grabber

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

sys.path.append('./xmlrewriter')
sys.path.append('./converter')

from optparse import OptionParser
from write_xmltv import write_xml
from convert_tvm_gz_xml import convert_tvm_gz_xml
from mx.DateTime import *
import urllib



def printVersion():
	print "version 0.0.2 - downloading works now."

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

	return `todaysDate.year`+str(monthStr)+str(dayStr)

def getTvms(daysToGrab, daysOffset, user_configured_channels, tvmXmlUrl, tvmExtension, downloadFolder):
	print "downloading tvm files."
	count = 0

	for user_channel in user_configured_channels:
		while count < int(daysToGrab):
			tempTimeStr = getTvmDateString(count, daysOffset)
			downloadUrl = tvmXmlUrl+tempTimeStr+"_"+user_channel+tvmExtension
			print "downloading: "+downloadUrl
			
			urlHandler = urllib.urlopen(downloadUrl)
			urlReader = urlHandler.read()
			destFile = open(downloadFolder+tempTimeStr+"_"+user_channel+tvmExtension, 'w')
			destFile.write(urlReader)
			destFile.close()	
			if os.path.exists(downloadFolder+tempTimeStr+"_"+user_channel+tvmExtension):
				print "successfully downloaded: "+tempTimeStr+"_"+user_channel+tvmExtension
			else:
				print "download of "+tempTimeStr+"_"+user_channel+tvmExtension+" failed. exiting."
				sys.exit(1)
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
	parser.add_option("-f", "--config-file", dest="config_file", help="set the config file to use")
	parser.add_option("-o", "--output", dest="output_file", help="set the output file")
	parser.add_option("-c", "--channelid-file", dest="channelid_file", help="set location of the channel_ids file")
	parser.add_option("-v", "--version", action="store_true", dest="show_version", default=False, help="show version")
	parser.add_option("-b", "--capabilities", action="store_true", dest="show_capabilities", default=False, help="show capabilities")
	parser.add_option("-q", "--quiet", action="store_true", dest="be_quiet", default=False, help="only error msgs")
	parser.add_option("-n", "--nowx", action="store_true", dest="nowx", default=False, help="give it to nowx's class")

	(options, args) = parser.parse_args()


	if options.show_capabilities:
		print "baseline"
		print "manualconfig"
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
	downloadFolder = pytvHome+"grabedTvms"+os.sep
	gzsFolder = pytvHome+"convertedGzs"+os.sep
	xmlTvmFolder = pytvHome+"tvmovieXmls"+os.sep

	if not os.path.exists(downloadFolder):
		os.makedirs(downloadFolder)

	if options.run_configure:
		print "running channel configuration"
		runConfigure(userConfig,all_channels)
		sys.exit(0)
	
	tvmExtension = ".xml.tvm"
	gzExtension = ".gz"
	xmlExtension = ".xml"
	tvmXmlUrl = "http://tvmovie.kunde.serverflex.info/onlinedata/xml-gz5/"		

	print "grabing "+`daysToGrab`+" days."
	user_configured_channels = getUserChannels(userConfig)

	if options.nowx:
		xmlwriter = write_xml(all_channels)	
		sys.exit(0)	

	getTvms(daysToGrab, daysOffset, user_configured_channels, tvmXmlUrl, tvmExtension, downloadFolder)
	runConverter(downloadFolder, tvmExtension, gzExtension, xmlExtension, gzsFolder, xmlTvmFolder)

		






if __name__=='__main__': main()
