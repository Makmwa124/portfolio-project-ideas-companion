"""Generate the Riverton Bike Share practice data used in Chapter 4.

Riverton and its bike share scheme are fictional. The file layout copies the
public trip files published by real bike share systems (such as Citi Bike),
so the code in the book works on real data with few changes.

Run from the repository root:  python scripts/make_data.py
"""
import uuid
from pathlib import Path

import numpy as np
import pandas as pd

rng = np.random.default_rng(15)
OUT = Path("data")
OUT.mkdir(exist_ok=True)

# name, kind, lat, lng, weight
stations = [
    ("Central Station", "hub", -34.9210, 138.5960, 9),
    ("Ferry Terminal", "hub", -34.9150, 138.6010, 6),
    ("Market Square", "hub", -34.9285, 138.6000, 7),
    ("Treasury Lane", "hub", -34.9255, 138.5995, 6),
    ("Harbour Offices", "hub", -34.9180, 138.5935, 5),
    ("Courthouse Corner", "hub", -34.9268, 138.6030, 4),
    ("Hospital Gate", "hub", -34.9205, 138.6080, 4),
    ("University North", "hub", -34.9195, 138.6050, 5),
    ("Riverside Park", "leisure", -34.9170, 138.5880, 6),
    ("Botanic Garden", "leisure", -34.9180, 138.6110, 5),
    ("Beachfront Kiosk", "leisure", -34.9800, 138.5100, 6),
    ("Lighthouse Point", "leisure", -34.9900, 138.5050, 3),
    ("Zoo Entrance", "leisure", -34.9135, 138.6075, 3),
    ("Stadium West", "leisure", -34.9155, 138.5960, 3),
    ("Wetlands Trail", "leisure", -34.9400, 138.5300, 2),
]
residential = [
    "Elm Street", "Kingsway North", "Hillcrest Road", "Parade East",
    "Wattle Grove", "Foundry Lane", "Mill Creek", "Chapel Hill",
    "Bayview Terrace", "Station Road West", "Orchard Avenue", "Gum Tree Square",
    "Canal Walk", "Rosebank", "Quarry Road", "Seaview Heights",
    "Ashford Green", "Brickworks", "Tannery Row", "Westbourne",
]
for i, name in enumerate(residential):
    stations.append((name, "home", -34.88 - 0.006 * (i % 7), 138.55 + 0.01 * (i % 6), 3))

st = pd.DataFrame(stations, columns=["name", "kind", "lat", "lng", "w"])
st["station_id"] = [f"RV{100 + i}" for i in range(len(st))]

days = pd.date_range("2026-09-01", "2026-09-30", freq="D")
rain_days = {pd.Timestamp(d) for d in ["2026-09-04", "2026-09-05", "2026-09-14", "2026-09-22", "2026-09-23"]}


def pick(kinds, n, extra=None):
    sub = st[st.kind.isin(kinds)]
    w = sub.w.to_numpy(float)
    return sub.sample(n=n, replace=True, weights=w, random_state=int(rng.integers(1e9))).index.to_numpy()


rows = []
for day in days:
    weekend = day.dayofweek >= 5
    rain = day in rain_days
    # members
    n_mem = int(rng.normal(1250 if not weekend else 650, 60) * (0.75 if rain else 1))
    n_cas = int(rng.normal(380 if not weekend else 1050, 50) * (0.45 if rain else 1))
    for who, n in (("member", n_mem), ("casual", n_cas)):
        if who == "member" and not weekend:
            # commute: morning home->hub, evening hub->home, plus some midday
            k = rng.choice(["am", "pm", "mid"], size=n, p=[0.36, 0.40, 0.24])
            hrs = np.where(k == "am", rng.normal(8.1, 0.7, n),
                  np.where(k == "pm", rng.normal(17.4, 0.9, n), rng.uniform(10, 21, n)))
            start_kind = np.where(k == "am", "home", np.where(k == "pm", "hub", "any"))
        elif who == "member":
            hrs = rng.normal(13, 3, n)
            start_kind = np.full(n, "any")
        else:
            hrs = rng.normal(14 if weekend else 15, 2.8, n)
            start_kind = np.full(n, "leisure_mix")
        hrs = np.clip(hrs, 5, 22.9)
        for h, sk in zip(hrs, start_kind):
            if sk == "home":
                s, e = pick(["home"], 1)[0], pick(["hub"], 1)[0]
            elif sk == "hub":
                s, e = pick(["hub"], 1)[0], pick(["home"], 1)[0]
            elif sk == "leisure_mix":
                s = pick(["leisure", "hub"], 1)[0] if rng.random() < 0.8 else pick(["home"], 1)[0]
                e = pick(["leisure", "hub"], 1)[0]
            else:
                s, e = pick(["hub", "home", "leisure"], 1)[0], pick(["hub", "home", "leisure"], 1)[0]
            mins = rng.gamma(3.0, 4.2) if who == "member" else rng.gamma(2.6, 9.5)
            mins = max(mins, 1.2)
            start = day + pd.Timedelta(hours=float(h)) + pd.Timedelta(seconds=int(rng.integers(0, 3600)))
            rows.append((who, s, e, start, start + pd.Timedelta(minutes=float(mins))))

df = pd.DataFrame(rows, columns=["member_casual", "s", "e", "started_at", "ended_at"])
n = len(df)
df["ride_id"] = [uuid.UUID(int=int(rng.integers(0, 2**63)) << 64 | int(rng.integers(0, 2**63))).hex[:16].upper() for _ in range(n)]
df["rideable_type"] = np.where(rng.random(n) < 0.42, "electric_bike", "classic_bike")

# messiness, as in real trip files
false_start = rng.choice(n, 900, replace=False)
df.loc[false_start, "ended_at"] = df.loc[false_start, "started_at"] + pd.to_timedelta(rng.integers(5, 55, 900), unit="s")
df.loc[false_start, "e"] = df.loc[false_start, "s"]
long_idx = rng.choice(np.setdiff1d(np.arange(n), false_start), 60, replace=False)
df.loc[long_idx, "ended_at"] = df.loc[long_idx, "started_at"] + pd.to_timedelta(rng.integers(26, 90, 60), unit="h")
lost = rng.choice(np.setdiff1d(np.arange(n), np.r_[false_start, long_idx]), 140, replace=False)

out = pd.DataFrame({
    "ride_id": df.ride_id,
    "rideable_type": df.rideable_type,
    "started_at": df.started_at.dt.strftime("%Y-%m-%d %H:%M:%S"),
    "ended_at": df.ended_at.dt.strftime("%Y-%m-%d %H:%M:%S"),
    "start_station_name": st.name.to_numpy()[df.s],
    "start_station_id": st.station_id.to_numpy()[df.s],
    "end_station_name": st.name.to_numpy()[df.e],
    "end_station_id": st.station_id.to_numpy()[df.e],
    "start_lat": st.lat.to_numpy()[df.s].round(4),
    "start_lng": st.lng.to_numpy()[df.s].round(4),
    "end_lat": st.lat.to_numpy()[df.e].round(4),
    "end_lng": st.lng.to_numpy()[df.e].round(4),
    "member_casual": df.member_casual,
})
out.loc[lost, ["end_station_name", "end_station_id", "end_lat", "end_lng"]] = np.nan
out = out.sample(frac=1, random_state=3).sort_values("started_at", kind="stable").reset_index(drop=True)
out.to_csv(OUT / "riverton_trips_2026_09.csv", index=False)
st[["station_id", "name", "lat", "lng"]].rename(columns={"name": "station_name"}).to_csv(OUT / "riverton_stations.csv", index=False)
print(f"Wrote {len(out):,} trips and {len(st)} stations")
