# Copyright (C) 2006  Stefan Nistelberger (scuq@kages.at)
#		      Hans-Peter Schadler (blade.runner@gmx.at)
#		      Daniel Schrammel (nowx@gmx.at)
# tv_grab_de_tvtoday.py - tvtoday grabber
# dl_tvtoday.py - downloads the tvtoday tv program and saves it

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

class dl_tvtoday:
	def __init__(self, von, vonStep, moreShowsString):
		self.von = von
		self.vonStep = vonStep
		self.moreShowsString = moreShowsString
		
	def download(self, link, httpfile):
		weitereSendungen = 1
		big_html_file = ""
		von_start = 0
		while weitereSendungen > 0:
			x = urllib.urlopen(link+"&"+self.von+str(von_start))
			html_contents = x.read()
			if re.search(self.moreShowsString, html_contents):
				big_html_file =  big_html_file + html_contents
				von_start = von_start+self.vonStep
			else:
				weitereSendungen = 0
				
			
		f = open(httpfile, "w")
		f.write(big_html_file)
		
		return 0
