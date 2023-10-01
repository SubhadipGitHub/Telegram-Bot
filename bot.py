from telegram import InlineKeyboardButton, InlineKeyboardMarkup,Update,ForceReply,KeyboardButton,ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler,ConversationHandler,CallbackContext
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning
import praw
import requests
import random
import os
from dotenv import load_dotenv

#Supress warnings
filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

#Secrets
load_dotenv()

telegram_token = os.getenv('client_token')
telegram_botname = os.getenv('botname')

#creds
red_client_id = os.getenv('red_client_id')
red_client_token = os.getenv('red_client_token')
reddit = praw.Reddit(client_id=red_client_id,
                     client_secret=red_client_token,
                     user_agent='QueenBeth', check_for_async=False)

complete_news_url_country =os.getenv('complete_news_url_country')
complete_news_url_world = os.getenv('complete_news_url_world')
complete_news_url_tech = os.getenv('complete_news_url_tech')

rapid_api_token=os.getenv('rapid_api_token')

weather_api_key = os.getenv('weather_api')

#Static values
ENTER_CITY = 0
SELECT_OPTION,ENTER_LANGUAGE,ENTER_TOPIC=range(3)
ADD_WEATHER_CITY_PROMPT= "Please provide the city for which you want to check weather:"
ADD_CODE_TOPIC_PROMPT="Please provide the topic for programming language concept:"
ADD_CODE_LANG_PROMPT="Please provide the programming language for which you want to know about:"

#Enojis
thunderstorm = u'\U0001F4A8'    # Code: 200's, 900, 901, 902, 905
drizzle = u'\U0001F4A7'         # Code: 300's
rain = u'\U00002614'            # Code: 500's
snowflake = u'\U00002744'       # Code: 600's snowflake
snow = u'\U000026C4'         # Code: 600's snowman, 903, 906
fog = u'\U0001F301'      # Code: 700's foogy
clearSky = u'\U00002600'        # Code: 800 clear sky
fewClouds = u'\U000026C5'       # Code: 801 sun behind clouds
clouds = u'\U00002601'          # Code: 802-803-804 clouds general
hot = u'\U0001F525'      # Code: 904
defaultEmoji = u'\U0001F300'    # default emojis

#custom lists
weather = [thunderstorm,drizzle,rain,snowflake,snow,fog,clearSky,fewClouds,clouds,hot]

# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather?"

#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a message to start the bot"""
    user=update.message.from_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Please type something i am smart enough to provide you an answer")

async def rmemes_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a meme message when the command /rmemes is issued"""
    subreddit = reddit.subreddit('memes')

    cont = {}
    urls = []
    for submission in subreddit.hot(limit=50):
        urls.append(submission.url)
    posttopic = random.randint(0,50)
    cont['urlList'] = urls
    photourls = cont['urlList']
    photourl = photourls[posttopic]
    await update.message.reply_photo(caption=f'Hope you enjoy this Meme brought to you by {telegram_botname} from memes subreddit',photo=photourl,has_spoiler=True)

async def news_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("TECH", callback_data="tech"),
            InlineKeyboardButton("WORLD", callback_data="world"),
        ],
        [InlineKeyboardButton("COUNTRY", callback_data="country")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose the news you want to know about:", reply_markup=reply_markup)   

async def weather_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    """Sends a message with button to take custom input of city"""
    user = update.message.from_user
    await update.message.reply_text(f"Hi {user.first_name}! {ADD_WEATHER_CITY_PROMPT}")
    return ENTER_CITY

async def search_code_command(update:Update,context: CallbackContext) -> int:
    """Sends a message with 2 inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("TOPIC", callback_data="topic"),
            InlineKeyboardButton("LANGUAGE", callback_data="language"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose the programming topic/language:", reply_markup=reply_markup)
    return SELECT_OPTION

async def jokes_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    """Gets the best jokes"""
    url = "https://jokes-by-api-ninjas.p.rapidapi.com/v1/jokes"

    headers = {
	"X-RapidAPI-Key": rapid_api_token,
	"X-RapidAPI-Host": "jokes-by-api-ninjas.p.rapidapi.com"
}

    responsegetjoke = requests.get(url, headers=headers)
    responsegetjoke = responsegetjoke.json()
    #print(responsegetjoke)
    await update.message.reply_text(responsegetjoke[0].get("joke","No joke for you today!!"))

#Callbacks
async def button(update: Update, context: CallbackContext) -> int:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    context.user_data["choice"] = query.data
    #await query.edit_message_text(text=f"Selected option: {query.data}")
    if query.data.lower() == "tech":
            complete_news_url = complete_news_url_tech
            responsetechnews = requests.get(complete_news_url)
            responsetechnews = responsetechnews.json().get("articles")
            if responsetechnews != []:
                news = "----------\nTECH NEWS \n----------\n"
                max = 2
                if len(responsetechnews)<2:
                    max = len(responsetechnews)
                for item in range(max):
                    author = responsetechnews[item].get("author","NA")
                    title = responsetechnews[item].get("title","NA")
                    content = responsetechnews[item].get("content","NA")
                    url = responsetechnews[item].get("url", "NA")
                    news = news + "\nTitle :\n " + str(title) + "\nAuthor :\n " + str(author)  + "\nContent :\n " + str(content) + "\n Link :\n {} \n-------------------------------\n".format(url)
                await query.edit_message_text(text=news)
            else:
                await query.edit_message_text(text="No new tech news!!")
    elif query.data.lower() == "world":
        complete_news_url = complete_news_url_world
        responsetechnews = requests.get(complete_news_url)
        responsetechnews = responsetechnews.json().get("articles")
        if responsetechnews != []:
            news = "----------\nBBC NEWS \n----------\n"
            max = 2
            if len(responsetechnews)<2:
                max = len(responsetechnews)
            for item in range(max):
                author = responsetechnews[item].get("author","NA")
                title = responsetechnews[item].get("title","NA")
                content = responsetechnews[item].get("content","NA")
                url = responsetechnews[item].get("url", "NA")
                news = news + "\nTitle :\n " + str(title) + "\nAuthor :\n " + str(author)  + "\nContent :\n " + str(content) + "\n Link :\n {} \n-------------------------------\n".format(url)
            await query.edit_message_text(text=news)
        else:
            await query.edit_message_text(text="No new bbc news from all over the world!!")
    elif query.data.lower() == "country":
        complete_news_url = complete_news_url_country
        responsetechnews = requests.get(complete_news_url)
        responsetechnews = responsetechnews.json().get("articles")
        if responsetechnews != []:
            news = "----------\nINDIA NEWS \n----------\n"
            max = 2
            if len(responsetechnews)<2:
                max = len(responsetechnews)
            for item in range(max):
                author = responsetechnews[item].get("author","NA")
                title = responsetechnews[item].get("title","NA")
                content = responsetechnews[item].get("content","NA")
                url = responsetechnews[item].get("url", "NA")
                news = news + "\nTitle :\n " + str(title) + "\nAuthor :\n " + str(author)  + "\nContent :\n " + str(content) + "\n Link :\n {} \n-------------------------------\n".format(url)
            await query.edit_message_text(text=news)
        else:
            await query.edit_message_text(text="No news in INDIA!!")
    elif query.data.lower() == "topic":
        #print('topic button selected')
        #do something        
        await query.edit_message_text(text=f'You selected `{query.data.lower()}`.\nPlease provide the programming topic you want to lean about:')
        return ENTER_TOPIC
    elif query.data.lower() == "language":
        #print('language button selected')
        #do something
        #print("do something2")
        await query.edit_message_text(text=f'You selected `{query.data.lower()}`.\nPlease provide the programming language you want to learn concepts on:')
        return ENTER_LANGUAGE
    else:
        await query.edit_message_text(text="Please check category specified or check help and Try Again!")


#Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()
    #Bot logic to reply intelligently
    custom_response = 'I am not sure what you want.Please check menu of commands.'
    return custom_response

async def add_city_handler(update: Update,context: CallbackContext):
    """This is the handler to get input for city weather"""
    user_message = update.message.text
    city_name = user_message

    emote_weather = defaultEmoji
    complete_url = base_url + "appid=" + weather_api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found
    if x["cod"] != "404":
        # store the value of "main"
        # key in variable y
        y = x["main"]

        # store the value corresponding
        # to the "temp" key of y
        current_temperature = int(y["temp"]) -273.15

        # store the value corresponding
        # to the "pressure" key of y
        current_pressure = y["pressure"]

        # store the value corresponding
        # to the "humidity" key of y
        current_humidiy = y["humidity"]

        # store the value of "weather"
        # key in variable z
        z = x["weather"]
        # store the value corresponding
        # to the "description" key at
        # the 0th index of z
        weather_description = z[0]["description"]
        if weather_description == "fog" or weather_description == "haze":
            emote_weather =fog
        elif weather_description == "overcast clouds" or weather_description == "smoke":
            emote_weather =clouds
        elif weather_description == "snowy" or weather_description == "light snow" or weather_description == "heavy snow":
            emote_weather =snow
        elif weather_description == "clear sky":
            emote_weather =clearSky
        elif weather_description == "mist":
            emote_weather =fewClouds
        elif weather_description == "light intensity drizzle":
            emote_weather = drizzle
        else:
            emote_weather = defaultEmoji

        await update.message.reply_text("```````````\n \N{Circled Information Source} " + str(city_name) +" "+emote_weather+ "\n```````````\n"+" Temperature (in celcius unit) = " +
                str(current_temperature) +
                "\n atmospheric pressure (in hPa unit) = " +
                str(current_pressure) +
                "\n humidity (in percentage) = " +
                str(current_humidiy) +
                "\n description = " +
                str(weather_description))
    else:
        await update.message.reply_text("Please check the city entered")
    return ConversationHandler.END

async def find_topic_handler(update: Update,context: CallbackContext):
    """This is the handler to get input for search code topic"""
    #print("topic handler")
    user_message = update.message.text    
    search_query = user_message.lower()
    max= 3
    url = "https://syntaxdb.com/api/v1/concepts/search?q="+str(search_query)
    responseGET = requests.get(url)
    responseGET = responseGET.json()
    answerGET = "```````````\n \N{Circled Information Source} " + str(search_query) + "\n```````````\n"
    if len(responseGET)<3:
        max =len(responseGET)
    for item in range(max):
        itemLang =  responseGET[item].get("concept_search","NA")
        itemSyntax = responseGET[item].get("syntax","NA")
        itemdoc = responseGET[item].get("documentation","NA")
        itemdesc = responseGET[item].get("description","NA")
        itemnotes = responseGET[item].get("notes", "NA")
        try:
            itemdocurl = itemdoc.split('"')[1]
        except:
            itemdocurl = "NA"
        answerGET = answerGET+"\n`Language` : "+str(itemLang)+"\n`Syntax` : "+str(itemSyntax)+"\n Link : {} \n-------------------------------\n".format(itemdocurl)
    await update.message.reply_text(answerGET)
    return ConversationHandler.END

async def find_lang_handler(update: Update,context: CallbackContext):
    """This is the handler to get input for search programming language topic"""
    #print("language handler")
    user_message = update.message.text
    language=user_message.lower()
    url = "https://syntaxdb.com/api/v1/languages/"+language+"/concepts"
    responseGET = requests.get(url)
    responseGET = responseGET.json()
    #print(responseGET)
    max = 3
    answerGET = "```````````\n \N{Circled Information Source} " + str(language) + "\n```````````\n"
    try:
        if (len(responseGET) < max):
            for item in range(len(responseGET)):
                itemLang = responseGET[item].get("concept_search", "NA")
                itemSyntax = responseGET[item].get("syntax", "NA")
                itemdoc = responseGET[item].get("documentation", "NA")
                itemdesc = responseGET[item].get("description", "NA")
                itemnotes = responseGET[item].get("notes", "NA")
                try:
                    itemdocurl = itemdoc.split('"')[1]
                except:
                    itemdocurl = "NA"
                answerGET = answerGET + "\n`Language` : " + str(itemLang) + "\n`Syntax` : " + str(
                    itemSyntax) + "\n Link : {} \n-------------------------------\n".format(itemdocurl)
        else:
            for item in range(0, max):
                itemLang = responseGET[item]["concept_search"]
                itemSyntax = responseGET[item]["syntax"]
                itemdoc = responseGET[item].get("documentation", "NA")
                itemdesc = responseGET[item].get("description", "NA")
                itemnotes = responseGET[item].get("notes", "NA")
                try:
                    itemdocurl = itemdoc.split('"')[1]
                except:
                    itemdocurl = "NA"
                answerGET = answerGET + "\n`Language` : " + str(itemLang) + "\n`Syntax` : " + str(
                    itemSyntax) + "\n Link : {} \n-------------------------------\n".format(itemdocurl)
        await update.message.reply_text(answerGET)
    except Exception as e:
        await update.message.reply_text(f'Failed to Retrieve any concepts for programming language provided : {language}')
    return ConversationHandler.END

async def handle_message(update: Update,context: ContextTypes.DEFAULT_TYPE):
    message_type: str= update.message.chat.type
    text:str=update.message.text
    choice = context.user_data["choice"]

    #print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type =='group':
        if telegram_botname in text:
            new_text:str=text.replace(telegram_botname,'').strip()
            response:str=handle_response(new_text)
        else:
            return
    else:
        if choice == "topic":
            await find_topic_handler(update,context)
        elif choice == "language":
            await find_lang_handler(update,context)
        else:
            return            
            #response:str=handle_response(text)

    #print(f'Bot: {response}')
    #await update.message.reply_text(response)

#error handler
async def error(update:Update,context:ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print(f'Starting Bot Application : {telegram_botname}')
    app = Application.builder().token(telegram_token).build()

    #commands
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('rmemes',rmemes_command))
    app.add_handler(CommandHandler('news',news_command))
    app.add_handler(CommandHandler('jokes',jokes_command))
    app.add_handler(CommandHandler('search_code',search_code_command))

    #conversation handler
    conv_handler_weather = ConversationHandler(
        entry_points=[CommandHandler('weather',weather_command)],
        states={
            ENTER_CITY:[MessageHandler(filters.ALL & ~filters.COMMAND, add_city_handler)]
        },
        fallbacks=[]
    )
    conv_handler_code=ConversationHandler(
        entry_points=[CommandHandler('search_code',search_code_command)],
        states={
            SELECT_OPTION: [CallbackQueryHandler(button)],
            ENTER_TOPIC:[MessageHandler(filters.TEXT & ~filters.COMMAND, find_topic_handler)],
            ENTER_LANGUAGE:[MessageHandler(filters.TEXT & ~filters.COMMAND, find_lang_handler)],
        },
        fallbacks=[]
    )
    app.add_handler(conv_handler_weather)
    app.add_handler(conv_handler_code)  

    #callback
    app.add_handler(CallbackQueryHandler(button)) 

    #messages
    app.add_handler(MessageHandler(filters.TEXT,handle_message))    

    #errors
    app.add_error_handler(error)

    #Check for new messages through polling(in seconds)
    print('Polling...')
    app.run_polling(poll_interval=5)