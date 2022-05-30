# Generates histograms displaying the distribution of alpha rejection and beta acceptance values (among others) around the detector given real simulated data (NEW UNITS)

#Useful generic python imports
from __future__ import print_function
from string import Template
import os, sys, time, math
import numpy as np
from array import array
import matplotlib as m
m.use('Agg')

#Imports particularly important for our purposes
import ROOT as r
import rat
import csv
import math
import matplotlib.pyplot as p
import significantFigures as s
import findRatio as f
import os

parser = argparse.ArgumentParser()
parser.add_argument('--filetype', '-a', type = str, default = '', help = 'File type of alpha and beta files ("ntuple" OR "ratds")')
parser.add_argument('--alphafile', '-a', type = str, default = '', help = 'Alpha file to use (no ".root" extension)')
parser.add_argument('--betafile', '-b', type = str, default = '', help = 'Beta file to use (no ".root" extension)')
parser.add_argument('--shape', '-s', type = str, default = 'list', help = 'Shape for plot ("list" OR "square")')

args = parser.parse_args()

r.gROOT.SetBatch(1) 

if args.filetype == "ntuple"
        r.gROOT.LoadMacro("./NtupleValues.cpp+")
else if args.filetype == "ratds"
        r.gROOT.LoadMacro("./RATDSValues.cpp+")
else
        raise Exception("Filetype must be either 'ntuple' OR 'ratds'")

rhoCoordinates = []
zCoordinates = []
distance = 1

if args.shape == "square"
        squareLength = int(raw_input("Please enter the side length of your square:"))
        distance = int(raw_input("Please enter the distance between the coordinates:"))
        for i in range(-math.floor(squareLength/distance, math.floor(squareLength/distance)
                for j in range(-math.floor(squareLength/distance, math.floor(squareLength/distance)
                        rhoCoordinates.extend(i)
                        zCoordinates.extend(j)
                       
if args.shape == "list"
        rhoCoordinates = list(map(int, raw_input("Please enter the rho coordinates in the form '3 2 3 4 8':").split()))
        zCoordinates = list(map(int, raw_input("Please enter the z coordinates in the form '4 6 3 8 8':").split()))
        distance = int(raw_input("Please enter the distance between the coordinates:"))
                                 
xTicks = []
yTicks = []

for i in range(0, math.floor(min(rhoCoordinates)-max(rhoCoordinates)/distance))
        xTicks.append(min(rhoCoordinates) + (distance*i))
                                 
for i in range(0, math.floor(min(zCoordinates)-max(zCoordinates)/distance))
        yTicks.append(min(zCoordinates) + (distance*i))
                

# set ratio Alpha/Beta
ratio = 9
ratio2 = str(s.significantFigures(ratio,3)).replace(".","-")

ClassifierYoudenArray = []
ValueYoudenArray = []
ClassifierGeneralArray = []
ValueGeneralArray = []

AlphaRejectionYoudenArray = []
BetaAcceptanceYoudenArray = []
AlphaRejectionGeneralArray = []
BetaAcceptanceGeneralArray = []


graphs = [ClassifierYoudenArray, ClassifierGeneralArray, ValueYoudenArray, ValueGeneralArray, AlphaRejectionYoudenArray, BetaAcceptanceYoudenArray, AlphaRejectionGeneralArray, BetaAcceptanceGeneralArray, ClassifierAlphaArray, NhitAlphaArray, ClassifierBetaArray, NhitBetaArray]
titles = ["Youden Classifier Cut Value","General Classifier Cut Value", "Youden Cut Value", "General Cut Value", r"Youden $\alpha$ Rejection", r"Youden $\beta$ Acceptance", r"General $\alpha$ Rejection", r"General $\beta$ Acceptance", r"Classification $\alpha$ Summary",r"$N_{\mathrm{hit}}$ $\alpha$ Summary", r"Classification $\beta$ Summary", r"$N_{\mathrm{hit}}$ $\beta$ Summary"]
graphs2 = ["YoudenClassifierCut", "GeneralClassifierCut", "YoudenCutValue", "GeneralCutValue", "YoudenAlphaRejection", "YoudenBetaAcceptance", "GeneralAlphaRejection", "GeneralBetaAcceptance", "ClassifierAlphaArray", "NhitAlphaArray", "ClassifierBetaArray", "NhitBetaArray"]
colorbar = ["Classifier Value", "Classifier Value", "Youden Statistic Value", "General Statistic Value", r"$\alpha$ Rejection", r"$\beta$ Acceptance", r"$\alpha$ Rejection", r"$\beta$ Acceptance", "Classifier Value", r"$N_{\mathrm{hit}}$ Value", "Classifier Value", r"$N_{\mathrm{hit}}$ Value"]

for i in range(0, len(rhoCoordinates)):

        if args.filetype == "ntuple"
                values = r.rejectionInfo("{}*.root".format(args.alphafile), "{}*.root".format(args.betafile), rhoCoordinates[i], zCoordinates[i], ratio, distance)
                alphaHistogram = r.NhitHistogram("{}*.root".format(args.alphafile), 0, 0, 0, "full")
                betaHistogram = r.NhitHistogram("{}*.root".format(args.betafile), 0, 0, 0, "full")
        
        else if args.filetype == "ratds"
                values = r.rejectionInfo("{}*.root".format(args.alphafile), "{}*.root".format(args.betafile), "partialFitter", "BerkeleyAlphaBeta:partialFitter", "likelihood", 9, rhoCoordinates[i], zCoordinates[i], distance)
                alphaHistogram = r.NhitHistogram("{}*.root".format(args.alphafile), "{}*.root".format(args.betafile), "partialFitter", "BerkeleyAlphaBeta:partialFitter", "likelihood", "alpha")
                betaHistogram = r.NhitHistogram("{}*.root".format(args.alphafile), "{}*.root".format(args.betafile), "partialFitter", "BerkeleyAlphaBeta:partialFitter", "likelihood", "beta")
                

        ClassifierYoudenArray.append(values[0])
        ValueYoudenArray.append(values[1])
        ClassifierGeneralArray.append(values[2])
        ValueGeneralArray.append(values[3])
        AlphaRejectionYoudenArray.append(values[4])
        BetaAcceptanceYoudenArray.append(values[5])
        AlphaRejectionGeneralArray.append(values[6])
        BetaAcceptanceGeneralArray.append(values[7])
                                          
        ClassifierAlphaArray.append(alphaHistogram.GetMean(2))
        NhitAlphaArray.append(alphaHistogram.GetMean(1))
        ClassifierBetaArray.append(betaHistogram.GetMean(2))
        NhitBetaArray.append(betaHistogram.GetMean(1))                              

for graph in graphs:
        graph.extend([-100, -100, -100])

rhoCoordinates.extend(3, 4, 4)
zCoordinates.extend([4, 4, 4])

for i in range(0,12):
        p.hist2d(rhoCoordinates, zCoordinates, bins=(5,4), range=((-.5,4.5),(1.5,4.5)), weights = graphs[i], cmap=p.cm.viridis, cmin=-10)

        for k in range(len(rhoCoordinates)):
                array = graphs[i]
                p.text(rhoCoordinates[k], zCoordinates[k], s.significantFigures(array[k], 4), ha="center",va="center",color="w")

        p.xlabel(r"$\rho$ coordinate")
        p.ylabel(r"$z$ coordinate (m)")
        p.title(titles[i])
        p.xticks(xTicks)
        p.yticks(yTicks)
        p.colorbar(label=colorbar[i])
        p.show()               
        p.savefig("partialFillPDFs/SummaryPartialFill{}.pdf".format(graphs2[i]))
        p.clf()