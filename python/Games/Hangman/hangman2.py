import random as rnd

with open('food.txt', 'r') as food:
    food_read = food.read()
    food_list = food_read.split('\n')

with open('movies.txt', 'r') as movie:
    movie_read = movie.read()
    movie_list = movie_read.split('\n')


def choice():

    global game_choice
    game_choice = input("Food Or Movies? ").lower()

    if game_choice == 'food':

        game_choice = food_list
        game()

    else:

        game_choice = movie_list
        game()


def game():

    lives = 5

    game_board = []

    word = rnd.choice(game_choice)

    x = 1

    while x <= len(word):

        game_board.append('_')

        x += 1

    letter_index = 0
    for letter in word:

        if letter == ' ':
            game_board[letter_index] = ' '

        letter_index += 1

    print(' '.join(game_board))

    while True:

        if '_' not in game_board:
            print(f'You won! the word was {word}!')
            break

        guess = input("Submit a letter to guess: ").lower()

        wrong_guess = True

        letter_index = 0
        for letter in word:

            if letter == guess:
                game_board[letter_index] = guess
                wrong_guess = False

            letter_index += 1

        if wrong_guess:
            lives -= 1
            print(f'You have {lives} lives left!')

            if lives == 0:
                print(f'You lost! the word was {word}')
                break

        print(' '.join(game_board))


choice()
