import ROOT
import os

def setPlotOptions() :
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetOptStat(0)

def compareTH1Fs(canvasName, folderName, histos, minY, maxY, rescale = True, colors = [1,2,3,4], markers = [20,24,21,25]) :

    if len(histos) > len(colors) or \
       len(histos) > len(markers) :

        print "[compareTH1Fs] WARNING: more histograms than colors or markers, plots not processed"

        return ROOT.TCanvas("c","c",500,500)
        
    canvas = ROOT.TCanvas(canvasName,canvasName,500,500)

    canvas.SetGrid()

    for iHisto, histo in enumerate(histos) :

        if rescale :
            histo.Scale(1. / histo.Integral())

        histo.SetLineColor(colors[iHisto])
        histo.SetMarkerColor(colors[iHisto])
        histo.SetMarkerStyle(markers[iHisto])

        histo.GetYaxis().SetRangeUser(minY, maxY)

        if iHisto == 0 :
            histo.Draw()
        else :
            histo.Draw("same")
    
    canvas.Update()

    if not os.path.exists(folderName):
        os.mkdir(folderName)
    canvas.SaveAs("%s/%s.png" % (folderName,canvasName))

    return canvas


def compareTEfficiencies(canvasName, folderName, effs, minY, maxY, colors = [1,2,3,4], markers = [20,24,21,25]) :

    if len(effs) > len(colors) or \
       len(effs) > len(markers) :

        print "[compareTEfficiencies] WARNING: more histograms than colors or markers, plots not processed"

        return ROOT.TCanvas("c","c",500,500)
        
    canvas = ROOT.TCanvas(canvasName,canvasName,500,500)

    canvas.SetGrid()

    for iEff, eff in enumerate(effs) :

        eff.SetLineColor(colors[iEff])
        eff.SetMarkerColor(colors[iEff])
        eff.SetMarkerStyle(markers[iEff])

        if iEff == 0 :
            eff.Draw()
        else :
            eff.Draw("same")

        canvas.Update()

        eff.GetPaintedGraph().GetYaxis().SetRangeUser(minY, maxY)

    
    canvas.Update()

    if not os.path.exists(folderName):
        os.mkdir(folderName)
    canvas.SaveAs("%s/%s.png" % (folderName,canvasName))

    return canvas


def compareGraphs(canvasName, folderName, graphs, minY, maxY, colors = [1,2,3,4], markers = [20,24,21,25]) :

    if len(graphs) > len(colors) or \
       len(graphs) > len(markers) :

        print "[compareGraphs] WARNING: more graphs than colors or markers, plots not processed"

        return ROOT.TCanvas("c","c",500,500)
        
    canvas = ROOT.TCanvas(canvasName,canvasName,500,500)

    canvas.SetGrid()

    for iGraph, graph in enumerate(graphs) :

        graph.SetLineColor(colors[iGraph])
        graph.SetMarkerColor(colors[iGraph])
        graph.SetMarkerStyle(markers[iGraph])

        if iGraph == 0 :
            graph.Draw("AP")
        else :
            graph.Draw("sameP")

        canvas.Update()

        graph.GetYaxis().SetRangeUser(minY, maxY)
        
    canvas.Update()

    if not os.path.exists(folderName):
        os.mkdir(folderName)
    canvas.SaveAs("%s/%s.png" % (folderName,canvasName))

    canvas.SaveAs("%s.png" % canvasName)

    return canvas
