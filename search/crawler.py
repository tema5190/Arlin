import lxml.html as html
from pandas import DataFrame

def parse_sql(sql_adress):
    collection = html.parse(sql_adress)

    print(collection)

str = 'https://yandex.by/'

parse_sql(str)