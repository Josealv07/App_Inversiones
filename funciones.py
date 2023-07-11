import pandas as pd
import time


def calcular_bollinger_bands(precios, dias=20, k=2):
    # Convertir la lista de precios a una serie de Pandas
    precios = pd.Series(precios)

    # Calcular la media móvil de los precios
    sma = precios.rolling(window=dias).mean()

    # Calcular la desviación estándar de los precios
    std = precios.rolling(window=dias).std()

    # Calcular las bandas de Bollinger superior e inferior
    upper_band = sma + (k * std)
    lower_band = sma - (k * std)

    # Devolver un DataFrame con las bandas de Bollinger y la media móvil
    return pd.DataFrame({'Precio': precios, 'Media Móvil': sma, 'Banda Superior': upper_band, 'Banda Inferior': lower_band})





def estrecho(BS,BI,moneda):
    parametros = {'BTCUSDT':0.0375, 'XLMUSDT':0.2, 'ETHUSDT':0.2,'EOSUSDT':0.2}
    margen = (BS/BI)-1
    if margen <= parametros[moneda]:
        return True
    else:
        return False
    