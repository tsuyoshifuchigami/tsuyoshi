#coding:utf-8
import time
import urllib.request
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import csv
from tqdm import tqdm
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import numpy as np
from numpy import nan as NA

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

pp=0
Q=0

columns=["num","racename","date","where","weather","condition","course","distance","money_r","ryou","yayaomo","omo","furyou","shiba","suna","hare","kumori","kosame","ame","koyuki","yuki","tyaku","waku","waku_1","waku_2","waku_3","waku_4","waku_5","waku_6","waku_7","waku_8","umaban","name","sex","boba","hinba","senba","age","age_2","age_3","age_4","age_5","age_6","age_7","age_8","age_9","age_10","age_11","age_12","j_weight","jockey","time","ozzu","h_weight","h_weight_c","trainer","owner","father","j_weight_c","distance_c","jockey_fuku","trainer_fuku","owner_fuku","f_condition","f_distance","kaisai","tousuu","zensoutimesa","money_c","zenagari","zenyes_f","zenno_f","zenyes_c","zenno_c","log_fuku","log_tan","fuku","tan"]

race=pd.DataFrame(columns=columns)


def numStr(num):
    if num>=10:
        return str(num)
    else:
        return '0'+str(num)
Base1="https://db.sp.netkeiba.com/race/"
#2 馬の血統
Base3="https://db.sp.netkeiba.com/horse/result/"
#4 過去のレース
Base5="https://db.sp.netkeiba.com/jockey/result/year/"
Base6="https://db.sp.netkeiba.com/trainer/result/year/"
Base7="https://db.sp.netkeiba.com/owner/result/year/"
Base8a="https://db.sp.netkeiba.com/horse/sire_detail.html?id="
Base8b="&course=1&mode=1&type=1"
Base8c="&course=1&mode=1&type=2"

for year in (range(2020, 2021)):#年
    for i in (range(9,10)):#競馬場1 11
#1ok 2ok 3ok 4ok 5ok 6ok 7ok 8ok 9ok 10ok

#1札幌2函館3福島4新潟5東京6中山7中京8京都9阪神10小倉
        for j in (range(2,3)):#何回開催1 7
            for k in (range(6,7)):#何日開催1 11
                for l in (range(11,12)): #何レース目か1 13
                    url1a=str(year) + numStr(i) + numStr(j) + numStr(k) + numStr(l)
                    url1 = Base1 + url1a+"/"
                    #time.sleep(1)
                    html1=requests.get(url1, verify=False)
                    html1.encoding='EUC-JP'
                    soup1=BeautifulSoup(html1.text,'html.parser')
                    print(url1)
                    
                    
                    if soup1.find_all('a')==[]:
                        break;
                    elif soup1.title.text.split()[0]=="error":
                        break;
                    #elif (soup1.find_all('div',class_='RaceData')[0].text.split())[1].split("(")[0]!="芝1200m":
                    elif(len(soup1.find_all('td',class_='speed_index')))>=8 and soup1.find_all('td')[20].text!="600.0" and soup1.find_all('td')[20].text!="700.0" and ((soup1.find_all('div',class_='RaceData')[0].text.split())[1])[0]=="芝":
#(soup1.find_all('div',class_='RaceData')[0].text.split())[1].split("(")[0]=="芝1200m":                                                                                              
#((soup1.find_all('div',class_='RaceData')[0].text.split())[1])[0]=="芝": 
                        Q=Q+1
                        for b in range(len(soup1.find_all('td',class_='speed_index'))):
                            if (soup1.find_all('div',class_='RaceData')[0].text.split()[1])[0]=="障":
                                sleep=0
                            elif soup1.find_all('td')[21*b+0].text=="取" or soup1.find_all('td')[21*b+0].text=="除" or soup1.find_all('td')[21*b+0].text=="中" or soup1.find_all('td')[21*b+0].text=="失":
                                sleep=0
                            else:
                                k0=float(k)
                                r0=soup1.title.text.split()
                                r1a=r0[3].split("年")
                                r1b=r1a[1].split("月")
                                r1c=r1b[1].split("日")
                                r1=numStr(int(r1a[0]))+numStr(int(r1b[0]))+numStr(int(r1c[0]))#日付2
                                r2=(r0[4])[0]+(r0[4])[1]#競馬場
                                r3=soup1.find_all('div',attrs={'class','RaceData'})[0].text.split()
                                r4=(r3[1])[0]#コース
                                r5a=r3[1].split("(")
                                r5b=r5a[0].strip("芝 ダ m")#距離
                                r5=float(r5b)
                                r6a=soup1.find_all('td')[20].text#１着賞金
                                if len(r6a)==5:
                                    r6=r6a
                                elif len(r6a)==7:
                                    r6=r6a[0]+r6a[2]+r6a[3]+r6a[4]+r6a[5]+r6a[6]
                                elif len(r6a)==8:
                                    r6=r6a[0]+r6a[1]+r6a[3]+r6a[4]+r6a[5]+r6a[6]+r6a[7]
                                else:
                                    r6=r6a[100]



                                r8a=len(soup1.find_all('td',attrs={'class','speed_index'}))
                                r8=float(r8a)
                                h0a=soup1.find_all('td')[21*b+0].text.split("(")#着順
                                h0=float(h0a[0])
                                h1a=soup1.find_all('td')[21*b+1].text#枠番
                                h1=float(h1a)
                                h2a=soup1.find_all('td')[21*b+2].text#馬番
                                h2=float(h2a)
                                h3=soup1.find_all('td')[21*b+3].text#馬名
                                h3_u=soup1.find_all('td')[21*b+3].a.get('href')
                                print(h3)
                                waku_1=0.0
                                waku_2=0.0
                                waku_3=0.0
                                waku_4=0.0
                                waku_5=0.0
                                waku_6=0.0
                                waku_7=0.0
                                waku_8=0.0
                                if h1a=="1":
                                    waku_1=1.0
                                elif h1a=="2":
                                    waku_2=1.0
                                elif h1a=="3":
                                    waku_3=1.0
                                elif h1a=="4":
                                    waku_4=1.0
                                elif h1a=="5":
                                    waku_5=1.0
                                elif h1a=="6":
                                    waku_6=1.0
                                elif h1a=="7":
                                    waku_7=1.0
                                elif h1a=="8":
                                    waku_8=1.0
                                else:
                                    print(pro[111])
                                y=soup1.find_all('div',attrs={'class','Result_Pay_Back'})[0].text.split()
                                for c in range(len(y))[::-1]:#複勝
                                    if y[c]==h2a:
                                        fuku=(y[c+1].replace(",","")).replace("円","")
                                        break
                                    else:
                                        fuku=0.0

                                

                                h4_=soup1.find_all('td')[21*b+4].text
                                h4a=h4_[0]#性別
                                if h4_[1]=="1":
                                    h4bb=h4_[1]+h4_[2]
                                else:
                                    h4bb=h4_[1]
                                
                                age_2=0.0
                                age_3=0.0
                                age_4=0.0
                                age_5=0.0
                                age_6=0.0
                                age_7=0.0
                                age_8=0.0
                                age_9=0.0
                                age_10=0.0
                                age_11=0.0
                                age_12=0.0
                                age_13=0.0
                                if h4bb=="2":
                                    age_2=1.0
                                elif h4bb=="3":
                                    age_3=1.0
                                elif h4bb=="4":
                                    age_4=1.0
                                elif h4bb=="5":
                                    age_5=1.0  
                                elif h4bb=="6":
                                    age_6=1.0
                                elif h4bb=="7":
                                    age_7=1.0
                                elif h4bb=="8":
                                    age_8=1.0
                                elif h4bb=="9":
                                    age_9=1.0
                                elif h4bb=="10":
                                    age_10=1.0
                                elif h4bb=="11":
                                    age_11=1.0
                                elif h4bb=="12":
                                    age_12=1.0
                                elif h4bb=="13":
                                    age_13=1.0
                                else:
                                    print(pro[1])

                                h5a=soup1.find_all('td')[21*b+5].text#斤量
                                h5=float(h5a)
                                h6=soup1.find_all('td')[21*b+6].text#騎手名
                                h6_u=soup1.find_all('td')[21*b+6].a.get('href')
                                h7_=re.split('[:.]',soup1.find_all('td')[21*b+7].text)
                                h7=int(h7_[0])*60+int(h7_[1])+0.1*int(h7_[2])#タイム
                                h8=soup1.find_all('td')[21*b+12].text#単勝オッズ
                                tan=int(float(h8)*100)
                                h9a=soup1.find_all('td')[21*b+14].text
                                h9bb=h9a.split("(")#h9bb[0]=馬体重
                                h9b=float(h9bb[0])
                                h9cc=h9bb[1].strip("+ - )")#馬体重変化
                                h9c=float(h9cc)
                                h10=soup1.find_all('td')[21*b+18].text#調教師
                                h10_u=soup1.find_all('td')[21*b+18].a.get('href')
                                h11=soup1.find_all('td')[21*b+19].text#馬主
                                h11_u=soup1.find_all('td')[21*b+19].a.get('href')


                                url5a=h6_u[-6]+h6_u[-5]+h6_u[-4]+h6_u[-3]+h6_u[-2]
                                url5=Base5+url5a+"/"
                                #time.sleep(1)
                                html5=requests.get(url5, verify=False)
                                html5.encoding='EUC-JP'
                                soup5=BeautifulSoup(html5.text,'html.parser')
                                

                                h21a=soup5.find_all('td')[10].text
                                h21=h21a.strip("％")


                                url6a=h10_u[-6]+h10_u[-5]+h10_u[-4]+h10_u[-3]+h10_u[-2]
                                url6=Base6+url6a+"/"
                                #time.sleep(1)
                                html6=requests.get(url6, verify=False)
                                html6.encoding='EUC-JP'
                                soup6=BeautifulSoup(html6.text,'html.parser')
                                h22a=soup6.find_all('td')[10].text
                                h22=h22a.strip("％")

                                
                                
                                if h11=="高浪宣昭":
                                    h23=NA
                                else:
                                    url7a=h11_u[-7]+h11_u[-6]+h11_u[-5]+h11_u[-4]+h11_u[-3]+h11_u[-2]
                                    url7=Base7+url7a+"/"
                                    #time.sleep(1)
                                    html7=requests.get(url7, verify=False)
                                    html7.encoding='EUC-JP'
                                    soup7=BeautifulSoup(html7.text,'html.parser')
                                    h23a=soup7.find_all('td')[10].text
                                    h23=h23a.strip("％")
                                
                                h4a_a=0.0;
                                h4a_b=0.0;
                                h4a_c=0.0;
                                if h4a=="牡":
                                    h4a_a=1.0;
                                elif h4a[0]=="牝":
                                    h4a_b=1.0;
                                elif h4a[0]=="セ":
                                    h4a_c=1.0;

                                else:
                                    print(data111)

                                r3_a=0.0
                                r3_b=0.0
                                r3_c=0.0
                                r3_d=0.0
                                if r3[-1]=="良":
                                    r3_a=1.0
                                elif r3[-1]=="稍":
                                    r3_b=1.0
                                elif r3[-1]=="重":
                                    r3_c=1.0
                                elif r3[-1]=="不":
                                    r3_d=1.0
                                else:
                                    print(data88[111]);

                                if r4=="芝":
                                    r4_a=1.0
                                    r4_b=0.0
                                elif r4=="ダ":
                                    r4_a=0.0
                                    r4_b=1.0
                                else:
                                    print(data88[111]);

                                r7_a=0.0
                                r7_b=0.0
                                r7_c=0.0
                                r7_d=0.0
                                r7_e=0.0
                                r7_f=0.0
                                if r3[-2]=="晴":
                                    r7_a=1.0
                                elif r3[-2]=="曇":
                                    r7_b=1.0
                                elif r3[-2]=="小雨":
                                    r7_c=1.0
                                elif r3[-2]=="雨":
                                    r7_d=1.0
                                elif r3[-2]=="小雪":
                                    r7_e=1.0
                                elif r3[-2]=="雪":
                                    r7_f=1.0
                                else:
                                    print(data88[111]);

                                #time.sleep(1)
                                html2=requests.get(h3_u, verify=False)
                                html2.encoding='EUC-JP'
                                soup2=BeautifulSoup(html2.text,'html.parser')


                                h12=soup2.find_all('td',attrs={'class','Sire'})[0].text.split()[0]#父

                                

                                h12a=soup2.find_all('td',attrs={'class','Sire'})[0].a.get('href')
                                url8a=h12a[-11]+h12a[-10]+h12a[-9]+h12a[-8]+h12a[-7]+h12a[-6]+h12a[-5]+h12a[-4]+h12a[-3]+h12a[-2]
                                url8=Base8a+url8a+Base8b
                                #time.sleep(1)
                                html8=requests.get(url8, verify=False)
                                html8.encoding='EUC-JP'
                                soup8=BeautifulSoup(html8.text,'html.parser')


                                
                                if r4!="芝":
                                    f_condition=1.0
                                elif h12=="War" or h12=="Running" or h12=="DAYLAMI" or h12=="Daylami":
                                    f_condition=NA
                                else:
                                    if r3[-1]=="良":#父の馬場状態の成績
                                        f_condition=(float(soup8.find_all('td')[0].text.replace(',', ''))+float(soup8.find_all('td')[1].text.replace(',', ''))+float(soup8.find_all('td')[2].text.replace(',', '')))/(float(soup8.find_all('td')[0].text.replace(',', ''))+float(soup8.find_all('td')[1].text.replace(',', ''))+float(soup8.find_all('td')[2].text.replace(',', ''))+float(soup8.find_all('td')[3].text.replace(',', '')))*100
                                    elif r3[-1]=="稍":
                                        f_condition=(float(soup8.find_all('td')[4].text.replace(',', ''))+float(soup8.find_all('td')[5].text.replace(',', ''))+float(soup8.find_all('td')[6].text.replace(',', '')))/(float(soup8.find_all('td')[4].text.replace(',', ''))+float(soup8.find_all('td')[5].text.replace(',', ''))+float(soup8.find_all('td')[6].text.replace(',', ''))+float(soup8.find_all('td')[7].text.replace(',', '')))*100
                                    elif r3[-1]=="重":
                                        f_condition=(float(soup8.find_all('td')[8].text.replace(',', ''))+float(soup8.find_all('td')[9].text.replace(',', ''))+float(soup8.find_all('td')[10].text.replace(',', '')))/(float(soup8.find_all('td')[8].text.replace(',', ''))+float(soup8.find_all('td')[9].text.replace(',', ''))+float(soup8.find_all('td')[10].text.replace(',', ''))+float(soup8.find_all('td')[11].text.replace(',', '')))*100
                                    elif r3[-1]=="不":
                                        f_condition=(float(soup8.find_all('td')[12].text.replace(',', ''))+float(soup8.find_all('td')[13].text.replace(',', ''))+float(soup8.find_all('td')[14].text.replace(',', '')))/(float(soup8.find_all('td')[12].text.replace(',', ''))+float(soup8.find_all('td')[13].text.replace(',', ''))+float(soup8.find_all('td')[14].text.replace(',', ''))+float(soup8.find_all('td')[15].text.replace(',', '')))*100
                                    else:
                                        print(pro[11])
                                        
                                        

                                url8_1=Base8a+url8a+Base8c
                                #time.sleep(1)
                                html8_1=requests.get(url8_1, verify=False)
                                html8_1.encoding='EUC-JP'
                                soup8_1=BeautifulSoup(html8_1.text,'html.parser')

                                if r4!="芝":
                                    f_distance=1.0
                                elif h12=="War" or h12=="Running" or h12=="DAYLAMI" or h12=="Daylami":
                                    f_distance=NA
                                else:
                                    if r5<=1400:#父の距離別の成績
                                        f_distance=(float(soup8_1.find_all('td')[0].text.replace(',', ''))+float(soup8_1.find_all('td')[1].text.replace(',', ''))+float(soup8_1.find_all('td')[2].text.replace(',', '')))/(float(soup8_1.find_all('td')[0].text.replace(',', ''))+float(soup8_1.find_all('td')[1].text.replace(',', ''))+float(soup8_1.find_all('td')[2].text.replace(',', ''))+float(soup8_1.find_all('td')[3].text.replace(',', ''))+1)*100
                                    elif r5<=1800:
                                        f_distance=(float(soup8_1.find_all('td')[4].text.replace(',', ''))+float(soup8_1.find_all('td')[5].text.replace(',', ''))+float(soup8_1.find_all('td')[6].text.replace(',', '')))/(float(soup8_1.find_all('td')[4].text.replace(',', ''))+float(soup8_1.find_all('td')[5].text.replace(',', ''))+float(soup8_1.find_all('td')[6].text.replace(',', ''))+float(soup8_1.find_all('td')[7].text.replace(',', ''))+1)*100
                                    elif r5<=2200:
                                        f_distance=(float(soup8_1.find_all('td')[8].text.replace(',', ''))+float(soup8_1.find_all('td')[9].text.replace(',', ''))+float(soup8_1.find_all('td')[10].text.replace(',', '')))/(float(soup8_1.find_all('td')[8].text.replace(',', ''))+float(soup8_1.find_all('td')[9].text.replace(',', ''))+float(soup8_1.find_all('td')[10].text.replace(',', ''))+float(soup8_1.find_all('td')[11].text.replace(',', ''))+1)*100
                                    elif r5<=2600:
                                        f_distance=(float(soup8_1.find_all('td')[12].text.replace(',', ''))+float(soup8_1.find_all('td')[13].text.replace(',', ''))+float(soup8_1.find_all('td')[14].text.replace(',', '')))/(float(soup8_1.find_all('td')[12].text.replace(',', ''))+float(soup8_1.find_all('td')[13].text.replace(',', ''))+float(soup8_1.find_all('td')[14].text.replace(',', ''))+float(soup8_1.find_all('td')[15].text.replace(',', ''))+1)*100
                                    elif r5>=2600:
                                        f_distance=(float(soup8_1.find_all('td')[16].text.replace(',', ''))+float(soup8_1.find_all('td')[17].text.replace(',', ''))+float(soup8_1.find_all('td')[18].text.replace(',', '')))/(float(soup8_1.find_all('td')[16].text.replace(',', ''))+float(soup8_1.find_all('td')[17].text.replace(',', ''))+float(soup8_1.find_all('td')[18].text.replace(',', ''))+float(soup8_1.find_all('td')[19].text.replace(',', ''))+1)*100
                                    else:
                                        print(pro[111])

                                if f_condition==0:
                                    f_condition=NA
                                else:
                                    sleep=0
                                if f_distance==0:
                                    f_distance=NA
                                else:
                                    sleep=0
                                

                            

                                url3a=h3_u[-11]+h3_u[-10]+h3_u[-9]+h3_u[-8]+h3_u[-7]+h3_u[-6]+h3_u[-5]+h3_u[-4]+h3_u[-3]+h3_u[-2]

                                url3=Base3+url3a+"/"
                                #time.sleep(1)
                                html3=requests.get(url3, verify=False)
                                html3.encoding='EUC-JP'
                                soup3=BeautifulSoup(html3.text,'html.parser')


                                #pp 何回走ったか
                                for p in range(len(soup3.find_all('span',attrs={'class','Set_RaceName'}))):
                                    h15a=soup3.find_all('div',attrs={'class','List_TextBox'})[p].text.split()
                                    h15b=h15a[3].split("(")
                                    pp+=1

                                for q in range(pp):#前走との差
                                    h16a=soup3.find_all('div',attrs={'class','List_TextBox'})[q].text.split()
                                    h16b=h16a[0].split("/")

                                    h16=numStr(int(h16b[0]))+numStr(int(h16b[1]))+numStr(int(h16b[2]))#過去レースの日付
                                    if int(h16)-int(r1)<0:
                                        h17a=(soup3.find_all('div',attrs={'class','LinkBox_01'})[q].a).get('href')
                                        h17b=h17a.strip("/")
                                        url4a=h17b[-12]+h17b[-11]+h17b[-10]+h17b[-9]+h17b[-8]+h17b[-7]+h17b[-6]+h17b[-5]+h17b[-4]+h17b[-3]+h17b[-2]+h17b[-1]
                                        url4=Base1+url4a+"/"
                                 #       time.sleep(1)
                                        html4=requests.get(url4, verify=False)
                                        html4.encoding='EUC-JP'
                                        soup4=BeautifulSoup(html4.text,'html.parser')
                                        h18a=soup3.find_all('div',attrs={'class','List_TextBox'})[q].text.split()
                                        h18=h18a[3].split("(")#過去着順

                                        if h18[0]=="除" or h18[0]=="中" or h18[0]=="取" or h18[0]=="失":
                                            sleep=0

                                        elif h17b[-8]=="0" or h17b[-8]=="1":
                                            h19a=soup4.find_all('td')[21*(int(h18[0])-1)+5].text
                                            h19=float(h5)-float(h19a)#斤量変化
                                            h20a=soup4.find_all('div',attrs={'class','RaceData'})[0].text.split()
                                            h20b=h20a[1].split("(")
                                            h20c=h20b[0].strip("障 芝 ダ m")
                                            h20=float(r5)-float(h20c)#距離変化
                                            h24a=re.split('[:.]',soup4.find_all('td')[7].text)
                                            h24b=int(h24a[0])*60+int(h24a[1])+0.1*int(h24a[2])
                                            h24c=re.split('[:.]',soup4.find_all('td')[21*(int(h18[0])-1)+7].text)
                                            h24d=int(h24c[0])*60+int(h24c[1])+0.1*int(h24c[2])
                                            h24=h24b-h24d

                                            h25a=soup4.find_all('td')[20].text
                                            if len(h25a)==5:
                                                h25b=h25a
                                            elif len(h25a)==7:
                                                h25b=h25a[0]+h25a[2]+h25a[3]+h25a[4]+h25a[5]+h25a[6]
                                            elif len(h25a)==8:
                                                h25b=h25a[0]+h25a[1]+h25a[3]+h25a[4]+h25a[5]+h25a[6]+h25a[7]
                                            else:
                                                h25b=h25a[100]
                                            h25=float(r6)-float(h25b)
                                            h27=soup4.find_all('td')[21*(int(h18[0])-1)+11].text
                                            if len(h27)==0:
                                                h27=NA
                                            else:
                                                sleep=0

                                            h28a=soup4.title.text.split()
                                            h28b=(h28a[4])[0]+(h28a[4])[1]
                                            if h28b==r2:
                                                h28_a=1.0
                                                h28_b=0.0
                                            else:
                                                h28_a=0.0
                                                h28_b=1.0
                                            h29a=soup4.find_all('div',attrs={'class','RaceData'})[0].text.split()
                                            h29b=(h29a[1])[0]#コース
                                            if h29b==r4:
                                                h29_a=1.0
                                                h29_b=0.0
                                            else:
                                                h29_a=0.0
                                                h29_b=1.0
                                            break;



                                        else:
                                            h19=NA
                                            h20=NA
                                            h24=NA
                                            h25=NA
                                            h27=NA
                                            h28_a=NA
                                            h28_b=NA
                                            h29_a=NA
                                            h29_b=NA
                                    else:
                                        h19=NA
                                        h20=NA
                                        h24=NA
                                        h25=NA
                                        h27=NA
                                        h28_a=NA
                                        h28_b=NA
                                        h29_a=NA
                                        h29_b=NA
                                pp=0
         
                            se=pd.Series(index=columns)#Closes else:

                            if h0<=3:
                                h30=1
                            else:
                                h30=0
                            
                            if h0==1:
                                h31=1
                            else:
                                h31=0
                            
                            se["num"]=float(Q)
                            se["racename"]=r0[0]
                            se["date"]=r1
                            se["where"]=r2
                            se["weather"]=r3[-2]
                            se["hare"]=r7_a
                            se["kumori"]=r7_b
                            se["kosame"]=r7_c
                            se["ame"]=r7_d
                            se["koyuki"]=r7_e
                            se["yuki"]=r7_f
                            se["condition"]=r3[-1]
                            se["ryou"]=float(r3_a)
                            se["yayaomo"]=float(r3_b)
                            se["omo"]=float(r3_c)
                            se["furyou"]=float(r3_d)
                            se["course"]=r4
                            se["shiba"]=float(r4_a)
                            se["suna"]=float(r4_b)
                            se["distance"]=float(r5)
                            se["money_r"]=float(r6)
                            se["tousuu"]=float(r8)
                            se["tyaku"]=float(h0)
                            se["waku"]=float(h1)
                            se["waku_1"]=float(waku_1)
                            se["waku_2"]=float(waku_2)
                            se["waku_3"]=float(waku_3)
                            se["waku_4"]=float(waku_4)
                            se["waku_5"]=float(waku_5)
                            se["waku_6"]=float(waku_6)
                            se["waku_7"]=float(waku_7)
                            se["waku_8"]=float(waku_8)
                            se["umaban"]=float(h2)
                            se["name"]=h3
                            se["sex"]=h4a
                            se["boba"]=float(h4a_a)
                            se["hinba"]=float(h4a_b)
                            se["senba"]=float(h4a_c)
                            se["age"]=float(h4bb)
                            se["age_2"]=float(age_2)
                            se["age_3"]=float(age_3)
                            se["age_4"]=float(age_4)
                            se["age_5"]=float(age_5)
                            se["age_6"]=float(age_6)
                            se["age_7"]=float(age_7)
                            se["age_8"]=float(age_8)
                            se["age_9"]=float(age_9)
                            se["age_10"]=float(age_10)
                            se["age_11"]=float(age_11)
                            se["age_12"]=float(age_12)
                            se["j_weight"]=float(h5)
                            se["jockey"]=h6
                            se["time"]=float(h7)
                            se["ozzu"]=float(h8)
                            se["h_weight"]=float(h9b)
                            se["h_weight_c"]=float(h9c)
                            se["trainer"]=h10
                            se["owner"]=h11
                            se["father"]=h12
                            se["j_weight_c"]=float(h19)
                            se["distance_c"]=float(h20)
                            se["jockey_fuku"]=float(h21)
                            se["trainer_fuku"]=float(h22)
                            se["owner_fuku"]=float(h23)
                            se["f_condition"]=float(f_condition)
                            se["f_distance"]=float(f_distance)
                            se["zensoutimesa"]=float(h24)
                            se["kaisai"]=float(k0)
                            se["money_c"]=float(h25)
                            se["zenagari"]=float(h27)
                            se["zenyes_f"]=float(h28_a)
                            se["zenno_f"]=float(h28_b)
                            se["zenyes_c"]=float(h29_a)
                            se["zenno_c"]=float(h29_b)
                            se["log_fuku"]=h30
                            se["log_tan"]=h31
                            se["fuku"]=float(fuku)
                            se["tan"]=float(tan)
                            race=race.append(se,ignore_index=True)
                        
                        print(race)
                    
                    
                        

race=race.dropna()
race.drop_duplicates()
race.to_csv("ouka.csv",index=False,encoding="shift-jis")


