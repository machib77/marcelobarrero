format_dict = {
    "notional": "{:,.0f}",
    "amortization": "{:,.0f}",
    "interest": "{:,.2f}",
    "cashflow": "{:,.2f}",
    "df": "{:,.4f}",
    "pv": "{:,.2f}",
    "start_date": lambda x: x.strftime("%d-%m-%y"),
    "end_date": lambda x: x.strftime("%d-%m-%y"),
}

table_style_list = [
    {
        "selector": "td",
        "props": [
            ("text-align", "right"),
            ("border", "1px solid #959595"),
            ("color", "#CF822A"),
        ],
    },
    {
        "selector": "th",
        "props": [
            ("text-align", "right"),
            ("border", "1px solid #959595"),
            ("background-color", "#212121"),
            ("color", "#8B8B8B"),
            ("text-align", "center"),
        ],
    },
    {"selector": "tr:nth-child(odd)", "props": [("background-color", "#141414")]},
    {"selector": "tr:nth-child(even)", "props": [("background-color", "#212121")]},
]

format_dict_float = {
    "notional": "{:,.0f}",
    "amortization": "{:,.0f}",
    "interest": "{:,.2f}",
    "cashflow": "{:,.2f}",
    "df": "{:,.4f}",
    "pv": "{:,.2f}",
}


def format_number(number):
    formatted_number = "{:,.2f}".format(number)
    return formatted_number
