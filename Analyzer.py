import ROOT
import os
import sys
import numpy as np
import math

# Usage
# ---------------------------

def delta_phi(v1, v2, c=math.pi):
    r = math.fmod(v2 - v1, 2.0 * c)

    # In Python, fmod preserves sign, similar to C++
    if r < -c:
        r += 2.0 * c
    elif r > c:
        r -= 2.0 * c

    return r
    


if len(sys.argv) < 2:
    print("Usage: python analysis.py input1.root [input2.root ...] [--out output.root] [--ZJetsDecay Ztautau]")
    sys.exit(1)

# Parse arguments
args = sys.argv[1:]
if "--out" in args:
    out_index = args.index("--out")
    output_file = args[out_index + 1]
    input_files = args[:out_index]
else:
    output_file = "histograms.root"
    input_files = args

outZTau = False
if("--ZJetsDecay" in args):
    if(args[args.index("--ZJetsDecay") + 1] == "Ztautau"):
        outZTau = True

tree_name = "Events"

isMC = True
if "2012" in input_files[0]:
    isMC = False
    
isZJets = False
if "DYJets" in input_files[0]:
    isZJets = True






# histogram definitions
#muons
histo_muon_pt = ROOT.TH1F("histo_muon_pt", "Muon pT; pT [GeV]; Events", 100, 0, 200)
histo_muon_eta = ROOT.TH1F("histo_muon_eta", "Muon eta; eta; Events", 100, -2.5, 2.5)
histo_muon_phi = ROOT.TH1F("histo_muon_phi", "Muon phi; phi; Events", 64, -3.2, 3.2)
histo_muon_charge = ROOT.TH1F("histo_muon_charge", "Muon charge; charge; Events", 5, -2, 2)
histo_muon_GENpdgId = ROOT.TH1F("histo_muon_GENpdgId", "Muon GEN pdgId; pdgId; Events", 51, -25.5, 25.5)





# ---------------------------
# Build TChain
# ---------------------------
chain = ROOT.TChain(tree_name)
for f in input_files:
    print(f"Adding file: {f}")
    chain.Add(f)


# ---------------------------
# Event Loop
# ---------------------------
n_events = chain.GetEntries()
print(f"Total entries: {n_events}")

w=1.0

for i, event in enumerate(chain):
    if i % 10000 == 0:
        print(f"Processing event {i}/{n_events}")


    # Trigger selection
    if(event.HLT_IsoMu17_eta2p1_LooseIsoPFTau20 == 0):
        continue

    # Muon loop
    for j in range(event.nMuon):
        muon_pt = event.Muon_pt[j]
        muon_eta = event.Muon_eta[j]
        muon_phi = event.Muon_phi[j]
        muon_charge = event.Muon_charge[j]
        muon_tight = event.Muon_tightId[j]
        if(isMC):
            muon_genPartIdx = event.Muon_genPartIdx[j]
            muon_genPdgId = event.GenPart_pdgId[muon_genPartIdx]
        # Fill muon histograms
        histo_muon_pt.Fill(muon_pt)
        histo_muon_eta.Fill(muon_eta)
        histo_muon_phi.Fill(muon_phi)
        histo_muon_charge.Fill(muon_charge)
        if(isMC):
            histo_muon_GENpdgId.Fill(muon_genPdgId)


    # Build Higgs candidate
    if event.nMuon > 0 and event.nTau > 0:
        validpair_matrix = np.zeros((event.nMuon, event.nTau), dtype=int)
        higgs_candidates = []
        #loop over muons and taus
        for j in range(event.nMuon):
            # Add ID conditions for muons
            
            muon = ROOT.TLorentzVector()
            muon.SetPtEtaPhiM(event.Muon_pt[j], event.Muon_eta[j], event.Muon_phi[j], event.Muon_mass[j])
            for k in range(event.nTau):
                # Add ID conditions for taus
                tau = ROOT.TLorentzVector()
                tau.SetPtEtaPhiM(event.Tau_pt[k], event.Tau_eta[k], event.Tau_phi[k], event.Tau_mass[k])
                if(muon.DeltaR(tau) > 0.5):  
                    validpair_matrix[j][k] = 1
        
        #find the best muon-tau pair 
        #  1) highest pT muon
        max_pt=-1
        best_muon_index = -1
        for i in range(event.nMuon):
            if validpair_matrix[i].any(): #check if there is at least one valid tau for muon i
                muon = ROOT.TLorentzVector()
                muon.SetPtEtaPhiM(event.Muon_pt[i], event.Muon_eta[i], event.Muon_phi[i], event.Muon_mass[i])
                if(muon.Pt() > max_pt):
                    max_pt = muon.Pt()
                    best_muon_index = i
        #  2) most isolated tau
        min_iso=9999
        best_tau_index = 1

        #Higgs candidate four-vector
        if(best_muon_index != -1 and best_tau_index != -1):
            muon = ROOT.TLorentzVector()
            muon.SetPtEtaPhiM(event.Muon_pt[best_muon_index], event.Muon_eta[best_muon_index], event.Muon_phi[best_muon_index], event.Muon_mass[best_muon_index])
            #analogous for tau
            
            #higgs_candidate = muon + tau 

            # Fill histograms
            #if(math.fabs(event.GenPart_pdgId[event.Tau_genPartIdx[best_tau_index]]) != 15 or math.fabs(event.GenPart_pdgId[event.Muon_genPartIdx[best_muon_index]]) != 15):
                #if(event.Tau_charge[best_tau_index]*event.Muon_charge[best_muon_index] < 0):
                    #histo_higgs_pt.Fill(higgs_candidate.Pt())
                    #histo_higgs_eta.Fill(higgs_candidate.Eta())
                    #histo_higgs_phi.Fill(higgs_candidate.Phi())
                    #histo_higgs_mass.Fill(higgs_candidate.M())

                    #histo_BestMuon_pt.Fill(event.Muon_pt[best_muon_index])
                    #histo_BestMuon_eta.Fill(event.Muon_eta[best_muon_index])
                    #histo_BestMuon_phi.Fill(event.Muon_phi[best_muon_index])
                    #histo_BestMuon_charge.Fill(event.Muon_charge[best_muon_index])
                    #if(isMC):
                    #    histo_BestMuon_GENpdgId.Fill(event.GenPart_pdgId[event.Muon_genPartIdx[best_muon_index]])

                    #fill analogous histograms for tau
            
            

# ---------------------------
# Save histograms
# ---------------------------
# ---------------------------
output = ROOT.TFile(output_file, "RECREATE")
histo_muon_pt.Write()
histo_muon_eta.Write()
histo_muon_phi.Write()                          
histo_muon_charge.Write()
histo_muon_GENpdgId.Write()

output.Close()
print(f"Histograms saved to {output_file}")

                



