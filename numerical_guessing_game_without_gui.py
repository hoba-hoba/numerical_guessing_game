import random

def get_border():
    while True:
        border = input('Задайте диапазон: от 1 до ').strip()
        if border.isdigit() and int(border) > 1:
            return int(border)
        print('Максимальное число не подходит, введите целое число больше 1.')

def is_valid(n, border):
    return n.isdigit() and 1 <= int(n) <= border

def play(riddle, border):
    cnt = 0

    while True:
        n_user = input(f'Введите число от 1 до {border}: ').strip()

        if not is_valid(n_user, border):
            print(f'А может быть все-таки введем целое число от 1 до {border}?')
            continue

        n_user = int(n_user)
        cnt += 1

        if n_user < riddle:
            print('Ваше число меньше загаданного, попробуйте еще раз: ', end = '')
        elif n_user > riddle:
            print('Ваше число больше загаданного, попробуйте еще раз: ', end = '')
        elif n_user == riddle:
            word = '-ей' if (cnt != 13 and cnt % 10 == 3) else '-ой'
            print(f'Вы угадали число с {cnt}{word} попытки, поздравляем!',)
            break
    

def main():
    print('Добро пожаловать в числовую угадайку')

    while True:
        border = get_border()
        riddle = random.randint(1, border)
        print('Число загадано!')

        play(riddle, border)
        answer = input('Хотите поиграть еще?')

        if answer == 'нет':
            print('Спасибо, что играли в числовую угадайку. Еще увидимся...')
            break

        print('Отлично! Продолжаем игру!')

if __name__ == "__main__":
    main()
