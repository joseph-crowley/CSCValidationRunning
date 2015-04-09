#include <TH1.h>
#include <TDirectory.h>
#include <TROOT.h>
#include <TStyle.h>
#include <TPad.h>
#include <TPaveText.h>
#include <TText.h>
#include <TCanvas.h>

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

form_hist2(int bad_chambers[4][18][36]) {

  char* type_str[4]={"found","SameN","total","match"};
  char* det_str[3]={"ALCT","CLCT","LCT"};

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
    TH1F* h_num = (TH1F*)gROOT->FindObject(num_str1[k]);
    TH1F* h_den = (TH1F*)gROOT->FindObject(den_str1[k]);
    for(int i=0; i<36; i++) {
      for(int j=0; j<18; j++) {
	num[k][i][j]=h_num->GetBinContent(j+1,i+1);
	den[k][i][j]=h_den->GetBinContent(j+1,i+1);
      }
    }

    TH1F* h_num = (TH1F*)gROOT->FindObject(num_str2[k]);
    TH1F* h_den = (TH1F*)gROOT->FindObject(den_str2[k]);
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
  pave_title = new TPaveText(5,18,32,20);
  TText* text_title = pave_title->AddText("moo");
  text_title->SetTextSize(0.04);
  pave_title->SetBorderSize(0);
  pave_title->SetFillColor(0);
  pave_title->Draw();
  h_ratio->SetTitle("");

  char* label[18]={"ME-4/2","ME-4/1","ME-3/2","ME-3/1","ME-2/2","ME-2/1","ME-1/3","ME-1/2","ME-1/1",
		   "ME+1/1","ME+1/2","ME+1/3","ME+2/1","ME+2/2","ME+3/1","ME+3/2","ME+4/1","ME+4/2",};

  for(int i=0; i<18; i++) {
    h_ratio->GetYaxis()->SetBinLabel(i+1,label[i]);

  }

}



form_hist(int bad_chambers[4][18][36], char* num_str, char *den_str, char* title, int mode) {
  //  int chamber_hotwires[18][36];
  //  fill_hotwires(chamber_hotwires);
  //  gROOT->SetStyle("Plain");
  //  gStyle->SetOptStat("");
  //  gDirectory->cd("lctreader");

  
  int num[36][18];
  int den[36][18];
  char tmp_str[256];

  TH1F* h_num = (TH1F*)gROOT->FindObject(num_str);
  TH1F* h_den = (TH1F*)gROOT->FindObject(den_str);
  for(int i=0; i<36; i++) {
    for(int j=0; j<18; j++) {
      num[i][j]=h_num->GetBinContent(j+1,i+1);
      den[i][j]=h_den->GetBinContent(j+1,i+1);
    }
  }

  TPaveText *tb[36][18];

  TH2F* h_ratio = new TH2F("h_ratio","h_ratio",36,0.5,36.5,18,0,18);
  //  h_ratio->SetXTitle("Chamber");
  h_ratio->GetXaxis()->SetTickLength(0);
  h_ratio->GetXaxis()->CenterTitle();
  h_ratio->Draw();
  pave_title = new TPaveText(5,18,32,20);
  TText* text_title = pave_title->AddText(title);
  text_title->SetTextSize(0.04);
  pave_title->SetBorderSize(0);
  pave_title->SetFillColor(0);
  pave_title->Draw();
  h_ratio->SetTitle("");

  char* label[18]={"ME-4/2","ME-4/1","ME-3/2","ME-3/1","ME-2/2","ME-2/1","ME-1/3","ME-1/2","ME-1/1",
		   "ME+1/1","ME+1/2","ME+1/3","ME+2/1","ME+2/2","ME+3/1","ME+3/2","ME+4/1","ME+4/2",};

  for(int i=0; i<18; i++) {
    h_ratio->GetYaxis()->SetBinLabel(i+1,label[i]);

  }

  TPaveText* tb_xaxis1[36];
  TPaveText* tb_xaxis2[36];

  pave_legend = new TPaveText(-3.5,-2.2,36.6,-1.0);
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
  TText *text_legend_label = pave_legend_label->AddText("Problem Legend");
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

  int num_cnt=0;
  int den_cnt=0;
  int num_cnt2=0;
  int den_cnt2=0;
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
      tb[i][j] = new TPaveText(m*ix+0.5, ij, m*(ix+1)+0.5, ij+1);
      tb[i][j]->SetBorderSize(1);
      int _num=num[i][j];
      int _den=den[i][j];
      num_cnt+=_num;
      den_cnt+=_den;


      if(bad_chambers[0][j][i]!=1 && mode==0) {
	num_cnt2+=_num;
	den_cnt2+=_den;
      }

      if(bad_chambers[1][j][i]!=1 && mode==1) {
	num_cnt2+=_num;
	den_cnt2+=_den;
      }
      if(!(bad_chambers[0][j][i]==1 || bad_chambers[1][j][i]==1) && mode==2) {
	num_cnt2+=_num;
	den_cnt2+=_den;
      }


      if(_den!=0) {
	if(_den>=1000) {
	  if(_num==_den) {
	    sprintf(tmp_str,"%.0f%%",100.0*_num/_den);
	  }
	  else {
	    sprintf(tmp_str,"%.1f%%",100.0*_num/_den);
	    if(strcmp(tmp_str,"100.0%")==0) strcpy(tmp_str,"99.9%");
	  }

	}
	else {
	  sprintf(tmp_str,"#frac{%i}{%i}",_num,_den);
	}
	TText *text = tb[i][j]->AddText(tmp_str);
	text->SetTextSize(0.015);
	if(_den>1000)
	  text->SetTextSize(0.009);
	if(_num==_den) {
	  tb[i][j]->SetFillColor(kTeal+8);
	  problem_cnt[0]++;
	}
	else {
	  float r = 1.0*_num/_den;
	  if(r>0.99) { tb[i][j]->SetFillColor(kYellow+kGreen); problem_cnt[1]++;}
	  if(r<0.99 && r>0.90) { tb[i][j]->SetFillColor(kYellow); problem_cnt[2]++;}
	  if(r<=0.90 && r>=0.1) {tb[i][j]->SetFillColor(kRed); problem_cnt[3]++;}
	  //	  if(r<=0.) tb[i][j]->SetFillColor(kRed);
	  if(bad_chambers[0][j][i]==1 && mode==0) {
	    problem_cnt[4]++;
	    //	    tb[i][j]->SetFillColor(kBlue);
	    tb[i][j]->SetLineColor(kBlue);
	    tb[i][j]->SetLineWidth(3);
	  }
	  if(bad_chambers[1][j][i]==1 && mode==1) {
	    problem_cnt[4]++;
	    //	    tb[i][j]->SetFillColor(kBlue);
	    tb[i][j]->SetLineColor(kBlue);
	    tb[i][j]->SetLineWidth(3);
	  }
	  if((bad_chambers[0][j][i]==1 || bad_chambers[1][j][i])==1 && mode==2) {
	    problem_cnt[4]++;
	    //	    tb[i][j]->SetFillColor(kBlue);
	    tb[i][j]->SetLineColor(kBlue);
	    tb[i][j]->SetLineWidth(3);
	  }

	}

	tb[i][j]->SetBorderSize(1);
	//	if(mode==0) tb5[i][j]->SetFillStyle(0);
	//	if(_den!=0)
	tb[i][j]->Draw();
      }
      else {
	if(ij==0 || ij==17) {
	}
	else {
	  problem_cnt[5]++;
	
	  tb[i][j]->SetFillColor(kGray);
	  if(bad_chambers[2][j][i]==1) {
	    tb[i][j]->SetLineColor(kBlue);
	    tb[i][j]->SetLineWidth(3);
	    problem_cnt[4]++;
	  }
	  else {
	    tb[i][j]->SetLineColor(kRed);
	    tb[i][j]->SetLineWidth(3);
	  }
	  tb[i][j]->Draw();
	}
      }
    }
  }       
  for(int i=0; i<36; i++) {
    for(int j=0; j<18; j++) {
      if(bad_chambers[0][j][i]==1 && mode!=1) {
	tb[i][j]->Draw();
	//	    tb[i][j]->SetFillColor(kBlue);
	//	tb[i][j]->SetLineColor(kBlue);
	//	tb[i][j]->SetLineWidth(3);
      }
    }
  }
  TPaveText* pave_total = new TPaveText(36.6,17,40.9,18);
  pave_total->SetBorderSize(1.0);
  pave_total->AddText("Overall ratio:");
  pave_total->Draw();
  TPaveText* pave_total2 = new TPaveText(36.6,15,40.9,17);
  pave_total2->SetBorderSize(1.0);
  sprintf(tmp_str,"%.2f",100.0*num_cnt/den_cnt);
  if(strcmp(tmp_str,"100.00")==0) {
    sprintf(tmp_str,"#splitline{#frac{%i}{%i} #approx }{%.2f%%} ",num_cnt,den_cnt,100.0*num_cnt/den_cnt);
  }
  else sprintf(tmp_str,"#splitline{#frac{%i}{%i} = }{%.2f%%} ",num_cnt,den_cnt,100.0*num_cnt/den_cnt);    
  TText* text_total2 = pave_total2->AddText(tmp_str);
  text_total2->SetTextSize(0.015);
  pave_total2->Draw();
  TPaveText* pave_total3 = new TPaveText(36.6,13,40.9,14);
  pave_total3->AddText("#splitline{Excluding known }{problems:}");
  pave_total3->SetBorderSize(1.0);
  pave_total3->Draw();
  TPaveText* pave_total4 = new TPaveText(36.6,11,40.9,13);
  sprintf(tmp_str,"%.2f",100.0*num_cnt2/den_cnt2);
  if(strcmp(tmp_str,"100.00")==0) {
    sprintf(tmp_str,"#splitline{#frac{%i}{%i} #approx }{%.2f%%} ",num_cnt2,den_cnt2,100.0*num_cnt2/den_cnt2);
  }
  else sprintf(tmp_str,"#splitline{#frac{%i}{%i} = }{%.2f%%} ",num_cnt2,den_cnt2,100.0*num_cnt2/den_cnt2);    
  TText* text_total4 = pave_total4->AddText(tmp_str);
  text_total4->SetTextSize(0.015);
  pave_total4->SetBorderSize(1.0);
  pave_total4->Draw();

  char legend_str[6][256]={"ratio = 1","1 > ratio > 0.99","0.99 > ratio > 0.9","ratio < 0.9","known","no data"};
  TPaveText* pave_legend_a[6];
  TText* text_legend_a[6];
  TPaveText* pave_legend_a2[6];
  TText* text_legend_a2[6];
  for(int i=0; i<6; i++) {
    sprintf(legend_str[i],"%s (%i)",legend_str[i],problem_cnt[i]);
  }

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
  pave_legend_a[4]->SetFillColor(kWhite);
  pave_legend_a[4]->SetLineWidth(2);
  pave_legend_a[4]->SetLineColor(kBlue);
  pave_legend_a[5]->SetFillColor(kGray);
  pave_legend_a[4]->Draw();

  //  printf("num_cnt %i, den_cnt %i, ratio %f\n",num_cnt, den_cnt,1.0*num_cnt/den_cnt);
}

void makePlots_emulator2() {
  gROOT->SetStyle("Plain");
  gStyle->SetOptStat("");
  //  gStyle->SetPaintTextFormat(".0f");
  /*
  TStyle *mystyle = new TStyle("plain","style1");
  mystyle->SetPalette(1);
  mystyle->SetPaintTextFormat(".2f");
  */
  gDirectory->cd("lctreader");
  //  _file0->cd("lctreader");
  char* type_str[4]={"found","SameN","total","match"};
  char* det_str[3]={"ALCT","CLCT","LCT"};
  char* det_str2[3]={"ALCT","CLCT","ALCT*CLCT"};
  TCanvas *c1 = new TCanvas("c1","c1",0,0,1280,1024);

  int  bad_chambers[4][18][36];
  fill_hotwires(bad_chambers);
  //  form_hist2(bad_chambers);
  //  return;
  for(int i=0; i<3; i++) {
    char tmp_str1[256]; char tmp_str2[256]; char tmp_str3[256];
    /*
    sprintf(tmp_str1,"h_%s_%s",det_str[i],type_str[0]);
    sprintf(tmp_str2,"Number of %ss in data",det_str[i]);
    form_hist(tmp_str1,"",0,tmp_str2);
    sprintf(tmp_str1,"num_%s.png",det_str[i]);
    c1->Print(tmp_str1);
    */
    
    sprintf(tmp_str1,"h_%s_%s2i",det_str[i],type_str[1]);
    sprintf(tmp_str2,"h_%s_%s2i",det_str[i],type_str[0]);
    sprintf(tmp_str3,"Ratio of events with same number of %ss",det_str2[i]);
    form_hist(bad_chambers,tmp_str1,tmp_str2,tmp_str3,i);
    //    printBadChambers(tmp_str1, tmp_str2, tmp_str3);
    sprintf(tmp_str1,"num_%s.png",det_str[i]);
    c1->Print(tmp_str1);
    
    sprintf(tmp_str1,"h_%s_%s2i",det_str[i],type_str[3]);
    sprintf(tmp_str2,"h_%s_%s2i",det_str[i],type_str[2]);
    sprintf(tmp_str3,"Ratio of exact matched %ss",det_str2[i]);
    form_hist(bad_chambers,tmp_str1,tmp_str2,tmp_str3,i);
    //    printBadChambers(tmp_str1, tmp_str2, tmp_str3);
    sprintf(tmp_str1,"match_%s.png",det_str[i]);
    c1->Print(tmp_str1);

/*
    sprintf(tmp_str2,"h_%s_%s",det_str[i],type_str[2]);
    sprintf(tmp_str3,"Number of total %ss",det_str[i]);
    form_hist(tmp_str2,"",0,tmp_str3);
    sprintf(tmp_str1,"total_%s.png",det_str[i]);
    c1->Print(tmp_str1);
*/
  }
  return;
}
