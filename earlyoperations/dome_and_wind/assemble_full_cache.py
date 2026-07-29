#!/usr/bin/env python3
"""Assemble the full-window caches from per-night checkpoints written by build_full_cache.py.

Separated from the builder so it is idempotent and re-runnable without re-fetching: nights
where a numeric column is entirely null get read back as object dtype, which collides with
float64 nights on concat/save. We coerce those columns explicitly here.
"""
import pathlib, numpy as np, pandas as pd

d0, d1 = 20260107, 20260701
CACHE_DIR = pathlib.Path("../data")
NIGHT_DIR = CACHE_DIR / f"_wind_cache_nights_{d0}_{d1}"
CACHE_FILE = CACHE_DIR / f"wind_loading_{d0}_{d1}.parquet"
PSD_CACHE_FILE = CACHE_DIR / f"wind_loading_psd_{d0}_{d1}.parquet"

# columns that must be numeric (mixed float/object across nights due to all-null nights)
NUMERIC_COLS = [
    "dimm_seeing",
    "guider_altitude_drift",
    "guider_azimuth_drift",
    "guider_magnitude_drift",
    "guider_altitude_rms_detrended",
    "guider_azimuth_rms_detrended",
    "guider_magnitude_rms_detrended",
    "guider_focalplane_theta_drift",
    "guider_focalplane_theta_rms_detrended",
    "mount_motion_image_degradation",
    "mount_motion_image_degradation_az",
    "mount_motion_image_degradation_el",
    "mount_motion_image_degradation_rot",
    "mount_jitter_rms",
    "mount_jitter_rms_az",
    "mount_jitter_rms_el",
    "mount_jitter_rms_rot",
]


def coerce(df):
    for c in NUMERIC_COLS:
        if c in df:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    if (
        "can_see_sky" in df
    ):  # bool/object mix → normalize to nullable boolean-ish string kept as str
        df["can_see_sky"] = df["can_see_sky"].map(
            lambda v: (
                True
                if str(v).lower() in ("true", "1", "t")
                else (False if str(v).lower() in ("false", "0", "f") else np.nan)
            )
        )
    return df


# ── main analysis frame ──────────────────────────────────────────────────────
mfiles = sorted(p for p in NIGHT_DIR.glob("night_2*.parquet") if "_psd" not in p.name)
frames = []
for p in mfiles:
    d = pd.read_parquet(p)
    if not d.empty:
        frames.append(coerce(d))
main_df = pd.concat(frames).sort_index()
print(f"main frame: {len(main_df):,} exposures from {len(frames)} nights")

notv = (
    ~main_df["vignette"].astype(str).str.upper().isin(["FULLY", "PARTIALLY"])
    if "vignette" in main_df
    else True
)
main_df["analysis_ok"] = (
    (main_df["img_type"] == "science")
    & main_df["shutter_open"].fillna(False).astype(bool)
    & main_df["can_see_sky"].fillna(True).astype(bool)
    & notv
)
print(f"  analysis_ok (open-dome science): {int(main_df['analysis_ok'].sum()):,}")
main_df.to_parquet(CACHE_FILE)
print(f"  ✓ {CACHE_FILE}")

# ── PSD products ─────────────────────────────────────────────────────────────
pfiles = sorted(NIGHT_DIR.glob("night_2*_psd.parquet"))
pframes = [pd.read_parquet(p) for p in pfiles]
pframes = [f for f in pframes if not f.empty]
if pframes:
    psd = pd.concat(pframes).sort_index()
    # coerce any all-null numeric psd cols
    for c in psd.columns:
        if psd[c].dtype == object and c not in ("into_wind",):
            psd[c] = pd.to_numeric(psd[c], errors="coerce")
    psd.to_parquet(PSD_CACHE_FILE)
    print(f"psd frame: {len(psd):,} exposures  ✓ {PSD_CACHE_FILE}")
else:
    print("no PSD checkpoints")
print("DONE")
