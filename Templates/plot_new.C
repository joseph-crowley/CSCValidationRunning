#include <TH1.h>
#include <TH2.h>
#include <TDirectory.h>
#include <TROOT.h>
#include <TStyle.h>
#include <TPad.h>
#include <TPaveText.h>
#include <TText.h>
#include <TCanvas.h>
#include <iostream>
#include <fstream>

void printBadChambers(char* num_str, char *den_str, const char* type_str) {
  TH1F* num = (TH1F*)gROOT->FindObject(num_str)->Clone();
  TH1F *den = (TH1F*)gROOT->FindObject(den_str)->Clone();

  const char* label[18]={"ME-4/2","ME-4/1","ME-3/2","ME-3/1","ME-2/2","ME-2/1","ME-1/3","ME-1/2","ME-1/1",
		   "ME+1/1","ME+1/2","ME+1/3","ME+2/1","ME+2/2","ME+3/1","ME+3/2","ME+4/1","ME+4/2",};

  std::vector<string> badchambers;
  for(int i=0; i<num->GetNbinsX(); i++) {
     for(int j=0; j<num->GetNbinsY(); j++) {	
        int _num=num->GetBinContent(i+1,j+1);
        int _den=den->GetBinContent(i+1,j+1);
        if(_num!=_den) {

	  int ij=i;
	  int ix=j;
	  if(i<9) ij=9+i;
	  else {
	    ij=17-i;
	  }
	  int m=1;
	  if(ij==1 || ij==3 || ij==5 || ij==12 || ij==14 || ij==16)  { 
	    m=2;
	    if(j>=18) continue;
	  }

	  char _tmpstr[256];
	  float _error=1.0*_num/_den;
	  //	  printf("i %i, j %i, ij %i\n",i,j,ij);
	  sprintf(_tmpstr,"%s/%i %i/%i %.3f %s",label[ij],j+1,_num,_den,_error,type_str);
	  std::string _tmpstring = _tmpstr;
	  badchambers.push_back(_tmpstring);
        }

//        if(_num!=_den) printf("%s/%i %i/%i\n",label[i],j+1,_num,_den);
//                  else deadchambers.push_back(chamber);
     }
  }
   int n_dc = badchambers.size();
   //   ofstream file;
   //   file.open("bad_emulator_chamberlist.txt",ios::app);
   //   file << type_str << " fail:" << endl;
   if (n_dc > 0){
      for (int n = 0; n < n_dc; n++){
	printf("%s\n",badchambers[n].c_str());
	//         file << badchambers[n] << endl;
      }
   }
   printf("\n");
   //   file << endl;
   //   file.close();

}

bool is_bad_primitive(int bad1, int bad2, int mode) {
  if(bad1==1 && mode==0) {
    return true;
  }
  
  if(bad2==1 && mode==1) {
    return true;
  }
  if((bad1==1 || bad2==1) && mode==2) {
    return true;
  }
  return false;
}

void fill_hotwires(int bad_chambers[4][18][36]) {
  string filename[3] = {"../../templates/hot_wires.txt","../../templates/hot_strips.txt","../../templates/bad_chambers.txt"};
  for(int ifile=0; ifile<3; ifile++) {
    ifstream myfile(filename[ifile].c_str());
    if(myfile.fail()) {
      printf("Cant open file %s\n",filename[ifile].c_str());
      return;
    }
    string line;
    //  bool chamber_hotwires[18][36];
    for(int i=0; i<18; i++) {
      for(int j=0; j<36; j++) {
	bad_chambers[ifile][i][j]=0;
      }
    }

    while(getline(myfile,line)) {
      if(line.find("ME",0)!=string::npos) {
	//      printf("%s\n",line.c_str());
	int endcap=1;
	if(line[2]=='-') endcap=2;
	int station=line[3]-48;
	int ring=line[5]-48;
	int chamber=line[7]-48;
	if(line.size()==9) chamber=10*(line[7]-48)+line[8]-48;
	//      printf("endcap %i, station %i, ring %i, chamber %i\n",endcap,station,ring,chamber);
	int ix=0;
	if(station==1) ix=ring-1;
	else {
	  ix=3+2*(station-2)+ring-1;
	}
	if(endcap==2) ix+=9;
	bad_chambers[ifile][ix][chamber-1]=1;
	//      printf("ix %i\n",ix);
      }
    
    }
  }

  for(int i=0; i<18; i++) {
    //    printf("\nix %i\n",i);
    for(int j=0; j<36; j++) {
      //      printf("%i, ",chamber_hotwires[i][j]);
    }
  }
}

void form_hist2(int bad_chambers[4][18][36]) {

  const char* type_str[4]={"found","SameN","total","match"};
  const char* det_str[3]={"ALCT","CLCT","LCT"};
  const char* moo_str[3]={"A","C","L"};

  char num_str1[3][256];
  char num_str2[3][256];
  char den_str1[3][256];
  char den_str2[3][256];

  for(int i=0; i<3; i++) {
    sprintf(den_str1[i],"h_%s_%s2i",det_str[i],type_str[0]);
    sprintf(num_str1[i],"h_%s_%s2i",det_str[i],type_str[1]);
    sprintf(den_str2[i],"h_%s_%s2i",det_str[i],type_str[2]);
    sprintf(num_str2[i],"h_%s_%s2i",det_str[i],type_str[3]);
  }

  //  form_hist(bad_chambers,tmp_str1,tmp_str2,tmp_str3,i);
  
  int num[6][36][18];
  int den[6][36][18];
  char tmp_str[256];

  for(int k=0; k<3; k++) {
    char moo[256];
    TH1F* h_num = (TH1F*)gROOT->FindObject(num_str1[k]);
    TH1F* h_den = (TH1F*)gROOT->FindObject(den_str1[k]);
    sprintf(moo,"%s_num",det_str[k]);
    printBadChambers(num_str1[k], den_str1[k],moo);
    sprintf(moo,"%s_match",det_str[k]);
    printBadChambers(num_str2[k], den_str2[k],moo);
    for(int i=0; i<36; i++) {
      for(int j=0; j<18; j++) {
	num[k][i][j]=h_num->GetBinContent(j+1,i+1);
	den[k][i][j]=h_den->GetBinContent(j+1,i+1);
      }
    }

    h_num = (TH1F*)gROOT->FindObject(num_str2[k]);
    h_den = (TH1F*)gROOT->FindObject(den_str2[k]);
    for(int i=0; i<36; i++) {
      for(int j=0; j<18; j++) {
	num[k+3][i][j]=h_num->GetBinContent(j+1,i+1);
	den[k+3][i][j]=h_den->GetBinContent(j+1,i+1);
      }
    }
  }

  TH2F* h_ratio = new TH2F("h_ratio2","h_ratio2",36,0.5,36.5,18,0,18);
  //  h_ratio->SetXTitle("Chamber");
  h_ratio->GetXaxis()->SetTickLength(0);
  h_ratio->GetXaxis()->CenterTitle();
  h_ratio->Draw();
  TPaveText* pave_title = new TPaveText(5,18,32,20);
  TText* text_title = pave_title->AddText("Data versus trigger emulator agreement");
  text_title->SetTextSize(0.04);
  pave_title->SetBorderSize(0);
  pave_title->SetFillColor(0);
  pave_title->Draw();
  h_ratio->SetTitle("");

  const char* label[18]={"ME-4/2","ME-4/1","ME-3/2","ME-3/1","ME-2/2","ME-2/1","ME-1/3","ME-1/2","ME-1/1",
		   "ME+1/1","ME+1/2","ME+1/3","ME+2/1","ME+2/2","ME+3/1","ME+3/2","ME+4/1","ME+4/2",};

  for(int i=0; i<18; i++) {
    h_ratio->GetYaxis()->SetBinLabel(i+1,label[i]);

  }

  TPaveText* pave_legend_label = new TPaveText(-3.3,-2.0,0.5,-1.2);
  TText *text_legend_label = pave_legend_label->AddText("Problem Legend");
  pave_legend_label->SetBorderSize(0);
  pave_legend_label->SetFillColor(kGray+4);
  pave_legend_label->Draw();


  TPaveText* tb_xaxis1[36];
  TPaveText* tb_xaxis2[36];

  TPaveText* pave_legend = new TPaveText(-3.5,-2.2,36.6,-1.0);
  //  TText *text_legend = pave_legend->AddText("  Legend ");
  pave_legend->SetFillColor(kGray+4);
  pave_legend->SetBorderSize(1);
  //  pave_legend->Draw();
  int problem_cnt[6]={0};


  /*
  pave_good = new TPaveText(0.5,-2.0,9.5,-1.2);
  pave_bad = new TPaveText(12.5,-2.0,18.5,-1.2);
  pave_bad_known = new TPaveText(24.5,-2.0,36.5,-1.2);
  TText *text_legend_a[0] = pave_good->AddText("emulator and data agree");
  TText *text_legend_a[1]= pave_bad->AddText("unknown problem");
  TText *text_bad_known= pave_bad_known->AddText("known problem");

  pave_good->SetFillColor(kTeal+8);
  pave_bad->SetFillColor(kRed);
  pave_bad_known->SetFillColor(kYellow);
  pave_good->SetBorderSize(1);

  pave_bad->SetBorderSize(1);
  pave_bad_known->SetBorderSize(1);
  pave_good->Draw();
  pave_bad->Draw();
  pave_bad_known->Draw();
  */
  pave_legend_label = new TPaveText(-3.3,-2.0,0.5,-1.2);
  text_legend_label = pave_legend_label->AddText("Problem Legend");
  pave_legend_label->SetBorderSize(0);
  pave_legend_label->SetFillColor(kGray+4);
  pave_legend_label->Draw();



  for(int i=0; i<36; i++) {
    char stra[256]; sprintf(stra,"%i",i+1);
    tb_xaxis1[i] = new TPaveText(i+0.5, -0.5, i+1.5, 0);
    TText *text = tb_xaxis1[i]->AddText(stra);
    text->SetTextSize(0.015);
    tb_xaxis1[i]->SetFillColor(0);
    tb_xaxis1[i]->SetBorderSize(1);
    tb_xaxis1[i]->Draw();
  }
  for(int i=0; i<18; i++) {
    char stra[256]; sprintf(stra,"%i",i+1);
    tb_xaxis2[i] = new TPaveText(i*2+0.5, -1, 2*(i+1)+0.5, -0.5);
    TText *text = tb_xaxis2[i]->AddText(stra);
    text->SetTextSize(0.015);
    tb_xaxis2[i]->SetFillColor(0);
    tb_xaxis2[i]->SetBorderSize(1);
    tb_xaxis2[i]->Draw();
  }

  TPaveText *tb[3][36][18];
  int num_cnt1[3]={0};
  int den_cnt1[3]={0};
  int num_cnt2[3]={0};
  int den_cnt2[3]={0};

  int numb_cnt1[3]={0};
  int denb_cnt1[3]={0};
  int numb_cnt2[3]={0};
  int denb_cnt2[3]={0};


  for(int k=0; k<3; k++) {
    int mode=k;
    for(int i=0; i<36; i++) {
      for(int j=0; j<18; j++) {
	bool red_pass=false;
	for(int redi=0; redi<6; redi++) {
	  if(den[redi][i][j]!=0) red_pass=true;
	}
	int ij=j;
	int ix=i;
	if(j<9) ij=9+j;
	else {
	  ij=17-j;
	}
	int m=1;
	if(ij==1 || ij==3 || ij==5 || ij==12 || ij==14 || ij==16)  { 
	  m=2;
	  if(i>=18) continue;
	}

	if(true) {
	  tb[k][i][j] = new TPaveText(m*ix+0.5, ij+k*1.0/3, m*(ix+1)+0.5, ij+(k+1)*1.0/3);
	}
	else {
	  tb[k][i][j] = new TPaveText(m*ix+0.5, ij, m*(ix+1)+0.5, ij+1);
	}
	tb[k][i][j]->SetBorderSize(1);
	tb[k][i][j]->SetLineStyle(2);
	//	tb[k][i][j]->SetLineWidth(1);

	int _num1=num[k][i][j];
	int _den1=den[k][i][j];
	int _num2=num[k+3][i][j];
	int _den2=den[k+3][i][j];

	num_cnt1[k]+=_num1;
	den_cnt1[k]+=_den1;
	num_cnt2[k]+=_num2;
	den_cnt2[k]+=_den2;


	if(bad_chambers[0][j][i]!=1 && mode==0) {
	  numb_cnt1[k]+=_num1;
	  denb_cnt1[k]+=_den1;
	  numb_cnt2[k]+=_num2;
	  denb_cnt2[k]+=_den2;
	}

	if(bad_chambers[1][j][i]!=1 && mode==1) {
	  numb_cnt1[k]+=_num1;
	  denb_cnt1[k]+=_den1;
	  numb_cnt2[k]+=_num2;
	  denb_cnt2[k]+=_den2;
	}
	if(!(bad_chambers[0][j][i]==1 || bad_chambers[1][j][i]==1) && mode==2) {
	  numb_cnt1[k]+=_num1;
	  denb_cnt1[k]+=_den1;
	  numb_cnt2[k]+=_num2;
	  denb_cnt2[k]+=_den2;
	}


	TPaveText *tb2 = new TPaveText(m*ix+0.5, ij, m*(ix+1)+0.5, ij+1);	
	tb2->SetFillColor(0);
	tb2->SetBorderSize(1);
	tb2->SetLineWidth(3);
	tb2->SetFillStyle(0);

	if(_den1!=0 || _den2!=0) {	  
	  TText *text = tb[k][i][j]->AddText(moo_str[k]);	  
	  text->SetTextSize(0.015);
	  if(_num1==_den1 && _num2==_den2) {
	    tb[k][i][j]->SetFillColor(kTeal+8);
	    problem_cnt[0]++;
	  }	  
	  else {
	    float r = _den1!=0  ? 1.0*_num1/_den1 : 0;
	    float r2 = _den2!=0 ? 1.0*_num2/_den2 : 0;
	    if(r2<r) r=r2;
	    if(r>0.99 ) { 
	      tb[k][i][j]->SetFillColor(kYellow+kGreen); 
	      if(!(is_bad_primitive(bad_chambers[0][j][i], bad_chambers[1][j][i], mode)))
		problem_cnt[1]++;
	    }
	    if(r<0.99 && r>0.90) { 
	      tb[k][i][j]->SetFillColor(kYellow); 
	      if(!(is_bad_primitive(bad_chambers[0][j][i], bad_chambers[1][j][i], mode)))
		problem_cnt[2]++;
	    }
	    if(r<=0.90) { 
	      tb[k][i][j]->SetFillColor(kRed); 
	      if(!(is_bad_primitive(bad_chambers[0][j][i], bad_chambers[1][j][i], mode)))
		problem_cnt[3]++;
	    }
	    //	  if(r<=0.) tb[k][i][j]->SetFillColor(kRed);

	  }
	  if(_den1<100 && _den2<100) {tb[k][i][j]->SetFillColor(kGray);}
	  //	  tb[k][i][j]->SetBorderSize(1);
	  //	if(mode==0) tb5[i][j]->SetFillStyle(0);
	  //	if(_den!=0)

	  //	  if(!bad) {
	  tb[k][i][j]->Draw();
	  tb2->Draw();
	    //	  }
	    //	  else {
	    //	    tb2->Draw();
	    //	    tb[k][i][j]->Draw();
	  //	  }
	}
	else {
	  if(ij==0 || (ij==17 && (ix<9 || ix>12))) {
	  }
	  else {
	    problem_cnt[5]++;	
	    tb[k][i][j]->SetFillColor(kWhite);
	    if(bad_chambers[k][j][i]==1) {
	      tb[k][i][j]->SetLineColor(kBlue);
	      tb[k][i][j]->SetLineWidth(2);
	      problem_cnt[4]++;
	    }


	    tb[k][i][j]->SetLineWidth(1);
	    tb[k][i][j]->SetLineStyle(2);
	    tb[k][i][j]->Draw();
	    tb2->Draw();
	  }
	
	}
      }
    }
  }
  for(int k=0; k<3; k++) {
    int mode=k;
    for(int i=0; i<36; i++) {
      for(int j=0; j<18; j++) {
	int ij=j;
	int ix=i;
	if(j<9) ij=9+j;
	else {
	  ij=17-j;
	}
	int m=1;
	if(ij==1 || ij==3 || ij==5 || ij==12 || ij==14 || ij==16)  { 
	  m=2;
	  if(i>=18) continue;
	}
	int _num1=num[k][i][j];
	int _den1=den[k][i][j];
	int _num2=num[k+3][i][j];
	int _den2=den[k+3][i][j];

	TPaveText *tb2 = new TPaveText(m*ix+0.5, ij, m*(ix+1)+0.5, ij+1);	
	tb2->SetFillColor(0);
	tb2->SetBorderSize(1);
	tb2->SetLineWidth(4);
	tb2->SetFillStyle(0);
	if(bad_chambers[2][j][i]==1) {
	  tb2->SetLineColor(kBlue);
	  tb2->Draw();
	}
	if(_num1!=_den1 || _num2!=_den2) {
	  if(bad_chambers[0][j][i]==1 && mode==0) {
	    problem_cnt[4]++;
	    //	    tb[k][i][j]->SetFillColor(kBlue);
	    tb[k][i][j]->SetLineColor(kBlue);
	    tb[k][i][j]->SetLineWidth(4);
	    tb[k][i][j]->SetLineStyle(1);
	    tb[k][i][j]->Draw();
	  }
	  if(bad_chambers[1][j][i]==1 && mode==1) {
	    problem_cnt[4]++;
	    //	    tb[k][i][j]->SetFillColor(kBlue);
	    tb[k][i][j]->SetLineColor(kBlue);
	    tb[k][i][j]->SetLineWidth(4);
	    tb[k][i][j]->SetLineStyle(1);
	    tb[k][i][j]->Draw();
	  }
	  if((bad_chambers[0][j][i]==1 || bad_chambers[1][j][i]==1) && mode==2) {
	    problem_cnt[4]++;
	    //	    tb[k][i][j]->SetFillColor(kBlue);
	    tb[k][i][j]->SetLineColor(kBlue);
	    tb[k][i][j]->SetLineWidth(4);
	    tb[k][i][j]->SetLineStyle(1);
	    tb[k][i][j]->Draw();
	  }
	}
      }
    }
  }


  /*
  int num_cnt[3];
  int den_cnt[3];
  for (int i=0; i<3; i++) {
    float r1=1.0*num_cnt1[i]/den_cnt1[i];
    float r2=1.0*num_cnt2[i]/den_cnt2[i];
    if(r1<r2) { 
      num_cnt[i]=num_cnt1[i];
      den_cnt[i]=den_cnt1[i];
    }
    else {
      num_cnt[i]=num_cnt2[i];
      den_cnt[i]=den_cnt2[i];
    }
  }
  */
  TPaveText* pave_totalx = new TPaveText(36.6,17,40.9,18);
  pave_totalx->SetBorderSize(1.0);
  pave_totalx->AddText("Trigger Primitives");
  pave_totalx->Draw();

  TPaveText* pave_total = new TPaveText(36.6,15,40.9,17);
  pave_total->SetBorderSize(1.0);
  pave_total->AddText("L = ALCT*CLCT");
  pave_total->AddText("C = CLCT            ");
  pave_total->AddText("A = ALCT            ");
  pave_total->Draw();

  pave_totalx = new TPaveText(36.6,14,40.9,14.5);
  pave_totalx->AddText("Number");
  pave_totalx->SetTextSize(0.015);
  pave_totalx->SetBorderSize(1.0);
  pave_totalx->Draw();

  pave_total = new TPaveText(36.6,12.5,40.9,14);
  pave_total->SetBorderSize(1.0);
  sprintf(tmp_str,"L = %.1E",(float)den_cnt1[2]);
  pave_total->AddText(tmp_str);
  sprintf(tmp_str,"C = %.1E",(float)den_cnt1[1]);
  pave_total->AddText(tmp_str);
  sprintf(tmp_str,"A = %.1E",(float)den_cnt1[0]);
  pave_total->AddText(tmp_str);
  pave_total->Draw();

  pave_totalx = new TPaveText(36.6,10.5,40.9,12);
  pave_totalx->SetBorderSize(1.0);
  pave_totalx->SetTextSize(0.014);
  pave_totalx->AddText("Number agreement");
  pave_totalx->AddText("with (without)");
  pave_totalx->AddText("known problems");
  pave_totalx->Draw();

  pave_total = new TPaveText(36.6,8.5,40.9,10.5);
  pave_total->SetTextSize(0.012);
  pave_total->SetBorderSize(1.0);
  sprintf(tmp_str,"L = %.2f%% (%.2f%%)",den_cnt1[2]!=0 ? 100.0*num_cnt1[2]/den_cnt1[2] : 0, denb_cnt1[2]!=0 ? 100.0*numb_cnt1[2]/denb_cnt1[2] : 0);
  pave_total->AddText(tmp_str);
  sprintf(tmp_str,"C = %.2f%% (%.2f%%)",den_cnt1[1]!=0 ? 100.0*num_cnt1[1]/den_cnt1[1] : 0, denb_cnt1[1]!=0 ? 100.0*numb_cnt1[1]/denb_cnt1[1] : 0);
  pave_total->AddText(tmp_str);
  sprintf(tmp_str,"A = %.2f%% (%.2f%%)",den_cnt1[0]!=0 ? 100.0*num_cnt1[0]/den_cnt1[0] : 0, denb_cnt1[0]!=0 ? 100.0*numb_cnt1[0]/denb_cnt1[0] : 0);
  pave_total->AddText(tmp_str);
  pave_total->Draw();


  pave_totalx = new TPaveText(36.6,6.5,40.9,8);
  pave_totalx->SetBorderSize(1.0);
  pave_totalx->SetTextSize(0.014);
  pave_totalx->AddText("Match agreement");
  pave_totalx->AddText("with (without)");
  pave_totalx->AddText("known problems");

  pave_totalx->Draw();


  pave_total = new TPaveText(36.6,4.5,40.9,6.5);
  pave_total->SetBorderSize(1.0);
  sprintf(tmp_str,"L = %.2f%% (%.2f%%)",den_cnt2[2]!=0 ? 100.0*num_cnt2[2]/den_cnt2[2] : 0, denb_cnt2[2]!=0 ? 100.0*numb_cnt2[2]/denb_cnt2[2] : 0);
  pave_total->AddText(tmp_str);
  sprintf(tmp_str,"C = %.2f%% (%.2f%%)",den_cnt2[1]!=0 ? 100.0*num_cnt2[1]/den_cnt2[1] : 0, denb_cnt2[1]!=0 ? 100.0*numb_cnt2[1]/denb_cnt2[1] : 0);
  pave_total->AddText(tmp_str);
  sprintf(tmp_str,"A = %.2f%% (%.2f%%)",den_cnt2[0]!=0 ? 100.0*num_cnt2[0]/den_cnt2[0] : 0, denb_cnt2[0]!=0 ? 100.0*numb_cnt2[0]/denb_cnt2[0] : 0);
  pave_total->AddText(tmp_str);
  pave_total->Draw();

  pave_totalx = new TPaveText(36.6,2.5,40.9,3);
  pave_totalx->SetBorderSize(1.0);
  pave_totalx->SetTextSize(0.014);
  pave_totalx->AddText("Unknown problems");
  pave_totalx->Draw();

  pave_total = new TPaveText(36.6,0.5,40.9,2.5);
  pave_total->SetBorderSize(1.0);
  sprintf(tmp_str,"MINOR = %i",problem_cnt[1]);
  pave_total->AddText(tmp_str);
  sprintf(tmp_str,"MODERATE = %i",problem_cnt[2]);
  pave_total->AddText(tmp_str);
  sprintf(tmp_str,"BAD = %i",problem_cnt[3]);
  pave_total->AddText(tmp_str);
  pave_total->Draw();

  pave_total = new TPaveText(36.6,-2,40.9,0);
  pave_total->SetBorderSize(1.0);
  pave_total->AddText("Blue box = ");
  pave_total->AddText("known problem");
  pave_total->SetLineColor(kBlue);
  pave_total->SetLineWidth(3);
  pave_total->Draw();



  /*
  TPaveText* pave_total2 = new TPaveText(36.6,15,40.9,17);
  pave_total2->SetBorderSize(1.0);
  sprintf(tmp_str,"%.2f",100.0*num_cnt[0]/den_cnt[0]);
  if(strcmp(tmp_str,"100.00")==0) {
    sprintf(tmp_str,"#splitline{#frac{%i}{%i} #approx }{%.2f%%} ",num_cnt[0],den_cnt[0],100.0*num_cnt[0]/den_cnt[0]);
  }
  else sprintf(tmp_str,"#splitline{#frac{%i}{%i} = }{%.2f%%} ",num_cnt[0],den_cnt[0],100.0*num_cnt[0]/den_cnt[0]);

  TText* text_total2 = pave_total2->AddText(tmp_str);
  text_total2->SetTextSize(0.015);
  pave_total2->Draw();

  TPaveText* pave_total3 = new TPaveText(36.6,13,40.9,14);
  pave_total3->AddText("Total CLCT");
  pave_total3->SetBorderSize(1.0);
  pave_total3->Draw();
  TPaveText* pave_total4 = new TPaveText(36.6,11,40.9,13);
  sprintf(tmp_str,"%.2f",100.0*num_cnt2/den_cnt2);
  if(strcmp(tmp_str,"100.00")==0) {
    sprintf(tmp_str,"#splitline{#frac{%i}{%i} #approx }{%.2f%%} ",num_cnt[1],den_cnt[1],100.0*num_cnt[1]/den_cnt[1]);
  }
  else sprintf(tmp_str,"#splitline{#frac{%i}{%i} = }{%.2f%%} ",num_cnt[1],den_cnt[1],100.0*num_cnt[1]/den_cnt[1]);

  TText* text_total4 = pave_total4->AddText(tmp_str);
  text_total4->SetTextSize(0.015);
  pave_total4->SetBorderSize(1.0);
  pave_total4->Draw();

  TPaveText* pave_total5 = new TPaveText(36.6,9,40.9,10);
  pave_total5->AddText("Total MLCT");
  pave_total5->SetBorderSize(1.0);
  pave_total5->Draw();
  TPaveText* pave_total6 = new TPaveText(36.6,7,40.9,9);
  sprintf(tmp_str,"%.2f",100.0*num_cnt2/den_cnt2);
  if(strcmp(tmp_str,"100.00")==0) {
    sprintf(tmp_str,"#splitline{#frac{%i}{%i} #approx }{%.2f%%} ",num_cnt[2],den_cnt[2],100.0*num_cnt[2]/den_cnt[2]);
  }
  else sprintf(tmp_str,"#splitline{#frac{%i}{%i} = }{%.2f%%} ",num_cnt[2],den_cnt[2],100.0*num_cnt[2]/den_cnt[2]);
  TText* text_total6 = pave_total6->AddText(tmp_str);
  text_total6->SetTextSize(0.015);
  pave_total6->SetBorderSize(1.0);
  pave_total6->Draw();
  */
  char legend_str[6][256]={"OK","MINOR","MODERATE","BAD","Low stats","No data"};
  TPaveText* pave_legend_a[6];
  TText* text_legend_a[6];
  //  TPaveText* pave_legend_a2[6];
  //  TText* text_legend_a2[6];
  /*
  for(int i=0; i<6; i++) {
    sprintf(legend_str[i],"%s (%i)",legend_str[i],problem_cnt[i]);
  }
  */
  for(int i=0; i<6; i++) {
    int x1 =36/6*i;
    int x2 =36/6*(i+1);
    pave_legend_a[i] = new TPaveText(0.5+x1,-2.0,0.5+x2,-1.2);
    pave_legend_a[i]->AddText(legend_str[i]);
    pave_legend_a[i]->SetBorderSize(1);
    pave_legend_a[i]->SetTextSize(0.017);
    pave_legend_a[i]->Draw();
    /*
    pave_legend_a2[i] = new TPaveText(0.5+x1,-2.0,0.5+x2,-1.5);
    pave_legend_a2[i]->AddText(legend_str[i]);
    pave_legend_a2[i]->SetBorderSize(1);
    pave_legend_a2[i]->Draw();
    */
  }
  pave_legend_a[0]->SetFillColor(kTeal+8);
  pave_legend_a[1]->SetFillColor(kYellow+kGreen);
  pave_legend_a[2]->SetFillColor(kYellow);
  pave_legend_a[3]->SetFillColor(kRed);
  //  pave_legend_a[3]->SetFillColor(kRed);
  //  pave_legend_a[4]->SetFillColor(kBlue);
  pave_legend_a[4]->SetFillColor(kGray);
  //  pave_legend_a[4]->SetLineWidth(2);
  //  pave_legend_a[4]->SetLineColor(kBlue);
  pave_legend_a[5]->SetFillColor(kWhite);
  pave_legend_a[4]->Draw();
}

void plot_new() {
  gROOT->SetStyle("Plain");
  gStyle->SetOptStat("");

  gDirectory->cd("lctreader");

  TCanvas *c1 = new TCanvas("c1","c1",0,0,1280,1024);

  int  bad_chambers[4][18][36];
  fill_hotwires(bad_chambers);
  form_hist2(bad_chambers);
  c1->Print("emu_all.png");
}
