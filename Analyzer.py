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

#taus
histo_tau_pt = ROOT.TH1F("histo_tau_pt", "Tau pT; pT [GeV]; Events", 100, 0, 200)
histo_tau_eta = ROOT.TH1F("histo_tau_eta", "Tau eta; eta; Events", 100, -2.5, 2.5)
histo_tau_phi = ROOT.TH1F("histo_tau_phi", "Tau phi; phi; Events", 64, -3.2, 3.2)
histo_tau_charge = ROOT.TH1F("histo_tau_charge", "Tau charge; charge; Events", 5, -2, 2)
histo_tau_GENpdgId = ROOT.TH1F("histo_tau_GENpdgId", "Tau GEN pdgId; pdgId; Events", 51, -25, 25)

#selected muon-tau
histo_BestMuon_pt = ROOT.TH1F("histo_BestMuon_pt", "Muon pT; pT [GeV]; Events", 100, 0, 200)
histo_BestMuon_eta = ROOT.TH1F("histo_BestMuon_eta", "Muon eta; eta; Events", 100, -2.5, 2.5)
histo_BestMuon_phi = ROOT.TH1F("histo_BestMuon_phi", "Muon phi; phi; Events", 64, -3.2, 3.2)
histo_BestMuon_charge = ROOT.TH1F("histo_BestMuon_charge", "Muon charge; charge; Events", 5, -2, 2)
histo_BestMuon_GENpdgId = ROOT.TH1F("histo_BestMuon_GENpdgId", "Muon GEN pdgId; pdgId; Events", 51, -25.5, 25.5)

histo_BestMuon_pt_cr = ROOT.TH1F("histo_BestMuon_pt_cr", "Muon pT; pT [GeV]; Events", 100, 0, 200)
histo_BestMuon_eta_cr = ROOT.TH1F("histo_BestMuon_eta_cr", "Muon eta; eta; Events", 100, -2.5, 2.5)
histo_BestMuon_phi_cr = ROOT.TH1F("histo_BestMuon_phi_cr", "Muon phi; phi; Events", 64, -3.2, 3.2)
histo_BestMuon_charge_cr = ROOT.TH1F("histo_BestMuon_charge_cr", "Muon charge; charge; Events", 5, -2, 2)
histo_BestMuon_GENpdgId_cr = ROOT.TH1F("histo_BestMuon_GENpdgId_cr", "Muon GEN pdgId; pdgId; Events", 51, -25.5, 25.5)

histo_BestTau_pt = ROOT.TH1F("histo_BestTau_pt", "Tau pT; pT [GeV]; Events", 100, 0, 200)
histo_BestTau_eta = ROOT.TH1F("histo_BestTau_eta", "Tau eta; eta; Events", 100, -2.5, 2.5)
histo_BestTau_phi = ROOT.TH1F("histo_BestTau_phi", "Tau phi; phi; Events", 64, -3.2, 3.2)
histo_BestTau_charge = ROOT.TH1F("histo_BestTau_charge", "Tau charge; charge; Events", 5, -2, 2)
histo_BestTau_GENpdgId = ROOT.TH1F("histo_BestTau_GENpdgId", "Tau GEN pdgId; pdgId; Events", 51, -25, 25)

histo_BestTau_pt_cr = ROOT.TH1F("histo_BestTau_pt_cr", "Tau pT; pT [GeV]; Events", 100, 0, 200)
histo_BestTau_eta_cr = ROOT.TH1F("histo_BestTau_eta_cr", "Tau eta; eta; Events", 100, -2.5, 2.5)
histo_BestTau_phi_cr = ROOT.TH1F("histo_BestTau_phi_cr", "Tau phi; phi; Events", 64, -3.2, 3.2)
histo_BestTau_charge_cr = ROOT.TH1F("histo_BestTau_charge_cr", "Tau charge; charge; Events", 5, -2, 2)
histo_BestTau_GENpdgId_cr = ROOT.TH1F("histo_BestTau_GENpdgId_cr", "Tau GEN pdgId; pdgId; Events", 51, -25, 25)

#Higgs candidate
histo_higgs_pt = ROOT.TH1F("histo_higgs_pt", "Higgs candidate pT; pT [GeV]; Events", 100, 0, 300)
histo_higgs_eta = ROOT.TH1F("histo_higgs_eta", "Higgs candidate eta; eta; Events", 100, -5, 5)
histo_higgs_phi = ROOT.TH1F("histo_higgs_phi", "Higgs candidate phi; phi; Events", 64, -3.2, 3.2)
histo_higgs_mass = ROOT.TH1F("histo_higgs_mass", "Higgs candidate mass; mass [GeV]; Events", 30, 20, 140)

histo_higgs_pt_cr = ROOT.TH1F("histo_higgs_pt_cr", "Higgs candidate pT; pT [GeV]; Events", 100, 0, 300)
histo_higgs_eta_cr = ROOT.TH1F("histo_higgs_eta_cr", "Higgs candidate eta; eta; Events", 100, -5, 5)
histo_higgs_phi_cr = ROOT.TH1F("histo_higgs_phi_cr", "Higgs candidate phi; phi; Events", 64, -3.2, 3.2)
histo_higgs_mass_cr = ROOT.TH1F("histo_higgs_mass_cr", "Higgs candidate mass; mass [GeV]; Events", 30, 20, 140)


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

    if i==0:
        w = event.weight

    # Trigger selection
    if(event.HLT_IsoMu17_eta2p1_LooseIsoPFTau20 == 0):
        continue

    #veto b jets
    #if(event.jbtag_1.size() > 0):
    #if(event.jbtag_1 ==1):
    #    continue

    #if(event.jbtag_2.size() > 0):
    #if(event.jbtag_2 ==1):
    #    continue

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

        #add muon ID conditions here 
        if(muon_pt < 17 or abs(muon_eta) > 2.1 or muon_tight==0):
        #if(muon_pt < 17 or abs(muon_eta) > 2.1):
            continue

        histo_muon_pt.Fill(muon_pt, w)
        histo_muon_eta.Fill(muon_eta, w)
        histo_muon_phi.Fill(muon_phi, w)
        histo_muon_charge.Fill(muon_charge, w)
        if(isMC):
            histo_muon_GENpdgId.Fill(muon_genPdgId, w)

    # Tau loop
    for j in range(event.nTau):
        tau_pt = event.Tau_pt[j]
        tau_eta = event.Tau_eta[j]
        tau_phi = event.Tau_phi[j]
        tau_charge = event.Tau_charge[j]
        tau_idDecayMode = event.Tau_idDecayMode[j]
        tau_idIsoTight = event.Tau_idIsoTight[j]
        tau_idAntiEleTight = event.Tau_idAntiEleTight[j]
        tau_idAntiMuTight = event.Tau_idAntiMuTight[j]
        if(isMC):
            tau_genPartIdx = event.Tau_genPartIdx[j]
            tau_genPdgId = event.GenPart_pdgId[tau_genPartIdx]

        #add tau ID conditions here
        if(tau_charge == 0 or tau_pt < 20 or abs(tau_eta) > 2.3 or tau_idDecayMode==0 or tau_idIsoTight==0 or tau_idAntiEleTight==0 or tau_idAntiMuTight==0):
            continue

        histo_tau_pt.Fill(tau_pt, w)
        histo_tau_eta.Fill(tau_eta, w)
        histo_tau_phi.Fill(tau_phi, w)
        histo_tau_charge.Fill(tau_charge, w)
        if(isMC):
            histo_tau_GENpdgId.Fill(tau_genPdgId, w)   

    # Build Higgs candidate
    if event.nMuon > 0 and event.nTau > 0:
        validpair_matrix = np.zeros((event.nMuon, event.nTau), dtype=int)
        higgs_candidates = []
        #loop over muons and taus
        for j in range(event.nMuon):
            # Add ID conditions for muons
            if(event.Muon_pt[j] < 17 or abs(event.Muon_eta[j]) > 2.1 or event.Muon_tightId[j]==0):
                continue
            muon = ROOT.TLorentzVector()
            muon.SetPtEtaPhiM(event.Muon_pt[j], event.Muon_eta[j], event.Muon_phi[j], event.Muon_mass[j])
            for k in range(event.nTau):
                # Add ID conditions for taus
                if(event.Tau_charge[k] == 0 or event.Tau_pt[k] < 20 or abs(event.Tau_eta[k]) > 2.3 or event.Tau_idDecayMode[k]==0 or event.Tau_idIsoTight[k]==0 or event.Tau_idAntiEleTight[k]==0 or event.Tau_idAntiMuTight[k]==0):
                    continue
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
        best_tau_index = -1
        for j in range(event.nTau):
                if validpair_matrix[best_muon_index, j] == 0:
                    continue
                tau_relIso = event.Tau_relIso_all[j]
                if(tau_relIso < min_iso):
                    min_iso = tau_relIso
                    best_tau_index = j

        #compute mt
        deltaPhi = delta_phi(event.Muon_phi[best_muon_index], event.phi_met)
        mt = math.sqrt(2*event.Muon_pt[best_muon_index]*event.pt_met*(1 - math.cos(deltaPhi)))
        #apply a cut on mt
        if(mt>30):
            continue

        #apply a cut on muon isolation
        if(event.Muon_pfRelIso03_all[best_muon_index] > 0.1):
            continue



        #Higgs candidate four-vector
        if(best_muon_index != -1 and best_tau_index != -1):
            muon = ROOT.TLorentzVector()
            muon.SetPtEtaPhiM(event.Muon_pt[best_muon_index], event.Muon_eta[best_muon_index], event.Muon_phi[best_muon_index], event.Muon_mass[best_muon_index])
            tau = ROOT.TLorentzVector()
            tau.SetPtEtaPhiM(event.Tau_pt[best_tau_index], event.Tau_eta[best_tau_index], event.Tau_phi[best_tau_index], event.Tau_mass[best_tau_index])
            higgs_candidate = muon + tau
            # Fill histograms
            if(isZJets):
                if(outZTau):
                    if(math.fabs(event.GenPart_pdgId[event.Tau_genPartIdx[best_tau_index]]) == 15 and math.fabs(event.GenPart_pdgId[event.Muon_genPartIdx[best_muon_index]]) == 15):

                        if(event.Tau_charge[best_tau_index]*event.Muon_charge[best_muon_index] < 0):
                            histo_higgs_pt.Fill(higgs_candidate.Pt(), w)
                            histo_higgs_eta.Fill(higgs_candidate.Eta(), w)
                            histo_higgs_phi.Fill(higgs_candidate.Phi(), w)
                            histo_higgs_mass.Fill(higgs_candidate.M(), w)

                            histo_BestMuon_pt.Fill(event.Muon_pt[best_muon_index], w)
                            histo_BestMuon_eta.Fill(event.Muon_eta[best_muon_index], w)
                            histo_BestMuon_phi.Fill(event.Muon_phi[best_muon_index], w)
                            histo_BestMuon_charge.Fill(event.Muon_charge[best_muon_index], w)
                            if(isMC):
                                histo_BestMuon_GENpdgId.Fill(event.GenPart_pdgId[event.Muon_genPartIdx[best_muon_index]], w)

                            histo_BestTau_pt.Fill(event.Tau_pt[best_tau_index], w)
                            histo_BestTau_eta.Fill(event.Tau_eta[best_tau_index], w)
                            histo_BestTau_phi.Fill(event.Tau_phi[best_tau_index], w)
                            histo_BestTau_charge.Fill(event.Tau_charge[best_tau_index], w)
                            if(isMC):
                                histo_BestTau_GENpdgId.Fill(event.GenPart_pdgId[event.Tau_genPartIdx[best_tau_index]], w)
                        
                        else:
                            histo_higgs_pt_cr.Fill(higgs_candidate.Pt(), w)
                            histo_higgs_eta_cr.Fill(higgs_candidate.Eta(), w)
                            histo_higgs_phi_cr.Fill(higgs_candidate.Phi(), w)
                            histo_higgs_mass_cr.Fill(higgs_candidate.M(), w)

                            histo_BestMuon_pt_cr.Fill(event.Muon_pt[best_muon_index], w)
                            histo_BestMuon_eta_cr.Fill(event.Muon_eta[best_muon_index], w)
                            histo_BestMuon_phi_cr.Fill(event.Muon_phi[best_muon_index], w)
                            histo_BestMuon_charge_cr.Fill(event.Muon_charge[best_muon_index], w)
                            if(isMC):
                                histo_BestMuon_GENpdgId_cr.Fill(event.GenPart_pdgId[event.Muon_genPartIdx[best_muon_index]], w)

                            histo_BestTau_pt_cr.Fill(event.Tau_pt[best_tau_index], w)
                            histo_BestTau_eta_cr.Fill(event.Tau_eta[best_tau_index], w)
                            histo_BestTau_phi_cr.Fill(event.Tau_phi[best_tau_index], w)
                            histo_BestTau_charge_cr.Fill(event.Tau_charge[best_tau_index], w)
                            if(isMC):
                                histo_BestTau_GENpdgId_cr.Fill(event.GenPart_pdgId[event.Tau_genPartIdx[best_tau_index]], w)

                else:
                    if(math.fabs(event.GenPart_pdgId[event.Tau_genPartIdx[best_tau_index]]) != 15 or math.fabs(event.GenPart_pdgId[event.Muon_genPartIdx[best_muon_index]]) != 15):
                        if(event.Tau_charge[best_tau_index]*event.Muon_charge[best_muon_index] < 0):
                            histo_higgs_pt.Fill(higgs_candidate.Pt(), w)
                            histo_higgs_eta.Fill(higgs_candidate.Eta(), w)
                            histo_higgs_phi.Fill(higgs_candidate.Phi(), w)
                            histo_higgs_mass.Fill(higgs_candidate.M(), w)

                            histo_BestMuon_pt.Fill(event.Muon_pt[best_muon_index], w)
                            histo_BestMuon_eta.Fill(event.Muon_eta[best_muon_index], w)
                            histo_BestMuon_phi.Fill(event.Muon_phi[best_muon_index], w)
                            histo_BestMuon_charge.Fill(event.Muon_charge[best_muon_index], w)
                            if(isMC):
                                histo_BestMuon_GENpdgId.Fill(event.GenPart_pdgId[event.Muon_genPartIdx[best_muon_index]], w)

                            histo_BestTau_pt.Fill(event.Tau_pt[best_tau_index], w)
                            histo_BestTau_eta.Fill(event.Tau_eta[best_tau_index], w)
                            histo_BestTau_phi.Fill(event.Tau_phi[best_tau_index], w)
                            histo_BestTau_charge.Fill(event.Tau_charge[best_tau_index], w)
                            if(isMC):
                                histo_BestTau_GENpdgId.Fill(event.GenPart_pdgId[event.Tau_genPartIdx[best_tau_index]], w)
                        
                        else:
                            histo_higgs_pt_cr.Fill(higgs_candidate.Pt(), w)
                            histo_higgs_eta_cr.Fill(higgs_candidate.Eta(), w)
                            histo_higgs_phi_cr.Fill(higgs_candidate.Phi(), w)
                            histo_higgs_mass_cr.Fill(higgs_candidate.M(), w)

                            histo_BestMuon_pt_cr.Fill(event.Muon_pt[best_muon_index], w)
                            histo_BestMuon_eta_cr.Fill(event.Muon_eta[best_muon_index], w)
                            histo_BestMuon_phi_cr.Fill(event.Muon_phi[best_muon_index], w)
                            histo_BestMuon_charge_cr.Fill(event.Muon_charge[best_muon_index], w)
                            if(isMC):
                                histo_BestMuon_GENpdgId_cr.Fill(event.GenPart_pdgId[event.Muon_genPartIdx[best_muon_index]], w)

                            histo_BestTau_pt_cr.Fill(event.Tau_pt[best_tau_index], w)
                            histo_BestTau_eta_cr.Fill(event.Tau_eta[best_tau_index], w)
                            histo_BestTau_phi_cr.Fill(event.Tau_phi[best_tau_index], w)
                            histo_BestTau_charge_cr.Fill(event.Tau_charge[best_tau_index], w)
                            if(isMC):
                                histo_BestTau_GENpdgId_cr.Fill(event.GenPart_pdgId[event.Tau_genPartIdx[best_tau_index]], w)
            else:
                if(event.Tau_charge[best_tau_index]*event.Muon_charge[best_muon_index] < 0):
                    histo_higgs_pt.Fill(higgs_candidate.Pt(), w)
                    histo_higgs_eta.Fill(higgs_candidate.Eta(), w)
                    histo_higgs_phi.Fill(higgs_candidate.Phi(), w)
                    histo_higgs_mass.Fill(higgs_candidate.M(), w)

                    histo_BestMuon_pt.Fill(event.Muon_pt[best_muon_index], w)
                    histo_BestMuon_eta.Fill(event.Muon_eta[best_muon_index], w)
                    histo_BestMuon_phi.Fill(event.Muon_phi[best_muon_index], w)
                    histo_BestMuon_charge.Fill(event.Muon_charge[best_muon_index], w)
                    if(isMC):
                        histo_BestMuon_GENpdgId.Fill(event.GenPart_pdgId[event.Muon_genPartIdx[best_muon_index]], w)

                    histo_BestTau_pt.Fill(event.Tau_pt[best_tau_index], w)
                    histo_BestTau_eta.Fill(event.Tau_eta[best_tau_index], w)
                    histo_BestTau_phi.Fill(event.Tau_phi[best_tau_index], w)
                    histo_BestTau_charge.Fill(event.Tau_charge[best_tau_index], w)
                    if(isMC):
                        histo_BestTau_GENpdgId.Fill(event.GenPart_pdgId[event.Tau_genPartIdx[best_tau_index]], w)
                
                else:
                    histo_higgs_pt_cr.Fill(higgs_candidate.Pt(), w)
                    histo_higgs_eta_cr.Fill(higgs_candidate.Eta(), w)
                    histo_higgs_phi_cr.Fill(higgs_candidate.Phi(), w)
                    histo_higgs_mass_cr.Fill(higgs_candidate.M(), w)

                    histo_BestMuon_pt_cr.Fill(event.Muon_pt[best_muon_index], w)
                    histo_BestMuon_eta_cr.Fill(event.Muon_eta[best_muon_index], w)
                    histo_BestMuon_phi_cr.Fill(event.Muon_phi[best_muon_index], w)
                    histo_BestMuon_charge_cr.Fill(event.Muon_charge[best_muon_index], w)
                    if(isMC):
                        histo_BestMuon_GENpdgId_cr.Fill(event.GenPart_pdgId[event.Muon_genPartIdx[best_muon_index]], w)

                    histo_BestTau_pt_cr.Fill(event.Tau_pt[best_tau_index], w)
                    histo_BestTau_eta_cr.Fill(event.Tau_eta[best_tau_index], w)
                    histo_BestTau_phi_cr.Fill(event.Tau_phi[best_tau_index], w)
                    histo_BestTau_charge_cr.Fill(event.Tau_charge[best_tau_index], w)
                    if(isMC):
                        histo_BestTau_GENpdgId_cr.Fill(event.GenPart_pdgId[event.Tau_genPartIdx[best_tau_index]], w)
            

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
histo_BestMuon_pt.Write()
histo_BestMuon_eta.Write()
histo_BestMuon_phi.Write()
histo_BestMuon_charge.Write()
histo_BestMuon_GENpdgId.Write()
histo_BestTau_pt.Write()
histo_BestTau_eta.Write()
histo_BestTau_phi.Write()
histo_BestTau_charge.Write()
histo_BestTau_GENpdgId.Write()
histo_higgs_pt.Write()
histo_higgs_eta.Write()
histo_higgs_phi.Write()
histo_higgs_mass.Write()
histo_BestMuon_pt_cr.Write()
histo_BestMuon_eta_cr.Write()
histo_BestMuon_phi_cr.Write()
histo_BestMuon_charge_cr.Write()
histo_BestMuon_GENpdgId_cr.Write()
histo_BestTau_pt_cr.Write()
histo_BestTau_eta_cr.Write()
histo_BestTau_phi_cr.Write()
histo_BestTau_charge_cr.Write()
histo_BestTau_GENpdgId_cr.Write()
histo_higgs_pt_cr.Write()
histo_higgs_eta_cr.Write()
histo_higgs_phi_cr.Write()
histo_higgs_mass_cr.Write()
output.Close()
print(f"Histograms saved to {output_file}")

                



