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

