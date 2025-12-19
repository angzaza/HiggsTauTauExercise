#!/bin/bash

echo "Starting analysis jobs..."
echo "python3 Analyzer.py GluGluToHToTauTauSkim.root --out rootfiles_output/GluGluToHToTauTauAna.root"
python3 Analyzer.py GluGluToHToTauTauSkim.root --out rootfiles_output/GluGluToHToTauTauAna.root
sleep 1

echo "python3 Analyzer.py VBF_HToTauTauSkim.root --out rootfiles_output/VBF_HToTauTauAna.root"
python3 Analyzer.py VBF_HToTauTauSkim.root --out rootfiles_output/VBF_HToTauTauAna.root
sleep 1

echo "python3 Analyzer.py DYJetsToLLkim.root --out rootfiles_output/DYJetsToTauTauAna.root --ZJetsDecay Ztautau"
python3 Analyzer.py DYJetsToLLSkim.root --out rootfiles_output/DYJetsToTauTauAna.root --ZJetsDecay Ztautau
sleep 1

echo "python3 Analyzer.py DYJetsToLLkim.root --out rootfiles_output/DYJetsToLLAna.root --ZJetsDecay Zll"
python3 Analyzer.py DYJetsToLLSkim.root --out rootfiles_output/DYJetsToLLAna.root --ZJetsDecay Zll
sleep 1

echo "python3 Analyzer.py TTbarSkim.root --out rootfiles_output/TTbarAna.root"
python3 Analyzer.py TTbarSkim.root --out rootfiles_output/TTbarAna.root
sleep 1

echo "python3 Analyzer.py W1JetsToLNuSkim.root --out rootfiles_output/W1JetsToLNuAna.root"
python3 Analyzer.py W1JetsToLNuSkim.root --out rootfiles_output/W1JetsToLNuAna.root
sleep 1

echo "python3 Analyzer.py W2JetsToLNuSkim.root --out rootfiles_output/W2JetsToLNuAna.root"
python3 Analyzer.py W2JetsToLNuSkim.root --out rootfiles_output/W2JetsToLNuAna.root
sleep 1

echo "python3 Analyzer.py W3JetsToLNuSkim.root --out rootfiles_output/W3JetsToLNuAna.root"
python3 Analyzer.py W3JetsToLNuSkim.root --out rootfiles_output/W3JetsToLNuAna.root
sleep 1

echo "python3 Analyzer.py Run2012B_TauPlusXSkim.root --out rootfiles_output/Run2012B_TauPlusXAna.root"
python3 Analyzer.py Run2012B_TauPlusXSkim.root --out rootfiles_output/Run2012B_TauPlusXAna.root
sleep 1

echo "python3 Analyzer.py Run2012C_TauPlusXSkim.root --out rootfiles_output/Run2012C_TauPlusXAna.root"
python3 Analyzer.py Run2012C_TauPlusXSkim.root --out rootfiles_output/Run2012C_TauPlusXAna.root
sleep 1 




