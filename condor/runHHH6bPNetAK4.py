#!/usr/bin/env python
from __future__ import print_function

import os
import copy

from runPostProcessing import get_arg_parser, run
import logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

nn_cfgname = 'hhh6b_cfg.json'
#default_config = {'run_mass_regression': False, 'mass_regression_versions': ['V01a', 'V01b', 'V01c'],
#                  'WRITE_CACHE_FILE': False,
#                  'jec': False, 'jes': None, 'jes_source': '', 'jes_uncertainty_file_prefix': '',
#                  'jer': 'nominal', 'met_unclustered': None, 'smearMET': True, 'applyHEMUnc': False,
#                  'allJME': False,
#}

default_config = {}

golden_json = {
    "2016APV": 'Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt',
    "2016"   : 'Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt',
    "2017"   : 'Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt',
    "2018"   : 'Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt',
    "2022"   : 'Cert_Collisions2022_355100_362760_Golden.json',
    "2022EE" : 'Cert_Collisions2022_355100_362760_Golden.json',
}

hlt_paths = {
            '2016':['HLT_QuadJet45_TripleBTagCSV_p087','HLT_PFHT400_SixJet30_DoubleBTagCSV_p056','HLT_PFHT450_SixJet40_BTagCSV_p056','HLT_AK8PFJet360_TrimMass30','HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV_p20','HLT_AK8PFJet450','HLT_QuadPFJet_BTagCSV_p016_p11_VBF_Mqq200','HLT_AK8PFHT600_TrimR0p1PT0p03Mass50_BTagCSV_p20','HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV_p20','HLT_PFJet450','HLT_QuadJet45_DoubleBTagCSV_p087','HLT_IsoMu24'],
            #'2016':['HLT_QuadJet45_TripleBTagCSV_p087','HLT_DoubleJet90_Double30_TripleBTagCSV_p087','HLT_IsoMu24'],
            #'2016APV':['HLT_QuadJet45_TripleBTagCSV_p087','HLT_DoubleJet90_Double30_TripleBTagCSV_p087','HLT_IsoMu24'],
        '2016APV':['HLT_QuadJet45_TripleBTagCSV_p087','HLT_PFHT400_SixJet30_DoubleBTagCSV_p056','HLT_PFHT450_SixJet40_BTagCSV_p056','HLT_AK8PFJet360_TrimMass30','HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV_p20','HLT_AK8PFJet450','HLT_QuadPFJet_BTagCSV_p016_p11_VBF_Mqq200','HLT_AK8PFHT600_TrimR0p1PT0p03Mass50_BTagCSV_p20','HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV_p20','HLT_PFJet450','HLT_PFMET120_BTagCSV_p067','HLT_QuadJet45_DoubleBTagCSV_p087','HLT_IsoMu24'],
#       '2016PostAPV' : ' HLT_QuadJet45_TripleBTagCSV_p087||  HLT_PFHT400_SixJet30_DoubleBTagCSV_p056||  HLT_PFHT450_SixJet40_BTagCSV_p056||  HLT_AK8PFJet360_TrimMass30||  HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV_p20||  HLT_AK8PFJet450||  HLT_QuadPFJet_BTagCSV_p016_p11_VBF_Mqq200||  HLT_AK8PFHT600_TrimR0p1PT0p03Mass50_BTagCSV_p20||  HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV_p20||  HLT_PFJet450||  HLT_QuadJet45_DoubleBTagCSV_p087 ',
        '2017':['HLT_PFJet450','HLT_PFJet500','HLT_PFHT1050','HLT_AK8PFJet550','HLT_AK8PFJet360_TrimMass30','HLT_AK8PFJet400_TrimMass30','HLT_AK8PFHT750_TrimMass50','HLT_AK8PFJet330_PFAK8BTagCSV_p17','HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0','HLT_PFMET100_PFMHT100_IDTight_CaloBTagCSV_3p1','HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2','HLT_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2','HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5','HLT_QuadPFJet98_83_71_15_DoubleBTagCSV_p013_p08_VBF1','HLT_QuadPFJet98_83_71_15_BTagCSV_p013_VBF2','HLT_IsoMu24'],
        #'2017':['HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0','HLT_IsoMu24'],
        '2018':['HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5','HLT_PFHT1050','HLT_PFJet500','HLT_AK8PFJet500','HLT_AK8PFJet400_TrimMass30','HLT_AK8PFHT800_TrimMass50','HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4','HLT_QuadPFJet103_88_75_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1','HLT_QuadPFJet103_88_75_15_PFBTagDeepCSV_1p3_VBF2','HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94','HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59','HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17','HLT_QuadPFJet98_83_71_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1','HLT_QuadPFJet98_83_71_15_PFBTagDeepCSV_1p3_VBF2','HLT_PFMET100_PFMHT100_IDTight_CaloBTagDeepCSV_3p1','HLT_IsoMu24'],
        #'2018':['HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5','HLT_IsoMu24']

        }



# Sum$() counts the number of FatJets that satisfy that condition
cut_dict_ak8 = {
    '5': 'Sum$(FatJet_pt > 250)>0 && Sum$((FatJet_ParticleNetMD_probXbb/(1.0-FatJet_ParticleNetMD_probXcc-FatJet_ParticleNetMD_probXqq))>0.8)>0',
    '10': 'Sum$(FatJet_pt > 200)>0',
    '21': 'Sum$(FatJet_pt > 200)>0',
    '8': 'Sum$(FatJet_pt > 200)>0',
    '0': '1',
    '1': '1',
    '2': '1',
    '3': '1',
    '4': 'nJet >= 4',
    #'4': 'nJet > -1',
}

# set samples to None this if you want to run over all the samples (e.g. for data)
# else, you can use this dict
samples = {
    '2016': [
        "WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8",
        "ZZZ_TuneCP5_13TeV-amcatnlo-pythia8",
        "WZZ_TuneCP5_13TeV-amcatnlo-pythia8",
        "WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8",
        "WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8_ext1",
        "ZZZ_TuneCP5_13TeV-amcatnlo-pythia8_ext1",
        "WZZ_TuneCP5_13TeV-amcatnlo-pythia8_ext1",
        "WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8_ext1",
        ],

    '2016APV': [
        "WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8",
        "ZZZ_TuneCP5_13TeV-amcatnlo-pythia8",
        "WZZ_TuneCP5_13TeV-amcatnlo-pythia8",
        "WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8",
        "WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8_ext1",
        "ZZZ_TuneCP5_13TeV-amcatnlo-pythia8_ext1",
        "WZZ_TuneCP5_13TeV-amcatnlo-pythia8_ext1",
        "WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8_ext1",

        ],
    '2017': [
        "WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8",
        "ZZZ_TuneCP5_13TeV-amcatnlo-pythia8",
        "WZZ_TuneCP5_13TeV-amcatnlo-pythia8",
        "WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8",
        "WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8_ext1",
        "ZZZ_TuneCP5_13TeV-amcatnlo-pythia8_ext1",
        "WZZ_TuneCP5_13TeV-amcatnlo-pythia8_ext1",
        "WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8_ext1",
    ],
    '2018': [
        #"WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8",
        #"ZZZ_TuneCP5_13TeV-amcatnlo-pythia8",
        #"WZZ_TuneCP5_13TeV-amcatnlo-pythia8",
        #"WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8",
        #"WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8_ext1",
        #"ZZZ_TuneCP5_13TeV-amcatnlo-pythia8_ext1",
        #"WZZ_TuneCP5_13TeV-amcatnlo-pythia8_ext1",
        #"WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8_ext1",
        "QCD_HT100to200_TuneCP5_13TeV-madgraphMLM-pythia8",
        "QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8",
        "QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8",
        "QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8",
        "QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8",
        "QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8",
        "QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8",
        "QCD_HT2000ToInf_TuneCP5_13TeV-madgraphMLM-pythia8",
    ],
}
#samples = None 

def _process(args):
    args.jet_type = 'ak8'
    default_config['jetType'] = args.jet_type
    if args.run_mass_regression:
        default_config['run_mass_regression'] = True
        if args.jet_type == 'ak8':
            default_config['mass_regression_versions'] = ['ak8V01a', 'ak8V01b', 'ak8V01c']
        logging.info('Will run mass regression version(s): %s' % ','.join(default_config['mass_regression_versions']))
    year = args.year
    option = args.option
    default_config['year'] = year
    default_config['option'] = option

    args.weight_file = 'samples/xSections.dat' if year in ["2016APV", "2016", "2017", "2018"] else 'samples/xSections_Run3.dat'
    if not args.weight_file.startswith("/"): args.weight_file = os.path.join(os.getcwd(), args.weight_file)
    basename = os.path.basename(args.outputdir) + '_' + args.jet_type + '_option' + option + '_' + year

    args.outputdir = os.path.join(os.path.dirname(args.outputdir), basename, 'data' if args.run_data else 'mc')
    args.jobdir = os.path.join('jobs_%s' % basename, 'data' if args.run_data else 'mc')
    if args.run_signal:
        args.outputdir = args.outputdir.replace('mc','signal')
        args.jobdir = os.path.join('jobs_%s' % basename, 'signal')

    sample_str = "hhh6bPNetAK4"
    if option == "10": sample_str = "tt"
    if option == "21": sample_str = "vqq"

    if args.run_data:
        args.datasets = '%s/%s_%s_DATA.yaml' % (args.sample_dir, sample_str, year)
        args.extra_transfer = os.path.expandvars(
            '$CMSSW_BASE/src/PhysicsTools/NanoNN/data/JSON/%s' % golden_json[year])
        args.json = golden_json[year]
    elif args.run_signal:
        args.datasets = '%s/%s_%s_signalMC.yaml' % (args.sample_dir, sample_str, year)

    else:
        args.datasets = '%s/%s_%s_MC.yaml' % (args.sample_dir, sample_str, year)
        #args.datasets = '%s/%s_%d_qcd.yaml' % (args.sample_dir, sample_str, year)
        if samples:
            args.select = ','.join(samples[args.year])

    if args.run_signal:
        args.imports = [('PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule',
                              'countHistogramsProducer')]
        args.imports.extend([('PhysicsTools.NanoNN.producers.hhh6bProducerPNetAK4','hhh6bProducerPNetAK4FromConfig')])
    else:
        args.imports = [('PhysicsTools.NanoNN.producers.hhh6bProducerPNetAK4','hhh6bProducerPNetAK4FromConfig')]
        #if option == '4':
        #    hlt = '||'.join(hlt_paths[str(year)])
        #    #args.cut = cut_dict_ak8[str(option)]%(hlt)
        #    args.cut = cut_dict_ak8[str(option)]
        #else:
    args.cut = cut_dict_ak8[str(option)]

    if not args.run_data:
        args.imports.extend([('PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer',
                              'puAutoWeight_2017' if year == "2017" else 'puWeight_%s' % year)])

    # select branches
    args.branchsel_in = None
    if year in ["2016APV", "2016", "2017", "2018"]:
        args.branchsel_out = os.path.expandvars('$CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/branch_hhh6b_output.txt')
    else:
        args.branchsel_out = os.path.expandvars('$CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/branch_hhh6b_output_Run3.txt')

    # data, or just nominal MC
    if args.run_data or not args.run_syst:
        cfg = copy.deepcopy(default_config)
        # set all JME to true
        cfg['allJME'] = False #fix later
        if args.run_data:
            cfg['allJME'] = False
            cfg['jes'] = None
            cfg['jer'] = None
            cfg['met_unclustered'] = None
        print('run ', args, nn_cfgname)
        run(args, configs={nn_cfgname: cfg})
        return

    # MC for syst
    if args.run_syst and not args.run_data:

        # nominal w/ PDF/Scale weights
        '''
        logging.info('Start making nominal trees with PDF/scale weights...')
        syst_name = 'LHEWeight'
        opts = copy.deepcopy(args)
        cfg = copy.deepcopy(default_config)
        opts.outputdir = os.path.join(os.path.dirname(opts.outputdir), syst_name)
        opts.jobdir = os.path.join(os.path.dirname(opts.jobdir), syst_name)
        opts.branchsel_out = os.path.expandvars('$CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/branch_hh4b_output_LHEweights.txt'
        run(opts, configs={nn_cfgname: cfg})
        '''

        # JES up/down
        for variation in ['up', 'down']:
            syst_name = 'jes_%s' % variation
            logging.info('Start making %s trees...' % syst_name)
            opts = copy.deepcopy(args)
            cfg = copy.deepcopy(default_config)
            cfg['jes'] = variation
            opts.outputdir = os.path.join(os.path.dirname(opts.outputdir), syst_name)
            opts.jobdir = os.path.join(os.path.dirname(opts.jobdir), syst_name)
            if args.run_signal:
                print('run signal')
                opts.outputdir = opts.outputdir+'_signal'
                opts.jobdir = opts.jobdir+'_signal'
            run(opts, configs={nn_cfgname: cfg})

        # JER up/down
        for variation in ['up', 'down']:
            syst_name = 'jer_%s' % variation
            logging.info('Start making %s trees...' % syst_name)
            opts = copy.deepcopy(args)
            cfg = copy.deepcopy(default_config)
            cfg['jer'] = variation
            opts.outputdir = os.path.join(os.path.dirname(opts.outputdir), syst_name)
            opts.jobdir = os.path.join(os.path.dirname(opts.jobdir), syst_name)
            if args.run_signal:
                print('run signal')
                opts.outputdir = opts.outputdir+'_signal'
                opts.jobdir = opts.jobdir+'_signal'
            run(opts, configs={nn_cfgname: cfg})

        for variation in ['up', 'down']:
            syst_name = 'jmr_%s' % variation
            logging.info('Start making %s trees...' % syst_name)
            opts = copy.deepcopy(args)
            cfg = copy.deepcopy(default_config)
            cfg['jmr'] = variation
            opts.outputdir = os.path.join(os.path.dirname(opts.outputdir), syst_name)
            opts.jobdir = os.path.join(os.path.dirname(opts.jobdir), syst_name)
            if args.run_signal:
                print('run signal')
                opts.outputdir = opts.outputdir+'_signal'
                opts.jobdir = opts.jobdir+'_signal'
            run(opts, configs={nn_cfgname: cfg})

        # MET unclustered up/down
        '''
        for variation in ['up', 'down']:
            syst_name = 'met_%s' % variation
            logging.info('Start making %s trees...' % syst_name)
            opts = copy.deepcopy(args)
            cfg = copy.deepcopy(default_config)
            cfg['met_unclustered'] = variation
            opts.outputdir = os.path.join(os.path.dirname(opts.outputdir), syst_name)
            opts.jobdir = os.path.join(os.path.dirname(opts.jobdir), syst_name)
            run(opts, configs={nn_cfgname: cfg})
        '''

def main():
    parser = get_arg_parser()

    parser.add_argument('--option',
                        type=str,
                        required=True,
                        help='Selection option'
                        )

    parser.add_argument('--run-syst',
                        action='store_true', default=False,
                        help='Run all the systematic trees. Default: %(default)s'
                        )

    parser.add_argument('--run-data',
                        action='store_true', default=False,
                        help='Run over data. Default: %(default)s'
                        )

    parser.add_argument('--run-signal',
                        action='store_true', default=False,
                        help='Run over signal. Default: %(default)s'
                        )

    parser.add_argument('--year',
                        type=str,
                        required=True,
                        help='Year: 2016APV, 2016, 2017, 2018, 2022, 2022EE or comma separated list e.g., `2016APV,2016,2017,2018`'
                        )

    parser.add_argument('--sample-dir',
                        type=str,
                        default='samples',
                        help='Directory of the sample list files. Default: %(default)s'
                        )

    parser.add_argument('--run-mass-regression',
                        action='store_true', default=False,
                        help='Run mass regression. Default: %(default)s'
                        )

    args = parser.parse_args()
    years = args.year.split(',')
    categories = ['data' if args.run_data else 'mc']

    for year in years:
        for cat in categories:
            opts = copy.deepcopy(args)
            if cat == 'data':
                opts.run_data = True
                #opts.nfiles_per_job *= 2
            opts.year = year
            logging.info('year=%s, cat=%s, syst=%s', opts.year,
                         'data' if opts.run_data else 'mc', 'syst' if opts.run_syst else 'none')
            _process(opts)


if __name__ == '__main__':
    main()
