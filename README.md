# Bot Scanner Binance price
### EN:
script that scans a price range 'X' in an interval 'Y' all the time and automatically sends an alert to a telegram channel through a telegram bot.It also reports the information sent through the console.
### ES:
script que scannea todo el tiempo un rango de precio 'X' en un intervalo 'Y' y manda alerta a un canal de telegram mediante un bot de telegram automaticamente.Tambien informa por consola la informacion mandada.

####  Requeriments
- telegram bot
- teelgram channel(join bot with administrator permission)
- libraries for python (requests v2.28.2)
- libraries for python (pandas v1.5.3)

#### instructions
- 1.download project from github
- 2.install the 2 libraries
- 3.create a bot and a telegram channel, and add the bot to the channel with permissions so that it can write to said channel.
- 4.change the values to your search preference for the following variables:
timelineinterval = 3     #type of sail that will be taken as a reference
cant_velas = 11          #How many candles will it take to carry out the search
move = 1                 #movement percentage to search
- 5.run script!!!.

# youtube video
[![Descripción del segundo video](http://img.youtube.com/vi/X8JchRszT4o/0.jpg)](https://youtu.be/X8JchRszT4o?si=dA_Rg9dUyDbevp97)
