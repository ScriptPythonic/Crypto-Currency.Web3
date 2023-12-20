import logging
import random
from telegram import Update
from telegram.ext._updater import Updater
from telegram._update import Update
from telegram.ext._callbackcontext import CallbackContext
from telegram.ext._commandhandler import CommandHandler
from telegram.ext._messagehandler import MessageHandler
from telegram.ext.filters import fil

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to start the game
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to Guess the Number Game! I'm thinking of a number between 1 and 100. Try to guess it.")

    # Generate a random number
    context.user_data['secret_number'] = random.randint(1, 100)
    context.user_data['attempts'] = 0

# Function to handle guesses
def guess(update: Update, context: CallbackContext) -> None:
    try:
        # Get the guess from the user
        user_guess = int(update.message.text)

        # Increment the attempts
        context.user_data['attempts'] += 1

        # Check if the guess is correct
        if user_guess == context.user_data['secret_number']:
            update.message.reply_text(f"Congratulations! You guessed the number in {context.user_data['attempts']} attempts.")
            context.user_data.clear()  # Clear user data after the game ends
            return
        elif user_guess < context.user_data['secret_number']:
            update.message.reply_text("Too low. Try again.")
        else:
            update.message.reply_text("Too high. Try again.")

    except ValueError:
        update.message.reply_text("Invalid input. Please enter a valid number.")

# Function to handle other messages
def handle_text(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Please enter a number as your guess.")

def main() -> None:
    # Set up the Updater
    updater = Updater("YOUR_BOT_TOKEN")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, guess))
    dp.add_handler(MessageHandler(Filters.text, handle_text))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()

    
    