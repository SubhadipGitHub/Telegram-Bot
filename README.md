# Telegram bot
 <b><i>This is a telegram bot with various features and functionalities.</i></b>

### Steps to setup bot
1)Add a token.txt file 
<br>
* client_token=****
* botname="@QueenBeth"
* red_client_id=****
* red_client_token=****
* complete_news_url_tech=****
* complete_news_url_world=****
* complete_news_url_country=****
* rapid_api_token=****
* weather_api=****
<br>
3)Go to Botfather chat in Telegram
* /setcommands add your command list
<br>
4)Docker Commands
* Build Docker image from the dockerfile
docker build -t python-docker-telegram . 
* Run docker container from image
docker container run -dit -p 80:80 python-docker-telegram
* Delete all image,container and volumes
docker system prune -a --volumes
