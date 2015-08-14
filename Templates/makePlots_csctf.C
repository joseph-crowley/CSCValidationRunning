{
  gROOT->ProcessLine(".L TEMPLATEDIR/myFunctions.C");

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
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/CSCTF_occupancies", f1, true, "csctOccupancies.png", true);
  Draw2DTempPlot("DQMData/Run RUNNUMBER/L1T/Run summary/L1TCSCTF/CSCTF_occupancies_H", f1, true, "csctOccupanciesHalo.png", true);

}
