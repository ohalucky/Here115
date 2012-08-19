#!/usr/bin/env python
#-*- coding:utf-8 -*-

import urllib
import urllib2
import cookielib
import json
import re,time

class Hack_115:
  def __init__(self):
    t=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(t)
    cj = cookielib.CookieJar()
    self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(self.opener)
    self.opener.addheaders = [('User-agent', 'IE')]

  def login(self, username, password):
    url = 'https://passport.115.com/?ac=login'
    data = urllib.urlencode({'back':'http://www.115.com', 'goto':'http://115.com', 'login[account]':username, 'login[passwd]':password})
    req = urllib2.Request(url, data)
    try:
      fd = self.opener.open(req)
    except Exception, e:
      print('网络连接错误！')
      return False
    fd.close()
    if not re.search('error_code', fd.url):
      print('%s 密码不正确！\n' % username)
      return False
    print('%s 登陆成功，准备摇奖..   ' % username),
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
      return

    url = 'http://115.com/?ct=ajax_user&ac=pick_space&token=' + token.group(1)
    req = urllib2.Request(url)
    fd = self.opener.open(req)
    res_json = json.loads(fd.read())
    fd.close()
    if res_json['state'] == False:
      print('摇奖失败！')
      return
    str=u'\n获取空间：%s, 总空间：%s, 已使用：%s, 获取雨露：%d\n' % (res_json['picked'], res_json['total_size'], res_json['used_percent'], res_json['exp'])
    print str.encode("u8")



accounts_here = [
    {"account":'50493437','password':'lailinfeng'},
    {"account":'50326789','password':'lailinfeng'},
    ]

if __name__ == '__main__':
  l = Hack_115()
  for i in accounts_here:
    if not l.login(i['account'],i['password']):
      continue
    l.pick_space()

