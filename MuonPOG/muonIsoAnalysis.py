import DataFormats.FWLite as fwlite
import python.PlotUtils as plotters
import python.IsoUtils as isoUtils

import array
import ROOT

############### CONTROL VARIABLES ##############################

SIG_INPUT_FILE = "/eos/cms/store/user/battilan/MuonPOG/DY.root"
BKG_INPUT_FILE = "/eos/cms/store/user/battilan/MuonPOG/QCDMuEnriched.root"
PLOT_FOLDER = "iso_analysis/"
MAX_EVENTS = 999999999
#MAX_EVENTS = 20000
MIN_PT = 20.0


############### ANALYSIS LOOP ##################################

def analysisLoop(inputFile, sampleLabel, histos, effs, rocs) :

    muons  = fwlite.Handle("std::vector<pat::Muon>") 
    vtxs   = fwlite.Handle("std::vector<reco::Vertex>") 

    events = fwlite.Events(inputFile)
        
    for iEv, event in enumerate(events) :

        if iEv % 10000 == 0 :
            print "[muonIsolation.py] processed %i %s entries" %  (iEv, sampleLabel)

        if iEv > MAX_EVENTS :
            break

        event.getByLabel("slimmedMuons", muons)
        event.getByLabel("offlineSlimmedPrimaryVertices", vtxs)

        nVtx = vtxs.product().size()
        
        for mu in muons.product() :
        
            muPt   = mu.pt()
            muEta  = mu.eta()
            muPhi  = mu.phi()
            
            if muPt < MIN_PT :
                continue

            pfIso04 = mu.pfIsolationR04()
            pfRelIso  = (pfIso04.sumChargedHadronPt + \
                             max(0., pfIso04.sumPhotonEt + pfIso04.sumNeutralHadronEt - 0.5 * pfIso04.sumPUPt)) / muPt;

            muIsTightIso = mu.passed(mu.PFIsoTight)

            # For DY we still use flavour to
            # ensure we look at prompt muons, this is not 
            # true for QCD, hence the following logic
            isGoodMu = (sampleLabel == "QCD" or mu.simFlavour() == 13)        

            # We want to study isolation for
            # events that already pass and ID
            muIsTight  = mu.passed(mu.CutBasedIdTight)

            if muIsTight and isGoodMu :
                histos["hPt%s"       % sampleLabel].Fill(muPt)
                histos["hNVtx%s"     % sampleLabel].Fill(nVtx)
                histos["hPfRelIso%s" % sampleLabel].Fill(min(pfRelIso,0.99))

                effs["eTightPfIsoPt%s"   % sampleLabel].Fill(muIsTightIso,muPt)
                effs["eTightPfIsoEta%s"  % sampleLabel].Fill(muIsTightIso,muEta)
                effs["eTightPfIsoNVtx%s" % sampleLabel].Fill(muIsTightIso,nVtx)

                rocs["pfTightWP"].fill(sampleLabel,pfRelIso)
                rocs["pfRelIso"].fill(sampleLabel,pfRelIso)
                
                
############### MAIN PROGRAM ################################## 

histos = {}
effs   = {}
rocs   = {}

plotTags = ["DY", "QCD"]

for plotTag in plotTags :

    histos["hPt%s" % plotTag] = ROOT.TH1F("hPt%s" % plotTag,
                                          "hPt%s;muon p_{T}; entries" % plotTag, 
                                          100, 0., 100)

    histos["hNVtx%s" % plotTag] = ROOT.TH1F("hNVtx%s" % plotTag,
                                            "hNVtx%s;# RECO vertices; entries" % plotTag, 
                                            50, 0., 100)

    histos["hPfRelIso%s" % plotTag] = ROOT.TH1F("hPfRelIso%s" % plotTag,
                                                 "hPfRelIso%s; TRK based reliso.; entries" % plotTag, 
                                                 50, 0., 1.0)

    ptBins = array.array('d',[0,5,10,15,20,25,30,40,50,60,80,100])
    effs["eTightPfIsoPt%s" % plotTag] = ROOT.TEfficiency("eTightPfIsoPt%s" % plotTag,
                                                         "eTightPfIsoPt%s;muon p_{T}; efficiency" % plotTag, 
                                                         11, ptBins)

    etaBins = array.array('d',[-2.4,-2.1,-1.6,-1.2,-0.9,-0.3,-0.2,0.2,0.3,0.9,1.2,1.6,2.1,2.4])
    effs["eTightPfIsoEta%s" % plotTag] = ROOT.TEfficiency("eTightPfIsoEta%s" % plotTag,
                                                          "eTightPfIsoEta%s;muon #eta; efficiency" % plotTag, 
                                                          13, etaBins)

    effs["eTightPfIsoNVtx%s" % plotTag] = ROOT.TEfficiency("eTightPfIsoNVtx%s" % plotTag,
                                                         "eTightPfIsoNVtx%s;# RECO vertices; efficiency" % plotTag, 
                                                           10, 5., 55.)

rocs["pfTightWP"] = isoUtils.Roc2DVec([0.15],"QCD","DY","PF RelIso WP")
rocs["pfRelIso"]  = isoUtils.Roc2DVec([0.01, 0.02, 0.04, 0.06, 0.08, 0.10, 0.20, 0.25, 0.30, 0.25, 0.40],"QCD","DY","PF RelIso")


analysisLoop(SIG_INPUT_FILE,"DY",  histos, effs, rocs)
analysisLoop(BKG_INPUT_FILE,"QCD", histos, effs, rocs)

plotters.setPlotOptions()

histosPt       = [histos["hPtDY"],       histos["hPtQCD"]      ]
histosNVtx     = [histos["hNVtxDY"],     histos["hNVtxQCD"]    ]
histosPfRelIso = [histos["hPfRelIsoDY"], histos["hPfRelIsoQCD"]]

effsPt   = [effs["eTightPfIsoPtDY"],   effs["eTightPfIsoPtQCD"]  ]
effsEta  = [effs["eTightPfIsoEtaDY"],  effs["eTightPfIsoEtaQCD"] ]
effsNVtx = [effs["eTightPfIsoNVtxDY"], effs["eTightPfIsoNVtxQCD"]]

graphsRocs  = [rocs["pfRelIso"].getGraph(), rocs["pfTightWP"].getGraph()]

canvasPt         = plotters.compareTH1Fs("histosPt",       PLOT_FOLDER, histosPt,  0.0, 0.25)
canvasNVtx       = plotters.compareTH1Fs("histosNVtx",     PLOT_FOLDER, histosNVtx,  0.0, 0.25)
canvasPfRelIso   = plotters.compareTH1Fs("histosPfRelIso", PLOT_FOLDER, histosPfRelIso,  0.001, 1.0)

canvasPfRelIso.SetLogy()
canvasPfRelIso.Update()

canvasEffPt   = plotters.compareTEfficiencies("effsPt",   PLOT_FOLDER, effsPt,   0.0, 1.0)
canvasEffEta  = plotters.compareTEfficiencies("effsEta",  PLOT_FOLDER, effsEta,  0.0, 1.0)
canvasEffNVtx = plotters.compareTEfficiencies("effsNVtx", PLOT_FOLDER, effsNVtx, 0.0, 1.0)

canvasRocs = plotters.compareGraphs("graphsRocs", PLOT_FOLDER, graphsRocs, 0.0, 1.0)
