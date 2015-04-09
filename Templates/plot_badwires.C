#include <TH1.h>
#include <TH2.h>
#include <TDirectory.h>
#include <TROOT.h>
#include <TStyle.h>
#include <TPad.h>
#include <TPaveText.h>
#include <TText.h>
#include <TCanvas.h>
#include <TPostScript.h>
#include <iostream>
#include <fstream>

void fill_hotwires(int bad_chambers[4][18][36]) {
  string filename[3] = {"hot_wires.txt","hot_strips.txt","bad_chambers.txt"};
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

void plot_badwires() {
  //  TH1FgROOT->FindObject("_file0");
  //  _file0->cd("lctreader");  

  int  bad_chambers[4][18][36];
  fill_hotwires(bad_chambers);

  gStyle->SetOptStat("0");
  gDirectory->cd("lctreader");
  TH1F* hHotWire1 = (TH1F*)gROOT->FindObject("hHotWire1");
  TH1F* hHotCham1 = (TH1F*)gROOT->FindObject("hHotCham1");
  int nx1=hHotWire1->GetNbinsX();
  int serial_old=-1;
  int chamber_old=-1;
  int layer_old=-1;
  int comma_cnt=0;

  TH1F* hHotWire_tmp  = new TH1F("hHotWire_tmp", "hHotWire_tmp",570*6*112,0,570*6*112);
  hHotWire_tmp->Sumw2();
  //  hHotWire_tmp->SetYTitle("Average number of time bins per wire group");
  int nwg=0;
  int nwg_bad=0;
  int ncham_hot=0;
  float r_avg=0;
  int r_cnt=0;

  int numa[36][18];
  int dena[36][18];
  int dena2[36][18];
  for(int i=0; i<18; i++) {
    for(int j=0; j<36; j++) {
      numa[j][i]=0;
      dena[j][i]=0;
      dena2[j][i]=0;
    }
  }


  int num_cnt=0;
  int den_cnt=0;



  for(int i=0; i<nx1; i++) {
    int serial=i/672;

    int num = hHotWire1->GetBinContent(i+1);
    int den = hHotCham1->GetBinContent(serial+1);
    if(num!=0) nwg++;
    if(serial!=serial_old) {
      serial_old=serial;
      //      printf("nserial1 %i\n",serial);
    }
    if(den==0) {
      int chamber=-999;
      int station=-999;
      int endcap=-999;
      int ring=-999;

      int bound[10]={0,36,72,108,126,162,180,216,234,300};
      int stationa[9]={1,1,1,2,2,3,3,4,4};
      int ringa[9]={1,2,3,1,2,1,2,1,2};

      if(serial<300) endcap=1;
      if(serial>=300) { 
	endcap=2;
      }      
      for(int j=0; j<9; j++) {
	if(serial>=bound[j] && serial<bound[j+1]) {
	  station=stationa[j];
	  ring=ringa[j];
	  chamber=serial-bound[j]+1;
	}
      }
      //      int nwg_a[9]={288, 384, 192, 672, 384, 576, 384, 576, 384};
      int nwg_a2[9]={48, 64, 32, 112, 64, 96, 64, 96, 64};
      int ix=0;
      if(station==1) ix=ring-1;
      else {
	ix=3+2*(station-2)+ring-1;
      }
      int layer = (i%672)/112;
      int wg = (i%672)%112;
      if(wg<nwg_a2[ix]) {
	char ec_str[2]={'+','-'};
	//	  printf("\n");
	//	printf("dead wire ME%c%i/%i/%i layer %i, wg %i\n",ec_str[endcap-1],station, ring, chamber,layer,wg);
      }
      
    }

    if(den!=0) { 
      float r=1.0*num/den;
      hHotWire_tmp->SetBinContent(i+1,r);
      hHotWire_tmp->SetBinError(i+1,r/sqrt(den));
      

      r_avg+=r;
      r_cnt++;
      //	printf("num %i, den %i, r %f \n",num,den,r);

      int layer = (i%672)/112;
      int wg = (i%672)%112;
      
      int chamber=-999;
      int endcap=-999;
      int station=-999;
      int ring=-999;
      //	printf("den %i, serial1 %i, serial2 %i",den,i,serial);
      if(serial<300) endcap=1;
      if(serial>=300) { 
	endcap=2;
	serial-=300;
      }
      int bound[10]={0,36,72,108,126,162,180,216,234,300};
      int stationa[9]={1,1,1,2,2,3,3,4,4};
      int ringa[9]={1,2,3,1,2,1,2,1,2};
      
      for(int j=0; j<9; j++) {
	if(serial>=bound[j] && serial<bound[j+1]) {
	  station=stationa[j];
	  ring=ringa[j];
	  chamber=serial-bound[j]+1;
	}
      }


      int ix=0;
      if(station==1) ix=ring-1;
      else {
	ix=3+2*(station-2)+ring-1;
      }
      if(endcap==2) ix+=9;
      
      if(num!=0) {
	dena[chamber-1][ix]++;
	dena2[chamber-1][ix]=den;
	den_cnt++;
      }
      if(r>=1) {
	if(num!=0) {
	  numa[chamber-1][ix]++;
	  num_cnt++;
	}
	bool new_chamber=false;
	if(chamber_old!=chamber) {	  
	  ncham_hot++;
	  new_chamber=true;
	  chamber_old=chamber;
	  layer_old=-1;
	  char ec_str[2]={'+','-'};
	  printf("\n");
	  printf("ME%c%i/%i/%i\n",ec_str[endcap-1],station, ring, chamber);
	}
	if (layer_old!=layer) {	  
	  comma_cnt=0;
	  layer_old=layer;
	  if(!new_chamber) printf("\n");
	  printf("Layer %i\nHot Wire Groups, average number of time bins on\n",layer);
	}
	//	if(comma_cnt>0) printf(", ");
	printf("%i %.2f\n",wg,r);
	comma_cnt++;
	nwg_bad++;
      }
    }

    //		    hHotWire->Fill(myendc*mystat,(chid-1)*672+(i_layer-1)*6+i_wire);
    
  }
  printf("r_avg %f\n",1.0*r_avg/r_cnt);
  //  hHotWire->GetZaxis()->SetRangeUser(1,16);
  printf("\n");
  printf("Number of hit wire groups %i\n",nwg);
  printf("Number of hot wire groups %i\n",nwg_bad);
  printf("Fraction of hot wire groups %e\n",1.0*nwg_bad/nwg);

  hHotWire_tmp->SetXTitle("Serialized wire groups for the entire detector");
  hHotWire_tmp->SetYTitle("Number of time bins on/events in chamber");
  hHotWire_tmp->GetXaxis()->CenterTitle();
  hHotWire_tmp->GetYaxis()->CenterTitle();
  hHotWire_tmp->SetTitle("");
  hHotWire_tmp->SetMarkerStyle(2);

 
  TCanvas *c1 = new TCanvas("c1","c1",10,10,1900,1200);
  TPad* pad1 = new TPad("pad1","pad1",0,0,1.0,0.9);
  TPad* pad2 = new TPad("pad2","pad2",0,0.9,1.0,1.0);

  pad1->Draw();
  pad1->cd();
  hHotWire_tmp->Draw(); 
  TLine *line[18];
  int lbound[10]={0,36,72,108,126,162,180,216,234,270};
  char* label[18]={"ME-4/2","ME-4/1","ME-3/2","ME-3/1","ME-2/2","ME-2/1","ME-1/3","ME-1/2","ME-1/1",
		   "ME+1/1","ME+1/2","ME+1/3","ME+2/1","ME+2/2","ME+3/1","ME+3/2","ME+4/1","ME+4/2"};
  TPaveText* lt[20];
  for(int i=0; i<20; i++) {
    int ix=0;
    if(i>=10) {
      ix=lbound[i-10]+300;
    }
    else {
      ix=lbound[i];
    }
    ix*=672;
    line[i]= new TLine(ix,0,ix,50);
    line[i]->Draw();
    line[i]->SetLineColor(kRed);
  }
  for(int i=0; i<18; i++) {
    int ix1=0;
    int ix2=0;
    if(i>=9) {
      ix1=lbound[i-9]+300;
      ix2=lbound[i-9+1]+300;
    }
    else {
      ix1=lbound[i];
      ix2=lbound[i+1];
    }
    ix1*=672;
    ix2*=672;
    ix1+=500;
    ix2-=500;
    lt[i] = new TPaveText(ix1,16.2,ix2,16.8,"br");
    if(i<9) {
      lt[i]->AddText(label[9+i]);
    }
    else {
      lt[i]->AddText(label[17-i]);
    }
    lt[i]->SetTextSize(0.015);
    lt[i]->SetFillColor(0);
    lt[i]->SetBorderSize(0);
    lt[i]->Draw();
  }



  pad2->Draw();
  pad2->cd(); 
  TPaveText *pt = new TPaveText(0.1,0.1,0.9,1.0,"br");
  pt->SetFillColor(0);
  pt->SetBorderSize(0);
  char asdf[256];
  sprintf(asdf,"Hit wire groups: %i",nwg);
  TText *text = pt->AddText(asdf);
  sprintf(asdf,"Hot wire groups: %i",nwg_bad);
  text = pt->AddText(asdf);
  sprintf(asdf,"Chambers with hot wire groups: %i",ncham_hot);
  text = pt->AddText(asdf);
  pt->Draw();

  c1->Print("hotwires.png");

  pad1->SetLogy();
  c1->Print("hotwires_log.png");

  char tmp_str[256];
  
  TCanvas *c2 = new TCanvas("c2","c2",10,10,1900,1200);
  TH2F* h_ratio = new TH2F("h_ratio","h_ratio",36,0.5,36.5,18,0,18);
  h_ratio->GetXaxis()->SetTickLength(0);
  h_ratio->GetXaxis()->CenterTitle();
  h_ratio->Draw();

  TPaveText* pave_title = new TPaveText(3,18.1,26,20);
  TText* text_title1 = pave_title->AddText("Top value in chamber = Number of hot wire group");
  TText* text_title2 = pave_title->AddText("Bottom value in chamber = Number of wire groups without hits");
  // TText* text_title = pave_title->AddText("Ratio in chamber = #frac{Number of hot wire groups}{Number of wire groups with hits + without hits}");
  text_title1->SetTextSize(0.02);
  text_title2->SetTextSize(0.02);
  pave_title->SetBorderSize(1);
  //  pave_title->SetFillColor(0);
  pave_title->Draw();
  h_ratio->SetTitle("");


  /*
  TPaveText* pave_title2 = new TPaveText(3,18.5,4,19.5);
  pave_title2->SetBorderSize(1);

  sprintf(tmp_str,"#frac{n}{N}=");
  TText* text_title2 = pave_title2->AddText(tmp_str);
  text_title2->SetTextSize(0.015);
  pave_title2->Draw();
  */
  //  char* label[18]={"ME-4/2","ME-4/1","ME-3/2","ME-3/1","ME-2/2","ME-2/1","ME-1/3","ME-1/2","ME-1/1",
  //		   "ME+1/1","ME+1/2","ME+1/3","ME+2/1","ME+2/2","ME+3/1","ME+3/2","ME+4/1","ME+4/2",};

  for(int i=0; i<18; i++) {
    h_ratio->GetYaxis()->SetBinLabel(i+1,label[i]);

  }
  TPaveText* tb_xaxis1[36];
  TPaveText* tb_xaxis2[36];

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

  for(int i=0; i<18; i++) {
    for(int j=0; j<36; j++) {
      
      //      printf("num %i, den %i\n",numa[j][i],dena[j][i]);
    }
  }

  TPaveText *tb[36][18];

  int num_nohit=0;
  int total_wg=0;
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
      int _num=numa[i][j];
      int _den=dena[i][j];
      int _den2=dena2[i][j];
      if(_den!=0) {
	int nwg_a[9]={288, 384, 192, 672, 384, 576, 384, 576, 384};
	//	int nwg_a2[9]={48, 64, 32, 112, 64, 96, 64, 96, 64};
	int nmiss=nwg_a[j<9 ? j: j-9]-_den;
	num_nohit+=nmiss;
	total_wg+=nwg_a[j<9 ? j: j-9];
	//	sprintf(tmp_str,"#frac{%i}{%i+%i}",_num,_den,nmiss);
	char tmp_str1[256];
	char tmp_str2[256];
	sprintf(tmp_str1,"%i",_num);
	sprintf(tmp_str2,"%i",nmiss);

	if(_num!=0 || nmiss!=0) {
	  TText *text1 = tb[i][j]->AddText(tmp_str1);
	  TText *text2 = tb[i][j]->AddText(tmp_str2);
	  text1->SetTextSize(0.015);
	  text2->SetTextSize(0.015);
	}
	tb[i][j]->SetBorderSize(1);


	if(_num==0) {
	  tb[i][j]->SetFillColor(kTeal+8);
	  if(nmiss!=0) { 
	    if(_den2>1000) {
	      tb[i][j]->SetFillColor(kYellow);
	    }
	    else {
	      tb[i][j]->SetFillColor(kGray);
	    }
	  }
	}
	else {
	  tb[i][j]->SetFillColor(kRed);
	}

	tb[i][j]->Draw();

      }
      else {
	tb[i][j]->SetFillColor(kWhite);
	tb[i][j]->Draw();
      }
    }
  }
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
      TPaveText *tb2 = new TPaveText(m*ix+0.5, ij, m*(ix+1)+0.5, ij+1);	
      tb2->SetFillColor(0);
      tb2->SetBorderSize(1);
      tb2->SetLineWidth(4);
      tb2->SetFillStyle(0);
      if(bad_chambers[0][j][i]==1 || bad_chambers[2][j][i]==1) {
       	tb2->SetLineWidth(4);
	tb2->SetLineColor(kBlue);
	tb2->Draw();
      }
    }
  }

  TPaveText* pave_total5 = new TPaveText(36.6,-0.1,39.1,18.1);
  pave_total5->SetBorderSize(1);
  pave_total5->Draw();


  TPaveText* pave_total4 = new TPaveText(38,0,39,18);
  pave_total4->SetBorderSize(0);
  TText* text_total4 = pave_total4->AddText("Total wire groups per chamber");
  text_total4->SetTextSize(0.030);
  text_total4->SetTextAngle(90);
  pave_total4->Draw();
  TPaveText *tb2[18];

  for(int j=0; j<18; j++) {
    int ij=0;
    if(j<9) ij=9+j;
    else {
      ij=17-j;
    }
    tb2[j] = new TPaveText(36.8, ij, 37.8, ij+1);
    int nwg_a[9]={288, 384, 192, 672, 384, 576, 384, 576, 384};
    char asdfasdf[256];
    sprintf(asdfasdf,"%i",nwg_a[j<9 ? j: j-9]);
    TText* asdf = tb2[j]->AddText(asdfasdf);
    tb2[j]->SetBorderSize(1);
    tb2[j]->SetFillColor(0);
    tb2[j]->Draw();
  }

  TPaveText* pave_total2 = new TPaveText(27,18.2,33,19.8);
  pave_total2->SetBorderSize(1.0);
  sprintf(tmp_str,"#frac{Total hot}{Total hit} = #frac{%i}{%i} = %.2f%%",num_cnt,den_cnt,100.0*num_cnt/den_cnt);    
  TText* text_total2 = pave_total2->AddText(tmp_str);
  text_total2->SetTextSize(0.015);
  pave_total2->Draw();

  TPaveText* pave_total3 = new TPaveText(33.1,18.2,40,19.8);
  pave_total3->SetBorderSize(1.0);
  sprintf(tmp_str,"#frac{Total without hits}{Total wire groups} = #frac{%i}{%i} = %.2f%%",num_nohit,total_wg,100.0*num_nohit/total_wg);    
  TText* text_total3 = pave_total3->AddText(tmp_str);
  text_total3->SetTextSize(0.015);
  pave_total3->Draw();

  char legend_str[6][256]={"no problems","dead wires","hot wires","low stats","no data"};
  TPaveText* pave_legend_a[5];
  TText* text_legend_a[5];
  TPaveText* pave_legend_a2[5];
  TText* text_legend_a2[5];
  for(int i=0; i<5; i++) {
    sprintf(legend_str[i],"%s",legend_str[i]);
  }
  
  for(int i=0; i<5; i++) {
    float x1 =1.0*36/5*i;
    float x2 =1.0*36/5*(i+1);
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
  pave_legend_a[1]->SetFillColor(kYellow);
  pave_legend_a[2]->SetFillColor(kRed);
  pave_legend_a[3]->SetFillColor(kGray);
  //  pave_legend_a[3]->SetFillColor(kRed);
  //  pave_legend_a[4]->SetFillColor(kBlue);
  //  printf("num_cnt %i, den_cnt %i, ratio %f\n",num_cnt, den_cnt,1.0*num_cnt/den_cnt);

  TPaveText* pave_total = new TPaveText(36.6,-2,40.9,-0.5);
  pave_total->SetBorderSize(1.0);
  pave_total->AddText("Blue box = ");
  pave_total->AddText("known problem");
  pave_total->SetLineColor(kBlue);
  pave_total->SetLineWidth(3);
  pave_total->Draw();

  c2->Print("hotchambers.png");
}
  
