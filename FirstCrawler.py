#-*-coding:utf8-*-
import requests
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class spider(object):
    def __init__(self):
        print u'starting to crawl contents...'

#getSource: get source code of web
    def getSource(self, url):
        html = requests.get(url)
        return html.text
#changePage: to produce connection of different pages
    def changePage(self, url, total_page):
        now_page = int(re.search('view=list&p=(\d+)', url, re.S).group(1))
        page_group = []
        for i in range(now_page, total_page + 1):
            link = re.sub('view=list&p=\d+', 'view=list&p=%s'%i, url, re.S)
            page_group.append(link)
        return page_group
#getClass: to get block of each class
    def getClass(self,source):
        everyclass = re.findall('class="course-card-wide">(.*?)</li>', source, re.S)
        return everyclass
#getInfo: to get important info of class
    def getInfo(self, eachclass):
        info={}
        info['title'] = re.search('title ellipsis fx">(.*?)</span>', eachclass, re.S).group(1)
        info['instructor'] = re.search('ins-name ellipsis"><b>(.*?)</b>', eachclass, re.S).group(1)
        info['students number'] = re.search('icon-user"></i><b>(.*?)</b> students', eachclass, re.S)
        info['rating'] = re.search('rating-number"><b>(.*?)</b>', eachclass, re.S)
        return  info
#saveInfo : to store to info.text
    def saveInfo(self, classinfo):
        f = open('info.txt','a')
        for each in classinfo:
            f.writelines('title: ' + each['title'] + '\n')
            f.writelines('instructor: ' + each['instructor'] + '\n')
            f.writelines('students numbers: ' + str(each['students number']) + '\n')
            f.writelines('rating: ' + str(each['rating']) + '\n')
        f.close()

if __name__ == '__main__':
    classinfo = []
    url = 'https://www.udemy.com/topic/python/?view=list&p=1'
    udemySpider = spider()
    all_links = udemySpider.changePage(url, 5)
    for link in all_links:
        print u'dealing with web page: ' + link
        html = udemySpider.getSource(link)
        everyclass = udemySpider.getClass(html)
        for each in everyclass:
            info = udemySpider.getInfo(each)
            classinfo.append(info)
    udemySpider.saveInfo(classinfo)
