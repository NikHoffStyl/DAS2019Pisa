import DataFormats.FWLite as fwlite
import ROOT

events = fwlite.Events("/eos/cms/store/user/battilan/MuonPOG/ttbar.root")
muons  = fwlite.Handle("std::vector<pat::Muon>") 

h_simTypeVsFlavour = ROOT.TH2F("simTypeVsFlavour",
                               "simTypeVsFlavour; sim type; sim", 
                               2001, -0.5, 2000.5, 41, -20.5, 20.5)


hPt = {}
hEta = {}
hPhi = {}
hSegComp = {}

ePt = {}
eEta = {}

plotTags = ["Prompt", "HeavyF", "LightF"]
effTags  = ["Loose", "Medium", "Tight"]

for plotTag in plotTags :

    hPt[plotTag] = ROOT.TH1F("hPt%s" % plotTag,
                             "hPt%s;muon p_{T}; entries" % plotTag, 
                             100, 0., 100)

    hEta[plotTag] = ROOT.TH1F("hEta%s" % plotTag,
                              "hEta%s;muon #eta; entries" % plotTag, 
                              24, -2.4, +2.4) #CB cambia con pT bin variabili

    hPhi[plotTag] = ROOT.TH1F("hPhi%s" % plotTag,
                              "hPhi%s;muon #phi; entries" % plotTag, 
                              24, -ROOT.TMath.Pi(), ROOT.TMath.Pi())

    hSegComp[plotTag] = ROOT.TH1F("hSegComp%s" % plotTag,
                                  "hSegComp%s; segment compatibility; entries" % plotTag, 
                                  20, 0., 1.0)


    for effTag in effTags :
        
        ePt[plotTag + effTag] = ROOT.TEfficiency("ePt%s%s" % (plotTag, effTag) ,
                                                 "ePt%s%s;muon p_{T}; efficiency" % (plotTag, effTag), 
                                                 20, 0., 100)

        eEta[plotTag + effTag] = ROOT.TH1F("eEta%s%s" % (plotTag, effTag),
                                           "eEta%s%s;muon #eta; efficiency" % (plotTag, effTag), 
                                           24, -2.4, +2.4) #CB cambia con pT bin variabili
        
        
for iEv, event in enumerate(events) :

    if iEv % 10000 == 0 :
        print "[muonIdVariables.py] processed", iEv, "entries\r"

    event.getByLabel("slimmedMuons", muons)
        
    for mu in muons.product() :
        
        muPt = mu.pt()
        muEta = mu.eta()
        muPhi = mu.phi()

        muIsTrk      = mu.isTrackerMuon()
        muIsTrkOrGlb = mu.isTrackerMuon() or mu.isGlobalMuon()

        muSegmComp = mu.segmentCompatibility()

        muIsLoose  = mu.passed(mu.CutBasedIdLoose) 
        muIsMedium = mu.passed(mu.CutBasedIdMedium) 
        muIsTight  = mu.passed(mu.CutBasedIdTight) 
        
        muSimType = min(mu.simType(), 2000)
        muSimFlavour = mu.simFlavour()        

        if muIsTrkOrGlb and muIsLoose:

            if mu.simFlavour() == 13 :
                hPt["Prompt"].Fill(muPt)
                hEta["Prompt"].Fill(muEta)
                hPhi["Prompt"].Fill(muPhi)

                hSegComp["Prompt"].Fill(muSegmComp)

                ePt["PromptLoose"].Fill(muIsLoose, muPt)
                ePt["PromptMedium"].Fill(muIsMedium, muPt)
                ePt["PromptTight"].Fill(muIsTight, muPt)

                eEta["PromptLoose"].Fill(muIsLoose, muEta)
                eEta["PromptMedium"].Fill(muIsMedium, muEta)
                eEta["PromptTight"].Fill(muIsTight, muEta)

            if mu.simFlavour() > 0 and  mu.simFlavour() < 4 :
                hPt["LightF"].Fill(muPt)
                hEta["LightF"].Fill(muEta)
                hPhi["LightF"].Fill(muPhi)

                hSegComp["LightF"].Fill(muSegmComp)

                ePt["LightFLoose"].Fill(muIsLoose, muPt)
                ePt["LightFMedium"].Fill(muIsMedium, muPt)
                ePt["LightFTight"].Fill(muIsTight, muPt)

                eEta["LightFLoose"].Fill(muIsLoose, muEta)
                eEta["LightFMedium"].Fill(muIsMedium, muEta)
                eEta["LightFTight"].Fill(muIsTight, muEta)


            if mu.simFlavour() > 3 and  mu.simFlavour() < 6 :
                hPt["HeavyF"].Fill(muPt)
                hEta["HeavyF"].Fill(muEta)
                hPhi["HeavyF"].Fill(muPhi)

                hSegComp["HeavyF"].Fill(muSegmComp)

                ePt["HeavyFLoose"].Fill(muIsLoose, muPt)
                ePt["HeavyFMedium"].Fill(muIsMedium, muPt)
                ePt["HeavyFTight"].Fill(muIsTight, muPt)

                eEta["HeavyFLoose"].Fill(muIsLoose, muEta)
                eEta["HeavyFMedium"].Fill(muIsMedium, muEta)
                eEta["HeavyFTight"].Fill(muIsTight, muEta)

        if muIsTrkOrGlb :
            h_simTypeVsFlavour.Fill(muSimType,muSimFlavour)
        

