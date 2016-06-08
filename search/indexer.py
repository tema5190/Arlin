from models import Word,URL,URL_Index
import re
from collections import Counter


class Indexer(object):

    def add_words(self, pair_word_and_count):

        words = pair_word_and_count
        res = []
        for word in words:
            if not Word.objects.filter(string = word).exists():
                res.append(Word(string=word))

        Word.objects.bulk_create(res)


    def add_url(self,url):

        if not URL.objects.filter(url = url).exists():
            URL.objects.create(url = url)

    def create_index(self, words, url):

        temp = URL.objects.get(url = url)

        index_id = [
                    URL_Index(url=temp,text = Word.objects.get(string = word),count=count)
                    for word,count in words if not
                    URL_Index.objects.filter(url = temp, text = Word.objects.get(string = word),count=count).exists()
                   ]

        URL_Index.objects.bulk_create(index_id)


    def search_query_result(self, query):
        query_words = re.findall(r'[0-9a-z]+', query.lower())

        words = Word.objects.filter(string__in = query_words)
        urls_index = URL_Index.objects.filter(text__in=words)

        result_index = [
                        index for index, count in Counter(urls_index).items()
                        if count == len(query_words)
                       ]
        lt = list()

        for index in result_index:
            lt.append((index.count, index.url.url))

        lt = sorted(lt, key= lambda x:x[0], reverse=True)

        response = list()

        for count_url in lt:
            if count_url[1] not in response:
                response.append(count_url[1])

        return response
