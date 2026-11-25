#!/bin/bash
#PBS -l storage=scratch/x77+scratch/tm70+gdata/zv30+gdata/p73+gdata/tm70+gdata/ki32+gdata/nf33+gdata/hr22+gdata/hh5+gdata/access+gdata/xp65+gdata/vk83+gdata/ol01+gdata/qv56+gdata/rt52+gdata/fs38+gdata/lg87+gdata/eg3+gdata/ct11+gdata/ik11+gdata/av17+gdata/x77+gdata/g40+gdata/v45+gdata/cj50+gdata/ia39
#PBS -m ae
#PBS -q normal
#PBS -W umask=0022
#PBS -l ncpus=16
# mem: matches access-om3-paper-1's mkfigs.sh, because this script also runs OM3 notebooks.
# Their dask Client(threads_per_worker=1) starts one worker per CPU and splits memory evenly:
# 190GB/16 = ~12GB per worker. OM3's SST.ipynb on CM3 output failed with KilledWorker at ~4.5GB
# per worker and succeeded at ~12GB. (The first CM3-only run used 63.99 of 64gb.)
# Gadi charges max(ncpus, mem/4gb) per hour, so 190GB costs the same as a whole 48-CPU node.
#PBS -l mem=190GB
#PBS -l jobfs=200GB
#PBS -l walltime=24:00:00

# Runs all the notebooks via the shared access-model-mkfigs engine (see
# external/access-model-mkfigs, a pinned git submodule -- same pattern as
# access-om3-paper-1's notebooks/mkfigs.sh). Replaces the previous
# raw-papermill version of this script.
#
## Workflow -- first run for a new experiment
#1. Create a Figshare token and save it to ~/.figshare_token
#1. `cd /g/data/$PROJECT/$USER && git clone --recurse-submodules git@github.com:ACCESS-Community-Hub/access-cm3-paper-1.git`
#1.   (already cloned without submodules? run: git submodule update --init --recursive)
#1. Edit this file: ENAME / ESMDIR below, and the notebook `array` if needed
#1. Ensure the experiment storage path is in the #PBS -l storage header above
#1. `qsub -v PROJECT="$PROJECT" mkfigs.sh`   (all notebooks, one after the other, in one job)
#1.   or, from a login node with the follow-up environment below:
#1.   `python3 -m mkfigs.submit`   (one PBS job per notebook, in parallel, plus a summary job)
#1. (login node, after the job) set up the environment for the follow-up commands -- see below
#1. `python3 -m mkfigs.pushit`
#1. Log in to Figshare and publish the article
#1. `python3 -m mkfigs.pushit --check-figshare-upload`   (follow the git commands it prints)
#
## To run follow-up commands (pushit) from a login node
## (this script only sets PYTHONPATH inside the batch job, so do it by hand here):
#   module purge; module use /g/data/xp65/public/modules; module load conda/analysis3-26.08
#   export PYTHONPATH="<WFOLDER>/external/access-model-mkfigs/src:${PYTHONPATH}"
#   cd <WFOLDER>/notebooks/polished-python
#   python3 -m mkfigs.pushit  [--dry-run] [--check-figshare-upload]
#
## Optional
#1. change email and log settings in above header
#1. this script can also be run from an ARE session

set -x
module purge
module use /g/data/xp65/public/modules
module load conda/analysis3-26.08 # same as access-om3-paper-1; has papermill and nci_ipynb (needed by mkfigs-pushit)
module list

# ---------------------------------------------------------------------------
# SET THESE
# ---------------------------------------------------------------------------
# Repo root, derived from where this script lives (notebooks/polished-python/)
# so it works from any clone location -- same approach as access-om3-paper-1.
if [ -n "$PBS_O_WORKDIR" ]; then
    WFOLDER="$(dirname "$(dirname "$PBS_O_WORKDIR")")/"
else
    WFOLDER="$(dirname "$(readlink -f "$0")")/../../"
fi
ESMDIR=/g/data/zv30/non-cmip/ACCESS-CM3/cm3-run-27-07-2026-PD-control/cm3-datastore/cm3-datastore.json
ENAME=cm3-run-27-07-2026-PD-control

# ---------------------------------------------------------------------------
# Model identity -- read by mkfigs.configdoc for the Figshare article
# title/description/keywords, instead of the ACCESS-OM3 default.
# ---------------------------------------------------------------------------
export MKFIGS_MODEL_NAME="ACCESS-CM3"
export MKFIGS_REPO_URL="https://github.com/ACCESS-Community-Hub/access-cm3-paper-1"

# ---------------------------------------------------------------------------
# access-model-mkfigs is provided via the external/access-model-mkfigs git
# submodule (pinned commit), not pip-installed.
# ---------------------------------------------------------------------------
export PYTHONPATH="${WFOLDER%/}/external/access-model-mkfigs/src:${PYTHONPATH}"

echo ""
echo "We are running ALL the notebooks."
echo "We are using ESMDIR: "${ESMDIR}
echo "We are using working folder (WFOLDER): "${WFOLDER}
echo ""

# CM3 notebooks (this directory, notebooks/polished-python/): add your script
# name to this `array` variable, spaces are between script names, script name
# does not include `*.ipynb` extension
array=(
    # 00_template_notebook   # template for new notebooks: not run or published
    global-time-series
    salinity
    water-conservation
    flux-conservation
    autocorrelation_and_amplitude
    # Bottom_age_tracer   # OM3-derived; use the #5 OM3-notebook route instead
    SST_trend_global
    TOA_CRE
    # Transects   # OM3-derived; use the #5 OM3-notebook route instead
)

# OM3 notebooks, run from the access-om3-paper-1 submodule (om3_dir, relative
# to the repo root) against this CM3 experiment. Names as in om3_dir, without
# `.ipynb`; they must not clash with a name in `array` above (both write to
# mkfigs_output_<ENAME>/). The landing page's Source column shows which repo
# each notebook came from.
#
# This list is kept by hand: it is access-om3-paper-1's own notebook `array`
# (same order), minus the notebooks that can't work on CM3 (commented out with
# the reason). OM3 notebooks don't automatically work on CM3 -- they need
# `if model_name == "ACCESS-CM3":` branches where CM3 output differs (see
# access-om3-paper-1#230). When a notebook is added to access-om3-paper-1 and
# works on CM3, add it here, plus its CM3 issue in mkfigs_issues.py. To pick up
# OM3 notebook changes, bump the submodule:
#   cd external/access-om3-paper-1 && git fetch && git checkout <commit on main>
om3_dir=external/access-om3-paper-1/notebooks
om3_array=(
    Bottom_age_tracer_in_ACCESS_OM3
    MLD
    MLD_max
    Overturning_in_ACCESS_OM3
    SeaIce_area
    SeaIce_mass_budget_climatology
    SSS
    SST
    StraitTransports
    MeridionalHeatTransport
    temp-salt-vs-depth-time
    pPV
    Equatorial_pacific
    # SSS_Restoring_Timeseries   # not expected to work on CM3: no salt_flux_added (no SSS restoring in CM3)
    Timeseries_daily_extreme_from_2D_fields
    timeseries
    # ocean_stats   # not expected to work on CM3: no ocean.stats.nc in CM3 output
    # Closure_assessment   # not expected to work on CM3: no bigthetaoga in CM3 output
    SSH
    # wombatlite_global   # not expected to work on CM3: no WOMBATlite (no3) in CM3
    Currents_streamfunction_variability
    SeaIce_Vol
    # SeaIce_speed   # not expected to work on CM3: needs sea-ice output CM3 doesn't have (empty datastore search)
    temp-salt-vs-depth-latitude
    Transects
    WM_evaluation
    MLD_manual
    Transects-mixing
    # numerical_mixing_ACCESS_OM3   # not expected to work on CM3: needs a temperature diagnostic CM3 doesn't write
    # Truncation_locations   # not expected to work on CM3: needs ocean.stats, which CM3 does not write (runs, but makes no figures)
)

# Passed to mkfigs-run as CM3 names plus <om3_dir>/<name> paths. A list given
# with `qsub -v MKFIGS_NOTEBOOKS=...` (python3 -m mkfigs.submit: one PBS job per
# notebook) is kept.
printf -v _all_notebooks '%s:' "${array[@]}" "${om3_array[@]/#/${om3_dir}/}"
MKFIGS_NOTEBOOKS="${MKFIGS_NOTEBOOKS:-${_all_notebooks%:}}"
export MKFIGS_NOTEBOOKS

# ---------------------------------------------------------------------------
# Hand off to mkfigs-run. --notebooks-subdir is needed because these
# notebooks live in notebooks/polished-python/, not directly in notebooks/
# like access-om3-paper-1's do.
# ---------------------------------------------------------------------------
cd "${WFOLDER}"
exec python3 -m mkfigs.run \
    --ename "${ENAME}" \
    --esmdir "${ESMDIR}" \
    --wfolder "${WFOLDER}" \
    --notebooks-subdir polished-python \
    "$@"
