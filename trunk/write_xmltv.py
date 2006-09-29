#!/usr/bin/python2.4
#nowx - 09/30/2006
import xml.dom.minidom
from xml.dom.ext import PrettyPrint

def write_xml():
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
	

def main():
	write_xml()
	
if __name__=='__main__': main()
