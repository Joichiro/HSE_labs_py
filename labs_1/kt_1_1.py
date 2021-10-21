# Вариант 10. Задача 1: Написать функцию, которая определяет принадлежность точки с координатами (x; y)
# заштрихованной фигуре (обратить внимание на закрашенность границ: если граница не закрашена,
# она не принадлежит фигуре) и возвращает логическое значение. В зависимости от ответа выводить “YES” / “NO”
def validation_check(coord_x, coord_y):
    if (coord_x + 8 < coord_y < coord_x + 12 and -coord_x - 2 < coord_y < -coord_x + 2) or (
            (coord_x - 8) ** 2 + (coord_y + 5) ** 2 <= 4 and -coord_x + 1 <= coord_y <= -coord_x + 5):
        return "YES"
    return "NO"


def main():
    while True:
        try:
            x = int(input('Введите координату x:> '))
            y = int(input('Введите координату y:> '))
        except ValueError:
            print("Вы ввели значение на являющееся целым числом, попробуйте еще раз.")
            continue
        else:
            break

    print("Принадлежит ли точка фигурам?\nРезультат:", validation_check(float(x), float(y)))


main()
