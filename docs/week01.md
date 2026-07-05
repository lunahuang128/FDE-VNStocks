# Week 1 — Docker, AWS bootstrap, first data

## Docker

- **Image vs container:** an image is a frozen recipe + filesystem; a
  container is one live run of it. Each `docker run` gets a fresh
  hostname (the container ID) — saw this directly in the hello output.
- **"Works on my machine" in action:** `main.py` ran fine locally but
  crashed in `python:3.12-slim` with `ZoneInfoNotFoundError`. Slim
  images strip the OS timezone database. Fix: `pip install tzdata`.
  Lesson: the container only has what you put in it.
- **Layer caching:** copying `requirements.txt` and installing *before*
  copying code means editing code skips the pip step (`CACHED` in the
  build output). Order of Dockerfile lines = rebuild speed.

## AWS

- New account on the **free plan**: $200 credits (signup + all 5
  activities). Hard deadline: **free plan auto-closes Jan 04, 2027** —
  calendar reminders set for ~Nov 16 (Week 20: upgrade to paid) and
  Dec 15 (backstop).
- Root user: MFA on, then locked away. Daily work happens as an IAM
  admin user (also MFA). Region pinned to **us-east-1**.
- **No access keys created** — deferred until Week 14 (GitHub OIDC),
  so there are no long-lived credentials to leak.
- $5 monthly budget alarm live. End-of-session sweep ritual: EC2
  instances → EBS volumes → Elastic IPs → RDS databases → RDS
  snapshots → Lambda. Resource Explorer turned on as a cross-region
  search backup.

## Data field notes — vnstock smoke test (2026-07-05)

- **Library:** vnstock 4.x. The `Vnstock` class and old methods are
  deprecated (Aug 2025) — new code must use `vnstock.api` modules
  (e.g. `vnstock.api.quote.Quote`). Migration planned for the Week 2
  ingest CLI.
- **REE:** 6,310 daily rows, 2000-07-28 → 2026-07-03. First close 0.40
  vs latest 48.80 → prices are **adjusted** for corporate actions and
  quoted in **thousands of VND**.
- **VNINDEX:** only 2004-01-05 onward from the VCI source (5,598
  rows). "From inception (2000)" is not available here. **Open
  question:** find another source for 2000–2003 or accept 2004+.
- **Funds:** fmarket now lists **65 open-ended funds** (plan assumed
  ~41 — the market grew). Listing includes fund type (equity/bond)
  and legacy codes (e.g. DCDS was VFMVF1).
- **SSISCA NAV:** 2,163 rows, 2014-09-26 → 2026-07-03. First NAV is
  exactly 10,000.00 — Vietnamese funds launch at 10,000 VND/unit.
- **T+1 check:** pulled on a Sunday, so Friday's NAV was already in.
  Re-verify on a weekday evening (expect prices for today, NAV only
  through yesterday).
- **Flakiness/limits:** free tier prints deprecation banners + ads on
  every call and advertises paid tiers with higher rate limits →
  assume rate limiting exists. Ingest design needs retries, backoff,
  and quiet logging from day one.

## Decisions

- Public repo. Safe because the vnstock license concern is about
  redistributing *data*, and `data/` is gitignored — verified in
  SourceTree that no CSVs were stageable.
- Monorepo layout: `/infra`, `/services`, `/pipelines`, `/docs`.
- Branch protection on `main`: PRs required, zero approvals (solo),
  no admin bypass.

## Next week

- Rewrite the smoke test as a containerized ingest CLI using the new
  `vnstock.api` interface.
- Decide the VNINDEX 2000–2003 approach.
- Scope all fund work to the full 65-fund listing.