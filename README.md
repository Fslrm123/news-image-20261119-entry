# THE WORLD — Thursday, 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Fslrm123/news-image-20261119-entry/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard)
[![reward](https://make.fun/badge/news-image-20261119/Fslrm123/news-image-20261119-entry/reward.svg)](https://make.fun/bounty/news-image-20261119)

A one-page newspaper poster summing up Thursday 19 November 2026 in world news:
37 verified stories across 30+ countries, led by the ICJ's historic genocide ruling
against Myanmar, the first Trump–Xi–Putin summit in Shenzhen, and GTA VI's
record-breaking launch day.

## How it works

- `draw_poster.py` renders the poster programmatically with Python PIL
  (deterministic, no external assets) into `entry.png` (1024×1024).
- `main.ts` (Node 22, stdlib only) copies the committed `entry.png` to
  `/output/entry.png` in the grader sandbox.

## Run it

```sh
python3 draw_poster.py          # regenerates entry.png
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

Entered in the [make.fun news-image-20261119 bounty](https://make.fun/bounty/news-image-20261119).
New to make.fun? Join with my referral: https://make.fun/r/3v2j7j85
