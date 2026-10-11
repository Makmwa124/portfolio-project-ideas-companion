"""Check that every dataset link in the project list still responds.

Usage (from the repository root):
    python scripts/check_links.py [projects/portfolio_projects.csv]

Prints one line per link and writes output/link_check.csv. A failure doesn't
always mean the dataset is gone: some sites block scripts or need a browser.
Search for the dataset name and publisher, and check the companion
repository for updated links.
"""
import csv
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HEADERS = {"User-Agent": "portfolio-project-ideas link checker (personal use)"}


def check(url, timeout=20):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, ""
    except urllib.error.HTTPError as e:
        return e.code, e.reason
    except Exception as e:  # timeouts, DNS, TLS
        return None, type(e).__name__


def main(path="projects/portfolio_projects.csv"):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    results = []
    for row in rows:
        status, note = check(row["url"])
        ok = status is not None and status < 400
        print(f"{row['id']:>3}  {'OK ' if ok else 'CHECK'}  {status or '-':>4}  {row['url']}")
        results.append({"id": row["id"], "url": row["url"], "status": status, "ok": ok, "note": note})
        time.sleep(1)  # be polite
    Path("output").mkdir(exist_ok=True)
    with open("output/link_check.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=results[0].keys())
        w.writeheader()
        w.writerows(results)
    bad = sum(not r["ok"] for r in results)
    print(f"\n{len(results) - bad} of {len(results)} links responded; {bad} to check by hand.")


if __name__ == "__main__":
    main(*sys.argv[1:])
