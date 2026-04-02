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

