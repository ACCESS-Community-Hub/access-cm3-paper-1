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
prefixed "Evaluation OM3:" (#32-42, #65-83) track individual OM3
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

    # OM3 notebooks (external/access-om3-paper-1 submodule, `om3_array` in mkfigs.sh).
    # Matched by issue title (several topics have two issues; both are listed).
    # No notebook found for #38 (western boundary current timeseries).
    "Bottom_age_tracer_in_ACCESS_OM3":         f"[#37]({_GH}/37) — Evaluation OM3: Bottom age",
    "Currents_streamfunction_variability":     f"[#76]({_GH}/76) — Evaluation OM3: mean surface current speed, standard deviation of sea level anomaly and mean barotropic streamfunction",
    "Equatorial_pacific":                      f"[#82]({_GH}/82) — Evaluation OM3: Contours (depth-longitude @ equator, depth-latitude @ 220E) of temperature and zonal velocity",
    "MLD":                                     f"[#65]({_GH}/65) — Evaluation OM3: Mixed layer depth",
    "MLD_max":                                 f"[#66]({_GH}/66) — Evaluation OM3: Meridional transects of mean planetary geostrophic potential vorticity, potential density anomaly and max/min monthly mean MLD",
    "MeridionalHeatTransport":                 f"[#78]({_GH}/78) — Evaluation OM3: Total meridional heat transport",
    "Overturning_in_ACCESS_OM3":               f"[#33]({_GH}/33), [#34]({_GH}/34), [#67]({_GH}/67) — Evaluation OM3: Mean zonally integrated overturning circulation and time series of AMOC",
    "SSH":                                     f"[#80]({_GH}/80) — Evaluation OM3: Mean dynamic sea level map",
    "SSS":                                     f"[#41]({_GH}/41) — Evaluation OM3: mean sea surface salinity bias",
    "SST":                                     f"[#36]({_GH}/36) — Evaluation OM3: Mean sea surface temperature bias",
    "StraitTransports":                        f"[#40]({_GH}/40), [#75]({_GH}/75) — Evaluation OM3: Time series of annual mean transport through the Indonesian straits, [#42]({_GH}/42) Drake Passage Transport",
    "Timeseries_daily_extreme_from_2D_fields": f"[#39]({_GH}/39) — Evaluation OM3: Timeseries of SST, SSS, SSH, surface speed and MLD extrema",
    "pPV":                                     f"[#66]({_GH}/66) — Evaluation OM3: Meridional transects of mean planetary geostrophic potential vorticity, potential density anomaly and max/min monthly mean MLD",
    "temp-salt-vs-depth-latitude":             f"[#83]({_GH}/83) — Evaluation OM3: Zonally averaged temperature and salinity bias",
    "temp-salt-vs-depth-time":                 f"[#35]({_GH}/35) — Evaluation OM3: Hovmoller (depth-time) of horizontally averaged temperature drift",
    "timeseries":                              f"[#32]({_GH}/32), [#77]({_GH}/77) — Evaluation OM3: Timeseries global averages",

    # access-om3-paper-1 notebooks with no CM3 issue yet: linked to the
    # access-om3-paper-1 issue instead.
    "SeaIce_area":                            f"[access-om3-paper-1#20]({_OM3}/20) Sea ice extent time series, [access-om3-paper-1#21]({_OM3}/21) Sea ice annual cycle",
    "SeaIce_Vol":                             f"[access-om3-paper-1#20]({_OM3}/20) Sea ice volume time series, [access-om3-paper-1#22]({_OM3}/22) Sea ice thickness/concentration, [access-om3-paper-1#48]({_OM3}/48) Sea ice volume and thickness vs observations",
    "SeaIce_mass_budget_climatology":         f"[access-om3-paper-1#52]({_OM3}/52) — Sea ice mass budget climatology",
    "Transects":                              f"[access-om3-paper-1#13]({_OM3}/13) — WOCE/GO-SHIP meridional T/S transects",
    "Transects-mixing":                       f"[access-om3-paper-1#13]({_OM3}/13) — WOCE/GO-SHIP transects",
    "WM_evaluation":                          f"[access-om3-paper-1#106]({_OM3}/106) — Water mass density change Hovmöller",
    "MLD_manual":                             f"[#65]({_GH}/65) — Evaluation OM3: Mixed layer depth (max MLD calculated manually)",
    "Truncation_locations":                   f"[access-om3-paper-1#154]({_OM3}/154) — Velocity truncation locations (numerical stability diagnostic)",
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
        "Transects", "Transects-mixing", "WM_evaluation", "MLD_manual", "Truncation_locations",
    ],
    "Sea ice":                         ["SeaIce_area", "SeaIce_Vol", "SeaIce_mass_budget_climatology"],
    "Atmosphere and radiation":        ["TOA_CRE"],
    "Variability":                     ["autocorrelation_and_amplitude"],
}
