# fde-vnstock

Self-hosted analytics for the Vietnamese stock market — HOSE end-of-day
prices, VNINDEX history, and open-ended fund NAVs — served through
[Metabase](https://www.metabase.com/) on AWS.

Data is pulled daily with the [vnstock](https://vnstocks.com) Python library.

## Layout

| Folder | Purpose |
|---|---|
| `infra/` | Terraform / AWS infrastructure |
| `services/` | Long-running services (ingest CLI, API, Metabase) |
| `pipelines/` | Batch & streaming data pipelines |
| `docs/` | Decisions, runbooks, weekly build notes |

## Data & licensing

Market data comes from vnstock, which is licensed for **personal and
research use**. Raw data is never committed to this repo (`data/` is
gitignored) and the deployed app is login-gated — this project publishes
architecture and code, not data.

## Status

🚧 Early days — Week 1 of a 30-week solo build (Docker fundamentals, AWS
bootstrap, vnstock smoke test). Nothing runnable yet; first shippable
container lands in Week 2.

Planned stack: Docker · FastAPI · Postgres · Terraform · AWS (ECS, RDS,
Lambda) · Redpanda · ClickHouse · Dagster · dbt · Metabase

## Domain notes

Vietnamese-market quirks handled throughout: ICT timestamps
(`Asia/Ho_Chi_Minh`), the HOSE trading calendar incl. Tết holidays, ±7%
daily price limits, adjusted vs. raw prices, and T+1 fund NAV publication.
Details in [`docs/`](docs/).