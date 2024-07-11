from pathlib import Path
import time
import concurrent.futures
from multiprocessing import set_start_method

def wrapper(result_dict):
    # print('globals', globals().keys())
    # print('locals', locals().keys())
    def search_func(file):
        # функція для запуска в процесах
        res_list = []
        with open(file, 'r') as f:
            string = f.read().lower()
        for key in result_dict.keys():
            if string.find(key) != -1:
                res_list.append((key, file))
        print(f'{file}\'s processing process is finished')
        return res_list # повертаємо список таплів
    return search_func

if __name__ == '__main__':
    # set_start_method('forkserver')

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
    print('globals', globals().keys())
    print('locals', locals().keys())
    print(search_func_in_result_dict)
    print(type(search_func_in_result_dict))
    print(dir(search_func_in_result_dict))
    print(search_func_in_result_dict(file_list[1]))

    # запуск процесів (по замовчанню запускається стільки процесів, скільки ядер)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        ll = executor.map(search_func_in_result_dict, file_list)

    # об'єднуємо список результатів від кожного процеса в єдиний список
    list_of_pair = []
    for l in ll:
        list_of_pair.extend(l)

    # створення словника з результатом
    for pair in list_of_pair:
        temp_list = result_dict[pair[0]]
        temp_list.append(pair[1])
        result_dict[pair[0]] = temp_list

    end_time = time.time()

    # вивід результату
    print(f'Result dictionary is {result_dict}')
    print(f'Time taken: {end_time - start_time}')


# word list for code testing:
# set, avoid, him, can, because, print, swim, game, who, somebody, trip