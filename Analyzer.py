import ROOT
import os
import sys
import numpy as np

# Usage
# ---------------------------
if len(sys.argv) < 2:
    print("Usage: python analysis.py input1.root [input2.root ...] [--out output.root]")
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

tree_name = "Events"

# histogram definitions
#muons
histo_muon_pt = ROOT.TH1F("histo_muon_pt", "Muon pT; pT [GeV]; Events", 100, 0, 200)
histo_muon_eta = ROOT.TH1F("histo_muon_eta", "Muon eta; eta; Events", 100, -2.5, 2.5)
histo_muon_phi = ROOT.TH1F("histo_muon_phi", "Muon phi; phi; Events", 64, -3.2, 3.2)
histo_muon_charge = ROOT.TH1F("histo_muon_charge", "Muon charge; charge; Events", 5, -2, 2)
histo_muon_GENpdgId = ROOT.TH1F("histo_muon_GENpdgId", "Muon GEN pdgId; pdgId; Events", 51, -25.5, 25.5)

#taus
histo_tau_pt = ROOT.TH1F("histo_tau_pt", "Tau pT; pT [GeV]; Events", 100, 0, 200)
histo_tau_eta = ROOT.TH1F("histo_tau_eta", "Tau eta; eta; Events", 100, -2.5, 2.5)
histo_tau_phi = ROOT.TH1F("histo_tau_phi", "Tau phi; phi; Events", 64, -3.2, 3.2)
histo_tau_charge = ROOT.TH1F("histo_tau_charge", "Tau charge; charge; Events", 5, -2, 2)
histo_tau_GENpdgId = ROOT.TH1F("histo_tau_GENpdgId", "Tau GEN pdgId; pdgId; Events", 51, -25, 25)

#Higgs candidate
histo_higgs_pt = ROOT.TH1F("histo_higgs_pt", "Higgs candidate pT; pT [GeV]; Events", 100, 0, 300)
histo_higgs_eta = ROOT.TH1F("histo_higgs_eta", "Higgs candidate eta; eta; Events", 100, -5, 5)
histo_higgs_phi = ROOT.TH1F("histo_higgs_phi", "Higgs candidate phi; phi; Events", 64, -3.2, 3.2)
histo_higgs_mass = ROOT.TH1F("histo_higgs_mass", "Higgs candidate mass; mass [GeV]; Events", 20, 20, 140)  


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

for i, event in enumerate(chain):
    if i % 10000 == 0:
        print(f"Processing event {i}/{n_events}")

    # Muon loop
    for j in range(event.nMuon):
        muon_pt = event.Muon_pt[j]
        muon_eta = event.Muon_eta[j]
        muon_phi = event.Muon_phi[j]
        muon_charge = event.Muon_charge[j]
        muon_genPartIdx = event.Muon_genPartIdx[j]
        muon_genPdgId = event.GenPart_pdgId[muon_genPartIdx]

        histo_muon_pt.Fill(muon_pt)
        histo_muon_eta.Fill(muon_eta)
        histo_muon_phi.Fill(muon_phi)
        histo_muon_charge.Fill(muon_charge)
        histo_muon_GENpdgId.Fill(muon_genPdgId)

    # Tau loop
    for j in range(event.nTau):
        tau_pt = event.Tau_pt[j]
        tau_eta = event.Tau_eta[j]
        tau_phi = event.Tau_phi[j]
        tau_charge = event.Tau_charge[j]
        tau_genPartIdx = event.Tau_genPartIdx[j]
        tau_genPdgId = event.GenPart_pdgId[tau_genPartIdx]

        histo_tau_pt.Fill(tau_pt)
        histo_tau_eta.Fill(tau_eta)
        histo_tau_phi.Fill(tau_phi)
        histo_tau_charge.Fill(tau_charge)
        histo_tau_GENpdgId.Fill(tau_genPdgId)   

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
                if(muon.DeltaR(tau) > 0.5 and event.Tau_charge[k]*event.Muon_charge[j] < 0):  
                    validpair_matrix[j][k] = 1
        
        #find the best muon-tau pair 
        #  1) highest pT muon
        max_pt=-1
        best_muon_index = -1
        for i in range(event.nMuon):
            for j in range(event.nTau):
                if validpair_matrix[i, j] == 0:
                    continue
                muon = ROOT.TLorentzVector()
                muon.SetPtEtaPhiM(event.Muon_pt[i], event.Muon_eta[i], event.Muon_phi[i], event.Muon_mass[i])
                if(muon.Pt() > max_pt):
                    max_pt = muon.Pt()
                    best_muon_index = i
        #  2) most isolated tau
        min_iso=9999
        best_tau_index = -1
        for j in range(event.nTau):
                if validpair_matrix[best_muon_index, j] == 0:
                    continue
                tau_relIso = event.Tau_relIso_all[j]
                if(tau_relIso < min_iso):
                    min_iso = tau_relIso
                    best_tau_index = j



        #Higgs candidate four-vector
        if(best_muon_index != -1 and best_tau_index != -1):
            muon = ROOT.TLorentzVector()
            muon.SetPtEtaPhiM(event.Muon_pt[best_muon_index], event.Muon_eta[best_muon_index], event.Muon_phi[best_muon_index], event.Muon_mass[best_muon_index])
            tau = ROOT.TLorentzVector()
            tau.SetPtEtaPhiM(event.Tau_pt[best_tau_index], event.Tau_eta[best_tau_index], event.Tau_phi[best_tau_index], event.Tau_mass[best_tau_index])
            higgs_candidate = muon + tau
            # Fill histograms
            histo_higgs_pt.Fill(higgs_candidate.Pt())
            histo_higgs_eta.Fill(higgs_candidate.Eta())
            histo_higgs_phi.Fill(higgs_candidate.Phi())
            histo_higgs_mass.Fill(higgs_candidate.M())

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
histo_tau_pt.Write()
histo_tau_eta.Write()
histo_tau_phi.Write()
histo_tau_charge.Write()
histo_tau_GENpdgId.Write()
histo_higgs_pt.Write()
histo_higgs_eta.Write()
histo_higgs_phi.Write()
histo_higgs_mass.Write()
output.Close()
print(f"Histograms saved to {output_file}")

                



