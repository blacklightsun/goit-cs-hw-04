from pathlib import Path
from multiprocessing import Process, Queue
import time


def search_func(file, keywords, jq):
    # функція для запуска в процессах
    with open(file, 'r') as f:
        string = f.read().lower()

    for key in keywords:
        if string.find(key) != -1:
            q.put((key, file))

    print(f'{file}\'s processing process is finished')

if __name__ == '__main__':
    # створення списку файлів з вказаної папки
    search_path = Path(input('Enter search path: '))
    file_list = [str(x) for x in search_path.iterdir() if x.is_file()]

    # створення словника з ключовими словами пошуку
    result_dict = {}
    for word in tuple(map(lambda x: x.strip(' ').lower(), input('Enter comma separated keywords: ').split(','))):
        result_dict[word] = []

    start_time = time.time()

    # створення черги
    q = Queue()

    # запуск потоків
    processes = []
    for file in file_list:
        pr = Process(target=search_func, args=(file, result_dict.keys(), q))
        print(f'{file}\'s processing process is started')
        pr.start()
        processes.append(pr)

    # чекаємо завершення всіх процесів
    [el.join() for el in processes]

    # створення словника з результатом
    while not q.empty():
        word, file = q.get()
        temp_list = result_dict[word]
        temp_list.append(file)
        result_dict[word] = temp_list

    end_time = time.time()

    # вивід результату
    print(f'Result dictionary is {result_dict}')
    print(f'Time taken: {end_time - start_time}')


# word list for code testing:
# set, avoid, him, can, because, print, swim, game, who, somebody, trip