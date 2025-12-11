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
    "ZTT": ["rootfiles_output/DYJetsToTauTauAna.root"],
}

colors = {
        "ggH": ROOT.TColor.GetColor("#BF2229"),
        #"qqH": ROOT.TColor.GetColor("#00A88F"),
        #"TT": ROOT.TColor.GetColor(155, 152, 204),
        #"W": ROOT.TColor.GetColor(222, 90, 106),
        #"QCD":  ROOT.TColor.GetColor(250, 202, 255),
        #"ZLL": ROOT.TColor.GetColor(100, 192, 232),
        "ZTT": ROOT.TColor.GetColor(248, 206, 104),
    }




ggH_histo = load_histos_from_files("histo_BestTau_eta", input_files["ggH"][0])
ggH_histo.SetLineColor(colors["ggH"])

ztt_histo = load_histos_from_files("histo_BestTau_eta", input_files["ZTT"][0])
ztt_histo.SetLineColor(colors["ZTT"])
ztt_histo.SetFillColor(colors["ZTT"])



# Create stack
stack = ROOT.THStack("stack", "histo_BestTau_eta")
stack.Add(ztt_histo)
    
    
    
# Create canvas
canvas = ROOT.TCanvas("c1", "c1", 800, 600)
stack.Draw("HIST")
stack.SetMaximum(stack.GetMaximum()*1.3)
ggH_histo.Scale(10)  # scale signal for visibility
ggH_histo.SetLineWidth(2)
ggH_histo.Draw("HIST SAME")

legend = ROOT.TLegend(0.7, 0.6, 0.9, 0.9)
legend.AddEntry(ggH_histo, "ggH (x10)", "l")
legend.AddEntry(ztt_histo, "ZTT", "f")
legend.Draw()
canvas.SaveAs(f"plots/BestTau_pt_stack.png")


