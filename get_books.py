from bs4 import BeautifulSoup


# Выбирает список ссылок на книги с одной страницы
class GetBook:
    def get_books(html, books):
        soup = BeautifulSoup(html, 'lxml')
        links = soup.find_all('a', class_='brow-book-name with-cycle')
        for link in links:
            link_parsed = link.get('href').split('?')
            books.append(link_parsed[0])
        return books
