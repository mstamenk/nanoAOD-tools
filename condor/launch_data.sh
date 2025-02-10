VERSION=v34
YEAR=$1
TYPE=$2

#python2 runHHH6b.py --option 0 -o ${VERSION} --year 2017 --run-data -n 1
#condor_submit jobs_${VERSION}_ak8_option0_2017/data/submit.cmd

#python2 runHHH6b.py --option 1 -o ${VERSION} --year 2017 --run-data -n 1
#condor_submit jobs_${VERSION}_ak8_option1_2017/data/submit.cmd

#python2 runHHH6b.py --option 2 -o ${VERSION} --year 2017 --run-data -n 1
#condor_submit jobs_${VERSION}_ak8_option2_2017/data/submit.cmd

#python2 runHHH6b.py --option 3 -o ${VERSION} --year 2017 --run-data -n 1
#condor_submit jobs_${VERSION}_ak8_option3_2017/data/submit.cmd

#python2 runHHH6bPNetAK4.py --option 4 -o ${VERSION} --year ${YEAR} --run-data -n 8
#condor_submit jobs_${VERSION}_ak8_option4_${YEAR}/data/submit.cmd

python3 runHHH6bPNetAK4.py --option 4 -o /isilon/data/users/mstamenk/hhh-6b-producer-run3/CMSSW_13_3_0/src/PhysicsTools/NanoAODTools/condor/${VERSION} --year ${YEAR} --run-data -n 1 --jobprocessor run_processor_lxplus.sh --condordesc 2 --tmpoutdir "\$TMPDIR" ${TYPE} 

#condor_submit jobs_${VERSION}_ak8_option4_${YEAR}/data/submit.cmd

