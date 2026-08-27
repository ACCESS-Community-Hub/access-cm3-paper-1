#!/bin/bash
#PBS -l storage=gdata/eg3+gdata/ct11+gdata/fs38+gdata/xp65+gdata/zv30
#PBS -M christine.chung@bom.gov.au
#PBS -m ae
#PBS -q normal
#PBS -W umask=0022
#PBS -l ncpus=8
#PBS -l mem=24gb
#PBS -l walltime=2:00:00
#PBS -o /g/data/eg3/cxc548/logs
#PBS -e /g/data/eg3/cxc548/logs

# bash script that runs all the notebooks
#set -x
module purge
module use /g/data/xp65/public/modules
module load conda/analysis3-25.09 #contains papermill 2.6.0 - https://github.com/ACCESS-NRI/ACCESS-Analysis-Conda/issues/310
module list

## workflow
#1. `cd /g/data/tm70/cyb561;git clone git@github.com:ACCESS-Community-Hub/access-cm3-paper-1.git`
#1. Edit this file and `chmod u+x mkfigs.sh`
#1. add path to WFOLDER
#1. set path to ESMDIR (ESM-datastore for experiment)
#1. ensure the experiment folder is availble in storage header above
#1. `qsub mkfigs.sh`

## Optional
#1. change email and log settings in above header
#1. this script can also be run from an ARE session


# SET THESE START
WFOLDER=/home/548/cxc548/nesp/eval_metrics/access_cm3/access-cm3-paper-1/notebooks/sandbox-python/
ESMDIR=/g/data/zv30/non-cmip/ACCESS-CM3/cm3-run-11-08-2025-25km-beta-om3-new-um-params/cm3-demo-datastore/cm3-demo-datastore.json

# SET THESE END

#best not mess with the path here...
OFOL=/g/data/eg3/cxc548/access-cm3-paper-1/notebooks/mkfigs_cm3/

cd ${WFOLDER}
#cd notebooks
mkdir -p ${OFOL}

echo ""
echo ""
echo "We are running ALL the notebooks."
echo "We are using ESMDIR: "${ESMDIR}
echo "We are using working folder (WFOLDER): "${WFOLDER}
echo "Output will be in: "${OFOL}
echo ""
echo ""

#make the figures
array=( mean_state_eval decadal_eval eofs ENSO_IOD_properties )

for FNAME in "${array[@]}"
do
    echo "Running notebook: "${FNAME}".ipynb"
    python3 run_nb.py ${FNAME}.ipynb; papermill ${FNAME}.ipynb ${OFOL}${FNAME}_rendered.ipynb -p esm_file ${ESMDIR} -p plotfolder ${OFOL} ; jupyter nbconvert --to markdown ${OFOL}${FNAME}_rendered.ipynb
done
