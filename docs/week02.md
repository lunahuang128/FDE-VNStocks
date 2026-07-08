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

