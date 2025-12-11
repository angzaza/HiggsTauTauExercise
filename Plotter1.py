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
    "ggH": ["/lustrehome/azaza/Higgstautau_exercise/CMSSW_14_2_2/src/HiggsTauTauNanoAODOutreachAnalysis/rootfiles_output/GluGluToHToTauTauAna.root"],
}

colors = {
        "ggH": ROOT.TColor.GetColor("#BF2229"),
        #"qqH": ROOT.TColor.GetColor("#00A88F"),
        #"TT": ROOT.TColor.GetColor(155, 152, 204),
        #"W": ROOT.TColor.GetColor(222, 90, 106),
        #"QCD":  ROOT.TColor.GetColor(250, 202, 255),
        #"ZLL": ROOT.TColor.GetColor(100, 192, 232),
        #"ZTT": ROOT.TColor.GetColor(248, 206, 104),
    }



ggH_histo = load_histos_from_files("histo_muon_pt", input_files["ggH"][0])
ggH_histo.SetLineColor(colors["ggH"])


# Create canvas
canvas = ROOT.TCanvas("canvas_muonPt", "canvas_muonPt", 800, 600)
ggH_histo.Scale(ggH_histo.Integral())
ggH_histo.SetTitle("Muon pT Distribution; pT [GeV]; Normalized to 1")
ggH_histo.Draw("HIST")

legend = ROOT.TLegend(0.7, 0.6, 0.9, 0.9)
legend.AddEntry(ggH_histo, "ggH", "l")
legend.Draw()
canvas.SaveAs(f"plots/muon_pt.png")


