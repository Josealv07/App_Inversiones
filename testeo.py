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
        price_df.close = pd.to_numeric(price_df.close)

        ##-------------------------------------------------------- extraemos lista con precios close-------------------------
        lista_precios = [ element for element in price_df['close']]


        while (len(lista_precios) <= 4800):
            time.sleep(3)
            candles = client.get_klines(symbol= moneda, interval=Client.KLINE_INTERVAL_1MINUTE, limit = 1)
            price_df = pd.DataFrame(candles, columns=['dateTime',
                                                    'open',
                                                    'high', 'low',
                                                    'close', 'volume',
                                                    'closeTime',
                                                    'quoteAssetVolume',
                                                    'numberOfTrades',
                                                    'takerBuyBaseVol',
                                                    'takerBuyQuoteVol', 'ignore'])
            price_df.close = pd.to_numeric(price_df.close)
            lista_precios.append(price_df['close'][0])
            #Dataframes_monedas[str(moneda) + '_df'] = lista_precios


            final1 = calcular_bollinger_bands(precios = lista_precios, dias = 1000, k = 1)

            dato = len(lista_precios) - 2
            print(f"Dato= {dato}")
            BS = final1["Banda Superior"][dato] #Banda superior
            print(f"BS= {BS}")
            BI = final1["Banda Inferior"][dato] #Banda inferior
            print(f"BI= {BI}")
            UP = lista_precios[-1] #Ultimo Precio
            print(f"UP= {UP}")

            """Encima = False
            Debajo = True

            if UP > BS:
                Encima=True
                print(f"Moneda:{moneda} --> Esta por encima de la banda de bollinger")
            elif UP < BI:
                Debajo=True
                print(f"Moneda:{moneda} --> Esta por debajo de la banda de bollinger")
            else:
                Encima=False
                Debajo=False
                pass

            PosicionAbierta = True
            if PosicionAbierta and (Encima or Debajo):
                pass


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