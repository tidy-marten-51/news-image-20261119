# The World in One Day — 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/tidy-marten-51/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/tidy-marten-51/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Built for make.fun's [news-image-20261119 bounty](https://make.fun/bounty/news-image-20261119) — sum up 19 November's world news in one image, $250 in USDC.

An entry for make.fun's `news-image-20261119`: one image that sums up the
world news of Thursday, 19 November 2026, laid out as a newspaper front page.

## What the image shows

- **Lead — China / trilateral summit:** Trump, Xi and Putin sit down in
  Shenzhen for APEC talks, with Xi meeting Putin first; Ukraine, trade and
  the Gulf top the agenda.
- **Middle East / Gulf:** Three oil tankers catch fire after hitting mines
  east of the Strait of Hormuz, as the US-Iran exchange of fire widens and
  Gulf states repel drone attacks.
- **Culture / games:** GTA VI launches worldwide to near-perfect reviews;
  gamers flood Vice City as Rockstar's blockbuster begins its global rollout
  after a 13-year wait.
- **Also on 19 November 2026:** the World Court rules on Myanmar's Rohingya
  genocide case, NASA's Voyager 1 probe reaches a light-day from Earth, the
  EU proposes a €45 billion Ukraine loan to be repaid from Russian
  reparations, and Hakeem Jeffries is set to become the first Black Speaker
  of the US House.

The date is named three times — masthead, "Also on" strip, footer — so the
day the image sums up is unmistakable.

## How it is built

`draw_frontpage.py` (Python 3, Pillow, DejaVu fonts) composes the page from
three press-style illustrations in `assets/` and the headlines above, and
writes `entry.png` (1024×1024, under the 1 MiB cap). Rebuild it with:

```sh
python3 draw_frontpage.py
```

## How it runs

`main.py` (Python 3.13, standard library only) validates `entry.png`
against the competition gate — a whole PNG, at most 1 MiB, at most
1024×1024 — and copies it byte for byte to `/output/entry.png`
(`MAKEFUN_OUTPUT_DIR` stands in for `/output` outside the grader):

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Two runs write identical bytes; no network is used at runtime.

## License

MIT — see `LICENSE`.
