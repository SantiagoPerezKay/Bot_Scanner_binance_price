# https://api.telegram.org/
# https://core.telegram.org/bots/api
import requests
import pandas as pd

# ingresa el token de tu bot de telegram
TELEGRAM_TOKEN = ""
# ingresar el chat numero del chat id ejemplo:" -4008930669"
TELEGRAM_CHAT_ID = ""

# PETICION DE INFORMACION A URL
urlbinance = 'https://fapi.binance.com/fapi/v1/exchangeInfo'
data = requests.get(urlbinance).json()

listsymbol = []
listcoins = []

for symbol in data["symbols"]:
    listsymbol.append(symbol["symbol"])

for symbol in listsymbol:
    if symbol[-4:] == 'USDT':
        listcoins.append(symbol)


# ******* SETTINGS*****

# tipo de vela, ej: velas de 1 minuto,2 minutos,3 minutos.
timelineinterval = 3
# cantidad de velas
cant_velas = 11
# porcentaje de moviento 1% ,2% ,3% etc
move = 5


def crecimiento(DATOS_VELA, move: float):
    """DATOS_VELA : dataframe
       move : float
       return variation : float
       funcion que devuelve el % de variacion del precio de crecimiento positivo
    """
    minimo = DATOS_VELA['low'].min()
    fechamin = DATOS_VELA.loc[DATOS_VELA['low'] == minimo, ['open_time']]
    fechamin = fechamin.iloc[0]['open_time']

    maximo = DATOS_VELA['high'].max()
    fechamax = DATOS_VELA.loc[DATOS_VELA['high'] == maximo, ['open_time']]
    fechamax = fechamax.iloc[0]['open_time']

    fechamin = int(fechamin)
    fechamax = int(fechamax)
    maximo = float(maximo)
    minimo = float(minimo)

    if fechamax > fechamin:
        variation = ((maximo*100)/minimo)-100
        if variation > move:  # 5
            return variation
        else:
            return ""
    else:
        return ""


def decrecimiento(DATOS_VELA, move: float):
    """DATOS_VELA : dataframe
       move : float
       return variation : float
       Función que devuelve el % de variación del precio de decrecimiento negativo
    """
    # Obtener el primer y último índice
    first_index = DATOS_VELA.index[0]
    last_index = DATOS_VELA.index[-1]

    # Obtener los valores del primer y último índice
    first_value = DATOS_VELA.at[first_index, 'open']
    last_value = DATOS_VELA.at[last_index, 'close']

    # Calcular la variación porcentual
    variation = ((float(last_value) - float(first_value)) /
                 float(first_value)) * 100

    if variation < -move:
        return variation
    else:
        return ""


def cuerpo():
    """muestra por pantalla infinitamente mientras se cumpla la condicion crecimiento_porcentaje!="": (no este vacio) 
       coin_symbol : string
       percentage : float
       link : string """

    while True:
        print(
            f"Buscando monedas que en las ultimas {cant_velas} velas de {timelineinterval} minutos,variaron > {move}% ")
        for symbol in listcoins:
            # modificar &limit=11 por el tiempo que uno quiera tomar ej:&limit=30 en ves de 11 velas tomaria las ultimas 30 velas
            url = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + \
                symbol+'&interval='+str(timelineinterval) + \
                'm'+'&limit='+str(cant_velas)

            dataurl = requests.get(url).json()

            # CONVERSION DE INFORMACION A DATAFRAME PANDAS
            DATOS_VELA = pd.DataFrame(data=dataurl, columns=['open_time', 'open', 'high', 'low', 'close', 'volume',
                                      'close_time', 'qav', 'num_trades', 'taker_base_vol', 'taker_qoute_vol', 'is_best_match'])
            crecimiento_porcentaje = crecimiento(DATOS_VELA, move)
            decrecimiento_porcentaje = decrecimiento(DATOS_VELA, move)
            # muestro el symbolo y su respectivo dataset
            if crecimiento_porcentaje != "":

                # menaje a enviar
                msj = f"⚡️coin: {symbol}\n🩸Short\n🔝Porcentaje: {round(crecimiento_porcentaje,2)}%\n"

                # posteo de informacion a tu bot ,que una vez ingresado a un canal reenvia lo recibido a dicho canal
                response = requests.post("https://api.telegram.org/bot"+TELEGRAM_TOKEN +
                                         "/sendMessage", data={'chat_id': TELEGRAM_CHAT_ID, 'text': msj})

                print(
                    f"informacion de la moneda'{symbol}' se ha enviado a 'https://web.telegram.org/k/#-2113865967'")
                print(msj)

            if (decrecimiento_porcentaje != ""):
                # menaje a enviar
                msj = f"⚡️coin: {symbol}\n🚀Long\n🔝Porcentaje: {round(decrecimiento_porcentaje,2)}%\n"

                # posteo de informacion a tu bot ,que una vez ingresado a un canal reenvia lo recibido a dicho canal
                response = requests.post("https://api.telegram.org/bot"+TELEGRAM_TOKEN +
                                         "/sendMessage", data={'chat_id': TELEGRAM_CHAT_ID, 'text': msj})

                print(
                    f"informacion de la moneda'{symbol}' se ha enviado a 'https://web.telegram.org/k/#-2113865967'")
                print(msj)


cuerpo()
