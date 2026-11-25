# The World in One Image — 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/ramdanromandany94/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/ramdanromandany94/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

One page, one day, the whole world: a single 1024×1024 newspaper front page
summing up the world news of **Wednesday, 25 November 2026**.

Entry for the [news-image-20261125 bounty](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) on make.fun.
Want to try it yourself? [Join make.fun with my referral link](https://make.fun/r/hxd0fhbx).

## What's on the page

**Hero — Pakistan reaches orbit.** China's Shenzhou-24 docks at the
Tiangong space station carrying Muhammad Zeeshan Ali, the first foreign
astronaut ever to fly aboard a Chinese crew mission. Launched 08:18, docked
11:56, Jiuquan, China. (Reuters, AP)

**The grid:**

- **Indonesia** — Three dead as a flood traps 26 in a gold mine: rescuers pull
  three bodies from a 100-metre shaft in Bogor, West Java, after a river
  bursts into an illegal mine; 23 men remain trapped. (Reuters, AP)
- **Colombia** — All hostages freed in the Cartagena siege: troops storm an
  Exito supermarket after a day-long standoff and rescue every remaining
  captive; one kidnapper killed, four arrested. (Reuters, AFP)
- **Bangladesh** — Garment pay rises 36% to 17,000 taka: Dhaka lifts the
  minimum wage for four million garment workers after weeks of protests that
  shut factories — the smallest rise in more than a decade. (Reuters)
- **North Korea** — Pyongyang expels the Swiss envoy in 48 hours: the regime
  orders Switzerland's diplomatic office shut in a row over sanctions on a
  children's camp. (Reuters, KCNA)

**Also today:** a US jury convicts Huawei on 10 of 12 counts; Anthropic
shares slide further below the $83 IPO price; the Houthis claim fresh strikes
on a Saudi oil refinery and Riyadh's financial district; Zelensky says Ukraine
needs €115bn in outside financing for 2027.

## How it's made

`tools/render.py` draws the whole front page from scratch with PIL only —
masthead, hero panel with a hand-drawn rocket, the 2×2 story grid and the
"Also Today" strip. No photos, no downloaded assets, no copied code.

```sh
python3 tools/render.py   # writes entry.png (1024x1024, PNG)
```

`main.ts` (Node 22, stdlib only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png`. It resolves the image grader-safely:
`$MAKEFUN_INPUT_DIR`, then `$MAKEFUN_BOT_DIR`, then the directory this file
lives in, then the working directory — so it works even when the grader runs
`node /bot/main.ts` with no input dir set and a different cwd.

## License

MIT — see [LICENSE](LICENSE).
