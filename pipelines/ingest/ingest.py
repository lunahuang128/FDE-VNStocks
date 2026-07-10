"""fde-vnstock ingest CLI.

Pulls Vietnamese market data (stock EOD prices, the VN-Index, and open-ended
fund NAV history) from the vnstock library and writes one CSV per symbol.

This is Week 2 Session A: a plain command-line tool, no Docker yet. Run it
inside your Week-1 virtualenv:

    python ingest.py prices --symbols REE,FPT --start 2000-07-28 --out ./data
    python ingest.py index  --symbol VNINDEX  --start 2004-01-05 --out ./data
    python ingest.py funds  --symbols SSISCA,VESAF          --out ./data
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

# vnstock v4 unified API. These are the imports your Week-1 smoke test proved
# work; the old `Vnstock` class is deprecated, so we use the api modules.
from vnstock.api.quote import Quote
from vnstock.explorer.fmarket.fund import Fund

# --- constants ---------------------------------------------------------------

# Every timestamp in this project is Ho Chi Minh City time (UTC+7). "today"
# always means today in ICT, never the machine's local zone or UTC.
ICT = ZoneInfo("Asia/Ho_Chi_Minh")

# vnstock's free tier is rate-limited. These control our polite retry loop.
MAX_TRIES = 3          # give each fetch up to 3 attempts before giving up
BASE_SLEEP = 2.0       # seconds; doubles each retry: 2s -> 4s -> 8s
PAUSE_BETWEEN = 1.0    # seconds to wait between symbols, to stay under limits


# --- retry helper ------------------------------------------------------------

def with_retry(label, fetch_fn):
    """Call fetch_fn(), retrying on any exception with exponential backoff.

    `label` is just a human-readable name for log messages (e.g. "REE").
    `fetch_fn` is a zero-argument function that does the actual network call
    and returns a DataFrame.
    """
    for attempt in range(1, MAX_TRIES + 1):
        try:
            return fetch_fn()
        except Exception as err:  # noqa: BLE001 - free API fails many ways
            if attempt == MAX_TRIES:
                # Out of attempts: re-raise so the caller can report the failure.
                raise
            wait = BASE_SLEEP * (2 ** (attempt - 1))  # 2, then 4, then 8
            print(
                f"  ! {label}: attempt {attempt} failed ({err}); "
                f"retrying in {wait:.0f}s",
                file=sys.stderr,
            )
            time.sleep(wait)


# --- fetch functions ---------------------------------------------------------
# Each returns a pandas DataFrame. This is the Week-1 smoke-test code, lifted
# into named functions so the CLI can call them in a loop.

def fetch_prices(symbol, start, end):
    """Daily EOD price history for one HOSE stock, from `start` to `end`."""
    quote = Quote(symbol=symbol, source="VCI")
    return quote.history(start=start, end=end, interval="1D")


def fetch_index(symbol, start, end):
    """Daily history for a market index (e.g. VNINDEX). Same call as a stock."""
    quote = Quote(symbol=symbol, source="VCI")
    return quote.history(start=start, end=end, interval="1D")


def fetch_fund_nav(symbol):
    """Full NAV-per-unit history for one fmarket open-ended fund."""
    fund = Fund()
    return fund.details.nav_report(symbol)


# --- output helper -----------------------------------------------------------

def write_csv(df, out_dir, subfolder, symbol):
    """Write `df` to <out_dir>/<subfolder>/<symbol>.csv and print field notes."""
    folder = Path(out_dir) / subfolder
    folder.mkdir(parents=True, exist_ok=True)  # make the folder if missing
    path = folder / f"{symbol}.csv"
    df.to_csv(path, index=False)

    # Field-note habit from Week 1: log rows + date range for every file.
    rows = len(df)
    date_span = ""
    if "time" in df.columns and rows:
        lo, hi = df["time"].min(), df["time"].max()
        date_span = f"   {lo} -> {hi}"
    print(f"  \u2713 {path}   {rows} rows{date_span}")


# --- subcommand handlers -----------------------------------------------------
# One function per subcommand. argparse hands each the parsed `args` object.

def cmd_prices(args):
    symbols = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
    for symbol in symbols:
        df = with_retry(symbol, lambda: fetch_prices(symbol, args.start, args.end))
        write_csv(df, args.out, "prices", symbol)
        time.sleep(PAUSE_BETWEEN)


def cmd_index(args):
    symbol = args.symbol.strip().upper()
    df = with_retry(symbol, lambda: fetch_index(symbol, args.start, args.end))
    write_csv(df, args.out, "index", symbol)


def cmd_funds(args):
    symbols = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
    for symbol in symbols:
        df = with_retry(symbol, lambda: fetch_fund_nav(symbol))
        write_csv(df, args.out, "funds", symbol)
        time.sleep(PAUSE_BETWEEN)


# --- argument parser ---------------------------------------------------------

def build_parser():
    """Assemble the argparse CLI: one parent parser + three subparsers."""
    today_ict = datetime.now(ICT).strftime("%Y-%m-%d")

    parser = argparse.ArgumentParser(
        prog="ingest",
        description="Pull Vietnamese market data from vnstock into CSV files.",
    )
    # `dest="command"` stores which subcommand was chosen; `required=True`
    # means running the tool with no subcommand is an error (prints help).
    sub = parser.add_subparsers(dest="command", required=True)

    # ---- prices ----
    p_prices = sub.add_parser("prices", help="daily EOD stock prices")
    p_prices.add_argument("--symbols", required=True,
                          help="comma-separated tickers, e.g. REE,FPT")
    p_prices.add_argument("--start", default="2000-01-01",
                          help="start date YYYY-MM-DD (default 2000-01-01)")
    p_prices.add_argument("--end", default=today_ict,
                          help="end date YYYY-MM-DD (default: today, ICT)")
    p_prices.add_argument("--out", default="./data",
                          help="output folder (default ./data)")
    p_prices.set_defaults(func=cmd_prices)  # link this subcommand to its handler

    # ---- index ----
    p_index = sub.add_parser("index", help="daily market-index history")
    p_index.add_argument("--symbol", default="VNINDEX",
                         help="index symbol (default VNINDEX)")
    p_index.add_argument("--start", default="2004-01-05",
                         help="start date YYYY-MM-DD (VCI VNINDEX from 2004-01-05)")
    p_index.add_argument("--end", default=today_ict,
                         help="end date YYYY-MM-DD (default: today, ICT)")
    p_index.add_argument("--out", default="./data",
                         help="output folder (default ./data)")
    p_index.set_defaults(func=cmd_index)

    # ---- funds ----
    p_funds = sub.add_parser("funds", help="open-ended fund NAV history")
    p_funds.add_argument("--symbols", required=True,
                         help="comma-separated fund codes, e.g. SSISCA,VESAF")
    p_funds.add_argument("--out", default="./data",
                         help="output folder (default ./data)")
    p_funds.set_defaults(func=cmd_funds)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)  # argv=None -> read from the real command line
    print(f"ingest: {args.command}  (started {datetime.now(ICT):%Y-%m-%d %H:%M %Z})")
    args.func(args)  # call the handler that set_defaults wired up
    print("ingest: done")


if __name__ == "__main__":
    # This block runs only when the file is executed directly (python ingest.py),
    # not when it's imported. Standard Python entry-point guard.
    main()

# adding some notes to test 