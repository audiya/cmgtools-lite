from math import *
from CMGTools.HToZZ4L.analyzers.FourLeptonAnalyzer import *

        
class FourLeptonAnalyzer2P2F( FourLeptonAnalyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(FourLeptonAnalyzer2P2F,self).__init__(cfg_ana,cfg_comp,looperName)
        self.tag = cfg_ana.tag
    def declareHandles(self):
        super(FourLeptonAnalyzer2P2F, self).declareHandles()

    def beginLoop(self, setup):
        super(FourLeptonAnalyzer2P2F,self).beginLoop(setup)
        self.counters.addCounter('FourLepton')
        count = self.counters.counter('FourLepton')
        count.register('all events')


    #For the good lepton preselection redefine the thingy so that leptons are loose    
    def leptonID(self,lepton):
        return self.leptonID_loose(lepton)


    def zSorting(self,Z1,Z2):
        return True

    def fourLeptonIsolation(self,fourLepton):
        ##Fancy! Here require that Z1 leptons pass tight ID and isolationand the two other leptons fail ID or isolation
        for l in [fourLepton.leg1.leg1,fourLepton.leg1.leg2]:
            if not self.leptonID_tight(l):
                return False
            if abs(l.pdgId())==11:
                if not (self.electronIsolation(l)):
                    return False
            if abs(l.pdgId())==13:
                if not self.muonIsolation(l):
                    return False

        nFail = 0
        for l in [fourLepton.leg2.leg1,fourLepton.leg2.leg2]:
            if not self.leptonID_tight(l):
                nFail += 1
                continue
            if abs(l.pdgId())==11:
                if not self.electronIsolation(l):
                    nFail += 1
                    continue
            if abs(l.pdgId())==13:
                if not self.muonIsolation(l):
                    nFail += 1
                    continue
        return (nFail == 2)
