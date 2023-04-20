from binance.cm_futures import CMFutures
from binance.client import Client
from funciones import *
import pandas as pd
import matplotlib.pyplot as plt
import os
import time


# Enlace conexión a binance
def funcion_comparacion(monedas):
    cm_futures_client = CMFutures(key="3a6Q0unsfYV8RXpehFENffnE4hgbWcNAaRRVjrEM99dUTt05l9vPQR1tCeZ8RTOh", secret="aDW3Bwd0POckjdUrBm68kMYdm5CGpBW4FiWzVopLPkGuSOhqlwLLevy2VjOEkwIL")
    client = Client(api_key= "3a6Q0unsfYV8RXpehFENffnE4hgbWcNAaRRVjrEM99dUTt05l9vPQR1tCeZ8RTOh", api_secret="aDW3Bwd0POckjdUrBm68kMYdm5CGpBW4FiWzVopLPkGuSOhqlwLLevy2VjOEkwIL")

    Dataframes_monedas = {}

    for moneda in monedas:
        candles = client.get_klines(symbol= moneda, interval=Client.KLINE_INTERVAL_1HOUR, limit = 21)

        price_df = pd.DataFrame(candles, columns=['dateTime',
                                                'open',
                                                'high', 'low',
                                                'close', 'volume',
                                                'closeTime',
                                                'quoteAssetVolume',
                                                'numberOfTrades',
                                                'takerBuyBaseVol',
                                                'takerBuyQuoteVol', 'ignore'])
        price_df.dateTime = pd.to_datetime(price_df.dateTime, unit='ms')
        price_df.set_index('dateTime')
        price_df.closeTime = pd.to_datetime(price_df.closeTime, unit='ms')
        price_df.close = pd.to_numeric(price_df.close)
        price_df.volume = pd.to_numeric(price_df.volume)
        price_df.high = pd.to_numeric(price_df.high)
        price_df.low = pd.to_numeric(price_df.low)

        ##-------------------------------------------------------- extraemos lista con precios close-------------------------
        lista_precios = [ element for element in price_df['close']]
        Dataframes_monedas[str(moneda)+ '_df'] = lista_precios


    final1 = calcular_bollinger_bands(precios = Dataframes_monedas['ETHUSDT_df'], dias = 20, k = 1)
    final2 = calcular_bollinger_bands(precios = Dataframes_monedas['BTCUSDT_df'], dias = 20, k = 4)
    final3 = calcular_bollinger_bands(precios = Dataframes_monedas['XLMUSDT_df'], dias = 20, k = 4)

    BS = final1["Banda Superior"][20]
    BI = final1["Banda Inferior"][20]
    UP = Dataframes_monedas['ETHUSDT_df'][20]

    if UP > BS:
        print("Esta por encima de la banda de bollinger")
    elif UP < BI:
        print("Esta por debajo de la banda de bollinger")
    else:
        print("Dentro de bandas")


    """
    fig, ax = plt.subplots()
    final1.plot( y=['Banda Superior', 'Banda Inferior', 'Media Móvil'], ax=ax)
    plt.show()

    fig, ax = plt.subplots()
    final2.plot( y=['Banda Superior', 'Banda Inferior', 'Media Móvil'], ax=ax)
    plt.show()

    fig, ax = plt.subplots()
    final3.plot( y=['Banda Superior', 'Banda Inferior', 'Media Móvil'], ax=ax)
    plt.show()
    """




# Tiempo inicial
tiempo_inicial = time.time()

# Duración del ciclo en segundos
duracion_ciclo = 15
n = 0

while True:
    # Obtener el tiempo actual
    tiempo_actual = time.time()

    # Calcular la diferencia de tiempo en segundos
    diferencia_tiempo = tiempo_actual - tiempo_inicial
    # Si ha pasado la duración del ciclo, salir del ciclo
    if diferencia_tiempo >= duracion_ciclo:
        funcion_comparacion(['BTCUSDT', 'XLMUSDT', 'ETHUSDT'])
        print("Comparando nuevamente")
        tiempo_inicial = time.time()

    # Si no ha pasado la duración del ciclo, hacer algo aquí
    print(f"van {n} segundos")
    n += 1
    # Pausar la ejecución del programa durante un segundo
    time.sleep(1)