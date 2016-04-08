#include "TEMPLATEDIR/myFunctions.C"

void makePlots_csctf() {

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

  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/CSCTF_Chamber_Occupancies", f1, true, "csctfChamberOccupancy.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/CSCTF_LCT", f1, true, "csctfLct.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/CSCTF_Track_ModeVsQual", f1, true, "csctfTrackModeVQual.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/CSCTF_bx", f1, true, "csctfBx.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/CSCTF_bx_H", f1, true, "csctfBxHalo.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/CSCTF_occupancies", f1, true, "csctfOccupancies.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/CSCTF_occupancies_H", f1, true, "csctfOccupanciesHalo.png", true);

  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_strip_MEminus11", f1, true, "csctfStripm11.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_strip_MEminus12", f1, true, "csctfStripm12.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_strip_MEminus13", f1, true, "csctfStripm13.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_strip_MEminus21", f1, true, "csctfStripm21.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_strip_MEminus22", f1, true, "csctfStripm22.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_strip_MEminus31", f1, true, "csctfStripm31.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_strip_MEminus32", f1, true, "csctfStripm32.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_strip_MEminus41", f1, true, "csctfStripm41.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_strip_MEminus42", f1, true, "csctfStripm42.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_strip_MEplus11", f1, true, "csctfStripp11.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_strip_MEplus12", f1, true, "csctfStripp12.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_strip_MEplus13", f1, true, "csctfStripp13.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_strip_MEplus21", f1, true, "csctfStripp21.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_strip_MEplus22", f1, true, "csctfStripp22.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_strip_MEplus31", f1, true, "csctfStripp31.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_strip_MEplus32", f1, true, "csctfStripp32.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_strip_MEplus41", f1, true, "csctfStripp41.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_strip_MEplus42", f1, true, "csctfStripp42.png", true);

  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_wire_MEminus11", f1, true, "csctfWirem11.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_wire_MEminus12", f1, true, "csctfWirem12.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_wire_MEminus13", f1, true, "csctfWirem13.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_wire_MEminus21", f1, true, "csctfWirem21.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_wire_MEminus22", f1, true, "csctfWirem22.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_wire_MEminus31", f1, true, "csctfWirem31.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_wire_MEminus32", f1, true, "csctfWirem32.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_wire_MEminus41", f1, true, "csctfWirem41.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_wire_MEminus42", f1, true, "csctfWirem42.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_wire_MEplus11", f1, true, "csctfWirep11.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_wire_MEplus12", f1, true, "csctfWirep12.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_wire_MEplus13", f1, true, "csctfWirep13.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_wire_MEplus21", f1, true, "csctfWirep21.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_wire_MEplus22", f1, true, "csctfWirep22.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_wire_MEplus31", f1, true, "csctfWirep31.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_wire_MEplus32", f1, true, "csctfWirep32.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_wire_MEplus41", f1, true, "csctfWirep41.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/csc_wire_MEplus42", f1, true, "csctfWirep42.png", true);



}
