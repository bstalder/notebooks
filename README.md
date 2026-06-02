# notebooks

General personal development notebooks.  Currently:

aiv - Assembly, Integration, and Verification related notebooks

eotesting - raft-scale analyses and investigative processes

vandv - first pass at verification tests for integration activities

earlyoperations - summit/operations exploratory analyses, organized into:
- **thermal/** – Mirror thermal tracking, HVAC daytime conditioning,
	thermal-differential PSF impact, and twilight temperature forecasting.
- **dome_and_wind/** – Wind vs dome-pointing turbulence correlations,
	dome-closed wind-blocking efficiency, and dome airflow estimation.
- **optical_psf/** – ConsDB+EFD PSF diagnostics, guider drift/motion RMS,
	MTAOS wavefront-error Zernikes, focal-plane PSF maps, and mirror
	reflectivity/scattering exploration.
- **engineering/** – Glycol line pressure-drop blockage diagnosis.
- **exploration/** – Early EFD/ESS telemetry exploration notebooks.
- **data/** – Shared parquet caches, CSV reference tables, and generated PDFs.

## Recent updates

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

