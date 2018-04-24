#coding:utf-8
from __future__ import unicode_literals

import logging
import urllib
import urllib2
import re
import random
import string
import sys



__all__ = ["geturl"]

USER_AGENTS = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', \
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
        (KHTML, like Gecko) Element Browser 5.0', \
        'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)', \
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
        'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14', \
        'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
        Version/6.0 Mobile/10A5355d Safari/8536.25', \
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/28.0.1468.0 Safari/537.36', \
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']

logger=logging.getLogger("baidu.com")

def baidu_search(keyword, pn):
    p = {'wd': keyword}
    res = urllib2.urlopen(("http://www.baidu.com/s?"+urllib.urlencode(p)+"&pn={0}&cl=3&rn=10").format(pn)) #rn为每页的显示数目 pn表示当前显示的是第pn条搜索结果
    html = res.read()
    return html


def getList(regex, text):
    arr = []
    res = re.findall(regex, text)
    if res:
        for r in res:
            arr.append(r)
    return arr

def getMatch(regex, text):
    res = re.findall(regex, text)
    if res:
        return res[0]
    return ''

def is_get(url):
    regex = r'(\S*?)\?.*=.*'
    res = re.match(regex,url)
    if res:
        #print res.group(1)
        return res.group(1)
    else:
        return 0
# def Deduplication():
#     regex=r'\S'

def geturl(keyword, pages): #获取url
    targets = []
    hosts = []
    for page in range(0,int(pages)):
        pn = (page+1)*10
        html = baidu_search(keyword, pn)
        content = unicode(html, 'utf-8','ignore')
        arrList = getList(u"<div class=\"f13\">(.*)</div>", content) #分割页面块
        #print arrList[0]
        # f2=open('content.txt','a')
        # f2.write(str(arrList)+'\n')#调试使用，获取内容
        # f2.close()
        for item in arrList:
            regex = u"data-tools='\{\"title\":\"(.*)\",\"url\":\"(.*)\"\}'"
            link = getMatch(regex,item)
            url = link[1]                     #获取百度改写url
            try:
                domain = urllib2.Request(url)
                r = random.randint(0, len(USER_AGENTS))
                domain.add_header('User-agent', USER_AGENTS[r])
                domain.add_header('connection', 'keep-alive')
                response = urllib2.urlopen(domain)
                uri = response.geturl()      #获取真实url
                urs = is_get(uri)            #是否是传统的get型
                if (uri in targets) or (urs in hosts) :
                    continue
                else:
                    targets.append(uri)
                    hosts.append(urs)
                    f1 = open('data/targets.txt','a') #存放url链接
                    f1.write(uri+'\n')
                    f1.close()
            except:
                continue
    logger.info("urls have been grabed already!!!")
    return targets

def get_host(keyword,pages):
    targets = []
    hosts = []
    result={}
    for page in range(0, int(pages)):
        pn = (page + 1) * 10
        html = baidu_search(keyword, pn)
        content = unicode(html, 'utf-8', 'ignore')
        arrList = getList(u"<div class=\"f13\">(.*)</div>", content)  # 分割页面块
        #print arrList[0]
        for item in arrList:
            regex = u"data-tools='\{\"title\":\"(.*)\",\"url\":\"(.*)\"\}'"
            link = getMatch(regex,item)
            url = link[1]
            description=link[0]
            #print type(description)
            #print description
            #print link[0]
            try:
                domain = urllib2.Request(url)
                r = random.randint(0, len(USER_AGENTS))
                domain.add_header('User-agent', USER_AGENTS[r])
                domain.add_header('connection', 'keep-alive')
                response = urllib2.urlopen(domain)
                uri = response.geturl()
                res=uri.split("//")[1].split('/')[0]
                #print res
                result[description]=uri
            except:
                continue
    return result


def get_sql(i):
    sql="inurl:asp?id="
    for url in geturl(sql,i):
        print url

def get_host_2(host,i):
    h="site:"+host
    result=get_host(h,i)
    for key in result.iterkeys():
        print key
        print result[key]





if __name__ =="__main__":
    if "sql" in sys.argv[1]:
        get_sql(sys.argv[2])
    elif "host" in sys.argv[1]:
        get_host_2(sys.argv[2],sys.argv[3])











