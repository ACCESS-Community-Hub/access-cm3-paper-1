#!/bin/bash
#PBS -l storage=gdata/eg3+gdata/ct11+gdata/fs38+gdata/xp65+gdata/p66+scratch/p66
#PBS -M christine.chung@bom.gov.au
#PBS -m ae
#PBS -q normal
#PBS -W umask=0022
#PBS -l ncpus=8
#PBS -l mem=24gb
#PBS -l walltime=6:00:00
#PBS -o /g/data/eg3/cxc548/esm16logs_tauu
#PBS -e /g/data/eg3/cxc548/esm16logs_tauu

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
#WFOLDER=/g/data/eg3/cxc548/access-cm3-paper-1/
WFOLDER=/home/548/cxc548/nesp/eval_metrics/access-cm3-paper-1/notebookx/sandbox-python/ENSO_recipes/
ESMDIR=/scratch/p66/yz9299/OCT_B/tauu_Amon_ACCESS-ESM1-5_piControl_r1i1p1f1_gn_144401-184312.nc
STARTYR=1444
ENDYR=1644
LABEL='OctB'
# SET THESE END

#best not mess with the path here...
OFOL=/g/data/eg3/cxc548/nesp/ACCESS_testing/notebooks/mkfigs_esm16/

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
array=( 04-eq_Taux_bias 08-eq_Taux_sea_cycle )

for FNAME in "${array[@]}"
do
    echo "Running notebook: "${FNAME}".ipynb"
    python3 /home/548/cxc548/nesp/eval_metrics/ACCESS-eval/run_nb.py ${FNAME}.ipynb; papermill ${FNAME}.ipynb ${OFOL}${FNAME}_rendered.ipynb -p esm_file ${ESMDIR} -p plotfolder ${OFOL} -p startyear ${STARTYR} -p endyear ${ENDYR} -p mylabel ${LABEL}; jupyter nbconvert --to markdown ${OFOL}${FNAME}_rendered.ipynb
done
