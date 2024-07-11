from pathlib import Path
import time
import concurrent.futures

def wrapper(result_dict):
    def search_func(file):
        # функція для запуска в потоках
        with open(file, 'r') as f:
            string = f.read().lower()
        for key in result_dict.keys():
            if string.find(key) != -1:
                temp_list = result_dict[key]
                temp_list.append(file)
                result_dict[key] = temp_list
        print(f'{file}\'s processing thread is finished')
    return search_func

if __name__ == '__main__':

    # створення списку файлів з вказаної папки
    search_path = Path(input('Enter search path: '))
    file_list = [str(x) for x in search_path.iterdir() if x.is_file()]

    # створення словника з ключовими словами пошуку
    result_dict = {}
    for word in tuple(map(lambda x: x.strip(' ').lower(), input('Enter comma separated keywords: ').split(','))):
        result_dict[word] = []

    start_time = time.time()

    # створення замикання для вказання цільового словника result_dict
    search_func_in_result_dict = wrapper(result_dict)

    # запуск потоків (без обмеження по кількості)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(search_func_in_result_dict, file_list)

    end_time = time.time()

    # вивід результату
    print(f'Result dictionary is {result_dict}')
    print(f'Time taken: {end_time - start_time}')


# word list for code testing:
# set, avoid, him, can, because, print, swim, game, who, somebody, trip