"""Fetch the Mar 25 (day_obs 20260324) BLOCK-T698 science block: WFE Zernikes (Z4)
plus camera (salIndex=1) and M2 (salIndex=2) hexapod focus. Unlike the dither-style
T698 runs characterized in Section 12, this block has M2 effectively frozen
(~0.4 µm ptp) and the camera only LUT-drifting — yet Z4 still wanders with a high
ACF, the same disturbance the open-loop T614 test (Section 14) isolates. Caches to
parquet so the notebook need not re-query the EFD.

WFE here uses only the 4 SW0 corner sensors (191/195/199/203), like T614.
"""
import asyncio, pandas as pd, numpy as np
from lsst_efd_client import EfdClient
from astropy.time import Time

# T698 science block, night of Mar 25 (start of night). Trim to the block itself;
# a wider pad pulls in slew spikes that inflate the hexapod ptp.
T0 = Time("2026-03-25T23:55:00"); T1 = Time("2026-03-26T02:05:00")
OUT_WFE = "../data/t698_mar25_wfe.parquet"
OUT_HEX = "../data/t698_mar25_hexapod.parquet"


async def main():
    c = EfdClient("usdf_efd")
    nv = [f"nollZernikeValues{i}" for i in range(25)]
    w = await c.select_time_series("lsst.sal.MTAOS.logevent_wavefrontError",
                                   fields=["sensorId", "visitId"] + nv, start=T0, end=T1)
    print(f"WFE rows: {len(w)}")
    for i in range(25):
        w[f"z{i+4}_um"] = pd.to_numeric(w[f"nollZernikeValues{i}"], errors="coerce")
    if w.index.tz is None:
        w.index = w.index.tz_localize("UTC")
    keep = ["sensorId", "visitId"] + [f"z{i+4}_um" for i in range(25)]
    w[keep].reset_index().rename(columns={"index": "ts"}).to_parquet(OUT_WFE)
    print(f"  sensorIds: {sorted(w['sensorId'].unique())}")
    print(f"  visits: {w['visitId'].nunique()}, Z4 range {w['z4_um'].min():.3f}..{w['z4_um'].max():.3f}")

    hex_all = []
    for idx in (1, 2):
        h = await c.select_time_series("lsst.sal.MTHexapod.application",
                fields=["salIndex", "position2", "demand2"], start=T0, end=T1, index=idx)
        h = h[h["salIndex"] == idx]
        if h.index.tz is None:
            h.index = h.index.tz_localize("UTC")
        r = h[["position2", "demand2"]].resample("2s").median().dropna(how="all")
        r["salIndex"] = idx
        hex_all.append(r.reset_index().rename(columns={"index": "ts"}))
    pd.concat(hex_all, ignore_index=True).to_parquet(OUT_HEX)
    print(f"Saved {OUT_WFE}, {OUT_HEX}")


asyncio.run(main())
