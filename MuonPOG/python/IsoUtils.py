import ROOT

class Roc2DBin :

    def __init__(self) :

        self.denX = 0
        self.numX = 0

        self.denY = 0
        self.numY = 0

    def fillX(self,passed) :
        self.denX += 1
        if passed:
            self.numX += 1

    def fillY(self,passed) :
        self.denY += 1
        if passed:
            self.numY += 1

    def effX(self) :
        return float(self.numX) / self.denX

    def effY(self) :
        return float(self.numY) / self.denY

class Roc2DVec :

        def __init__(self, cuts, xLabel, yLabel, title) :
            self.roc2Dbins = {}
            for cut in cuts :
                self.roc2Dbins[cut] = Roc2DBin()
            self.xLabel = xLabel
            self.yLabel = yLabel
            self.title  = title
            
        def fill(self, label, val) :            
            if label == self.xLabel :
                for cut, rocBin in self.roc2Dbins.iteritems() :
                    rocBin.denX += 1
                    if val < cut:
                        rocBin.numX += 1
            elif label == self.yLabel :
                for cut, rocBin in self.roc2Dbins.iteritems() :
                    rocBin.denY += 1
                    if val < cut:
                        rocBin.numY += 1
            else :
                print "[Roc2DVec::fill] WARNING, unrecognized label :", label, "skipping fill"

        def getGraph(self):
            graph = ROOT.TGraph(len(self.roc2Dbins))

            for iBin, rocBin in enumerate(self.roc2Dbins.values()):
                graph.SetPoint(iBin,rocBin.effX(),rocBin.effY())

                graph.SetTitle(self.title)
                graph.GetXaxis().SetTitle(self.xLabel)
                graph.GetYaxis().SetTitle(self.yLabel)

            return graph
