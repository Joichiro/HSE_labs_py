# Написать декоратор, который подсчитывает время выполнения функции в секундах (использовать модуль time).
import time


def show_time(f):
    def wrapper(*args, **kwargs):
        start = time.time()
        f(*args, **kwargs)
        stop = time.time()
        result = stop - start
        print('Времени затрачено: ' + str(result))

    return wrapper()


# Демонстрация использования декоратора
@show_time
def list_num():
    numbers = []
    for i in range(9999999):
        numbers.append(i)
    print('Список создан')
    return numbers
