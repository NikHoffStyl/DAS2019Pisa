import DataFormats.FWLite as fwlite
import python.PlotUtils as plotters
import python.RoccoR as roccor

import array
import ROOT

############### CONFIG VARIABLES ###############################

INPUT_FILE = "/gpfs/ddn/cms/user/cmsdas/2019/muon/data/ZMu.root"
PLOT_FOLDER = "scale_analysis/"
MAX_EVENTS = 999999999
#MAX_EVENTS = 50000
MIN_PT = 20.0


############### MAIN PROGRAM ################################## 

rc = roccor.RoccoR("data/RoccoR2017.txt")

events      = fwlite.Events(INPUT_FILE)
muonsHandle = fwlite.Handle("std::vector<pat::Muon>") 


############### HISTO BOOKING ################################# 

histos = {}
effs   = {}

plotTags = ["Prompt", "Corr"]

for plotTag in plotTags :

    if plotTag == "Prompt" :

            histos["hPt%s" % plotTag] = ROOT.TH1F("hPt%s" % plotTag,
                                                  "hPt%s;muon p_{T}; entries" % plotTag, 
                                                  100, 0., 100)

            histos["hEta%s" % plotTag] = ROOT.TH1F("hEta%s" % plotTag,
                                                   "hEta%s;muon #eta; entries" % plotTag, 
                                                   24, -2.4, +2.4)

            histos["hPhi%s" % plotTag] = ROOT.TH1F("hPhi%s" % plotTag,
                                                   "hPhi%s;muon #phi; entries" % plotTag, 
                                                   24, -ROOT.TMath.Pi(), ROOT.TMath.Pi())

    histos["hMass%s" % plotTag] = ROOT.TH1F("hMass%s" % plotTag,
                                            "hMass%s; m_{(mu+,mu-)}; entries" % plotTag, 
                                            40, 80., 120)

    histos["pMassVsPhiPlus%s" % plotTag] = ROOT.TProfile("pMassVsPhiPlus%s" % plotTag,
                                                         "pMassVsPhiPlus%s;muon #phi; m_{(mu+,mu-)}" % plotTag, 
                                                         12, -ROOT.TMath.Pi(), ROOT.TMath.Pi())

    histos["pMassVsPhiMinus%s" % plotTag] = ROOT.TProfile("pMassVsPhiMinus%s" % plotTag,
                                                          "pMassVsPhiMinus%s;muon #phi; m_{(mu+,mu-)}" % plotTag, 
                                                          12, -ROOT.TMath.Pi(), ROOT.TMath.Pi())
        

############### ANALYSIS LOOP ##################################

for iEv, event in enumerate(events) :

    if iEv % 10000 == 0 :
        print "[muonScaleAnalysis.py] processed", iEv, "entries\r"

    if iEv > MAX_EVENTS :
        break

    event.getByLabel("slimmedMuons", muonsHandle)
            
    muons = muonsHandle.product()
    nMuons = muons.size()

    for iMu1 in range(0, nMuons) :
        mu1 = muons[iMu1]

        mu1Tk = ROOT.TLorentzVector()
        mu1Tk.SetPtEtaPhiM(mu1.pt(),mu1.eta(),mu1.phi(),0.106)

        for iMu2 in range(iMu1+1, nMuons) :
            mu2 = muons[iMu2]

            mu2Tk = ROOT.TLorentzVector()
            mu2Tk.SetPtEtaPhiM(mu2.pt(),mu2.eta(),mu2.phi(),0.106)

            mass = (mu1Tk + mu2Tk).M()

            if mu1.pt() > MIN_PT and \
               mu2.pt() > MIN_PT and \
               mu1.passed(mu1.CutBasedIdTight) and \
               mu2.passed(mu2.CutBasedIdTight) and \
               mu1.passed(mu1.PFIsoTight) and \
               mu2.passed(mu2.PFIsoTight) and \
               mu1.charge() * mu2.charge() == -1 and \
               mass > 80. and mass < 120. :
                
                mu1Corr = rc.kScaleDT(mu1.charge(),mu1.pt(),mu1.eta(),mu1.phi())
                mu2Corr = rc.kScaleDT(mu2.charge(),mu2.pt(),mu2.eta(),mu2.phi())

                mu1TkCorr = ROOT.TLorentzVector()
                mu1TkCorr.SetPtEtaPhiM(mu1.pt()*mu1Corr,mu1.eta(),mu1.phi(),0.106)

                mu2TkCorr = ROOT.TLorentzVector()
                mu2TkCorr.SetPtEtaPhiM(mu2.pt()*mu2Corr,mu2.eta(),mu2.phi(),0.106)

                massCorr = (mu1TkCorr + mu2TkCorr).M()

                histos["hMassPrompt"].Fill(mass)
                histos["hMassCorr"].Fill(massCorr)

                histos["hPtPrompt"].Fill(mu1.pt())
                histos["hEtaPrompt"].Fill(mu1.eta())
                histos["hPhiPrompt"].Fill(mu1.phi())

                histos["hPtPrompt"].Fill(mu2.pt())
                histos["hEtaPrompt"].Fill(mu2.eta())
                histos["hPhiPrompt"].Fill(mu2.phi())

                if mass > 86. and mass < 96. :
                    if mu1.charge() > 0 and mu1.eta() > 2.0 :
                        histos["pMassVsPhiPlusPrompt"].Fill(mu1.phi(), mass)
                    if mu2.charge() > 0 and mu2.eta() > 2.0 :
                        histos["pMassVsPhiPlusPrompt"].Fill(mu2.phi(), mass)

                    if mu1.charge() < 0 and mu1.eta() > 2.0 :
                        histos["pMassVsPhiMinusPrompt"].Fill(mu1.phi(), mass)
                    if mu2.charge() < 0 and mu2.eta() > 2.0 :
                        histos["pMassVsPhiMinusPrompt"].Fill(mu2.phi(), mass)

                if massCorr > 86. and massCorr < 96. :
                    if mu1.charge() > 0 and mu1.eta() > 2.0 :
                        histos["pMassVsPhiPlusCorr"].Fill(mu1.phi(), massCorr)
                    if mu2.charge() > 0 and mu2.eta() > 2.0 :
                        histos["pMassVsPhiPlusCorr"].Fill(mu2.phi(), massCorr)

                    if mu1.charge() < 0 and mu1.eta() > 2.0 :
                        histos["pMassVsPhiMinusCorr"].Fill(mu1.phi(), massCorr)
                    if mu2.charge() < 0 and mu2.eta() > 2.0 :
                        histos["pMassVsPhiMinusCorr"].Fill(mu2.phi(), massCorr)


############### HISTO PLOTTING ################################ 

plotters.setPlotOptions()

histosPt   = [histos["hPtPrompt"]]
histosEta  = [histos["hEtaPrompt"]]
histosPhi  = [histos["hPhiPrompt"]]

histosMass = [histos["hMassPrompt"], histos["hMassCorr"]]
histosMassVsPhi     = [histos["pMassVsPhiPlusPrompt"], histos["pMassVsPhiMinusPrompt"]]
histosMassVsPhiCorr = [histos["pMassVsPhiPlusCorr"],   histos["pMassVsPhiMinusCorr"]]

canvasPt   = plotters.compareTH1Fs("histosPt",   PLOT_FOLDER, histosPt,   0.0, 0.1)
canvasEta  = plotters.compareTH1Fs("histosEta",  PLOT_FOLDER, histosEta,  0.0, 0.1)
canvasPhi  = plotters.compareTH1Fs("histosPhi",  PLOT_FOLDER, histosPhi,  0.0, 0.1)

canvasMass          = plotters.compareTH1Fs("histosMass",          PLOT_FOLDER, histosMass,          0.0, 0.2)
canvasMassVsPhi     = plotters.compareTH1Fs("histosMassVsPhi",     PLOT_FOLDER, histosMassVsPhi,     90.4, 91.4, False)
canvasMassVsPhiCorr = plotters.compareTH1Fs("histosMassVsPhiCorr", PLOT_FOLDER, histosMassVsPhiCorr, 90.4, 91.4, False)

