from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, CallbackContext, MessageHandler, filters,Application
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning
import os
from dotenv import load_dotenv

load_dotenv()

telegram_token = os.getenv('client_token')
telegram_botname = os.getenv('botname')

filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

# Define the states for the conversation
SELECT_OPTION, GET_TEXT_INPUT = range(2)

# Define constants for your states
CANCEL = ConversationHandler.END

# Function to start the conversation
async def start(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [InlineKeyboardButton("Option 1", callback_data="option1")],
        [InlineKeyboardButton("Option 2", callback_data="option2")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please select an option:", reply_markup=reply_markup)
    return SELECT_OPTION

# Function to handle the button selection
async def button_choice(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data["choice"] = query.data
    await query.edit_message_text(f"You selected: {query.data}. Please provide your input or /cancel to exit.")
    return GET_TEXT_INPUT

# Function to handle user text input
async def get_text_input(update: Update, context: CallbackContext) -> int:
    user_input = update.message.text
    choice = context.user_data["choice"]
    
    # Process user input based on the selected choice
    if choice == "option1":
        response = f"You chose Option 1, and you said: {user_input}"
    elif choice == "option2":
        response = f"You chose Option 2, and you said: {user_input}"
    else:
        response = "Invalid choice."
    
    await update.message.reply_text(response)
    return ConversationHandler.END

# Function to cancel the conversation
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("You have canceled the conversation.")
    return ConversationHandler.END

def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    app = Application.builder().token(telegram_token).build()

    # Define the conversation handler with states
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECT_OPTION: [CallbackQueryHandler(button_choice)],
            GET_TEXT_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_text_input)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(conversation_handler)

    # Start the bot
    app.run_polling(poll_interval=5)

if __name__ == '__main__':
    main()
