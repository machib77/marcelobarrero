import pandas as pd
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from scipy.interpolate import interp1d


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
            df.loc[i, "df"] = interp1d(df_usd["days"], df_usd["df"])(df.loc[i, "dtm"])
    for i in range(years):
        df.loc[i, "pv"] = df.loc[i, "cashflow"] * df.loc[i, "df"]  # type:ignore

    return df
