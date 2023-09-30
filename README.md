# Telegram bot
 <b><i>This is a telegram bot with various features and functionalities.</i></b>

### Steps to setup bot
1)Add a token.txt file 
<br>
* xxxxxxxxxxxx--client token
* xxxxxxxxxxxx--weather api token
* xxxxxxxxxxxx--rapid_api_token
* xxxxxxxxxxxx--subredit client id
* xxxxxxxxxxxx--subredit client token
<br>
2)pip install -r requirements.txt
<br>
3)conda environment for python 3.7
* conda create --name TelegramEnvPython3.7 python=3.7
<br>
4)Go to Botfather chat in Telegram
* /setcommands add your command list
<br>
5)Docker Commands
* Build Docker image from the dockerfile
docker build -t python-docker . 

* Run docker container from image
docker container run -dit -p 80:80 python-docker

* Delete all image,container and volumes
docker system prune -a --volumes
