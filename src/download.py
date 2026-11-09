"""Download NQ 1-minute bars from Databento, one year at a time.

Per Dr. Rubin's plan: pull 1 year -> check remaining credit -> repeat.
Every run prints the cost of each year first; nothing is billed without --download.

    python src/download.py 2023 2024 2025            # cost check only
    python src/download.py 2023 --download           # fetch one year

Needs DATABENTO_API_KEY in the environment or in a .env file at the repo root.
Raw files are saved untouched as data/raw/NQ_ohlcv-1m_<year>.dbn.zst so the
study can be re-run from the exact bytes Databento sent.
"""
import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

import databento as db

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def load_key() -> str:
    for env in (ROOT / ".env.local", ROOT / ".env"):
        if not env.exists():
            continue
        for line in env.read_text().splitlines():
            k, _, v = line.partition("=")
            if k.strip() == "DATABENTO_API_KEY" and v.strip():
                os.environ.setdefault("DATABENTO_API_KEY", v.strip().strip('"'))
    key = os.getenv("DATABENTO_API_KEY")
    if not key:
        sys.exit("DATABENTO_API_KEY not set (env var, .env.local or .env).")
    return key


def year_range(year: int) -> tuple[str, str]:
    # Start Dec 31 of the prior year so the first Asia session (20:00 ET the
    # evening before) of the year is included. Overlap between files is
    # de-duplicated when loading.
    start = f"{year - 1}-12-31"
    end = min(dt.date(year + 1, 1, 1), dt.date.today()).isoformat()
    return start, end


SPEND_LOG = ROOT / "data" / "spend_log.json"


def spent_so_far() -> float:
    if not SPEND_LOG.exists():
        return 0.0
    return sum(e["cost"] for e in json.loads(SPEND_LOG.read_text()))


def record_spend(year: int, cost: float, params: dict) -> None:
    log = json.loads(SPEND_LOG.read_text()) if SPEND_LOG.exists() else []
    log.append({"year": year, "cost": round(cost, 4), "when": dt.datetime.now().isoformat(timespec="seconds"),
                "start": params["start"], "end": params["end"], "symbol": params["symbols"][0]})
    SPEND_LOG.parent.mkdir(parents=True, exist_ok=True)
    SPEND_LOG.write_text(json.dumps(log, indent=2))


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("years", nargs="+", type=int)
    p.add_argument("--download", action="store_true", help="actually fetch (billed)")
    args = p.parse_args()

    client = db.Historical(load_key())
    out_dir = ROOT / config.RAW_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    total = 0.0
    for year in args.years:
        start, end = year_range(year)
        params = dict(dataset=config.DATASET, symbols=[config.SYMBOL], schema=config.SCHEMA,
                      stype_in=config.STYPE_IN, start=start, end=end)
        cost = client.metadata.get_cost(**params)
        size = client.metadata.get_billable_size(**params)
        total += cost
        print(f"{year}: {start} -> {end}  est. ${cost:.2f}  ({size / 1e6:.1f} MB)")

        if args.download:
            path = out_dir / f"NQ_{config.SCHEMA}_{year}.dbn.zst"
            if path.exists():
                print(f"  already have {path.name}, skipping")
                continue
            spent = spent_so_far()
            if cost > config.MAX_PER_REQUEST:
                sys.exit(f"  REFUSED: ${cost:.2f} is over MAX_PER_REQUEST (${config.MAX_PER_REQUEST:.2f}).")
            if spent + cost > config.MAX_TOTAL_SPEND:
                sys.exit(f"  REFUSED: would bring total to ${spent + cost:.2f}, over "
                         f"MAX_TOTAL_SPEND (${config.MAX_TOTAL_SPEND:.2f}). Free credit is $125.")
            client.timeseries.get_range(**params, path=str(path))
            record_spend(year, cost, params)
            print(f"  saved {path.relative_to(ROOT)}  (total spent: ${spent + cost:.2f} "
                  f"of ${config.MAX_TOTAL_SPEND:.2f} cap)")

    print(f"Total est. ${total:.2f}   Already spent per log: ${spent_so_far():.2f}")
    if not args.download:
        print("Cost check only. Check your remaining credit in the Databento portal, "
              "then re-run with --download.")


if __name__ == "__main__":
    main()
