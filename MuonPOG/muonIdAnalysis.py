import DataFormats.FWLite as fwlite
import python.PlotUtils as plotters

import array
import ROOT

############### CONFIG VARIABLES ###############################

INPUT_FILE  = "/gpfs/ddn/cms/user/cmsdas/2019/muon/data/ttbar.root"
PLOT_FOLDER = "id_analysis/"
MAX_EVENTS = 999999999
#MAX_EVENTS = 20000
MIN_PT = 15.0


############### MAIN PROGRAM ################################## 

events = fwlite.Events(INPUT_FILE)
muons  = fwlite.Handle("std::vector<pat::Muon>") 


############### HISTO BOOKING ################################# 

histos = {}
effs   = {}

plotTags = ["Prompt", "HeavyF", "LightF"]

for plotTag in plotTags :

    histos["hPt%s" % plotTag] = ROOT.TH1F("hPt%s" % plotTag,
                                          "hPt%s;muon p_{T}; entries" % plotTag, 
                                          100, 0., 100)

    histos["hEta%s" % plotTag] = ROOT.TH1F("hEta%s" % plotTag,
                                           "hEta%s;muon #eta; entries" % plotTag, 
                                           24, -2.4, +2.4)

    histos["hPhi%s" % plotTag] = ROOT.TH1F("hPhi%s" % plotTag,
                                           "hPhi%s;muon #phi; entries" % plotTag, 
                                           24, -ROOT.TMath.Pi(), ROOT.TMath.Pi())

##    histos["hSegComp%s" % plotTag] = ROOT.TH1F("hSegComp%s" % plotTag,
##                                               "hSegComp%s; segment compatibility; entries" % plotTag, 
##                                               20, 0., 1.0)

##    effTags  = ["Medium", "Tight"]
##
##    for effTag in effTags :
##        
##        ptBins = array.array('d',[0,5,10,15,20,25,30,40,50,60,80,100])
##        effs["ePt%s%s" % (plotTag, effTag)] = ROOT.TEfficiency("ePt%s%s" % (plotTag, effTag) ,
##                                                               "ePt%s%s;muon p_{T}; efficiency" % (plotTag, effTag), 
##                                                               11, ptBins)
##
##        etaBins = array.array('d',[-2.4,-2.1,-1.6,-1.2,-0.9,-0.3,-0.2,0.2,0.3,0.9,1.2,1.6,2.1,2.4])
##        effs["eEta%s%s" % (plotTag, effTag)] = ROOT.TEfficiency("eEta%s%s" % (plotTag, effTag),
##                                                                "eEta%s%s;muon #eta; efficiency" % (plotTag, effTag), 
##                                                                13, etaBins)

        
############### ANALYSIS LOOP ##################################

for iEv, event in enumerate(events) :

    if iEv % 10000 == 0 :
        print "[muonIdVariables.py] processed", iEv, "entries\r"

    if iEv > MAX_EVENTS :
        break

    event.getByLabel("slimmedMuons", muons)
        
    for mu in muons.product() :
        
        muPt  = mu.pt()
        muEta = mu.eta()
        muPhi = mu.phi()

        if muPt < MIN_PT :
            continue

        muIsTrkOrGlb = mu.isTrackerMuon() or mu.isGlobalMuon()

        # more in : https://github.com/cms-sw/cmssw/blob/CMSSW_10_2_X/DataFormats/PatCandidates/interface/Muon.h#L286-L290
        muSimFlavour = mu.simFlavour()        

        # Track quality plots: just look at muons that have an inner 
        # track standalone-only muons aren't typically used in analyses
        if muIsTrkOrGlb :

            if mu.simFlavour() == 13 :
                histos["hPtPrompt"].Fill(muPt)
                histos["hEtaPrompt"].Fill(muEta)
                histos["hPhiPrompt"].Fill(muPhi)

            if mu.simFlavour() > 0 and  mu.simFlavour() < 4 :
                histos["hPtLightF"].Fill(muPt)
                histos["hEtaLightF"].Fill(muEta)
                histos["hPhiLightF"].Fill(muPhi)

            if mu.simFlavour() > 3 and  mu.simFlavour() < 6 :
                histos["hPtHeavyF"].Fill(muPt)
                histos["hEtaHeavyF"].Fill(muEta)
                histos["hPhiHeavyF"].Fill(muPhi)


############### HISTO PLOTTING ################################ 

plotters.setPlotOptions()

histosPt  = [histos["hPtPrompt"],  histos["hPtHeavyF"],  histos["hPtLightF"] ]
histosEta = [histos["hEtaPrompt"], histos["hEtaHeavyF"], histos["hEtaLightF"]]
histosPhi = [histos["hPhiPrompt"], histos["hPhiHeavyF"], histos["hPhiLightF"]]

## histosSegComp = [histos["hSegCompPrompt"], histos["hSegCompHeavyF"], histos["hSegCompLightF"]]

## effsPtMedium  = [effs["ePtPromptMedium"],  effs["ePtHeavyFMedium"],  effs["ePtLightFMedium"] ]
## effsPtTight   = [effs["ePtPromptTight"],   effs["ePtHeavyFTight"],   effs["ePtLightFTight"]  ]
## effsEtaMedium = [effs["eEtaPromptMedium"], effs["eEtaHeavyFMedium"], effs["eEtaLightFMedium"]]
## effsEtaTight  = [effs["eEtaPromptTight"],  effs["eEtaHeavyFTight"],  effs["eEtaLightFTight"] ]

canvasPt  = plotters.compareTH1Fs("histosPt",  PLOT_FOLDER, histosPt,  0.0, 0.25)
canvasEta = plotters.compareTH1Fs("histosEta", PLOT_FOLDER, histosEta, 0.0, 0.15)
canvasPhi = plotters.compareTH1Fs("histosPhi", PLOT_FOLDER, histosPhi, 0.0, 0.15)

## canvasSegComp = plotters.compareTH1Fs("histosSegComp", PLOT_FOLDER, histosSegComp, 0.0, 0.4)

## canvasPtMedium = plotters.compareTEfficiencies("effsPtMedium",   PLOT_FOLDER, effsPtMedium, 0.0, 1.0)
## canvasPtTight  = plotters.compareTEfficiencies("effsPtTight",    PLOT_FOLDER, effsPtTight, 0.0, 1.0)
## canvasEtaMedium = plotters.compareTEfficiencies("effsEtaMedium", PLOT_FOLDER, effsEtaMedium, 0.0, 1.0)
## canvasEtaTight  = plotters.compareTEfficiencies("effsEtaTight",  PLOT_FOLDER, effsEtaTight, 0.0, 1.0)

