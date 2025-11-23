import random
import os
from datetime import datetime

def create_stats_directory():
    # Здесь заведем директорию для статистики
    stats_dir = "C:/game_stats"
    if not os.path.exists(stats_dir):
        os.makedirs(stats_dir)
        print('c')
    return stats_dir

def save_game_results(size, game_mode, first_player, result, board):
    # Здесь будет происходить сохранение результатов игры в файл
    print(f"\n End game, Player {result} \n")
    stats_dir = create_stats_directory()
    print(stats_dir)
    #timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{stats_dir}/game_.txt"
    gamemode = ("Игрок против игрока" if game_mode == 1 else "Игрок против Робота")
    with open(filename, 'w', encoding = 'utf-8') as f:
        f.write(f"Размер поля: {size}\n")
        f.write(f"Режим игры: { gamemode }\n")
        f.write(f"Первый ход: {first_player}\n")
        f.write(f"Результат: {result}\n")
        f.write("Финальное поле после завершения игры:\n")
        f.write(board_to_string(board))

def get_valid_size():
    # Здесь получаем и проверяем размеры доски
    while True:
        try:
            size = int(input("Введите поля от 3 до 9: "))
            if 3 <= size <= 9:
                return size
            else:
                print('Неверный размер поля')
        except ValueError:
            print('Неверный размер поля, введите новый')
def initialize_board(size):
    # Создадим игровое поле
    return [['.' for _ in range(size)] for _ in range(size)]

def choose_first_player():
    # Здесь случайно выбираем кто ходит первый
    first_player = 'X' if random.choice([True, False]) else 'O'
    print(f'Первым ходит: {first_player}')
    return first_player

def choose_game_mode():
    # Выбираем игровой режим
    while True:
        try:
            print('Выбери режим игры')
            print('1 - Игрок против Игрока')
            print('2 - Игрок против Робота')
            mode = int(input('Выбор: '))
            if mode in [1,2]:
                return mode
            else:
                print('Неверный выбор')
        except ValueError:
            print('Введи корректные данные')

def board_to_string(board):
    # Преобразуем строку для вывода на экран
    size = len(board)
    lengh = int(((os.get_terminal_size().columns)/2)-(len(f"{1}" + " ".join("1"))))
    result = (" " + " ".join(str(i) for i in range(1, size + 1)) + "\n").rjust(lengh)

    for i in range(size):

        result += (f"{i + 1}" + " ".join(board[i]) + "\n").rjust(lengh)
    return result


def print_board(board):
    os.system('cls')
    print(board_to_string(board))

def is_valid_move(board, row, col):
    # Проверяем является ли ход допустимым
    size = len(board)
    return (0 <= row < size and 0 <= col < size and board[row][col] == '.')

class Move_Error(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def get_player_move(board, current_player):
    # Получаем и обрабатываем ход игрока
    while True:
        try:
            move = input('Введи ход: ')
            parts = move.split()
            if len(parts)!=2:
                raise Move_Error("qwe")
            row, col = int(parts[0]) - 1, int(parts[1]) - 1
            if is_valid_move(board, row, col):
                return row, col
            else:
                print("Неправильный ход")
        except ValueError:
            print("Введи корректные данные")
        except Move_Error:
            print("Введи корректные данные")

def get_ai_move(board):
    # Генерируем ход для робота
    size = len(board)
    # Будем выдавать роботу случайный допустимый ход, который выпадет с помощью рандома
    available_moves = []
    for i in range(size):
        for j in range(size):
            if board[i][j] == '.':
                available_moves.append((i,j))
    # Заполнили массив всеми допустимыми ходами, теперь можно делать случайный выбор
    return random.choice(available_moves)

def check_winner(board, current_player):
    # Сейчас будем проверять победителя всей партии
    size = len(board)
    # Отдельно проверим выигрыш по строка и затем по столбцам
    for i in range(size):
        if all(board[i][j] == current_player for j in range(size)):
            return True
    for j in range(size):
        if all(board[i][j] == current_player for i in range(size)):
            return True

    # Проверка по диагоналям

    if all(board[i][i] == current_player for i in range(size)):
        return True
    if all(board[i][size - 1 - i] == current_player for i in range(size)):
        return True

    return False

def is_board_full(board):
    # Проверка того, что вся доска заполнена и у нас ничья в игре
    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[i][j] == '.':
                return False
    return True

def make_move(board, row, col, current_player):
    # С помощью этой функции будут совершаться ходы
    board[row][col] = current_player

def switch_player(current_player):
    # Переключаем ход с одного игрока на другого по очереди
    return 'O' if current_player == 'X' else 'X'

# Напишем основную игровую функцию

def play_game():
    game_mode = choose_game_mode()
    size = get_valid_size()
    board = initialize_board(size)
    current_player = choose_first_player()
    first_player = current_player
    while True:
        print_board(board)
        if current_player == 'O' and game_mode == 2:
            # Ход робота
            print('Робот делает ход')
            row, col = get_ai_move(board)
        else:
            # Ход Игрока
            row, col = get_player_move(board, current_player)
        make_move(board, row, col, current_player)

        # Проверяем победу в игре
        if check_winner(board, current_player):
            print_board(board)
            save_game_results(size, game_mode, first_player, current_player + " win!", board)
            break
        # Проверим ничью
        if is_board_full(board):
            print_board(board)
            save_game_results(size, game_mode, first_player, "НИЧЬЯ", board)
            break
        current_player = switch_player(current_player)

def main():
    os.system("cls")
    # Здесь запускается игра целиком
    title = "крестики нолики"
    print( title.rjust(int((os.get_terminal_size().columns/2)+6)) )
    while True:
        play_game()

if __name__ == "__main__":
    main()