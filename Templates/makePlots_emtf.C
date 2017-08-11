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

  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitOccupancy", f1, true, "emtfChamberOccupancy.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitBX_bx", f1, true, "emtfBx.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfTrackOccupancy", f1, true, "emtfTrackOccupancies.png", true);
  // Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCTF_LCT", f1, true, "csctfLct.png", true);
  // Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCTF_bx_H", f1, true, "csctfBxHalo.png", true);
  // Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCTF_Track_ModeVsQual", f1, true, "csctfTrackModeVQual.png", true);
  // Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCTF_occupancies_H", f1, true, "csctfOccupanciesHalo.png", true);

  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitStripMENeg11", f1, true, "emtfStripm11.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitStripMENeg12", f1, true, "emtfStripm12.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitStripMENeg13", f1, true, "emtfStripm13.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitStripMENeg21", f1, true, "emtfStripm21.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitStripMENeg22", f1, true, "emtfStripm22.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitStripMENeg31", f1, true, "emtfStripm31.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitStripMENeg32", f1, true, "emtfStripm32.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitStripMENeg41", f1, true, "emtfStripm41.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitStripMENeg42", f1, true, "emtfStripm42.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitStripMEPos11", f1, true, "emtfStripp11.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitStripMEPos12", f1, true, "emtfStripp12.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitStripMEPos13", f1, true, "emtfStripp13.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitStripMEPos21", f1, true, "emtfStripp21.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitStripMEPos22", f1, true, "emtfStripp22.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitStripMEPos31", f1, true, "emtfStripp31.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitStripMEPos32", f1, true, "emtfStripp32.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitStripMEPos41", f1, true, "emtfStripp41.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitStripMEPos42", f1, true, "emtfStripp42.png", true);

  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitWireMENeg11", f1, true, "emtfWirem11.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitWireMENeg12", f1, true, "emtfWirem12.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitWireMENeg13", f1, true, "emtfWirem13.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitWireMENeg21", f1, true, "emtfWirem21.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitWireMENeg22", f1, true, "emtfWirem22.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitWireMENeg31", f1, true, "emtfWirem31.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitWireMENeg32", f1, true, "emtfWirem32.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitWireMENeg41", f1, true, "emtfWirem41.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitWireMENeg42", f1, true, "emtfWirem42.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitWireMEPos11", f1, true, "emtfWirep11.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitWireMEPos12", f1, true, "emtfWirep12.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitWireMEPos13", f1, true, "emtfWirep13.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitWireMEPos21", f1, true, "emtfWirep21.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitWireMEPos22", f1, true, "emtfWirep22.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitWireMEPos31", f1, true, "emtfWirep31.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitWireMEPos32", f1, true, "emtfWirep32.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitWireMEPos41", f1, true, "emtfWirep41.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitWireMEPos42", f1, true, "emtfWirep42.png", true);



}
