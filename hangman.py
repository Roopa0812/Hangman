import random
import os

# ── Word bank by category ─────────────────────────────────────────────────────
WORD_BANK = {
    "tech": [
        ("python",       "A popular high-level programming language"),
        ("algorithm",    "Step-by-step procedure to solve a problem"),
        ("database",     "Organised collection of structured data"),
        ("compiler",     "Translates source code to machine code"),
        ("recursion",    "A function that calls itself"),
        ("interface",    "Boundary between two systems or components"),
        ("bandwidth",    "Maximum data transfer rate of a network"),
        ("debugging",    "Process of finding and fixing code errors"),
    ],
    "animals": [
        ("elephant",    "Largest land animal on Earth"),
        ("penguin",     "Flightless bird native to Antarctica"),
        ("crocodile",   "Large reptile that hasn't changed in millions of years"),
        ("chameleon",   "Lizard famous for changing colour"),
        ("flamingo",    "Tall pink wading bird"),
        ("narwhal",     "Whale with a long spiral tusk"),
        ("axolotl",     "Smiling Mexican salamander"),
        ("chimpanzee",  "Our closest living primate relative"),
    ],
    "science": [
        ("photosynthesis", "How plants convert sunlight into food"),
        ("molecule",       "Smallest unit of a chemical compound"),
        ("neutron",        "Neutral particle found in the nucleus"),
        ("evolution",      "Darwin's theory explaining how life changes over time"),
        ("gravity",        "Force that pulls objects with mass together"),
        ("chromosome",     "Structure that carries genetic information"),
        ("telescope",      "Instrument used to observe distant stars"),
        ("quantum",        "The smallest discrete amount of a physical quantity"),
    ],
    "food": [
        ("spaghetti",   "Long thin Italian pasta"),
        ("avocado",     "Green creamy fruit with a large pit"),
        ("cinnamon",    "Warm spice from tree bark"),
        ("croissant",   "Buttery crescent-shaped French pastry"),
        ("dumpling",    "Filled dough that is steamed or fried"),
        ("pomegranate", "Red fruit packed with tiny juicy seeds"),
        ("mozzarella",  "Soft white Italian cheese"),
        ("tiramisu",    "Italian coffee-flavoured dessert"),
    ],
}

# ── ASCII hangman stages (0 = safe, 6 = dead) ────────────────────────────────
HANGMAN_STAGES = [
    # 0 lives lost
    """
  +---+
  |   |
      |
      |
      |
      |
=========""",
    # 1
    """
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
    # 2
    """
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
    # 3
    """
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
    # 4
    """
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========""",
    # 5
    """
  +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========""",
    # 6
    """
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
=========""",
]

MAX_LIVES = 6


# ── Helpers ───────────────────────────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def display_state(word: str, guessed: set, lives: int, hint: str, wrong: list):
    """Print the full game state to the terminal."""
    clear()
    print(HANGMAN_STAGES[MAX_LIVES - lives])
    print(f"\n  Category hint: {hint}\n")

    # Word progress
    display = " ".join(ch if ch in guessed else "_" for ch in word)
    print(f"  Word: {display}")
    print(f"  ({len(word)} letters)\n")

    # Wrong guesses and lives
    print(f"  Lives left : {'♥ ' * lives}{'♡ ' * (MAX_LIVES - lives)}")
    if wrong:
        print(f"  Wrong so far: {', '.join(sorted(wrong)).upper()}")
    print()


def choose_category() -> str:
    """Let the player pick a category."""
    cats = list(WORD_BANK.keys())
    print("\n  Choose a category:\n")
    for i, cat in enumerate(cats, 1):
        print(f"    [{i}] {cat.capitalize()}")
    print(f"    [{len(cats) + 1}] Random\n")

    while True:
        choice = input("  Your choice: ").strip()
        if choice.isdigit():
            n = int(choice)
            if 1 <= n <= len(cats):
                return cats[n - 1]
            elif n == len(cats) + 1:
                return random.choice(cats)
        print("  Invalid choice, try again.")


def get_guess(guessed: set) -> str:
    """Prompt the player for a valid, unused letter."""
    while True:
        guess = input("  Guess a letter: ").strip().lower()
        if len(guess) != 1 or not guess.isalpha():
            print("  Please enter a single letter.")
        elif guess in guessed:
            print(f"  You already guessed '{guess.upper()}'. Try another.")
        else:
            return guess


# ── Core game loop ────────────────────────────────────────────────────────────

def play_game():
    category = choose_category()
    word, hint = random.choice(WORD_BANK[category])

    word_letters = set(word)   # unique letters still to find
    guessed = set()            # all letters guessed so far
    wrong = []                 # letters that were wrong
    lives = MAX_LIVES

    while word_letters and lives > 0:
        display_state(word, guessed, lives, hint, wrong)

        guess = get_guess(guessed)
        guessed.add(guess)

        if guess in word_letters:
            word_letters.remove(guess)
            print(f"\n  ✓ '{guess.upper()}' is in the word!")
        else:
            lives -= 1
            wrong.append(guess)
            remaining = lives
            print(f"\n  ✗ '{guess.upper()}' is not in the word. {remaining} {'life' if remaining == 1 else 'lives'} left.")

        input("  Press Enter to continue...")

    # ── End screen ────────────────────────────────────────────────────────────
    display_state(word, guessed, lives, hint, wrong)

    if lives == 0:
        print(f"  Game over! The word was: {word.upper()}\n")
    else:
        full_word = " ".join(word.upper())
        print(f"  You won! The word was: {full_word}\n")


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    print("\n  Welcome to Hangman!\n")

    while True:
        play_game()
        again = input("  Play again? (y/n): ").strip().lower()
        if again != "y":
            print("\n  Thanks for playing. Goodbye!\n")
            break


if __name__ == "__main__":
    main()
