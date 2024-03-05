import pandas as pd
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from scipy.interpolate import interp1d
import numpy as np


def fix_leg_valuation(notional, fix_rate, years, df_usd):
    today = date.today()
    df = pd.DataFrame(
        columns=[
            "dtm",
            "start_date",
            "end_date",
            "btw_days",
            "notional",
            "amortization",
            "interest",
            "cashflow",
            "df",
            "pv",
        ]
    )
    for i in range(years):
        if i == 0:
            df.loc[i, "start_date"] = today
        else:
            df.loc[i, "start_date"] = df.loc[i - 1, "start_date"] + relativedelta(
                years=1
            )  # type:ignore

        df.loc[i, "end_date"] = df.loc[i, "start_date"] + relativedelta(
            years=1
        )  # type:ignore
        df.loc[i, "btw_days"] = (
            df.loc[i, "end_date"] - df.loc[i, "start_date"]
        ).days  # type:ignore
        df.loc[i, "dtm"] = (df.loc[i, "end_date"] - today).days  # type:ignore
    for i in range(years):
        if i == df.index[-1]:
            df.loc[i, "amortization"] = notional
        else:
            df.loc[i, "amortization"] = 0
    for i in range(years):
        if i == 0:
            df.loc[i, "notional"] = notional
        else:
            df.loc[i, "notional"] = (
                df.loc[i - 1, "notional"] - df.loc[i - 1, "amortization"]  # type:ignore
            )
    for i in range(years):
        df.loc[i, "interest"] = (
            df.loc[i, "notional"] * fix_rate * df.loc[i, "btw_days"] / 360
        )
        df.loc[i, "cashflow"] = (
            df.loc[i, "amortization"] + df.loc[i, "interest"]
        )  # type:ignore
    for i in range(years):
        if df.loc[i, "dtm"] <= 0:  # type:ignore
            pass
        else:
            df.loc[i, "df"] = (
                interp1d(df_usd["days"], df_usd["df"])(df.loc[i, "dtm"]) * 1
            )
    for i in range(years):
        df.loc[i, "pv"] = df.loc[i, "cashflow"] * df.loc[i, "df"]  # type:ignore

    return df


def float_leg_valuation(df):
    df["notional"] = df["notional"].apply(lambda x: -x)
    df["amortization"] = df["amortization"].apply(lambda x: -x)

    df["reset_rate"] = np.nan
    df["interest"] = np.nan
    df["cashflow"] = np.nan
    df["pv"] = np.nan

    # Reordeno las columnas
    df = df[
        [
            "dtm",
            "start_date",
            "end_date",
            "btw_days",
            "notional",
            "amortization",
            "reset_rate",
            "interest",
            "cashflow",
            "df",
            "pv",
        ]
    ]

    # Identifico el cupón vigente
    vig_dtm = df.loc[df["dtm"] > 0, "dtm"].min()

    for i in df.index:
        if df.loc[i, "dtm"] == vig_dtm:
            df.loc[i, "reset_rate"] = (
                (((1 / df.loc[i, "df"]) / (1 / 1)) - 1) * 360 / df.loc[i, "btw_days"]
            )
        else:
            df.loc[i, "reset_rate"] = (
                (((1 / df.loc[i, "df"]) / (1 / df.loc[i - 1, "df"])) - 1)
                * 360
                / df.loc[i, "btw_days"]
            )
    for i in df.index:
        df.loc[i, "interest"] = (
            df.loc[i, "notional"]
            * df.loc[i, "reset_rate"]
            * df.loc[i, "btw_days"]
            / 360
        )
    for i in df.index:
        df.loc[i, "cashflow"] = df.loc[i, "amortization"] + df.loc[i, "interest"]
        df.loc[i, "pv"] = df.loc[i, "cashflow"] * df.loc[i, "df"]

    return df
