import re

from bs4 import BeautifulSoup
from csv_writer import CsvWriter
from get_html import GetHTML
from get_books import GetBook


def get_books_pages(ll_login):
    url_base = 'https://livelib.ru/reader/'
    url_text = ll_login + '/wish/~'

    list_of_books_is_empty = True

    books = []
    webpage = 6

    while list_of_books_is_empty:
        url = url_base + url_text + str(webpage)
        html = GetHTML.get_html(url)
        soup = BeautifulSoup(html, 'lxml')

        checkList = soup.find('div', class_='with-pad')
        if checkList is None:
            books = GetBook.get_books(html, books)
            webpage += 1
            parse_books_info(books)
            books = []
        else:
            list_of_books_is_empty = False

    return books


def parse_books_info(books):
    for i in range(len(books)):
        link = 'https://livelib.ru/' + books[i]
        print(link)
        print('Скачано ', i + 1, ' из ', len(books))
        html = GetHTML.get_html(link)

        soup = BeautifulSoup(html, 'lxml')

        name = soup.find('title', id="title-head")
        name = str(name.text)

        author = soup.find(href=re.compile("author/"))
        if author is None:
            author = 'No Author Info'
        else:
            author = soup.find(href=re.compile("author/")).text

        page = soup.find('div', id="row-details", class_='book-content-data')
        if page is None:
            page = 'No Pages Info'
        else:
            page = page.find('p').text
            page = str(page.replace('  ', '').replace('\n', ' '))
            print(page)

        genre = ""
        genres = soup.find_all(href=re.compile("genre"))
        if not genres:
            genre = 'No Genre'
        else:
            for i in range(len(genres)):
                genre_tmp = str(genres[i])
                genre_tmp = genre_tmp[genre_tmp.find('>') + 1:genre_tmp.find('</')]
                if i == len(genres) - 1:
                    genre = genre + genre_tmp
                else:
                    genre = genre + genre_tmp + ", "

        isbn = soup.find('span', itemprop="isbn")
        if isbn is None:
            isbn = 'No ISBN'
        else:
            isbn = str(isbn.text)

        data = [[name, author, page, genre, isbn]]
        filename = 'books.csv'
        CsvWriter.csv_write(filename, data)


if __name__ == '__main__':
    ll_login = 'EvaRob'  # login пользователя livelib
    links = get_books_pages(ll_login)
    print('Load completed')
