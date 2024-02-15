#!/usr/bin/bash
#SBATCH --partition=exfel
#SBATCH --time=0-00:39:00
#SBATCH --nodes=3
#SBATCH --job-name XFEL-DAQ
#SBATCH --output jobout/XFEL-DAQ-%j-%N.out
#SBATCH --error jobout/XFEL-DAQ-%j-%N.err
#SBATCH --mail-type BEGIN,END,FAIL                 # Type of email notification- BEGIN,END,FAIL,ALL
#SBATCH --mail-user christian.grech@desy.de  # Email to which notifications will be sent
#SBATCH --mail-type END
##SBATCH --nodelist=max-exfl450

. /net/xfeluser1/export/doocs/server/daq_server/ENVIRONMENT.new; 
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH_OLD:/export/doocs/lib:/net/doocsdev16/export/doocs/lib:$LD_LIBRARY_PATH; 
export PATH=/opt/anaconda/bin:$PATH:/export/doocs/bin; 
export PYTHONPATH=$PYTHONPATH_OLD:/home/doocsadm/bm/python/DAQ/classes:/export/doocs/lib:/net/doocsdev16/export/doocs/lib:$PYTHONPATH;


#  Run workflow
#
start=`date +%s`
startdate=`date`
measdate=`date +'%Y_%m_%d'`
pastdate='2023_07_20'
date=$measdate
SASE='SA1'
outdir='/pnfs/desy.de/m/projects/felrd/modeling/' 
starttime='06:55:00' 
stoptime='08:29:00' 
workdir='/home/grechc/Documents/xfel_data/'
modulesdir='/home/grechc/Documents/DAQ/modules/'

rsync -av /daq/xfel /pnfs/desy.de/m/projects/felrd/daq/

python ${modulesdir}check_SA1_datastream.py
state_SA1=$?
python ${modulesdir}check_SA2_datastream.py
state_SA2=$?
python ${modulesdir}check_SA3_datastream.py
state_SA3=$?

if [ $state_SA1 == 0 ]; then

    # 1. Folder creation
    mkdir -p "$outdir$SASE/$date"
    mkdir -p -m 777 "$outdir$SASE/$date/processed"
    mkdir -p -m 777 "$outdir$SASE/$date/tmp"

    mkdir -p -m 777 "$workdir$SASE/$date"
    echo ".....Created directory $outdir$SASE/$date"

    # 2. DOOCS raw file conversion
    python ${modulesdir}level0_maxwell.py --dest $SASE --start "$(tr -s '_' '-' <<< $date)T$starttime" --stop "$(tr -s '_' '-' <<< $date)T$stoptime" --dout "$workdir$SASE"

    find $workdir$SASE -name "xfel_sase*" -exec mv '{}' "$outdir$SASE/$date" \;
    echo ".....Moved files to $outdir$SASE/$date/"
else
    echo "No SA1 acquisition in the last hour."
fi

# SASE 2 
SASE='SA2'

if [ $state_SA2 == 0 ]; then

    # 1. Folder creation
    mkdir -p "$outdir$SASE/$date"
    mkdir -p -m 777 "$outdir$SASE/$date/processed"
    mkdir -p -m 777 "$outdir$SASE/$date/tmp"

    mkdir -p -m 777 "$workdir$SASE/$date"
    echo ".....Created directory $outdir$SASE/$date"

    # 2. DOOCS raw file conversion
    python ${modulesdir}level0_maxwell.py --dest $SASE --start "$(tr -s '_' '-' <<< $date)T$starttime" --stop "$(tr -s '_' '-' <<< $date)T$stoptime" --dout "$workdir$SASE"

    find $workdir$SASE -name "xfel_sase*" -exec mv '{}' "$outdir$SASE/$date" \;
    echo ".....Moved files to $outdir$SASE/$date/"
else
    echo "No SA2 acquisition in the last hour."
fi

# SASE 3
SASE='SA3'

if [ $state_SA3 == 0 ]; then

    # 1. Folder creation
    mkdir -p "$outdir$SASE/$date"
    mkdir -p -m 777 "$outdir$SASE/$date/processed"
    mkdir -p -m 777 "$outdir$SASE/$date/tmp"

    mkdir -p -m 777 "$workdir$SASE/$date"
    echo ".....Created directory $outdir$SASE/$date"

    # 2. DOOCS raw file conversion
    python ${modulesdir}level0_maxwell.py --dest $SASE --start "$(tr -s '_' '-' <<< $date)T$starttime" --stop "$(tr -s '_' '-' <<< $date)T$stoptime" --dout "$workdir$SASE"

    find $workdir$SASE -name "xfel_sase*" -exec mv '{}' "$outdir$SASE/$date" \;
    echo ".....Moved files to $outdir$SASE/$date/"
else
    echo "No SA3 acquisition in the last hour."
fi