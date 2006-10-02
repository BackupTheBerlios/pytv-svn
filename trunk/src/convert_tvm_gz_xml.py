# Copyright (C) 2006  Stefan Nistelberger (scuq@kages.at)
#		      Hans-Peter Schadler (blade.runner@gmx.at)
#		      Daniel Schrammel (nowx@gmx.at)
# tv_grab_de_tvmovie.py - tv movie grabber
# convert_tvm_gz_xml.py - module### - converts a tvm file over gz to xml

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

import gzip

class convert_tvm_gz:
	def __init__(self, tvmfile, gzfile):
		self.tvmfile = tvmfile
		self.gzfile = gzfile

		f = open(tvmfile, "rb")
		g = open(gzfile, "wb")

		f.seek(0x006a,0)
		g.write(f.read(6))
		f.seek(0x0064,0)
		g.write(f.read(6))
		f.seek(0x0070,0)
		g.write(f.read(88))
		f.seek(0x0320,0)
		g.write(f.read(17))
		f.seek(0x0011,0)
		g.write(f.read(83))
		f.seek(0x012c,0)
		g.write(f.read(100))
		f.seek(0x0000,0)
		g.write(f.read(17))
		f.seek(0x0331,0)
		g.write(f.read(183))
		f.seek(0x0258,0)
		g.write(f.read(200))
		f.seek(0x0190,0)
		g.write(f.read(200))
		f.seek(0x00c8,0)
		g.write(f.read(100))
		f.seek(0x03e8,0)
		g.write(f.read())

		f.close()
		g.close()

		return 0
		
class extract_xml:
	def __init__(self, gzfile, xmlfile):
		self.gzfile = gzfile
		self.xmlfile = xmlfile

		gzipfile = gzip.open(gzfile)
		
		g = open(xmlfile, "wb")
		g.write(gzipfile.read())
		g.close
						
		return 0