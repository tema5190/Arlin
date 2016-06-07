import urllib2
from bs4 import BeautifulSoup
import robotparser
import re

class Crawler(object):

    def __init__(self):
        self.visited_url = set()
        self.root_url = None

    def pass_robot_txt(self,url):
        robot = robotparser.RobotFileParser()
        robot.set_url(self.root_url)
        robot.read()

        return robot.can_fetch('*',url)#:
            #return True
        #else:
         #   return False

    def define_root_url(self,url):
        self.root_url = url

    def add_included_suburls(self,soup):
        refs = soup.findALL('a')
        urls = set()

        for ref in refs:
            try:
                href = ref['href']
            except Exception:
                print("Doesn't contains suburl")
                continue

            if len(href) < 2:
                continue

            if href.first() != '/':
                continue

            if self.root_url in href:
                urls.add(href)

            urls.add(self.root_url + href)

        return urls

    def visit(self,url,width,depth):

        if not self.pass_robot_txt(url):
           raise Exception("are you idiot?")

        try:
            html = urllib2.urlopen(url).read()
        except Exception:
            print("Can't open this *** url")
            return

        soup = BeautifulSoup(html)
        urls = self.add_included_suburls(soup)

        for url in urls:
            if url in self.visited_url:
                continue

            if width == 0:
                break

            self.visited_url.add(url)
            width -=1
            self.visit(url,width,depth)

        # words = self.

    # def get_html(url):
    #     response = urllib2.urlopen(url)
    #     return response.read()
    #
    # def parse(html):
    #     soup = BeautifulSoup(html)
    #     title = soup.find('title')
