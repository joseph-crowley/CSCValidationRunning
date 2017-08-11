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
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfHitBX", f1, true, "emtfBx.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfTrackOccupancy", f1, true, "emtfTrackOccupancies.png", true);
  // Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCTF_LCT", f1, true, "csctfLct.png", true);
  // Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCTF_bx_H", f1, true, "csctfBxHalo.png", true);
  // Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCTF_Track_ModeVsQual", f1, true, "csctfTrackModeVQual.png", true);
  // Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/CSCTF_occupancies_H", f1, true, "csctfOccupanciesHalo.png", true);

  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberStripMENeg11", f1, true, "emtfStripm11.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberStripMENeg12", f1, true, "emtfStripm12.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberStripMENeg13", f1, true, "emtfStripm13.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberStripMENeg21", f1, true, "emtfStripm21.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberStripMENeg22", f1, true, "emtfStripm22.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberStripMENeg31", f1, true, "emtfStripm31.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberStripMENeg32", f1, true, "emtfStripm32.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberStripMENeg41", f1, true, "emtfStripm41.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberStripMENeg42", f1, true, "emtfStripm42.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberStripMEPos11", f1, true, "emtfStripp11.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberStripMEPos12", f1, true, "emtfStripp12.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberStripMEPos13", f1, true, "emtfStripp13.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberStripMEPos21", f1, true, "emtfStripp21.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberStripMEPos22", f1, true, "emtfStripp22.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberStripMEPos31", f1, true, "emtfStripp31.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberStripMEPos32", f1, true, "emtfStripp32.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberStripMEPos41", f1, true, "emtfStripp41.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberStripMEPos42", f1, true, "emtfStripp42.png", true);

  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberWireMENeg11", f1, true, "emtfWirem11.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberWireMENeg12", f1, true, "emtfWirem12.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberWireMENeg13", f1, true, "emtfWirem13.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberWireMENeg21", f1, true, "emtfWirem21.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberWireMENeg22", f1, true, "emtfWirem22.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberWireMENeg31", f1, true, "emtfWirem31.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberWireMENeg32", f1, true, "emtfWirem32.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberWireMENeg41", f1, true, "emtfWirem41.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberWireMENeg42", f1, true, "emtfWirem42.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberWireMEPos11", f1, true, "emtfWirep11.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberWireMEPos12", f1, true, "emtfWirep12.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberWireMEPos13", f1, true, "emtfWirep13.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberWireMEPos21", f1, true, "emtfWirep21.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberWireMEPos22", f1, true, "emtfWirep22.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberWireMEPos31", f1, true, "emtfWirep31.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberWireMEPos32", f1, true, "emtfWirep32.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberWireMEPos41", f1, true, "emtfWirep41.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TStage2EMTF/emtfChamberWireMEPos42", f1, true, "emtfWirep42.png", true);



}
