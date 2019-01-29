"""
 Markdown.py
 0. just print whatever is passed in to stdin
 0. if filename passed in as a command line parameter, 
    then print file instead of stdin
 1. wrap input in paragraph tags
 2. convert single asterisk or underscore pairs to em tags
 3. convert double asterisk or underscore pairs to strong tags

"""

import fileinput
import re

global openBlockQuote
global willUnflag

def convertStrong(line):
  line = re.sub(r'\*\*(.*)\*\*', r'<strong>\1</strong>', line)
  line = re.sub(r'__(.*)__', r'<strong>\1</strong>', line)
  return line

def convertEm(line):
  line = re.sub(r'\*(.*)\*', r'<em>\1</em>', line)
  line = re.sub(r'_(.*)_', r'<em>\1</em>', line)
  return line

def convertH1(line):
  line = re.sub(r'# (.+)', r'<h1>\1</h1>', line)
  return line

def convertH2(line):
  line = re.sub(r'## (.+)', r'<h2>\1</h2>', line)
  return line

def convertH3(line):
  line = re.sub(r'### (.+)', r'<h3>\1</h3>', line)
  return line

def convertBlock(line):
  global openBlockQuote
  global willUnflag

  realFirst = line[0]

  if openBlockQuote == False:
    line = re.sub(r'> (.+)', r'<blockquote>\1', line)
  else:
    line = re.sub(r'> (.+)', r'\1', line)

  if (realFirst != '>' and openBlockQuote == True):
    print '</blockquote>'
    willUnflag = True
  elif 'blockquote' in line:
    openBlockQuote = True
  return line
  

openBlockQuote = False
willUnflag = False
for line in fileinput.input():
  line = line.rstrip() 
  

  line = convertBlock(line)
  line = convertStrong(line)
  line = convertEm(line)
  line = convertH3(line)
  line = convertH2(line)
  line = convertH1(line)
 
  if openBlockQuote == False:
    print '<p>' + line + '</p>'
  else:
    print line + '\n'

  if willUnflag == True:
    openBlockQuote = False
    willUnflag = False

