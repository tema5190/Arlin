from models import Word,URL,URL_Index

class Indexer():

    def index_words(self, words):

        res = []
        for word in words:
            if not Word.objects.filter(text = word).exists():
                res.append(Word(text=word))

        Word.objects.bulk_create(res) #За раз - не забыть

    def index_url(self,url):

        if not URL.objects.filter(url = url).exists():
            URL.objects.create(url=url)

    def indexing(self, words, url):

        temp = URL.objects.get(url = url)

        index_id = [
                    URL_Index(url=temp,text = Word.objects.get(text = word),count=count)
                    for word,count in words if not
                    URL_Index.objects.filter(url = temp, text = Word.objects.get(text = word),count=count).exists()
                   ]

        URL_Index.objects.bulk_create(index_id)