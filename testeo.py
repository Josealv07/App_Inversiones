from binance.cm_futures import CMFutures
from binance.client import Client
from funciones import *
import pandas as pd
import matplotlib.pyplot as plt
import os
import time


# Enlace conexión a binance
def funcion_comparacion(monedas:list):
    cm_futures_client = CMFutures(key="3a6Q0unsfYV8RXpehFENffnE4hgbWcNAaRRVjrEM99dUTt05l9vPQR1tCeZ8RTOh", secret="aDW3Bwd0POckjdUrBm68kMYdm5CGpBW4FiWzVopLPkGuSOhqlwLLevy2VjOEkwIL")
    client = Client(api_key= "3a6Q0unsfYV8RXpehFENffnE4hgbWcNAaRRVjrEM99dUTt05l9vPQR1tCeZ8RTOh", api_secret="aDW3Bwd0POckjdUrBm68kMYdm5CGpBW4FiWzVopLPkGuSOhqlwLLevy2VjOEkwIL")

    Dataframes_monedas = {}

    for moneda in monedas:
        candles = client.get_klines(symbol= moneda, interval=Client.KLINE_INTERVAL_1MINUTE, limit = 1000)
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

        #Dataframes_monedas[str(moneda) + '_df'] = lista_precios

        final1 = calcular_bollinger_bands(precios = lista_precios, dias = 1000, k = 1)

        dato = 999
        BS = final1["Banda Superior"][dato] #Banda superior
        BI = final1["Banda Inferior"][dato] #Banda inferior
        UP = lista_precios[dato] #Ultimo Precio

        if UP > BS:
            print(f"Moneda:{moneda} --> Esta por encima de la banda de bollinger")
        elif UP < BI:
            print(f"Moneda:{moneda} --> Esta por debajo de la banda de bollinger")
        else:
            pass


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

while True:
    # Si ha pasado la duración del ciclo, salir del ciclo
    funcion_comparacion(['BTCUSDT', 'XLMUSDT', 'ETHUSDT','EOSUSDT'])
    print("Comparando nuevamente")
    tiempo_inicial = time.time()

    # Pausar la ejecución del programa durante un segundo
    time.sleep(15) #TODO cambiar a 60 s cuando ya vaya a dejarse funcionando