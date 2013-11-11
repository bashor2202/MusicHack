from HTMLParser import HTMLParser
import urllib2
from htmlentitydefs import name2codepoint
import os
import re

URL = '' #Enter album URL here

#It should look something like
#URL = 'http://www.goldenmp3.ru/adele/21'

base = 'http://files.musicmp3.ru/lofi/'

r = urllib2.urlopen('URL')

html = r.read()

rels = []
namestemp = []
names = []

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        self.inLink = False
        if tag == 'a':
            for name, value in attrs:
                if name == 'rel' and value != 'add_color':
                    rels.append(value)
        if tag == 'div':
            self.inDiv = False
            for name, value in attrs:
                if name == 'class' and value == 'title_td_wrap':
                    self.inDiv = True;
        if tag == 'span':
            if self.inDiv == True:
                for name, value in attrs:
                    if name == 'itemprop' and value == 'name':
                        self.inLink = True
                        self.lasttag = tag

    def handle_endtag(self, tag):
        if tag == 'span':
            self.inlink = False
        if tag == 'div':
            self.inDiv = False
    def handle_data(self, data):
        if self.lasttag == 'span' and self.inLink:
            namestemp.append(data)


parser = MyHTMLParser()

x = parser.feed(html)

for i in range(0, len(namestemp)):
    if namestemp[i][0] != "(":
        names.append(namestemp[i])

for i in range(0, len(names)):
    names[i] = names[i].replace("'", "")

for i in range(0, len(names)):
    names[i] = names[i].replace("&", "\&")

for i in range(0, len(names)):
    names[i] = names[i].replace(" ", "\ ")

for i in range(0, len(names)):
    names[i] = names[i].replace("?", "")

for i in range(0, len(names)):
    names[i] = names[i].replace("(", "\(")

for i in range(0, len(names)):
    names[i] = names[i].replace(")", "\)")

for i in range(len(names)):
    os.system('wget ' + base + rels[i] + ' --output-document=' + names[i] + '.mp3')
