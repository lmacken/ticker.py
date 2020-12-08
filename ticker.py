"""
ASCII Price Ticker.

SPDX-License-Identifier: GPL-3.0-only

TODO:
- Write a ticker API to easily make single-line scrolling feeds from any data
  source.  Weather, Air Quality Index, Hacker News headlines, etc.
- Handle lines going at different speeds & directions
- hook into currently playing song if spotifyd is running
    - scrolling lyrics
    - ASCII EQ effects
- colorized prices based on direction
- ascii sparklines to show volume over time

"""
import requests
import time
import datetime
import shutil

import art

PRICE_URL = "https://api.pro.coinbase.com/products/{}/ticker"


def out(s):
    print(s.center(shutil.get_terminal_size().columns))


def get_price(symbol="BTC-USD"):
    try:
        result = requests.get(PRICE_URL.format(symbol)).json()
        price = float(result["price"])
        return price
    except Exception as e:
        return str(e)


def print_price():
    price = get_price()
    nmr_price = get_price("NMR-USD")
    eth_price = get_price("ETH-USD")
    if not price:
        print("! Unable to fetch price")
        time.sleep(60)
        return

    # Clear the line
    print("\033c", end="")

    # Date & Time
    now = datetime.datetime.now()
    now_date_str = art.text2art(
        now.strftime("%m/%d/%y") + " " + now.strftime("%H:%M"),
        font="fancy5",
        decoration="barcode1",
    )
    out(f"{now_date_str}")

    # Price
    print("\n\n\n\n")
    price_art = "₿itcoin\n" + art.text2art(f"${price:,.2f}")
    for line in price_art.split("\n"):
        out(line)
    print("\n")

    out(f"${nmr_price:,.2f} NMR | ${eth_price:,.2f} ETH")
    print("\n")

    # Random emoji second ticker
    buf = ""
    rndart = art.art("random")
    rndart_orig = rndart  # .copy()?
    num_cols = shutil.get_terminal_size().columns
    rndart_len = len(rndart_orig)
    init = True  # not fully showing art

    for i in range(num_cols + rndart_len):
        # handle scrolling in
        if i < rndart_len:
            rndart = rndart_orig[-i-1:]
        else:
            if init:
                init = False
                rndart = rndart_orig
                buf += " "

        # scrolling out
        if len(buf + rndart) > num_cols:
            rndart = rndart[:-1]

        print(buf + rndart, end="\r")
        time.sleep(1)

        if not init:
            buf += " "

        print("\033[A")


while True:
    try:
        print_price()
    finally:
        pass
