# fde-vnstock ingest

A containerized command-line tool that pulls Vietnamese market data from the
[vnstock](https://vnstocks.com) library and writes one CSV per symbol:

- **prices** — daily end-of-day prices for HOSE-listed stocks
- **index** — daily history for a market index (e.g. VN-Index)
- **funds** — NAV history for fmarket open-ended funds

Data is fetched from unofficial brokerage APIs, so the tool is built to
tolerate failure: each fetch retries with exponential backoff, and there is a
short pause between symbols to respect free-tier rate limits.

## Requirements

Only **Docker**. No local Python or virtualenv needed to run the image.

## Build

From this directory (`pipelines/ingest/`):

```bash
docker build -t fde-vnstock/ingest:0.2.0 .
```

## Run

The container writes CSVs to `/data` inside itself; mount a host folder there
so the files land on your machine. All dates are `YYYY-MM-DD` in ICT.

```bash
# Stock EOD prices (one CSV per symbol) -> ./data/prices/*.csv
docker run --rm -v "$PWD/data:/data" fde-vnstock/ingest:0.2.0 \
    prices --symbols REE,FPT --start 2024-01-01 --out /data

# Market index history -> ./data/index/VNINDEX.csv
docker run --rm -v "$PWD/data:/data" fde-vnstock/ingest:0.2.0 \
    index --symbol VNINDEX --start 2024-01-01 --out /data

# Fund NAV history -> ./data/funds/*.csv
docker run --rm -v "$PWD/data:/data" fde-vnstock/ingest:0.2.0 \
    funds --symbols SSISCA,VESAF --out /data
```

Run with no arguments to see the help text:

```bash
docker run --rm fde-vnstock/ingest:0.2.0
```

## Flags

| subcommand | flag        | default        | notes                                   |
|------------|-------------|----------------|-----------------------------------------|
| prices     | `--symbols` | *(required)*   | comma-separated tickers, e.g. `REE,FPT` |
|            | `--start`   | `2000-01-01`   | start date                              |
|            | `--end`     | today (ICT)    | end date                                |
|            | `--out`     | `./data`       | output folder                           |
| index      | `--symbol`  | `VNINDEX`      | index symbol                            |
|            | `--start`   | `2004-01-05`   | VCI VN-Index history begins here        |
|            | `--end`     | today (ICT)    | end date                                |
|            | `--out`     | `./data`       | output folder                           |
| funds      | `--symbols` | *(required)*   | comma-separated fund codes              |
|            | `--out`     | `./data`       | output folder                           |

## Known quirks (see `docs/week-02.md` for the full log)

- VCI ignores `--start` at the margin — it may return a little more history
  than requested.
- Price/index data uses a `time` column; fund NAV data uses a different date
  column name.
- `funds` re-fetches the full 65-fund listing on every call (a Phase 4
  optimization target).
- The free tier prints a notice/ad banner to stdout that cannot be suppressed.