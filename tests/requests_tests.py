import requests as req
from random import choice
import datetime
import os
import sys

URL_APP = "http://192.168.1.144:5000/api"
URL_BACON = "http://baconipsum.com/api/"
URL_USER = "http://api.randomuser.me/"
URL_WORDLIST = r"http://dictionary-thesaurus.com/wordlists/Nouns%285,449%29.txt"

word_list = ['annoyware','blammo','bletch','bloatware','bogometer','bogon',
'bogosity','bogotify','copyleft','cruft','crufty','deliminator','delint',
'dirtball','flamage','foobar','grep','hackish','hackishness','hackitude',
'lexer','nagware','newline','overclock','regexp','rehi','segfault',
'spamblock','superuser','sysadmin','tarball','unixism','webmaster','xor',
'xref','annoyware','annoywares','blammo','blammoed','blammoing',
'blammos','bletch','bloatware','bloatwares','boga','bogometer',
'bogometers','bogon','bogosities','bogosity','bogotified','bogotifies',
'bogotify','bogotifying','copyleft','copylefts','cruft','crufted',
'crufties','crufting','crufts','crufty','deliminator','deliminators',
'delint','delinted','delinting','delints','dirtball','dirtballs',
'flamage','flamages','foobar','foobars','grep','grepped','grepping',
'greps','hackish','hackishes','hackishness','hackishnesses','hackitude',
'hackitudes','lexer','lexers','nagware','nagwares','newline','newlines',
'overclock','overclocked','overclocking','overclocks','regexp','regexps',
'rehi','segfault','segfaults','spamblock','spamblocks','superuser',
'superusers','sysadmin','sysadmins','tarball','tarballs','unixism',
'unixisms','webmaster','webmasters','xor','xref','xreffed','xreffing','xrefs']


class User:
  def __init__(self, uname, email, password):
    self.uname = uname
    self.email = email
    self.password = password

def info_message(message):
  time_string = '%Y-%m-%d %H:%M:%S'
  print "[INFO %s]: %s" %\
    (datetime.datetime.now().strftime(time_string), message)

def get_bacon(**kwargs):
  params = {'type': 'meat-and-filler'}
  params['paras'] = kwargs.get('paras', None)
  params['sentences'] = kwargs.get('sentences', None)
  info_message("Retrieving bacon...")
  return req.get(URL_BACON, params=params).json()[0]

def get_user():
  user = req.get(URL_USER).json()['results'][0]['user']
  return User(user['username'], user['email'], user['password'])

def add_post(**kwargs):
  data = {}
  data['title'] = kwargs.get('title', get_bacon(sentences=1))
  data['content'] = kwargs.get('content', get_bacon())
  data['labels'] = kwargs.get('labels', [1])
  info_message("Adding post")
  print data
  return req.post(URL_APP+"/blogs", data).text

def add_user(**kwargs):
  if(len(kwargs) in (0,1)):
    user = get_user()
  data = {}
  info_message("Adding user")
  data['uname'] = kwargs.get('uname', user.uname)
  data['email'] = kwargs.get('email', user.email)
  data['password'] = kwargs.get('password', user.password)
  print data
  return req.post(URL_APP+"/users", data).json()

def run_tests():
  info_message("Adding 10 blogs")
  for x in range(10):
    info_message(add_post())
  info_message("Adding 10 users")
  for x in range(10):
    info_message(add_user())

run_tests()
