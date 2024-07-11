from pathlib import Path
from threading import Thread
import time

def search_func(file, result_dict):
    # функція для запуска в потоках
    with open(file, 'r') as f:
        string = f.read().lower()
    for key in result_dict.keys():
        if string.find(key) != -1:
            temp_list = result_dict[key]
            temp_list.append(file)
            result_dict[key] = temp_list
    print(f'{file}\'s processing thread is finished')

if __name__ == '__main__':

    # створення списку файлів з вказаної папки
    search_path = Path(input('Enter search path: '))
    file_list = [str(x) for x in search_path.iterdir() if x.is_file()]

    # створення словника з ключовими словами пошуку
    result_dict = {}
    for word in tuple(map(lambda x: x.strip(' ').lower(), input('Enter comma separated keywords: ').split(','))):
        result_dict[word] = []

    start_time = time.time()

    # запуск потоків
    threads = []
    for file in file_list:
        thread = Thread(target=search_func, args=(file, result_dict,))
        print(f'{file}\'s processing thread is started')
        thread.start()
        threads.append(thread)

    # чекаємо завершення всіх потоків
    [el.join() for el in threads]

    end_time = time.time()

    # вивід результату
    print(f'Result dictionary is {result_dict}')
    print(f'Time taken: {end_time - start_time}')


# word list for code testing:
# set, avoid, him, can, because, print, swim, game, who, somebody, trip