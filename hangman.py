import random

# List of words to choose from
word_list = ['python', 'hangman', 'computer', 'science', 'developer']

# Choose a random word
word = random.choice(word_list)
word_letters = set(word)  # unique letters in the word
guessed_letters = set()
lives = 6

print("Welcome to Hangman!")
print("_ " * len(word))  # show empty blanks

while len(word_letters) > 0 and lives > 0:
    print("\nYou have", lives, "lives left.")
    print("Guessed letters:", " ".join(sorted(guessed_letters)))

    # Show current word progress
    word_display = [letter if letter in guessed_letters else '_' for letter in word]
    print("Current word:", " ".join(word_display))

    # Get user input
    guess = input("Guess a letter: ").lower()

    if len(guess) != 1 or not guess.isalpha():
        print("Please enter a single alphabetic character.")
        continue

    if guess in guessed_letters:
        print("You already guessed that letter.")
        continue

    guessed_letters.add(guess)

    if guess in word_letters:
        word_letters.remove(guess)
        print("Good guess!")
    else:
        lives -= 1
        print("Wrong guess!")

# Game over messages
if lives == 0:
    print("\nYou lost! The word was:", word)
else:
    print("\nYou won! The word was:", word)
