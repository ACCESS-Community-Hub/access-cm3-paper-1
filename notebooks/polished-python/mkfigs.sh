#!/bin/bash
#PBS -l storage=gdata/zv30+gdata/p73+gdata/tm70+gdata/ki32+gdata/nf33+gdata/hr22+gdata/hh5+gdata/access+gdata/xp65+gdata/vk83+gdata/ol01+gdata/qv56+gdata/rt52+gdata/fs38+gdata/lg87+gdata/eg3+gdata/ct11+gdata/ik11+gdata/av17
#PBS -m ae
#PBS -q normal
#PBS -W umask=0022
#PBS -l ncpus=16
#PBS -l mem=64gb
#PBS -l walltime=4:00:00

# Runs all the notebooks via the shared access-model-mkfigs engine (see
# external/access-model-mkfigs, a pinned git submodule -- same pattern as
# access-om3-paper-1's notebooks/mkfigs.sh). Replaces the previous
# raw-papermill version of this script.
#
## Workflow -- first run for a new experiment
#1. Create a Figshare token and save it to ~/.figshare_token
#1. `cd /g/data/$PROJECT/$USER && git clone --recurse-submodules git@github.com:ACCESS-Community-Hub/access-cm3-paper-1.git`
#1.   (already cloned without submodules? run: git submodule update --init --recursive)
#1. Edit this file: RUN / ESMDIR below, and the notebook `array` if needed
#1. Ensure the experiment storage path is in the #PBS -l storage header above
#1. `qsub -v RUN="cm3-run-27-07-2026-PD-control",PROJECT="$PROJECT" mkfigs.sh`
#1. `python3 -m mkfigs.pushit`
#1. Log in to Figshare and publish the article
#1. `python3 -m mkfigs.pushit --check-figshare-upload`   (follow the git commands it prints)
#
## Optional
#1. change email and log settings in above header
#1. this script can also be run from an ARE session

set -x
module purge
module use /g/data/xp65/public/modules
module load conda/analysis3-25.09 # contains papermill 2.6.0
module list

# ---------------------------------------------------------------------------
# SET THESE
# ---------------------------------------------------------------------------
WFOLDER=/g/data/$PROJECT/$USER/Notebooks/access-cm3-paper-1/
ESMDIR=/g/data/zv30/non-cmip/ACCESS-CM3/${RUN}/cm3-datastore/cm3-datastore.json
ENAME=${RUN}

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

# please add your script name to this `array` variable, spaces are between
# script names, script name does not include `*.ipynb` extension
array=(
    00_template_notebook
    global-time-series
    salinity
    water-conservation
    flux-conservation
    autocorrelation_and_amplitude
    Bottom_age_tracer
    SST_trend_global
    TOA_CRE
    Transects
)

printf -v MKFIGS_NOTEBOOKS '%s:' "${array[@]}"
MKFIGS_NOTEBOOKS="${MKFIGS_NOTEBOOKS%:}"
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
