# Вариант 10.
# Дана последовательность из n целых чисел. Найти максимальный элемент и вывести его на экран,
# а потом всю последовательность целиком (каждый элемент в отдельной строке). Списки не использовать.
def main():
    n = input("Введите кол-во чисел:> ")
    while n != 'q':
        max_num = None
        result_print = ''
        for i in range(int(n)):
            while True:
                try:
                    number = int(input("Введите целое число:> "))
                except ValueError:
                    print("Вы ввели значение на являющееся целым числом, попробуйте еще раз.")
                    continue
                else:
                    break
            result_print += str(number) + '\n'
            if max_num is None:
                max_num = number
            if number > max_num:
                max_num = number
        print("Максимальное число последовательности = ", max_num)
        print("Последовательность чисел целиком")
        print(result_print)


main()
