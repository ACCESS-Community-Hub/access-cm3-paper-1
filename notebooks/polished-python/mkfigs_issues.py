"""
Notebook → GitHub issue mappings for access-cm3-paper-1.

Used by mkfigs-pushit to populate the "GitHub Issue(s)" column in the
run summary table on the documentation website.  Add an entry here for
each notebook you want linked to one or more GitHub issues.  Notebooks
not listed will show an empty cell.

ISSUES maps notebook stem (filename without .ipynb) to a Markdown string.

CATEGORIES (optional) groups the landing-page run-summary table into one
sub-headed table per category (the left-hand nav stays a flat, alphabetical
list of notebooks). Each entry lists issue numbers
(int, matched against the links in ISSUES) and/or notebook stems (str); each
notebook appears exactly once, and anything unmatched goes last under
"Miscellaneous". CM3 has no per-theme tracking issue yet (cf.
access-om3-paper-1#23), so these are listed by notebook stem -- DRAFT
groupings, please review. Once such an issue exists, set CATEGORIES_SOURCE to
its URL and the landing-page intro will link to it.

Confidence varies by entry -- some notebook stems are named directly in
an issue title (high confidence), others are inferred from a general
"Evaluation: ..." issue's description (lower confidence, worth a human
check). Notebooks with no known issue are left out (empty cell) rather
than pointed at the mega-issue #1. Issues
prefixed "Evaluation OM3:" (#32-42, #65-98) track individual OM3
notebooks run on CM3 (see #5); they are used for the OM3 notebooks that
mkfigs.sh runs from the access-om3-paper-1 submodule (`om3_array`), which
are keyed here by their OM3 notebook name.
"""

_GH = "https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues"
_OM3 = "https://github.com/ACCESS-Community-Hub/access-om3-paper-1/issues"

ISSUES: dict[str, str] = {
    # High confidence: notebook filename is named directly in the issue.
    "00_template_notebook": f"[#3]({_GH}/3) — Update 00_template_notebook.ipynb to use CM3 data",
    "global-time-series":   f"[#63]({_GH}/63) — global-time-series.ipynb using incorrect CM2 simulation",
    "salinity":             f"[#63]({_GH}/63) — salinity.ipynb using incorrect CM2 simulation, [#48]({_GH}/48) Salinity time series for various ocean basins",
    "SST_trend_global":     f"[#16]({_GH}/16) — Evaluation: Global SST trend",
    "TOA_CRE":              f"[#22]({_GH}/22) — Evaluation: TOA LW and SW and cloud forcing c.f. CERES obs.",

    # Lower confidence: inferred from a general "Evaluation: ..." issue
    # that plausibly matches this notebook's topic, not a direct filename
    # reference -- worth confirming with whoever filed the issue.
    "water-conservation":   f"[#29]({_GH}/29) — Evaluation: Global water budget time series",
    "flux-conservation":    f"[#28]({_GH}/28) — Evaluation: Coupled fluxes global means and relative errors",

    # No known issue yet (left out on purpose, add one when it exists):
    # autocorrelation_and_amplitude.

    # OM3 notebooks (external/access-om3-paper-1 submodule, `om3_array` in mkfigs.sh):
    # the CM3 "Evaluation OM3:" issue in bold, then the access-om3-paper-1 issue it
    # mirrors in brackets. One CM3 issue per OM3 issue (title "Evaluation OM3: " + the
    # OM3 title); written by open_om3_issues.py, which also opens missing CM3 issues.
    "Bottom_age_tracer_in_ACCESS_OM3":        f"**[CM3 #37: Bottom age]({_GH}/37)** ([OM3 #31]({_OM3}/31))",
    "Currents_streamfunction_variability":    f"**[CM3 #76: mean surface current speed, standard deviation of sea level anomaly and mean barotropic streamfunction]({_GH}/76)** ([OM3 #18]({_OM3}/18))",
    "Equatorial_pacific":                     f"**[CM3 #82: Contours (depth-longitude @ equator, depth-latitude @ 220E) of temperature and zonal velocity]({_GH}/82)** ([OM3 #17]({_OM3}/17))<br>**[CM3 #92: Contours (latitude-longitude, global) of annual 1993-2017 mean depth of the 20C isotherm]({_GH}/92)** ([OM3 #19]({_OM3}/19))",
    "MLD":                                    f"**[CM3 #65: Mixed layer depth]({_GH}/65)** ([OM3 #38]({_OM3}/38))",
    "MLD_max":                                f"**[CM3 #65: Mixed layer depth]({_GH}/65)** ([OM3 #38]({_OM3}/38))",
    "MeridionalHeatTransport":                f"**[CM3 #78: Total meridional heat transport]({_GH}/78)** ([OM3 #12]({_OM3}/12))",
    "Overturning_in_ACCESS_OM3":              f"**[CM3 #67: Mean zonally integrated overturning circulation and Time series of AMOC]({_GH}/67)** ([OM3 #6]({_OM3}/6), [OM3 #7]({_OM3}/7))",
    "SSH":                                    f"**[CM3 #80: Mean dynamic sea level map]({_GH}/80)** ([OM3 #4]({_OM3}/4), [OM3 #5]({_OM3}/5))",
    "SSS":                                    f"**[CM3 #41: mean sea surface salinity bias]({_GH}/41)** ([OM3 #10]({_OM3}/10))",
    "SST":                                    f"**[CM3 #36: Mean sea surface temperature bias]({_GH}/36)** ([OM3 #9]({_OM3}/9))",
    "StraitTransports":                       f"**[CM3 #42: Drake Passage Transport]({_GH}/42)** ([OM3 #1]({_OM3}/1))<br>**[CM3 #75: Time series of annual mean transport through the Indonesian straits]({_GH}/75)** ([OM3 #16]({_OM3}/16))",
    "Timeseries_daily_extreme_from_2D_fields":f"**[CM3 #39: Timeseries of SST, SSS, SSH, surface speed and MLD extrema]({_GH}/39)** ([OM3 #34]({_OM3}/34))",
    "pPV":                                    f"**[CM3 #66: Meridional transects of mean planetary geostrophic potential vorticity, potential density anomaly and max/min monthly mean MLD]({_GH}/66)** ([OM3 #14]({_OM3}/14))",
    "temp-salt-vs-depth-latitude":            f"**[CM3 #83: Zonally averaged temperature and salinity bias]({_GH}/83)** ([OM3 #11]({_OM3}/11))<br>**[CM3 #91: Meridional transects of 1993-2017 mean potential temperature and salinity]({_GH}/91)** ([OM3 #13]({_OM3}/13))",
    "temp-salt-vs-depth-time":                f"**[CM3 #35: Hovmoller (depth-time) of horizontally averaged temperature drift]({_GH}/35)** ([OM3 #8]({_OM3}/8))",
    "timeseries":                             f"**[CM3 #77: Timeseries global averages]({_GH}/77)** ([OM3 #3]({_OM3}/3))",

    "SeaIce_area":                            f"**[CM3 #93: Time series of running 12-month minimum, mean and maximum sea ice extent and volume]({_GH}/93)** ([OM3 #20]({_OM3}/20))<br>**[CM3 #94: Sea ice area / extent]({_GH}/94)** ([OM3 #21]({_OM3}/21))",
    "SeaIce_Vol":                             f"**[CM3 #93: Time series of running 12-month minimum, mean and maximum sea ice extent and volume]({_GH}/93)** ([OM3 #20]({_OM3}/20))<br>**[CM3 #95: Contours (latitude, longitude, regional) of 1993-2017 sea ice thickness and concentration]({_GH}/95)** ([OM3 #22]({_OM3}/22))<br>**[CM3 #96: Sea-Ice Volume and Thickness]({_GH}/96)** ([OM3 #48]({_OM3}/48))",
    "SeaIce_mass_budget_climatology":         f"**[CM3 #97: Climatological cycle of sea ice mass budget terms]({_GH}/97)** ([OM3 #52]({_OM3}/52))",
    "Transects":                              f"**[CM3 #91: Meridional transects of 1993-2017 mean potential temperature and salinity]({_GH}/91)** ([OM3 #13]({_OM3}/13))",
    "Transects-mixing":                       f"**[CM3 #91: Meridional transects of 1993-2017 mean potential temperature and salinity]({_GH}/91)** ([OM3 #13]({_OM3}/13))",
    "WM_evaluation":                          f"**[CM3 #98: Water mass density change hovmoller]({_GH}/98)** ([OM3 #106]({_OM3}/106))",
    "MLD_manual":                             f"**[CM3 #65: Mixed layer depth]({_GH}/65)** ([OM3 #38]({_OM3}/38))",
}

# DRAFT -- proposed groupings, to be confirmed by the CM3 evaluation team.
CATEGORIES: dict[str, list[int | str]] = {
    "Global means and conservation":   ["global-time-series", "water-conservation", "flux-conservation"],
    "Ocean":                           [
        "salinity", "SST_trend_global",
        # access-om3-paper-1 notebooks (om3_array in mkfigs.sh)
        "Bottom_age_tracer_in_ACCESS_OM3", "Currents_streamfunction_variability", "Equatorial_pacific",
        "MLD", "MLD_max", "MeridionalHeatTransport", "Overturning_in_ACCESS_OM3", "SSH", "SSS", "SST",
        "StraitTransports", "Timeseries_daily_extreme_from_2D_fields", "pPV",
        "temp-salt-vs-depth-latitude", "temp-salt-vs-depth-time", "timeseries",
        "Transects", "Transects-mixing", "WM_evaluation", "MLD_manual",
    ],
    "Sea ice":                         ["SeaIce_area", "SeaIce_Vol", "SeaIce_mass_budget_climatology"],
    "Atmosphere and radiation":        ["TOA_CRE"],
    "Variability":                     ["autocorrelation_and_amplitude"],
}
