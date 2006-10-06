# Copyright (C) 2006  Stefan Nistelberger (scuq@kages.at)
#		      Hans-Peter Schadler (blade.runner@gmx.at)
#		      Daniel Schrammel (nowx@gmx.at)
# tv_grab_de_tvmovie.py - tv movie grabber
# dl_tvmovie.py - module### - downloads the tvmovie tv program and saves it

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

class dl_tvmovie:
	def __init__(self, von):
		self.von = von
		
	def download(self, link, httpfile):
		x = urllib.urlopen(link)
		f = open(httpfile, "w")
		f.write(x.read())
		
		return 0
