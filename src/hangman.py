import random
import time

def load_words(filename):
    """Load words or phrases from a file"""
    try:
        with open(filename, 'r') as file:
            return [line.strip().lower() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Warning: {filename} not found. Using default words.")
        return ["python", "hangman", "programming"] if "words" in filename else ["test phrase"]

# Load word lists
words = load_words('words.txt')
phrases = load_words('phrases.txt')

def select_word():
    """Select a random word"""
    return random.choice(words) if words else "hangman"

def select_phrase():
    """Select a random phrase"""
    return random.choice(phrases) if phrases else "test phrase"

class HangmanGame:
    def __init__(self, secret_word, lives=6):
        self.secret_word = secret_word.lower()
        self.guessed_letters = set()
        self.lives = lives
        self.display_word = self._initialize_display_word()
        self.start_time = None
        self.time_limit = 15
    
    def _initialize_display_word(self):
        display = []
        for char in self.secret_word:
            if char.isalpha():
                display.append('_')
            else:  # For spaces in phrases
                display.append(' ')
        return ' '.join(display)
    
    def start_timer(self, time_limit=15):
        self.start_time = time.time()
        self.time_limit = time_limit
    
    def is_time_up(self):
        if self.start_time is None:
            return False
        
        elapsed = time.time() - self.start_time
        if elapsed > self.time_limit:
            self.lives -= 1
            self.start_time = time.time()  # Reset timer for next guess
            return True
        return False
    
    def get_remaining_time(self):
        if self.start_time is None:
            return self.time_limit
        elapsed = time.time() - self.start_time
        return max(0, self.time_limit - elapsed)
    
    def guess_letter(self, letter):
        letter = letter.lower()
        if letter in self.guessed_letters:
            return None  # Already guessed
        
        self.guessed_letters.add(letter)
        
        if letter in self.secret_word:
            # Update display word
            new_display = []
            secret_chars = list(self.secret_word)
            display_chars = self.display_word.replace(' ', '')
            
            for i, secret_char in enumerate(secret_chars):
                if secret_char == letter:
                    new_display.append(letter)
                elif i < len(display_chars) and display_chars[i] != '_':
                    new_display.append(display_chars[i])
                else:
                    new_display.append('_')
            
            self.display_word = ' '.join(new_display)
            return True
        else:
            self.lives -= 1
            return False
    
    def is_won(self):
        return '_' not in self.display_word
    
    def is_lost(self):
        return self.lives <= 0
    
    def is_game_over(self):
        return self.is_won() or self.is_lost()

def main():
    print("Welcome to Hangman!")
    print("Select level:")
    print("1. Basic (Word)")
    print("2. Intermediate (Phrase)")
    
    try:
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == "1":
            secret_word = select_word()
            print("I'm thinking of a word...")
        else:
            secret_word = select_phrase()
            print("I'm thinking of a phrase...")
        
        game = HangmanGame(secret_word, lives=6)
        game.start_timer()
        
        while not game.is_game_over():
            print(f"\nWord: {game.display_word}")
            print(f"Lives: {game.lives}")
            print(f"Time remaining: {game.get_remaining_time():.1f}s")
            print(f"Guessed letters: {', '.join(sorted(game.guessed_letters))}")
            
            guess = input("Guess a letter: ").strip().lower()
            
            if guess == 'quit':
                print(f"Game ended. The word was: {game.secret_word}")
                break
            
            if len(guess) != 1 or not guess.isalpha():
                print("Please enter a single letter.")
                continue
            
            if game.is_time_up():
                print("Time's up! Life deducted.")
            
            result = game.guess_letter(guess)
            
            if result is None:
                print("You already guessed that letter.")
            elif result:
                print("Good guess!")
            else:
                print("Wrong guess!")
        
        if game.is_won():
            print(f"\n🎉 Congratulations! You won! The word was: {game.secret_word}")
        elif game.is_lost():
            print(f"\n💀 Game over! The word was: {game.secret_word}")
    
    except KeyboardInterrupt:
        print(f"\nGame interrupted. The word was: {game.secret_word if 'game' in locals() else 'unknown'}")

if __name__ == "__main__":
    main()