import random
import getpass

from urllib import request, error

word_url = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"

try:
    content = request.urlopen(word_url)
    long_txt = content.read().decode()
    words = long_txt.splitlines()
except error.HTTPError:
    print("You seem to be behind a proxy!")
    print("Enter the following details to authenticate yourself:")
    proxy_ip = input("Proxy ip: ")
    proxy_port = input("Proxy port: ")
    username = input("Username: ")
    password = getpass.getpass()
    proxy = request.ProxyHandler({"http": "http://" + username + ":" + password + "@" + proxy_ip + ":" + proxy_port})
    auth = request.HTTPBasicAuthHandler()
    opener = request.build_opener(proxy, auth, request.HTTPHandler)
    request.install_opener(opener)
    content = request.urlopen(word_url)
    long_txt = content.read().decode()
    words = long_txt.splitlines()

words_9 = [word for word in words if len(word) == 9 and word[0].islower() and "'" not in word]


def print_hangman(chances):
    if chances == 0:
        print("   |\n   O\n  /|\\\n  / \\")
    elif chances == 1:
        print("   |\n   O\n  /|\\\n  /")
    elif chances == 2:
        print("   |\n   O\n  /|\\")
    elif chances == 3:
        print("   |\n   O\n  /|")
    elif chances == 4:
        print("   |\n   O\n   |")
    elif chances == 5:
        print("   |\n   O")
    elif chances == 6:
        print("   |")


def start_game():
    guess_word = ''
    guessed_letters = []
    chances = 7
    print("Save He-Man from getting hanged by guessing the correct name in 7 chances")
    print("Following word is an English word:")
    word = random.choice(words_9)
    while True:
        i = random.randint(0, 8)
        j = random.randint(0, 8)
        indices_i = [k for k, e in enumerate(word) if e == word[i] and k != i]
        indices_j = [k for k, e in enumerate(word) if e == word[j] and k != j]
        if i != j and len(indices_i) == 0 and len(indices_j) == 0:
            break
    for k in range(0, 9):
        if k == i or k == j:
            guess_word += word[k]
        else:
            guess_word += '_'
    print(guess_word)
    print("Please type a letter!")
    let = input()

    while chances:
        if len(let)!=1:
            print("Enter a single letter.")
            let = input()
            continue

        if guess_word.count(let):
            print("The given character is already present in given word.")
            let = input()
            continue

        if let in guessed_letters:
            print("The given character is already guessed.")
            let = input()
            continue

        indices = [i for i, e in enumerate(word) if e == let]
        if len(indices) == 0:
            guessed_letters.append(let)
            chances -= 1
            if chances:
                print("Bad Guess!!")
                print_hangman(chances)
                print("Given Word:", guess_word)
                print("Chances left:", chances)
                print("Guessed letters:", guessed_letters)
                print("\nPlease type next letter!")
                let = input()
                continue
            else:
                print("Game Over!")
                print_hangman(chances)
                print("The correct word was:", word)
                break

        list1 = list(guess_word)
        for i in range(0, 9):
            if i in indices:
                list1[i] = let
        guess_word = ''.join(list1)

        if '_' in guess_word:
            guessed_letters.append(let)
            print("Good Guess!!")
            print_hangman(chances)
            print("Given Word:", guess_word)
            print("Chances left:", chances)
            print("Guessed letters:", guessed_letters)
            print("\nPlease type next letter!")
            let = input()
            continue
        else:
            print("You got the correct word \"", word, "\" and saved He-Man's life!", sep="")
            break

    print("Wanna play again? Type 'y' to play again or 'n' to quit")
    option = input()
    if option == 'y':
        start_game()


start_game()
