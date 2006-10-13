# Copyright (C) 2006  Stefan Nistelberger (scuq@kages.at)
#		      Hans-Peter Schadler (blade.runner@gmx.at)
#		      Daniel Schrammel (nowx@gmx.at)
# tv_grab_de_siehferninfo.py - tvtoday grabber
# dl_page.py - downloads the tv program and saves it

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

import urllib
import re

class dl_page:
#	def __init__(self):
		
	def download_main(self, link, httpfile):
		x = urllib.urlopen(link)
		html_contents = x.read()
		description_numbers = re.findall('\(([0-9]+)\)', html_contents)
		html_snipper = re.compile('</h3>(.*?)</table>', re.DOTALL) 
		html_contents_sniped = html_snipper.search(html_contents)
		html_contents = html_contents_sniped.group(1)	
		html_contents = re.sub('^$', '', html_contents)
		html_contents = re.sub('\r', '', html_contents)
		html_contents = re.sub('\t', '', html_contents)
		html_contents = re.sub('\n', '', html_contents)
		html_contents = re.sub('</td>', '</td>\n', html_contents)
		html_contents = re.sub('</tr>', '</tr>\n', html_contents)
		f = open(httpfile, "w")
		f.write(html_contents)
		
		return description_numbers

	def download_desc(self, link, httpfile):
		x = urllib.urlopen(link)
		html_contents = x.read()
		f = open(httpfile, "w")
		f.write(html_contents)
