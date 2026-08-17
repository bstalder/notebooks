# notebooks

General personal development notebooks.  Currently:

## Development setup

Linting/formatting is handled by [pre-commit](https://pre-commit.com):
`nbstripout` (clears notebook outputs so diffs stay reviewable and the repo
stays small) and `black-jupyter`. CI runs the same hooks on every push.

The git hook itself lives in `.git/hooks/` and is **not** version-controlled,
so it must be installed once per clone — otherwise commits bypass the hooks
locally and only fail later in CI:

```bash
pip install pre-commit          # or: python3 -m pip install --user pre-commit
pre-commit install
```

Note that `nbstripout` strips outputs from committed notebooks. After running a
notebook, `git status` will therefore show it as modified even when no code
changed; that is expected, and the outputs are intentionally local-only.

aiv - Assembly, Integration, and Verification related notebooks

eotesting - raft-scale analyses and investigative processes

vandv - first pass at verification tests for integration activities

earlyoperations - summit/operations exploratory analyses, organized into:
- **thermal/** – Mirror thermal tracking, HVAC daytime conditioning,
	thermal-differential PSF impact, and twilight temperature forecasting.
- **dome_and_wind/** – Wind vs dome-pointing turbulence correlations,
	dome-closed wind-blocking efficiency, dome airflow estimation, and
	wind-loading / oscillation / dust-ingression operational limits.
- **optical_psf/** – ConsDB+EFD PSF diagnostics, guider drift/motion RMS,
	MTAOS wavefront-error Zernikes, focal-plane PSF maps, and mirror
	reflectivity/scattering exploration.
- **engineering/** – Glycol line pressure-drop blockage diagnosis.
- **exploration/** – Early EFD/ESS telemetry exploration notebooks.
- **data/** – Shared parquet caches, CSV reference tables, and generated PDFs.

satellites - satellite-in-Rubin-imaging studies (GEO brightness, calibration analogs).

## Recent updates

- Added Wind_Loading_and_Ingression_Operational_Limits.ipynb in
  earlyoperations/dome_and_wind/ analyzing the effect of wind on the telescope
  as a function of wind speed and relative wind direction to pointing, and
  extrapolating two-sided (into-wind vs away-from-wind) operational wind-speed
  limits, including:
  - Three evidence layers: (A) measured per-exposure telemetry from a
    ConsDB+EFD join (reusing the `ConsDB_EFD_to_PSF_Effects_Diagnosis.ipynb`
    machinery), (B) a first-principles aerodynamic model (`q=½ρV²·Cd·A`, moment
    about the elevation axis) validated against the measured M1M3 hardpoint
    force excursion, and (C) synthesis into operational limits.
  - Static loading (M1M3 hardpoint forces), bulk motion (M1M3/M2 IMS), and
    wind-induced oscillations (per-exposure Welch PSDs of the ~50 Hz M1M3 IMS /
    hardpoint data with band-limited RMS and a wind-stacked resonance hunt).
  - Dust ingression via `lsst.sal.ESS.particleMeasurements` (idx 127/128/129)
    vs wind speed and relative direction through the open aperture.
  - Limits anchored to six metrics: M1M3 balance moment (mx,my), mount tracking
    jitter, M1M3 VMS accelerometer RMS, PSF FWHM, donut blur FWHM, and guider RMS
    motion — with confound-controlled attribution separating the wind-mechanical
    signal from the wind-seeing/thermal confound before extrapolation.
  - Mirror dynamic-motion / oscillation anchor uses the **M1M3 VMS**
    (`lsst.sal.MTVMS.data`, salIndex=1; 3 accelerometers × 3 axes at ~240 Hz),
    NOT the IMS in-exposure std, which sits at the sensor floor (~1e-7, no wind
    signal). VMS metrics (broadband + band-limited accel RMS, dominant peak
    frequency, wind-stacked median acceleration PSD for the §13b resonance hunt)
    are built by `build_vms.py` over a wind-stratified ~30-exposures/night sample
    (~2,200 exposures; per-exposure settled-window fetch). Result: M1M3 vibration
    is only weakly wind-correlated over the observed range — the mirror is not
    the wind-limited component.
  - Force anchor is the M1M3 **balance moment** (`appliedBalanceForces` mx,my),
    NOT the raw hardpoint forces: the force-balance loop drives HP loads to ~0,
    so HP forces are the loop error residual (dominated by slew-settle
    transients), while the balance moment is the loop's wind-disturbance
    response and gives the moment directly (no lever-arm assumption). Per-exposure
    stats skip the first 5 s (slew-settle transient — verified to ~halve the
    dynamic RMS) and use the native ~50 Hz rate (no 1 s pre-averaging).
  - Tracking anchors (mount jitter, guider RMS) use the **wind-buffeting jitter
    allocation (< 0.047″)** — the wind portion of the total 0.01″ tracking-jitter
    design requirement (which covers all sources: servo/encoder/thermal/wind).
    Since the analysis isolates the wind contribution, 0.047″ is the correct
    budget; 0.01″ is shown for context. Guider magnitude RMS is in milli-arcsec
    (verified) and converted to arcsec. Other anchors use data-informed relative
    budgets.
  - Analysis is guarded to genuine open-dome science observing (shutter >95%
    open at exposure midpoint, can-see-sky, not vignetted); a §10 diagnostic
    quantifies the observing selection bias (operators avoid/point away from
    high wind), which bounds the measured curves and motivates the model
    extrapolation.
  - Run over the full 25-week window (2026-01-07 → 2026-07-01; 36,425 science
    exposures, 35,962 passing the open-dome guard, wind to 17.5 m/s) via a
    per-night streaming cache builder (`build_full_cache.py` +
    `assemble_full_cache.py` + `build_stackpsd.py`) that fetches/reduces the
    ~50 Hz M1M3/M2 telemetry one night at a time (bounded memory) into
    day_obs-keyed parquet caches; the notebook then loads the caches.
    VALIDATE_WINDOW toggle switches back to a fast 2-week build.
  - Non-spec anchors use **data-informed relative budgets** (limit = wind speed
    at which a metric rises a stated margin above its own calm-wind V<3 m/s
    baseline), unit-agnostic; replace with project-official tolerances when
    available. IQ anchors (PSF FWHM, donut blur) use a **+50% margin** over the
    calm-wind nominal; tracking anchors use the 0.047″ wind-jitter allocation.
    Full-window result (36k exposures): with wind judged against its 0.047″ jitter
    allocation, **tracking is robust (mount jitter limits only at ~19 m/s; just
    0.3% of exposures exceed 0.047″) and the binding constraint is delivered image
    quality — donut blur FWHM at ~17.0 m/s into-wind and ~18.5 m/s away-from-wind**
    (PSF FWHM ~18.8/19.7 m/s). The dome-shielding asymmetry is small at high wind
    because image quality degrades similarly either way, while the tracking margin
    (where the dome helps) is not the limiter. M1M3 VMS vibration shows no clean
    wind crossing (mirror not wind-limited). With the +50% IQ margin, all anchors
    are model-extrapolated just beyond the observed ~17.5 m/s max (at a +30% margin
    the binding donut/PSF limits were ~13 m/s and measured within the data).
  - §16b decomposes the wind→image-quality pathway and estimates the degraded-ops
    (20 m/s) degradation. The PSF/donut–wind correlation is **not** free-atmosphere
    seeing (DIMM seeing barely responds to wind, ρ=−0.37, and the correlation
    *survives/strengthens* to +0.42 after removing DIMM + inside-dome turbulence
    proxies) and **not** rigid-body buffeting (§11–§13b) — it points to a
    near-field / dome-seeing pathway the outside DIMM does not sample. Extrapolated
    to the **20 m/s degraded-ops threshold** (above the observed ~17.5 m/s max, via
    a+k·V² fits): PSF FWHM ~1.0″→1.65″ (+63%) and donut blur ~0.88″→1.42″ (+61%),
    while AOS FWHM and wind-jitter stay flat — i.e. ~60% IQ degradation expected at
    20 m/s, dominated by the optical (dome-seeing) pathway, not the mechanical one.
  - §16c contrasts louver open vs closed (`build_louver.py`; valid channels
    [2,20,21,29]) as a dome-seeing discriminator. **Closed louvers show a ~4×
    steeper wind→PSF slope** (1.67″ vs 1.01″ at 12–18 m/s) — the opposite of
    louvers-as-turbulence-source, indicating louver ventilation is a *mitigation*:
    sealing the dome in high wind traps a stratified, turbulent air mass in the
    light path. Confounded by louvers being closed *because* it is windy; the
    matched-wind-bin comparison controls for wind speed but not all night-state.
  - Each anchor section carries a directional **compass** (polar rose of the
    metric binned by relative wind direction, wind ≥ 6 m/s; 0° = into wind) so
    the into/away asymmetry is visible per-metric — clearest on the M1M3 balance
    moment (§11, into-wind loading) and dust ingression (§15, into-wind influx).
    The §14 IQ compass falls back from the wind-driven Zernike RMS (z4–z8) to
    PSF FWHM because ConsDB `visit1_quicklook` Zernikes z4–z11 are **all-null in
    this window** (stored `"None"`); note `.sum()` over all-null columns silently
    returns 0.0, so the fallback gate uses `min_count=1` to keep null rows NaN.
- Added ASCENT_GEO_Brightness_Exploration.ipynb in satellites/ studying the
  GEO satellite ASCENT (NORAD 51287, a 12U CubeSat) as a size-analog for the
  proposed Landolt artificial calibration star, including:
  - Visibility/drift analysis and ConsDB FoV cross-match for LSSTCam science
    exposures; trail photometry from DP2 `preliminary_visit_image` data.
  - ASCENT comes out undetected (3σ upper limit AB ~21.6 even stacked),
    confirmed physical against a bright-satellite validation on GOES-19.
  - Section 13: second-epoch confirmation using the `main` repo's prompt
    single-frame products (DP2 covers only July 2025). Re-runs the star-masked
    trail photometry and stacking on the six processed 2026 FoV crossings
    (2 bands, 3 nights); ASCENT is undetected in all, with the deeper
    2026-05-24 i-band stack (N=3181 clean columns) giving 3σ AB ~20.1.
  - Section 12b: absolute flux calibration of the GOES-19 along-trail light
    curve to physical units, anchored to the validated full-trail PhotoCalib
    brightness (AB 11.67 = 77.8 mJy, i-band) rather than the per-row trailed
    sum. Reports mean flux density, in-band energy/photon flux, and the
    intrinsic glint modulation (7.3% raw / 1.8% smoothed RMS, 2.20 mag p-p),
    with a Landolt flux-scaling anchor f_ν(AB) = 78 mJy × 10^[-(AB-11.67)/2.5].
- Added MTAOS_Z4_Focus_Trends.ipynb in earlyoperations/optical_psf/ for
  nightly Z4 (focus/defocus) trends and AOS FWHM correlation, including:
  - EFD query of `lsst.sal.MTAOS.logevent_wavefrontError` for Z4
    (`nollZernikeValues0`, µm) from the four corner wavefront sensors
    (R00/R04/R40/R44) joined to ConsDB `visit1_quicklook` via `visitId`.
  - Nightly median Z4 timeline with IQR envelope and per-sensor tracks
    showing long-term focus trends across the observing season.
  - Nightly Z4 RMS (intra-night spread) to identify nights with poor
    focus stability.
  - Exposure-level Z4 vs `aos_fwhm` density scatter (corner-sensor
    average defocus vs AOS-delivered image FWHM).
- Refreshed thermal and guider-drift notebooks (2026-06):
	- ThermalDifferential_PSF_Impact.ipynb: added section 14 "PSF vs DIMM —
	  Atmospheric + Dome Excess" decomposing science PSF into the
	  free-atmosphere (DIMM) and dome/optics excess components.
	- Optical_Motion_Guider_Drift_RMS_Diagnosis.ipynb: added a ConsDB
	  ellipticity schema exploration cell and an explicit ellipticity vs
	  guider-drift scatter panel.
	- HVAC_DaytimeThermalConditioning, Mirror_Thermal_Tracking, and
	  twilight_forecast_history: refreshed with current EFD data.
- Earlier ConsDB / ESS exploration work (consolidated):
	- ConsDB quicklook fetches expanded to include
	  eff_time_zero_point_scale_median; pre-cut histograms and corrected
	  step-by-step quality-cut accounting.
	- ESS environmental integrations in
	  earlyoperations/optical_psf/Mirror_Reflectivity_Scattering_Exploration.ipynb,
	  including particle measurements (salIndex 127/128/129), humidity
	  (salIndex 113), and inside/outside wind correlations vs PM totals
	  and scattering trends.
- Added Optical_Motion_Guider_Drift_RMS_Diagnosis.ipynb in
	earlyoperations/optical_psf/ for guider-based mount and rotator motion diagnostics,
	including:
	- Per-night and per-exposure guider drift and detrended RMS metrics
	  (altitude, azimuth, focal-plane rotator) over 107 nights / 35,720
	  science exposures (2025-Oct through 2026-Apr).
	- MTAOS correction-type flag breakdown (hexapod, mount tracking drift,
	  mount optical movement, rotator tracking drift, rotator movement)
	  with paneled nightly histograms.
	- Scatter plots of detrended altitude/azimuth RMS vs guider and
	  PSF-star delta ellipticity (e1/e2), filtered to no-hexapod-correction
	  exposures.
	- ConsDB ellipticity schema exploration confirming only guider_e1_mean /
	  guider_e2_mean are available as simple (non-delta) ellipticity columns.
	- Histograms of mount drift magnitude, mount detrended RMS magnitude,
	  rotator drift, and rotator detrended RMS under no-hexapod-correction
	  guard.
- Added MTAOS_WavefrontError_Zernikes.ipynb in
	earlyoperations/optical_psf/ for per-corner-sensor Zernike coefficient time series,
	including:
	- EFD query of lsst.sal.MTAOS.logevent_wavefrontError for a single night,
	  fetching nollZernikeValues0–24 (Noll Z4–Z28) for all four corner
	  wavefront sensors (R00/R04/R40/R44, sensorIds 191/195/199/203).
	- Per-sensor Z4 (defocus) stacked time series with median overlay.
	- All-sensors overlaid single-axis Z4 plot for cross-sensor comparison.
	- Multi-mode grid plot (Z4 defocus, Z5/6 astigmatism, Z7/8 coma,
	  Z11 spherical) × sensor for a full-night overview.
- Added ESS_Inside_vs_Outside_Wind_DomeClosed_AHUOff.ipynb in
	earlyoperations/dome_and_wind/ for dome wind-blocking and air-infiltration analysis,
	including:
	- Inside wind (median of 5 ESS.airTurbulence sensors) vs outside wind
	  (ESS.airFlow index 301), filtered to dome-shutters-closed +
	  louvers-closed + HVAC AHUs-off periods.
	- Dome wind-blocking efficiency time series with 30-min rolling median
	  (~94% median efficiency over the 4-week study period 2026-Feb/Mar).
	- Azimuth perimeter gap air-leak rate Q(t) via the orifice equation,
	  using ESS pressure differential (indices 301 outside / 113 inside),
	  detrended for the static sensor offset; median |Q| ≈ 9 m³/s.
- Added HVAC_DaytimeThermalConditioning.ipynb in
	earlyoperations/thermal/ for dome HVAC daytime pre-conditioning performance, including:
	- Single-night and multi-night overlay plots of ΔT = T_interior − T_ambient
	  vs hours relative to evening nautical twilight (t₀).
	- 12-month time series of ΔT at t₀ (May 2025–May 2026) over 211 qualifying
	  nights; median ΔT = −0.08 °C, indicating excellent average conditioning.
	- Before/after louver commissioning comparison (split at Oct 20 / Nov 27, 2025):
	  night-to-night scatter halved (σ: 1.50 → 0.77 °C) after louver installation.
	- AHU topic-name cutover handling (old lowerAHU* topics before 2026-04-22,
	  new airHandlingUnit*Dome topics afterward).
	- AHU outage-duration effect analysis (111 dome-open nights, Nov 27 2025–present):
	  scatter + rolling median of ΔT vs max contiguous AHU-off run, binned
	  box plot (bins 0–0.5/0.5–1/1–2/2–4/≥4 h), and 2-D hexbin density;
	  Spearman r = +0.28 (longer outages → warmer interior at dome-open).
- Added Mirror_Thermal_Tracking.ipynb in
	earlyoperations/thermal/ for nighttime mirror thermal tracking, including:
	- Single-night two-panel plot: ΔT = T_air(ESS:113) − T_mirror(ESS:115
	  temperatureItem10) and absolute temperatures vs hours after t₀.
	- 8-week multi-night overlay (Mar–May 2026, ~55 nights) with median,
	  IQR, and 10–90th percentile envelope; nights colour-coded by ΔT at t₀.
	- Performance summary: median ΔT at t₀ = +1.23 °C; 83% of nights within
	  target band (−1 to +2 °C) at dome opening.
- Added VisitDetectorTable_PSF_FocalPlane.ipynb in
	earlyoperations/optical_psf/ for PSF size across the LSSTCam focal plane using the
	butler visit_detector_table dataset from LSSTCam/runs/DRP/DP2, including:
	- Full-collection load (10.1M rows, 28,613 visits, 180 science detectors,
	  all 6 bands u/g/r/i/z/y) via two pre-aggregated monolithic tables.
	- Per-detector PSF FWHM statistics (median, IQR, min, max) across all
	  visits and bands combined.
	- Focal-plane maps (side-by-side colour plots) of median PSF FWHM and
	  IQR per detector, overlaid on camera geometry from the butler.
	- Summary: overall median PSF FWHM = 1.170 arcsec; detector-to-detector
	  spread σ = 0.012 arcsec; visit-to-visit IQR per detector ≈ 0.38 arcsec.
- Added ThermalDifferential_PSF_Impact.ipynb in
	earlyoperations/thermal/ for temperature-differential effects on science image
	quality (mid-Apr 2025 – May 2026, 73,149 LSSTCam science exposures), including:
	- EFD fetches for inside dome temperature sensors (ESS:111/112/113 at
	  telescope-mounted locations), ESS:110 air-turbulence sensor, and
	  ESS:301 outside weather station wind and temperature.
	- ESS:114-117 mirror glass temperature arrays (4 × 16 = 64 sensors);
	  per-unit medians and bulk glass_temp_bulk / glass_temp_spread.
	- Elevation-based height correction for ESS:111-113 sensors that move
	  with the telescope (sin/cos decomposition; DOME_LAPSE_RATE = 0.0098 °C/m).
	- ConsDB join (±5 min tolerance) delivering psf_sigma_median, donut_blur,
	  and aos_fwhm per exposure; quality cuts (aos_fwhm < 0.75 arcsec,
	  eff_time_zero_point_scale_median ≥ 0.75, no y-band) → 54,471 exposures.
	- ΔT columns: inside−outside, intra-dome gradient (111−113, 112−113),
	  and glass−air (glass_temp_bulk − inside_temp_113).
	- Time-series overview, scatter plots of all ΔT metrics vs PSF σ / donut
	  blur / AOS FWHM, binned ΔT box+bar analyses for both inside−outside
	  and glass−air differentials, correlation matrix (Spearman), and
	  per-metric summary table.
	- Parquet exports of the full joined dataset (73,149 × 69 cols) and the
	  quality-cut subset (54,471 × 69 cols).
- Added GlycolLine_PressureDrop_Diagnosis.ipynb in
	earlyoperations/engineering/ for diagnosing a glycol line blockage, including:
	- Pressure differential ΔP = P_pier − P_chiller (bar) over a 90-day window,
	  combining MTMount pier sensor (lsst.sal.MTMount.cooling /
	  glycolPressurePier0101, bar) and MTCamera MAQ20 chiller supply pressure
	  (lsst.MTCamera Kafka db / chiller_maq20 / GlycSupplyP, PSI → bar).
	- Chiller switch annotation (~Apr 7 2026): ΔP sign flip from −1 bar (old
	  chiller) to +0.65 bar baseline (new chiller) clearly visible.
	- Blockage event (May 3–10 2026): ΔP escalates to +3.16 bar peak,
	  recovering to ~+0.87 bar after intervention.
	- Two-panel plot (absolute pressures + ΔP with 6-h rolling median) and
	  weekly ΔP summary table.
- Added twilight_forecast_history.ipynb in
	earlyoperations/thermal/ (authors: Brian Brondel, B. Stalder) for tracking how
	WeatherForecast.hourlyTrend temperature predictions evolve over time, including:
	- EFD query of lsst.sal.WeatherForecast.hourlyTrend over a configurable
	  rolling window (default: past 8 hours).
	- Per-issuance computation of the next end-of-evening nautical twilight
	  time (sun altitude = −12°) via Astropy solar-altitude solver + Brent's method.
	- Interpolation of each forecast's temperature grid at the predicted
	  twilight moment, replicating WeatherForecastModel.predict_temperature_at_time.
	- Time series plot of predicted twilight temperature vs. forecast
	  publication time, showing how the model's estimate converges (or drifts)
	  as successive forecasts are issued throughout the day.

