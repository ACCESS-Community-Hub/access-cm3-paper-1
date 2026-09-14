"""
Notebook -> GitHub issue mappings for access-cm3-paper-1's own (native,
coupled-model) notebooks.

Same convention as access-om3-paper-1's notebooks/mkfigs_issues.py: used
by mkfigs-pushit to populate the "GitHub Issue(s)" column in the run
summary table on the documentation website.

CM3 doesn't yet have per-notebook issues the way OM3 does, only the
general tracking issue (#1). Every native notebook is pointed at #1 for
now -- split individual notebooks out into their own issues as the
CM3-native evaluation work grows, the same way OM3's issue list grew
one notebook at a time.

(For the aggregated OM3 notebooks that CM3 pulls in via mkfigs-aggregate,
see mkfigs_issues_om3.py instead -- those already have their own
per-notebook issues, #66-#83.)
"""

_GH = "https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues"

_MEGA_ISSUE = f"[#1]({_GH}/1) — Evaluation metrics for CM3 (mega-issue)"

ISSUES: dict[str, str] = {
    "00_template_notebook":            _MEGA_ISSUE,
    "global-time-series":              _MEGA_ISSUE,
    "salinity":                        _MEGA_ISSUE,
    "water-conservation":              _MEGA_ISSUE,
    "flux-conservation":               _MEGA_ISSUE,
    "autocorrelation_and_amplitude":   _MEGA_ISSUE,
    "Bottom_age_tracer":               _MEGA_ISSUE,
    "SST_trend_global":                _MEGA_ISSUE,
    "TOA_CRE":                         _MEGA_ISSUE,
    "Transects":                       _MEGA_ISSUE,
}
