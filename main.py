import requests
import logging
import praw
import random
from telegram import Update, ParseMode
from telegram.ext import Updater, CallbackContext, CommandHandler,MessageHandler, Filters
from youtube_search import YoutubeSearch

# Corressponding emojis
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


weather = [thunderstorm,drizzle,rain,snowflake,snow,fog,clearSky,fewClouds,clouds,hot]
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        token = lines[0].strip()
        apikeyweathr = lines[1].strip()
        rapapitok = lines[2].strip()
        subred_cl_id = lines[3].strip()
        subred_cl_token = lines[4].strip()
        authlist = [token,apikeyweathr,rapapitok,subred_cl_id,subred_cl_token]
        return authlist

rapid_api_token = read_token()[2]
api_key = read_token()[1]
red_client_id = read_token()[3]
red_client_token = read_token()[4]

# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather?"

token = read_token()[0]

reddit = praw.Reddit(client_id=red_client_id,
                     client_secret=red_client_token,
                     user_agent='QueenBeth')

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to help students search for queries.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Program Query bot, search programming concepts.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging


# Enable logging
"""logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)"""


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def find_yt(update,context):
    """Find youtube videos easily"""
    try:
        results = YoutubeSearch(context.args[0], max_results=1).to_dict()
        ytd_url = "https://www.youtube.com" + str(results[0].get("url_suffix"))
        context.bot.send_message(chat_id=update.message.chat_id, text=ytd_url)
    except:
        context.bot.send_message(chat_id=update.message.chat_id, text="Try again!! Eg./find_yt kabhi-alvida-na-kehna")

def memes(update,context):
    """Get memes from reddit"""
    subreddit = reddit.subreddit('memes')

    cont = {}
    urls = []
    for submission in subreddit.hot(limit=50):
        urls.append(submission.url)
    posttopic = random.randint(0,50)
    cont['urlList'] = urls
    photourls = cont['urlList']
    photourl = photourls[posttopic]
    context.bot.send_photo(chat_id=update.message.chat_id,
                             photo=photourl)

def jokes(update,context):
    """Gets the best jokes"""
    url = "https://joke3.p.rapidapi.com/v1/joke"

    headers = {
        'x-rapidapi-key': rapid_api_token,
        'x-rapidapi-host': "joke3.p.rapidapi.com"
    }

    responsegetjoke = requests.request("GET", url, headers=headers)
    responsegetjoke = responsegetjoke.json()
    context.bot.send_message(chat_id=update.message.chat_id, text=responsegetjoke.get("content","No joke for you today!!"))

def news(update, context):
    """Gets the response from syntaxDB api and shows results for search context"""
    if len(context.args) == 1:
        news_category = context.args[0]
        if news_category.lower() == "tech":
            complete_news_url = "http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=ff63b1b5c1e340e3aa31f3edb254230e"
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
                context.bot.send_message(chat_id=update.message.chat_id, text=news)
            else:
                context.bot.send_message(chat_id=update.message.chat_id, text="No new tech news!!")
        elif news_category.lower() == "world":
            complete_news_url = "https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=ff63b1b5c1e340e3aa31f3edb254230e"
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
                context.bot.send_message(chat_id=update.message.chat_id, text=news)
            else:
                context.bot.send_message(chat_id=update.message.chat_id, text="No new bbc news from all over the world!!")
        elif news_category.lower() == "country":
            complete_news_url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=ff63b1b5c1e340e3aa31f3edb254230e"
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
                context.bot.send_message(chat_id=update.message.chat_id, text=news)
            else:
                context.bot.send_message(chat_id=update.message.chat_id, text="No news in INDIA!!")
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text="Please check category specified or check help and Try Again!")
    else:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Please check the no of keywords passed.For more info check /help")

def weather(update, context):
    """Gets the response from syntaxDB api and shows results for search context"""
    if len(context.args) == 1:
        emote_weather = defaultEmoji
        city_name = context.args[0]
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
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

            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="```````````\n \N{Circled Information Source} " + str(city_name) +" "+emote_weather+ "\n```````````\n"+" Temperature (in celcius unit) = " +
                  str(current_temperature) +
                  "\n atmospheric pressure (in hPa unit) = " +
                  str(current_pressure) +
                  "\n humidity (in percentage) = " +
                  str(current_humidiy) +
                  "\n description = " +
                  str(weather_description))
        else:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="Please check the city entered")
    else:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Please check the no of keywords passed.For more info check /help")

def search_code(update, context):
    """Gets the response from syntaxDB api and shows results for search context"""
    if len(context.args) == 1:
        search_query = context.args[0]
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
        context.bot.send_message(chat_id=update.message.chat_id, text=answerGET)
    elif len(context.args) == 2:
        #Get query based on language
        choice =context.args[0]
        language =context.args[1]
        if(choice == "1"):
            url = "https://syntaxdb.com/api/v1/languages/"+language+"/concepts"
            responseGET = requests.get(url)
            responseGET = responseGET.json()
            max = 3
            answerGET = "```````````\n \N{Circled Information Source} " + str(language) + "\n```````````\n"
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
            context.bot.send_message(chat_id=update.message.chat_id, text=answerGET)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="Please check the no of keywords passed.For more info check /help")


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!\nCommands Available--->\n\n1)search_code:\nSearch for syntax of programming languages.\nEg /search_code <search_query> or /search 1 <programming_language>\n\n2)weather:\nGet the current weather of a particular city.\nEg /weather <cityname>\n\n3)news:\nGet the latest top 3 news of a particular category.\nEg /news <category>(categories: tech,country and world)\n\n4)jokes:\nGet a laugh from a random joke.\nEg /jokes\n\n5)jokes:\nGet a random meme.\nEg /memes\n\n6)find_yt:\nGet a youtube video that you want to share instantly.\nEg /find_yt <name of video>')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("news", news))
    dp.add_handler(CommandHandler("jokes", jokes))
    dp.add_handler(CommandHandler("memes", memes))
    dp.add_handler(CommandHandler("weather", weather))
    dp.add_handler(CommandHandler("search_code", search_code))
    dp.add_handler(CommandHandler("find_yt", find_yt))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()



