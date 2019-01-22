import DataFormats.FWLite as fwlite

N_EVENTS = 5

events = fwlite.Events("/gpfs/ddn/cms/user/cmsdas/2019/muon/data/DY.root")
muons  = fwlite.Handle("std::vector<pat::Muon>") 

for iEv, event in enumerate(events):

    if iEv >= N_EVENTS: break

    print "***** Event", iEv

    event.getByLabel("slimmedMuons", muons)

    print "Muon collection size:", len(muons.product())
    for iMu, mu in enumerate(muons.product()):
        print "  Muon #:", iMu
        print "\t===== KINEMATICS:"
        print "\t  charge:",  mu.charge()
        print "\t  pT:",      mu.pt()
        print "\t  phi:",     mu.phi()
        print "\t  eta:",     mu.eta()
        print "\t===== ID VARIABLES:"
        print "\t  segment compatibility:", mu.segmentCompatibility()
        print "\t===== ID SELECTIONS:"
        print "\t  is TIGHT:",   mu.passed(mu.CutBasedIdTight)
        print "\t===== ISOLATION:"
        print "\t  TRK based relIso:", mu.isolationR03().sumPt / mu.pt()
        print "\t===== SIM INFO:"
        print "\t  sim flavour:",  mu.simFlavour()
