# Copyright (C) 2006  Stefan Nistelberger (scuq@kages.at)
#		      Hans-Peter Schadler (blade.runner@gmx.at)
#		      Daniel Schrammel (nowx@gmx.at)
# tv_grab_de_tvmobie.py - tv movie grabber
# write_xmltv.py - write out a xml file in xmltv format

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

import xml.dom.minidom
from xml.dom.ext import PrettyPrint

class write_xml:
  def __init__(self, arr_channels):
	 doc = xml.dom.minidom.Document()
	 tv = doc.createElement('tv')
	 doc.appendChild(tv)
	 channel = doc.createElement('channel')
	 channel.setAttribute('id', 'bbc.uk')
	 tv.appendChild(channel)
	 display_name = doc.createElement('display-name')
	 display_name.setAttribute('lang', 'de')
	 display_name.appendChild(doc.createTextNode('BBC'))
	 channel.appendChild(display_name)

	 programme = doc.createElement('programme')
	 programme.setAttribute('channel', 'bbc.uk')
	 programme.setAttribute('start', '+0100')
	 tv.appendChild(programme)
	 title = doc.createElement('title')
	 title.setAttribute('lang', 'en')
	 title.appendChild(doc.createTextNode('King of the Hill'))
	 programme.appendChild(title)
	 sub_title = doc.createElement('sub-title')
	 sub_title.setAttribute('lang', 'de')
	 sub_title.appendChild(doc.createTextNode('Meet the...'))
	 programme.appendChild(sub_title)
	 desc = doc.createElement('desc')
	 desc.setAttribute('lang','en')
	 desc.appendChild(doc.createTextNode('Bobby tours with a comedy troupe who spe....'))
	 programme.appendChild(desc)
	 credits = doc.createElement('credits')
	 programme.appendChild(credits)
	 actor = doc.createElement('actor')
	 actor.appendChild(doc.createTextNode('Mike Judge'))
	 actor.appendChild(doc.createTextNode('Lane Smith'))
	 credits.appendChild(actor)
	 category = doc.createElement('category')
	 category.setAttribute('lang', 'en')
	 category.appendChild(doc.createTextNode('animation'))
	 programme.appendChild(category)	

	 PrettyPrint(doc)
