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
    webpage = 1

    while list_of_books_is_empty:
        url = url_base + url_text + str(webpage)
        html = GetHTML.get_html(url)
        print(html)
        soup = BeautifulSoup(html, 'lxml')

        checkList = soup.find('div', class_='book-data')
        print(checkList)
        if checkList and webpage < 3:
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

        pages = soup.find_all('div', class_='bc-info__wrapper')  # id="5",
        page = ""
        publication_date = 'No date info'
        if pages is None:
            page = 'No Pages Info'
        else:
            try:
                page_tmp = pages[1]
            except IndexError:
                continue
            page_tmp = page_tmp.find_all('p')
            for i in range(len(page_tmp)):
                page_tmp_l = str(page_tmp[i])
                page_tmp_l = page_tmp_l.replace('  ', '').replace('\n', ' ').replace('<br/>', ' ')
                page_tmp_l = page_tmp_l[page_tmp_l.find('>') + 1:page_tmp_l.find('</')]
                if page_tmp_l[0:4] in ('ISBN', 'Язык', ' Тег', 'Том:', 'Форм', ' Жан'):
                    continue
                if page_tmp_l[0:3] == 'Год':
                    publication_date = page_tmp_l
                    continue
                if i == len(page_tmp) - 1:
                    page = page + page_tmp_l
                else:
                    page = page + page_tmp_l + ", "
            if page == "":
                page = "No Pages Info"

        genre = ""
        genre_list = list()
        genres = soup.find_all(href=re.compile("genre"))
        if not genres:
            genre = 'No Genre'
        else:
            for i in range(len(genres)):
                genre_tmp = str(genres[i])
                genre_tmp = genre_tmp[genre_tmp.find('>') + 1:genre_tmp.find('</')]
                if genre_tmp == 'Жанры':
                    continue
                if genre_tmp in genre_list:
                    continue
                else:
                    genre_list.append(genre_tmp)
                if i == len(genres) - 1:
                    genre = genre + genre_tmp
                else:
                    genre = genre + genre_tmp + ", "
            if genre == "":
                genre = 'No Genre'

        isbn = soup.find('span', itemprop="isbn")
        if isbn is None:
            isbn = 'No ISBN'
        else:
            isbn = str(isbn.text)

        data = [[name, author, page, genre, publication_date, isbn]]
        filename = 'wish_list.csv'
        CsvWriter.csv_write(filename, data)


if __name__ == '__main__':
    ll_login = 'jukka413'  # login пользователя livelib
    links = get_books_pages(ll_login)
    print('Load completed')
