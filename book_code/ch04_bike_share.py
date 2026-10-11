# Chapter 4: one project from start to finish
# Riverton Bike Share, September 2026 (fictional practice data)
# Run from the repository root:
#     python book_code/ch04_bike_share.py

# --- Block 1: load and look
import pandas as pd

trips = pd.read_csv("data/riverton_trips_2026_09.csv",
                    parse_dates=["started_at", "ended_at"])
print(trips.shape)
start = trips["started_at"]
print(start.min(), "to", start.max())
print(trips["member_casual"].value_counts())
print(trips.isna().sum()[lambda s: s > 0])

# --- Block 2: check durations and decide what to keep
duration = trips["ended_at"] - trips["started_at"]
trips["minutes"] = duration.dt.total_seconds() / 60

checks = pd.Series({
    "under 1 minute": (trips["minutes"] < 1).sum(),
    "over 24 hours": (trips["minutes"] > 24 * 60).sum(),
    "no end station": trips["end_station_id"].isna().sum(),
})
print(checks)

clean = trips[trips["minutes"].between(1, 24 * 60)].copy()
kept = len(clean) / len(trips)
print(f"Kept {len(clean):,} of {len(trips):,} trips ({kept:.1%})")

# --- Block 3: members and casual riders, weekdays and weekends
clean["hour"] = clean["started_at"].dt.hour
clean["day_type"] = clean["started_at"].dt.dayofweek.map(
    lambda d: "weekend" if d >= 5 else "weekday")

days = (clean.groupby("day_type")["started_at"]
        .apply(lambda s: s.dt.date.nunique()))
per_day = (clean.groupby(["day_type", "member_casual"])
           .size().unstack())
print(per_day.div(days, axis=0).round(0))
median_mins = clean.groupby("member_casual")["minutes"].median()
print(median_mins.round(1))

# --- Block 4: the weekday hourly profile
weekday = clean[clean["day_type"] == "weekday"]
profile = (weekday.groupby(["hour", "member_casual"])
           .size().unstack()
           .reindex(range(24), fill_value=0) / days["weekday"])
print(profile.loc[[7, 8, 12, 17, 18]].round(0))

peak = weekday["hour"].isin([7, 8, 16, 17, 18])
share = weekday.assign(peak=peak).groupby("member_casual")["peak"]
print(share.mean().round(3))

# --- Block 5: the chart
from pathlib import Path
import matplotlib.pyplot as plt

Path("output").mkdir(exist_ok=True)
fig, ax = plt.subplots(figsize=(6.5, 3.4))
ax.plot(profile.index, profile["member"],
        color="black", lw=2, label="Members")
ax.plot(profile.index, profile["casual"],
        color="grey", lw=2, ls="--", label="Casual riders")
ax.set_title("On weekdays, members ride at commute times; "
             "casual riders ride in the afternoon",
             loc="left", fontsize=9.5)
ax.set_xlabel("Hour trip started")
ax.set_ylabel("Average trips per weekday")
ax.set_xticks(range(0, 24, 3))
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig("output/ch04_weekday_profile.png", dpi=200)

# --- Block 6: which stations are commuter origins? (SQL)
import sqlite3

con = sqlite3.connect(":memory:")
clean.to_sql("trips", con, index=False)

query = """
SELECT start_station_name AS station,
       COUNT(*) AS weekday_trips,
       ROUND(AVG(CASE
             WHEN CAST(strftime('%H', started_at) AS INTEGER)
                  BETWEEN 7 AND 8 THEN 1.0
             ELSE 0 END), 3) AS share_7_to_9am
FROM trips
WHERE member_casual = 'member'
  AND strftime('%w', started_at) NOT IN ('0', '6')
GROUP BY start_station_name
HAVING COUNT(*) >= 300
ORDER BY share_7_to_9am DESC, station
LIMIT 6;
"""
print(pd.read_sql(query, con))
