#include "TEMPLATEDIR/myFunctions.C"

void makePlots_emtf() {
    
    std::string Path = "FILENAME";
    // define the functions from the external file
    extern TFile* OpenFiles(std::string path);
    extern void makeCSCOccupancy(std::string histoname, TFile* f1, std::string histotitle, std::string savename);
    extern void Draw2DTempPlot(std::string histo, TFile* f1, bool includeME11, std::string savename, bool hasLabels = false);
    extern void make1DPlot(std::string histoname, TFile* f1, std::string histotitle, int statoption, std::string savename);
    extern void make1DPlot(std::string histoname, TFile* f1, std::string histotitle, std::string xtitle, std::string ytitle, int statoption, std::string savename);
    extern void printEmptyChambers(std::string histoname, std::string oname, TFile* f);
    extern void GlobalPosfromTree(std::string graphname, TFile* f1, int endcap, int station, std::string type, std::string savename);
    extern void NikolaiPlots(TFile *f_in, int flag);
    extern void makeEffGif(std::string histoname, TFile* f1, std::string histotitle, std::string savename);
    extern void Draw2DEfficiency(std::string histo, TFile* f1, std::string title, std::string savename);
    extern void make2DPlot(std::string histoname, TFile* f1, std::string histotitle, int statoption, std::string savename);
    extern void make2DPlot(std::string histoname, TFile* f1, std::string histotitle, std::string xtitle, std::string ytitle, int statoption, std::string savename);
    extern void makeProfile(std::string histoname, TFile* f1, std::string histotitle, int statoption, std::string savename);
    extern void makeProfile(std::string histoname, TFile* f1, std::string histotitle, std::string xtitle, std::string ytitle,int statoption, std::string savename);

    TFile *f1;
    f1 = OpenFiles(Path);

    //From EMTFHitCollection
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/cscLCTOccupancy", f1, true, "cscLCTOccupancy.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/cscLCTBX", f1, true, "cscBx.png", true);

    //From EMTFTrackCollection
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfTrackOccupancy", f1, true, "emtfTrackOccupancies.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfTrackBX", f1, true, "emtfBx.png", true);
   
    //Introduced in CMSSW_10_0_0_pre3
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/cscDQMOccupancy", f1, true, "cscDQMOccupancy.png", true);
    //New timing plots --
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/Timing/cscLCTTimingBX0", f1, true, "cscLCTTimingBX0.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/Timing/cscLCTTimingFracBX0", f1, true, "cscLCTTimingFracBX0.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/Timing/cscLCTTimingBXNeg1", f1, true, "cscLCTTimingBXNeg1.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/Timing/cscLCTTimingFracBXNeg1", f1, true, "cscLCTTimingFracBXNeg1.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/Timing/cscLCTTimingBXNeg2", f1, true, "cscLCTTimingBXNeg2.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/Timing/cscLCTTimingFracBXNeg2", f1, true, "cscLCTTimingFracBXNeg2.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/Timing/cscLCTTimingBXPos1", f1, true, "cscLCTTimingBXPos1.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/Timing/cscLCTTimingFracBXPos1", f1, true, "cscLCTTimingFracBXPos1.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/Timing/cscLCTTimingBXPos2", f1, true, "cscLCTTimingBXPos2.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/Timing/cscLCTTimingFracBXPos2", f1, true, "cscLCTTimingFracBXPos2.png", true);
    

    

    //CSC Strips and Wires
    //06.09.2017 - For these "neighboring" hits in overlap of trigger sectors not counted
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberStripMENeg11a", f1, true, "cscStripm11a.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberStripMENeg11b", f1, true, "cscStripm11b.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberStripMENeg12", f1, true, "cscStripm12.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberStripMENeg13", f1, true, "cscStripm13.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberStripMENeg21", f1, true, "cscStripm21.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberStripMENeg22", f1, true, "cscStripm22.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberStripMENeg31", f1, true, "cscStripm31.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberStripMENeg32", f1, true, "cscStripm32.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberStripMENeg41", f1, true, "cscStripm41.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberStripMENeg42", f1, true, "cscStripm42.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberStripMEPos11a", f1, true, "cscStripp11a.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberStripMEPos11b", f1, true, "cscStripp11b.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberStripMEPos12", f1, true, "cscStripp12.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberStripMEPos13", f1, true, "cscStripp13.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberStripMEPos21", f1, true, "cscStripp21.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberStripMEPos22", f1, true, "cscStripp22.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberStripMEPos31", f1, true, "cscStripp31.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberStripMEPos32", f1, true, "cscStripp32.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberStripMEPos41", f1, true, "cscStripp41.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberStripMEPos42", f1, true, "cscStripp42.png", true);

    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberWireMENeg11a", f1, true, "cscWirem11a.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberWireMENeg11b", f1, true, "cscWirem11b.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberWireMENeg12", f1, true, "cscWirem12.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberWireMENeg13", f1, true, "cscWirem13.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberWireMENeg21", f1, true, "cscWirem21.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberWireMENeg22", f1, true, "cscWirem22.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberWireMENeg31", f1, true, "cscWirem31.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberWireMENeg32", f1, true, "cscWirem32.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberWireMENeg41", f1, true, "cscWirem41.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberWireMENeg42", f1, true, "cscWirem42.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberWireMEPos11a", f1, true, "cscWirep11a.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberWireMEPos11b", f1, true, "cscWirep11b.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberWireMEPos12", f1, true, "cscWirep12.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberWireMEPos13", f1, true, "cscWirep13.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberWireMEPos21", f1, true, "cscWirep21.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberWireMEPos22", f1, true, "cscWirep22.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberWireMEPos31", f1, true, "cscWirep31.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberWireMEPos32", f1, true, "cscWirep32.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberWireMEPos41", f1, true, "cscWirep41.png", true);
    Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCInput/cscChamberWireMEPos42", f1, true, "cscWirep42.png", true);

}
