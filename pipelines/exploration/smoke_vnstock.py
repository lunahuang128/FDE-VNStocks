from pathlib import Path
from vnstock import Vnstock
from vnstock.explorer.fmarket.fund import Fund

# repo-root/data/ — gitignored, data never enters git
DATA = Path(__file__).resolve().parents[2] / "data"
DATA.mkdir(exist_ok=True)

def describe(name, df):
    print(f"\n=== {name}: {df.shape[0]} rows x {df.shape[1]} cols ===")
    print(df.head(3))
    print(df.tail(3))

# 1. REE daily prices — one of HOSE's first two stocks (July 28, 2000)
stock = Vnstock().stock(symbol="REE", source="VCI")
ree = stock.quote.history(start="2000-07-28", end="2026-07-05", interval="1D")
describe("REE EOD", ree)
ree.to_csv(DATA / "ree_eod.csv", index=False)

# 2. VNINDEX — the market index, same start date
index = Vnstock().stock(symbol="VNINDEX", source="VCI")
vni = index.quote.history(start="2000-07-28", end="2026-07-05", interval="1D")
describe("VNINDEX", vni)
vni.to_csv(DATA / "vnindex.csv", index=False)

# 3. Funds — list them all, then one fund's NAV history
fund = Fund()
funds = fund.listing()
describe("Fund listing", funds)
funds.to_csv(DATA / "fund_listing.csv", index=False)

nav = fund.details.nav_report("SSISCA")
describe("SSISCA NAV", nav)
nav.to_csv(DATA / "ssisca_nav.csv", index=False)

print("\nCSVs written to:", DATA)