from saybot import Update,ContextTypes,logging,Bot,os,store_user_data,Any
from saybot.config import ConfigClass

# Create an alias for the default context type hint
Context = ContextTypes.DEFAULT_TYPE

# Define function to initialize bot and get message object
def get_message_data(update: Update) -> tuple:
    TOKEN = os.getenv("API_BOT")
    bot = Bot(TOKEN)
    message = update.message
    user_full_name = f"{message.chat.first_name} {message.chat.last_name}"
    return bot, message, user_full_name

# Define function to handle the /start command
async def handle_start_command(update: Update, context: Context) -> None:
    bot, message, user_full_name = get_message_data(update)
    logging.info(f"/start command pressed by {user_full_name}")
    welcome_text = f"Hello {user_full_name}\nI'm \"SayChatGPT\" \nYour AI-powered chatbot \nI'm here to assist you. \nAsk your question.!\n"
    await bot.send_message(chat_id=message.chat_id, text=welcome_text)
    await store_user_data(update=update) # storing user credentials in DB
 
 # Define function to handle the command processes
async def handle_model_selection_command(update: Update, context:Context, model_command: Any) -> None:
    bot, message, _ = get_message_data(update)
    ConfigClass.set_model_selection_command(model_command)  # set the new model selection command in the instance
    model_selection_command = ConfigClass.get_model_selection_command()  
    await bot.send_message(chat_id=message.chat_id, text=f"Model {model_command} selected for Conversation!!!")
    logging.info(f"***Inside handle_command_{model_command} ***" + str(model_selection_command))


# Define function to handle the /gpt35turbo command
async def handle_command_gpt35turbo(update: Update, context: Context) -> None:
    await handle_model_selection_command(update, context, "gpt-3.5-turbo")


# Define function to handle the /textdavinci003 command
async def handle_command_textdavinci003(update: Update, context: Context) -> None:
    await handle_model_selection_command(update, context, "text-davinci-003") 