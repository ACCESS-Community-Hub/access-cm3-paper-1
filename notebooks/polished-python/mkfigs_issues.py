"""
Notebook → GitHub issue mappings for access-cm3-paper-1.

Used by mkfigs-pushit to populate the "GitHub Issue(s)" column in the
run summary table on the documentation website.  Add an entry here for
each notebook you want linked to one or more GitHub issues.  Notebooks
not listed will show an empty cell.

ISSUES maps notebook stem (filename without .ipynb) to a Markdown string.

Confidence varies by entry -- some notebook stems are named directly in
an issue title (high confidence), others are inferred from a general
"Evaluation: ..." issue's description (lower confidence, worth a human
check), and the rest fall back to the general mega-issue #1. Issues
prefixed "Evaluation OM3:" (#32-42, #65-83) track individual OM3
notebooks once they're aggregated into this site (see #5) -- they are
NOT used here since that aggregation isn't part of this site yet.
"""

_GH = "https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues"
_MEGA = f"[#1]({_GH}/1) — Evaluation metrics for CM3 (mega-issue)"

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

    # No distinct issue found for these -- fall back to the mega-issue.
    # autocorrelation_and_amplitude and Transects have no notebook-specific
    # issue at all yet; Bottom_age_tracer only has an "Evaluation OM3:"
    # issue (#37) which tracks the *aggregated OM3* notebook of a similar
    # name, not this CM3-native one -- using that here would misattribute it.
    "autocorrelation_and_amplitude": _MEGA,
    "Bottom_age_tracer":             _MEGA,
    "Transects":                     _MEGA,
}
