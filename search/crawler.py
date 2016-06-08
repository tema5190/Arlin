from bs4 import BeautifulSoup
import robotparser
import urllib2
from indexer import Indexer
import re
from collections import Counter

class Crawler(object):

    def __init__(self):
        self.visited_url = set()
        self.root_url = None
        self.indexer = Indexer()

    def pass_robot_txt(self,url):
        robot = robotparser.RobotFileParser()
        robot.set_url(self.root_url)
        robot.read()

        return robot.can_fetch('*',url)

    def define_root_url(self,url):
        self.root_url = url

    def add_included_suburls(self,soup):
        refs = soup.findall('a')
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

    def get_pair_word_and_count(self, soup):

        def visible(element):
            if element.parent.name in ['head','script','style','document']:
                return False

            if re.match('<--.*-->',str(element)):
                return False

            if element == '\n':
                return False

            return True


        data = soup.findALL(text = True)

        visible_text = filter(visible, data)
        words = list()
        for text in visible_text:
            result = re.findall(r'[0-9a-z]',text.lower())

            for res in result:
                words.append(res)

        self.indexer.add_words(set(words))

        return Counter(words)


    def visit(self,url,width,depth):

        if depth<0:
            return

        if not self.pass_robot_txt(url):
           raise Exception("robot.txt founded")

        cur_url = url
        self.indexer.add_url(cur_url)

        depth = depth - 1

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
            width = width -1
            self.visit(url,width,depth)

        words = self.get_pair_word_and_count(soup).iteritems()

        self.indexer.create_index(words,cur_url )

    def run(self,url,width,depth):
        self.define_root_url(url)
        self.visit(url,width,depth)