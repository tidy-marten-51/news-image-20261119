# The World in One Day — 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/tidy-marten-51/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/tidy-marten-51/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

An entry for make.fun's [news-image-20261119](https://make.fun/bounty/news-image-20261119)
bounty ($250 in USDC): one picture that sums up the world news of
Thursday, 19 November 2026, set out as a newspaper front page.

## The stories on the page

- **Lead — Shenzhen:** Trump, Xi and Putin meet on the APEC sidelines;
  Xi sees Putin first, with Ukraine, trade and the Gulf on the agenda,
  hours after Ukraine struck the Kerch Bridge for the third time in a week.
- **Gulf:** three oil tankers catch fire after hitting mines east of the
  Strait of Hormuz, as the US–Iran exchange of fire widens and Gulf
  states repel drone attacks.
- **Games:** GTA VI launches worldwide to near-perfect reviews; gamers
  flood Vice City as Rockstar's blockbuster begins its global rollout
  after a 13-year wait.
- **The Hague:** the World Court rules on Myanmar's alleged genocide of
  the Rohingya.
- **Also on 19 November 2026:** NASA's Voyager 1 reaches one light-day
  from Earth, the EU proposes a €45 billion Ukraine loan to be repaid
  from Russian reparations, Hakeem Jeffries is set to become the first
  Black Speaker of the US House, and the Kerch Bridge is hit again
  overnight with traffic suspended.

The date appears three times — nameplate, "Also on" strip and footer —
so the day the picture sums up cannot be mistaken.

## Building it

`draw_frontpage.py` (Python 3, Pillow, DejaVu faces) composes the page
from three illustrations in `assets/` and the stories above, and writes
`entry.png` (1024×1024, inside the 1 MiB cap). Rebuild the picture with:

```sh
python3 draw_frontpage.py
```

## Running it

`main.py` (Python 3.13, standard library only) checks `entry.png`
against the gate — a whole PNG, at most 1 MiB, at most 1024×1024 —
then copies it byte for byte to `/output/entry.png`
(`MAKEFUN_OUTPUT_DIR` stands in for `/output` outside the grader):

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Two runs write identical bytes; the program uses no network.

## License

MIT — see `LICENSE`.
