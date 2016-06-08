from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Word(models.Model):
    string = models.CharField(max_length = 300)

class URL(models.Model):
    url = models.URLField(max_length = 1200)

class URL_Index(models.Model):
    url = models.ForeignKey(URL)
    text = models.ForeignKey(Word)
    count = models.IntegerField(default=0)

    def __eq__(self, other):
        return self.url.url == other.url.url

    def __hash__(self):
        return hash(self.url.url)
