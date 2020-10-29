import csv


# Запись списка книг в csv-файл
class CsvWriter:
    try:
        def csv_write(filename, data):
            my_file = open(filename, 'a', newline='')
            with my_file:
                writer = csv.writer(my_file, delimiter=';')
                writer.writerows(data)
    except UnicodeEncodeError as e:
        my_file = open('error.txt', 'a', newline='')
        with my_file:
            writer = csv.writer(my_file, delimiter=';')
            writer.writerows(e)
