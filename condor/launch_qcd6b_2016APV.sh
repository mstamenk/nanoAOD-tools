VERSION=v19-6jets-BDT-BTAG

python2 runHHH6b.py --option 4 -o ${VERSION} --year 2016APV -n 1
condor_submit jobs_${VERSION}_ak8_option4_2016APV/mc/submit.cmd
