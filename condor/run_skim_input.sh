#!/bin/bash

ifile=$1
nentries=$2
tag=$3
sample=$4

# remove old
source /cvmfs/cms.cern.ch/cmsset_default.sh
rm *.tgz

# copy environment
xrdcp -f root://cmseos.fnal.gov//store/user/cmantill/CMSSW_11_1_0_pre5_PY3.tgz ./CMSSW_11_1_0_pre5_PY3.tgz
tar -zxvf CMSSW_11_1_0_pre5_PY3.tgz
rm *.tgz
cd CMSSW_*/src
scram b ProjectRename
eval `scramv1 runtime -sh`
ls -l 
export PYTHONPATH=PYTHONPATH:"${CMSSW_BASE}/lib/${SCRAM_ARCH}"
cd PhysicsTools/NanoAODTools/

# run
mkdir tmp/
python -c "import sys; print('\n'.join(sys.path))"
#python scripts/nano_postproc_custom.py tmp/ ${ifile} -I PhysicsTools.NanoNN.producers.inputProducer InputProducer --cut "(FatJet_pt>300)&&(FatJet_msoftdrop>20)" -N ${nentries} --bi scripts/branch_inputs.txt --bo scripts/branch_inputs_output.txt --perJet
python scripts/nano_postproc_custom.py tmp/ ${ifile} -I PhysicsTools.NanoNN.producers.pfProducer pfProducer --cut "(FatJet_pt>300)&&(FatJet_msoftdrop>20)" -N ${nentries} --bi scripts/branch_inputs.txt --bo scripts/branch_inputs_output.txt --perJet

# copy output
for i in tmp/*; do xrdcp -f $i root://cmseos.fnal.gov//store/user/cmantill/PFNano/training/$tag/$sample/; done

rm -rf tmp/