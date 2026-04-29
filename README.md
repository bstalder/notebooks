# notebooks

General personal development notebooks.  Currently:

aiv - Assembly, Integration, and Verification related notebooks

eotesting - raft-scale analyses and investigative processes

vandv - first pass at verification tests for integration activities

earlyoperations - summit/operations exploratory analyses, including:
- ConsDB and EFD join workflows for LSSTCam science exposures.
- Wind, dome-pointing, and image-quality trend studies.
- Quality-cut diagnostics for AOS residual FWHM and
	eff_time_zero_point_scale_median thresholding.
- Per-corner-sensor Zernike coefficient time series from MTAOS EFD events.

## Recent updates

- Expanded ConsDB quicklook fetches to include
	eff_time_zero_point_scale_median.
- Added pre-cut distribution histograms for
	eff_time_zero_point_scale_median and aos_fwhm.
- Corrected image-quality cut accounting to report true step-by-step removals.
- Set eff_time_zero_point_scale_median as a minimum-threshold cut
	(keep rows with scale >= zp_scale_min).
- Added ESS integration in
	earlyoperations/Mirror_Reflectivity_Scattering_Exploration.ipynb
	for environmental context on M1M3 scattering trends.
- Added PM analyses using
	lsst.sal.ESS.particleMeasurements (salIndex 127/128/129),
	including total particle count from numberConcentration0-4.
- Added humidity analyses using
	lsst.sal.ESS.relativeHumidity.relativeHumidityItem
	with salIndex=113.
- Added turbulence and wind correlation studies for PM totals and
	scattering, including:
	- inside wind (ESS.airTurbulence; median across 5 sensors)
	- outside wind (ESS.airFlow index 301)
	- all-data and night+dome-open subsets.
- Added Optical_Motion_Guider_Drift_RMS_Diagnosis.ipynb in
	earlyoperations/ for guider-based mount and rotator motion diagnostics,
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
	earlyoperations/ for per-corner-sensor Zernike coefficient time series,
	including:
	- EFD query of lsst.sal.MTAOS.logevent_wavefrontError for a single night,
	  fetching nollZernikeValues0–24 (Noll Z4–Z28) for all four corner
	  wavefront sensors (R00/R04/R40/R44, sensorIds 191/195/199/203).
	- Per-sensor Z4 (defocus) stacked time series with median overlay.
	- All-sensors overlaid single-axis Z4 plot for cross-sensor comparison.
	- Multi-mode grid plot (Z4 defocus, Z5/6 astigmatism, Z7/8 coma,
	  Z11 spherical) × sensor for a full-night overview.
- Added ESS_Inside_vs_Outside_Wind_DomeClosed_AHUOff.ipynb in
	earlyoperations/ for dome wind-blocking and air-infiltration analysis,
	including:
	- Inside wind (median of 5 ESS.airTurbulence sensors) vs outside wind
	  (ESS.airFlow index 301), filtered to dome-shutters-closed +
	  louvers-closed + HVAC AHUs-off periods.
	- Dome wind-blocking efficiency time series with 30-min rolling median
	  (~94% median efficiency over the 4-week study period 2026-Feb/Mar).
	- Azimuth perimeter gap air-leak rate Q(t) via the orifice equation,
	  using ESS pressure differential (indices 301 outside / 113 inside),
	  detrended for the static sensor offset; median |Q| ≈ 9 m³/s.

