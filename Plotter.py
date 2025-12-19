import ROOT
import os
ROOT.gROOT.SetBatch(True)

def load_histos_from_files(histo_name,root_file):
    if not os.path.exists(root_file):
        print(f"Warning: file not found {root_file}")
    infile = ROOT.TFile.Open(root_file)
    if not infile or infile.IsZombie():
        print(f"Warning: cannot open {root_file}")
    obj = infile.Get(histo_name)
    if not obj:
        print(f"Warning: histogram '{histo_name}' not found in {root_file}")
        infile.Close()
        return None
    # ensure it's a TH1 (works for PyROOT proxies)
    try:
        is_hist = obj.InheritsFrom("TH1")
    except Exception:
        is_hist = False
    if not is_hist:
        print(f"Warning: object '{histo_name}' in {root_file} is not a TH1 (type: {type(obj)})")
        infile.Close()
        return None
    # clone and detach from file
    h = obj.Clone(f"{histo_name}__{os.path.basename(root_file)}")
    h.SetDirectory(0)
    infile.Close()
    return h



input_files = {
    "ggH": ["rootfiles_output/GluGluToHToTauTauAna.root"],
    "qqH": ["rootfiles_output/VBF_HToTauTauAna.root"],
    "TT": ["rootfiles_output/TTbarAna.root"],
    "W": ["rootfiles_output/W1JetsToLNuAna.root", "rootfiles_output/W2JetsToLNuAna.root", "rootfiles_output/W3JetsToLNuAna.root"],
    "QCD": ["rootfiles_output/Run2012B_TauPlusXAna.root", "rootfiles_output/Run2012C_TauPlusXAna.root"],
    "ZLL": ["rootfiles_output/DYJetsToLLAna.root"],
    "ZTT": ["rootfiles_output/DYJetsToTauTauAna.root"],
    "data": ["rootfiles_output/Run2012B_TauPlusXAna.root", "rootfiles_output/Run2012C_TauPlusXAna.root"],
}

colors = {
        "ggH": ROOT.TColor.GetColor("#BF2229"),
        "qqH": ROOT.TColor.GetColor("#00A88F"),
        "TT": ROOT.TColor.GetColor(155, 152, 204),
        "W": ROOT.TColor.GetColor(222, 90, 106),
        "QCD":  ROOT.TColor.GetColor(250, 202, 255),
        "ZLL": ROOT.TColor.GetColor(100, 192, 232),
        "ZTT": ROOT.TColor.GetColor(248, 206, 104),
    }

variables = {
    #"higgs_pt": ("histo_higgs_pt", "Higgs p_{T} [GeV]", 50, 0, 200),
    #"higgs_eta": ("histo_higgs_eta", "Higgs #eta", 50, -5, 5),
    #"higgs_phi": ("histo_higgs_phi", "Higgs #phi", 50, -3.5, 3.5),
    "higgs_mass": ("histo_higgs_mass", "Higgs mass [GeV]"),
    #"Muon_pt": ("histo_BestMuon_pt", "Muon p_{T} [GeV]", 50, 0, 200),
    #"Muon_eta": ("histo_BestMuon_eta", "Muon #eta", 50, -5, 5),
    #"Muon_phi": ("histo_BestMuon_phi", "Muon #phi", 50, -3.5, 3.5),
    #"Muon_charge": ("histo_BestMuon_charge", "Muon charge", 5, -2, 2),
    #"Muon_GENpdgId": ("histo_BestMuon_GENpdgId", "Muon GEN pdgId", 30, -15, 15),
    #"Tau_pt": ("histo_BestTau_pt", "Tau p_{T} [GeV]", 50, 0, 200),
    #"Tau_eta": ("histo_BestTau_eta", "Tau #eta", 50, -5, 5),
    #"Tau_phi": ("histo_BestTau_phi", "Tau #phi", 50, -3.5, 3.5),
    #"Tau_charge": ("histo_BestTau_charge", "Tau charge", 5, -2, 2),
    #"Tau_GENpdgId": ("histo_BestTau_GENpdgId", "Tau GEN pdgId", 30, -15, 15),
}

output_file = "rootfiles_output/Plotter_output.root"


for var, (histo_name, histo_title) in variables.items():
    ggH_histo = load_histos_from_files(histo_name, input_files["ggH"][0])
    ggH_histo.SetLineColor(colors["ggH"])
    if not ggH_histo:
        continue

    qqH_histo = load_histos_from_files(histo_name, input_files["qqH"][0])
    qqH_histo.SetLineColor(colors["qqH"])
    if not qqH_histo:
        continue

    tt_histo = load_histos_from_files(histo_name, input_files["TT"][0])
    tt_histo.SetLineColor(colors["TT"])
    tt_histo.SetFillColor(colors["TT"])
    if not tt_histo:
        continue    

    wjets_histo = load_histos_from_files(histo_name, input_files["W"][0])
    for wfile in input_files["W"][1:]:
        temp_histo = load_histos_from_files(histo_name, wfile)
        if temp_histo:
            wjets_histo.Add(temp_histo)
        wjets_histo.SetLineColor(colors["W"])
        wjets_histo.SetFillColor(colors["W"])
    if not wjets_histo:
        continue    

    zll_histo = load_histos_from_files(histo_name, input_files["ZLL"][0])
    zll_histo.SetLineColor(colors["ZLL"])
    zll_histo.SetFillColor(colors["ZLL"])
    if not zll_histo:
        continue

    ztt_histo = load_histos_from_files(histo_name, input_files["ZTT"][0])
    ztt_histo.SetLineColor(colors["ZTT"])
    ztt_histo.SetFillColor(colors["ZTT"])
    if not ztt_histo:
        continue

    data_histo = load_histos_from_files(histo_name, input_files["data"][0])
    for dfile in input_files["data"][1:]:
        temp_histo = load_histos_from_files(histo_name, dfile)
        if temp_histo:
            data_histo.Add(temp_histo)
    if not data_histo:
        continue

    qcd_histo = load_histos_from_files(histo_name+"_cr", input_files["data"][0])
    for dfile in input_files["data"][1:]:
        temp_histo = load_histos_from_files(histo_name+"_cr", dfile)
        if temp_histo:
            print("Adding QCD CR from ", dfile)
            qcd_histo.Add(temp_histo)
    tt_histo_cr = load_histos_from_files(histo_name+"_cr", input_files["TT"][0])
    if tt_histo_cr:
        qcd_histo.Add(tt_histo_cr, -1)
    wjets_histo_cr = load_histos_from_files(histo_name+"_cr", input_files["W"][0])
    if wjets_histo_cr:
        qcd_histo.Add(wjets_histo_cr, -1)
    zll_histo_cr = load_histos_from_files(histo_name+"_cr", input_files["ZLL"][0])
    if zll_histo_cr:
        qcd_histo.Add(zll_histo_cr, -1)
    ztt_histo_cr = load_histos_from_files(histo_name+"_cr", input_files["ZTT"][0])
    if ztt_histo_cr:
        qcd_histo.Add(ztt_histo_cr, -1) 
    
    QCDScaleFactor = 0.80
    qcd_histo.Scale(QCDScaleFactor)

    qcd_histo.SetLineColor(colors["QCD"])
    qcd_histo.SetFillColor(colors["QCD"])
    if not qcd_histo:
        continue

    # Create stack
    stack = ROOT.THStack("stack", histo_title)
    stack.Add(qcd_histo)
    stack.Add(tt_histo)
    stack.Add(wjets_histo)
    stack.Add(zll_histo)
    stack.Add(ztt_histo)

    
    
    
    # Create canvas
    canvas = ROOT.TCanvas("canvas_"+var, histo_title, 800, 600)
    stack.Draw("HIST")
    stack.SetMaximum(stack.GetMaximum()*1.3)
    data_histo.SetMarkerStyle(20)
    data_histo.Draw("E SAME")
    ggH_histo.Scale(10)  # scale signal for visibility
    qqH_histo.Scale(100)  # scale signal for visibility
    ggH_histo.SetLineWidth(2)
    qqH_histo.SetLineWidth(2)
    ggH_histo.Draw("HIST SAME")
    qqH_histo.Draw("HIST SAME")

    legend = ROOT.TLegend(0.7, 0.6, 0.9, 0.9)
    legend.AddEntry(data_histo, "Data", "lep")
    legend.AddEntry(ggH_histo, "ggH (x10)", "l")
    legend.AddEntry(qqH_histo, "qqH (x100)", "l")
    legend.AddEntry(tt_histo, "TT", "f")
    legend.AddEntry(wjets_histo, "W+jets", "f")
    legend.AddEntry(zll_histo, "Z->ll", "f")
    legend.AddEntry(ztt_histo, "Z->tt", "f")
    legend.AddEntry(qcd_histo, "QCD", "f")
    legend.Draw()
    canvas.SaveAs(f"plots/{var}_stack.png")


