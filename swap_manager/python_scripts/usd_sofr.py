import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

from dateutil.relativedelta import relativedelta
from datetime import timedelta, date

curve_defaults = {
    "1D": 5.31,
    "1W": 5.32,
    "2W": 5.33,
    "3W": 5.34,
    "1M": 5.35,
    "2M": 5.36,
    "3M": 5.38,
    "4M": 5.39,
    "5M": 5.37,
    "6M": 5.35,
    "7M": 5.32,
    "8M": 5.29,
    "9M": 5.25,
    "10M": 5.22,
    "11M": 5.18,
    "1Y": 5.14,
    "1.5Y": 4.80,
    "2Y": 4.55,
    "3Y": 4.24,
    "4Y": 4.09,
    "5Y": 4.02,
    "6Y": 3.98,
    "7Y": 3.97,
    "8Y": 3.96,
    "9Y": 3.96,
    "10Y": 3.97,
    "12Y": 3.99,
    "15Y": 4.01,
    "20Y": 3.99,
}

swap_defaults = {
    "notional": 10000000,
    "fix-rate": 4.0165,
    "flow-years": 5,
}


def discount_usd_sofr(rate_dict):
    today = date.today()
    today_str = today.strftime("%Y-%m-%d")

    # Creo un diccionario con las fechas de vencimiento de cada swap
    end_date = {}
    for key in rate_dict.keys():
        if key == "1D":
            end_date[key] = today + relativedelta(days=1)
        elif key == "1.5Y":
            end_date[key] = today + relativedelta(months=18, days=2)
        elif "W" in key:
            weeks = int(key.strip("W"))
            end_date[key] = today + relativedelta(weeks=weeks, days=2)
        elif "M" in key:
            months = int(key.strip("M"))
            end_date[key] = today + relativedelta(months=months, days=2)
        elif "Y" in key:
            years = int(key.strip("Y"))
            end_date[key] = today + relativedelta(years=years, days=2)

    # Creo un diccionario con los Days to Maturity
    days_to_mat = {}
    for key in end_date.keys():
        days_to_mat[key] = (end_date[key] - today).days

    # Los junto en un dataframe
    df = pd.DataFrame.from_dict(rate_dict, orient="index", columns=["spot_rate"])
    df["end_date"] = end_date.values()
    df["dtm"] = days_to_mat.values()

    # Preparo primero la parte corta
    short_end = df.iloc[:16, :].copy(deep=True)
    short_end["df"] = 1 / (
        1 + ((short_end[short_end.columns[0]] * short_end["dtm"]) / 36000)
    )

    # Para la parte larga, creo un diccinario anual que tiene de keys los dtm y de value su tasa spot interpolada correspondiente
    spot_date = []
    for i in range(20):
        spot_date.append(today + relativedelta(months=((12 * i) + 12), days=2))
    spot = {}
    for i in spot_date:
        spot[(i - today).days] = (
            interp1d(df["dtm"], df[df.columns[0]])((i - today).days) * 1
        )

    # Creo una lista para las fechas de inicio
    spot_date_start = []
    spot_date_start.append(today + relativedelta(days=2))
    for i in spot_date[:-1]:
        spot_date_start.append(i)

    # Creo una lista donde calculo los between days act/360
    btw_days = []
    for i, j in zip(spot_date_start, spot_date):
        btw_days.append((j - i).days)

    # Creo una lista donde calculo la fracción del año (act/360)
    act_360 = []
    for i in btw_days:
        act_360.append(i / 360)

    #######################################################
    # Creo un dataframe a partir de ese diccionario
    long_end = pd.DataFrame(spot.items(), columns=["days", "spot_rates"])
    long_end.set_index(["days"], inplace=True)
    long_end["btw_days"] = btw_days

    # Creo una lista del cupon para el cual ya tengo su factor de descuento calculado y agrego los fd a long_list
    short_list = long_end.index[:1].tolist()
    for i in short_list:
        long_end.loc[i, "df"] = interp1d(short_end["dtm"], short_end["df"])(i)

    # Creo una lista de los dias a los que todavía me falta calcular sus factores de descuento
    long_list = long_end.index[1:].tolist()
    # Agrego la columna de la fracción de año para cada fecha
    long_end["act/360"] = act_360

    ################################################

    # Bootstrapping: Calculo los factores de descuento de la parte larga
    # 1 = C1*FD1 + C2*FD2 + C3*FD3 + C4*FD4 + 1*FD4, donde:
    # Despejando FD4 y simplificando me da:
    # FDn = (1-(tasa[n]*(act/360[1]+act/360[2]+act/360[3]+...+act/360[n-1])))*
    #       (1/(1+(tasa[n]*act/360[n])))

    # Creo una lista que contiene los valores ya resueltos de la parte corta (en los tramos donde ya tengo calculados los FD)
    iter_list = long_end.index[:1].tolist()

    # Creo una variable donde iré almacenando temporalmente la
    # suma de la multiplicación de los act/360 * FD anteriores
    x = 0

    # Creo un loop que almacena los FD en el dataframe
    # La lógica de los loops y las listas es que la lista inter_list parte inicialmente con tres valores y a medida que se van guardando el nuevo FD, se aumenta un elemento en ésta lista.
    # El loop interior multiplica los act/360 * FD y los suma; y, a partir de eso saco el FD nuevo
    # La siguiente iteración del loop exterior hara que el loop interior itere con un elemento mas en la lista iter_list que la vez anterior.

    for j in long_list:
        for i in iter_list:
            x += long_end.loc[i, "act/360"] * long_end.loc[i, "df"]  # type:ignore

        long_end.loc[j, "df"] = (
            1 - (long_end.loc[j, "spot_rates"] / 100 * x)  # type:ignore
        ) * (
            1
            / (
                1
                + (
                    long_end.loc[j, "spot_rates"]  # type:ignore
                    / 100
                    * long_end.loc[j, "act/360"]
                )
            )
        )

        x = 0
        iter_list.append(j)
    #####################################################################
    # Añado en un nuevo dataframe los tenors de la parte corta que faltan

    df_usd_sofr = long_end[["spot_rates", "df"]].copy(deep=True)

    short_list = [
        "1D",
        "1W",
        "2W",
        "3W",
        "1M",
        "2M",
        "3M",
        "4M",
        "5M",
        "6M",
        "7M",
        "8M",
        "9M",
        "10M",
        "11M",
    ]

    for i in short_list:
        df_usd_sofr.loc[short_end.loc[i, "dtm"]] = [  # type:ignore
            short_end.loc[i, df.columns[0]],
            short_end.loc[i, "df"],
        ]

    # Para añadir 0D
    df_usd_sofr.loc[0, "spot_rates"] = short_end.loc["1D", df.columns[0]]
    df_usd_sofr.loc[0, "df"] = 1

    df_usd_sofr.sort_index(inplace=True)
    df_usd_sofr["date"] = df_usd_sofr.index.to_series().apply(
        lambda x: today + timedelta(days=x)
    )

    return df_usd_sofr
