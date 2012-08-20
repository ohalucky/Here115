#!/usr/bin/env python
#-*- coding:utf-8 -*-
accounts_here = [
    {'account':'13666666666','password':'xxxxxxxx'},
    ]
filename = 'C:\\Users\\(username)\\Desktop\\here115.txt'#输出文件名,username改为用户名，去掉括号


import urllib
import urllib2
import cookielib
import json
import re,time
import os,sys,datetime

startTime = time.localtime()
strStartTime = time.strftime('%Y-%m-%d %H:%M:%S', startTime)
f=open('here115.txt','a')
f.write(strStartTime+':\t')
#f.close()

class Here115:
  def __init__(self):
    t=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(t)
    cj = cookielib.CookieJar()
    self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(self.opener)
    self.opener.addheaders = [('User-agent', 'IE')]

  def login(self, username, password):
    url = 'https://passport.115.com/?ac=login'
    data = urllib.urlencode({'login[account]':username, 'login[passwd]':password,'login[time]':'on'})
    req = urllib2.Request(url, data)
    try:
      fd = self.opener.open(req)
    except Exception, e:
      print('网络连接错误！')
      f.write('网络连接错误！\n')
      f.close()
      return False
    res=fd.read()
    fd.close()
    if re.search('location\.href="http://115.com"', res) == None:
      str='%s 密码不正确！\n' % username
      print str
      f.write(str+'\n')
      f.close()
      return False
    else:
      str='%s 登陆成功，准备摇奖..   ' % username
      print str,
      f.write(str+'\n')
      return True

  def pick_space(self):
    url = 'http://115.com/?ct=file&ac=userfile&aid=1&cid=0&tpl=list_pg&limit=30'
    req = urllib2.Request(url)
    fd = self.opener.open(req)
    token_page = fd.read()
    fd.close()
    token = re.search("take_token:\s'(\w+)'", token_page)
    if not token:
      print('今天已经摇过了...')
      f.write('今天已经摇过了...\n')
      f.close()
      return

    url = 'http://115.com/?ct=ajax_user&ac=pick_space&token=' + token.group(1)
    req = urllib2.Request(url)
    fd = self.opener.open(req)
    res_json = json.loads(fd.read())
    fd.close()
    if res_json['state'] == False:
      print('摇奖失败！')
      f.write('摇奖失败！\n')
      f.close()
      return
    str=u'\n获取空间：%s, 总空间：%s, 已使用：%s, 获取雨露：%d\n' % (res_json['picked'], res_json['total_size'], res_json['used_percent'], res_json['exp'])
    print str.encode("u8")
    f.write(str+'\n')
    f.close()


if __name__ == '__main__':
  h = Here115()
  for i in accounts_here:
    if not h.login(i['account'],i['password']):
      continue
    h.pick_space()

