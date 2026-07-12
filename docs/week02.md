# Week 2 - Containerize the Ingest CLI

## API notes
- VCI VNINDEX ignores start at the margin — returned 2023-11-10 for a 2024-01-01 request
- Time column is a full timestamp (00:00:00), not a bare date

## Data ingestions:
-  ✓ data/index/VNINDEX.csv   659 rows   2023-11-10 00:00:00 -> 2026-07-07 00:00:00
-  ✓ data/prices/REE.csv   659 rows   2023-11-10 00:00:00 -> 2026-07-07 00:00:00
-  ✓ data/prices/FPT.csv   659 rows   2023-11-10 00:00:00 -> 2026-07-07 00:00:00
-  ✓ data/funds/SSISCA.csv   2165 rows
-  ✓ data/funds/VESAF.csv   1459 rows

## Docker Cache experiment
-  edit the python script (layer 5), rerun. [+] Building 1.6s (10/10). All layer 1-4 are cached
-  edit the requirement.txt (layer 3), rerun. [+] Building 38.0s (10/10). Rebuilding layers 3-5 
-  Editing code = only layer 5 rebuilds (1.6s) because pip install sits below it. Editing requirements = layers 3–5 rebuild (38s) because the install sits on top of the changed layer. Order deps before code so the common case (code edits) stays cheap

## Run observations
-  tzdata pin verified inside slim (no ZoneInfo error)
-  vnai shows different notices per version → pin justified
-  hit a VCI connect-timeout in-container; local worked → transient network, but flagged that vnstock may log errors without raising them, so with_retry didn't fire — revisit in W9

## MULTI-STAGE dockerization 
-  fde-vnstock/ingest            0.2.0     87282ef72db1   24 seconds ago   413MB
-  fde-vnstock/ingest            dev       0af566c306f3   36 minutes ago   410MB