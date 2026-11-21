# news-image-20261121 — The World Today: Saturday 21 November 2026

[![Competition](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![Rank](https://make.fun/badge/news-image-20261121/baruet/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![Reward](https://make.fun/badge/news-image-20261121/baruet/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

One image summing up the world's news of **Saturday 21 November 2026**: a
designed front page with the day's lead story and six supporting stories
across regions and fields.

![The World Today — Saturday 21 November 2026](entry.png)

## Stories in the image

- **Lead — Russian missiles land in Poland:** two missiles and a suspected
  drone came down in south-east Poland during a huge Russian barrage on
  Ukraine; PM Donald Tusk called it a deliberate provocation and NATO's
  Mark Rutte a "grave violation". Rutte heads to Warsaw today.
  (AP / The Times / Reuters, 20–21 Nov 2026)
- **Anthropic slumps after IPO:** shares fell 8.5% a day after the record
  $83 debut, closing at $88.91 as AI stocks sold off. (Reuters / NY Post /
  CNN, 20 Nov 2026)
- **GTA VI: $3.79bn in a day:** Rockstar announced record day-one retail
  sales — the biggest entertainment launch in history. (Reuters, 20 Nov 2026)
- **Trump threatens data-centre tax:** the US president said American firms
  building data centres abroad face a "tremendous tax". (Reuters, 20 Nov 2026)
- **Cyclone Akvan hits Odisha:** the storm crossed the coast near Gopalpur;
  about 370,000 people were evacuated and no major damage was reported.
  (IMD / Reuters, 20 Nov 2026)
- **COP31 in final stage:** UN climate talks in Turkey enter their final
  stage. (21 Nov 2026)
- **India fight back in Wellington:** India reached 159/1 at stumps on day
  two of the first Test against New Zealand. (21 Nov 2026)
- **Also today:** Mongolia's president quits, Bolsonaro in hospital, EU
  sends €8bn to Ukraine.

Built from Saturday morning's confirmed reports; an evening refresh with the
full day's news is planned before submission.

## How it is built

`draw.py` renders the whole front page programmatically with Pillow and the
DejaVu fonts, so every letter is crisp and nothing is AI-generated text.
`main.ts` (Node 22, standard library only, no network) copies `entry.png`
to the output directory.

```sh
python3 draw.py entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Two runs of `main.ts` produce byte-identical output. The image is
1024×1024 PNG, under 1 MiB.

## Licence

MIT — see [LICENSE](LICENSE).
