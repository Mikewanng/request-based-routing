#请求的密钥量需求增加

from ctypes.wintypes import INT
from Topo import *
from Net import *
from Alg1 import *
from Alg2 import *
import copy,random,time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from openpyxl import Workbook
import numpy as np

#参数初始化
run_round=1000  #运行次数
a=0.5
b=0.5
nodenum=50 #节点数量
reqkeyrate=100



reqkeynum=np.arange(50,500,50)
#数据统计
#请求满足
sraqa=[0]*len(reqkeynum)
srkod=[0]*len(reqkeynum)
sr2=[0]*len(reqkeynum)
#吞吐量
thaqa=[0]*len(reqkeynum)
thkod=[0]*len(reqkeynum)
th2=[0]*len(reqkeynum)
cthaqa=[0]*len(reqkeynum)
cthkod=[0]*len(reqkeynum)
cth2=[0]*len(reqkeynum)
#请求完成时间
timeaqa=[0]*len(reqkeynum)
timekod=[0]*len(reqkeynum)
time2=[0]*len(reqkeynum)
ctimeaqa=[0]*len(reqkeynum)
ctimekod=[0]*len(reqkeynum)
ctime2=[0]*len(reqkeynum)
#密钥消耗量
keyconaqa=[0]*len(reqkeynum)
keyconkod=[0]*len(reqkeynum)
keycon2=[0]*len(reqkeynum)
ckeyconaqa=[0]*len(reqkeynum)
ckeyconkod=[0]*len(reqkeynum)
ckeycon2=[0]*len(reqkeynum)
#创建excel表

#filename='1.xlsx'
filename='keynum'+str(run_round)+'a-'+str(a)+"b-"+str(b)+"nodenum-"+str(nodenum)+'.xlsx'
wb = Workbook()
ws = wb.active



head=["reqkeynum","SRaqa","SRkod","SR2","finishtimeaqa","finishtimekod","finishtime2","keyconaqa","keyconkod","keycon2","thaqa","thkod","th2"]
ws.append(head)


start_time=time.time()
for count in range(run_round):
    print("running:",count,"round")
    if count!=0:
        print("预计剩余时间为：",(time.time()-start_time)*(run_round-count)/count/60,"min")
    random_topo=Topo().create_random_topology(nodenum,a,b) #随机拓扑生成：点边集合
    NodeEdgeSet=Topo().CreatNodeEdgeSet(random_topo)
    topo=Topo().CreatTopo(NodeEdgeSet)
    Topo().Changelrate(topo,50,150)
    Topo().Changelc(topo,50,1000)
    source=random.randint(0,len(topo[0])-1)
    des=random.randint(0,len(topo[0])-1)
    #随机生成请求
    """
    flag=random.randint(1,3)
    if flag==1:
        req=[source,des,NULL ,random.randint(50,200)]
    elif flag==2:
        req=[source,des,random.randint(50,200),NULL]
    else:
        req=[source,des,random.randint(50,200),random.randint(50,200)]
    """
    while des==source:
        des=random.randint(0,len(topo[0])-1)

    for j in range(len(reqkeynum)):
        #更改请求的密钥速率
        flag=random.randint(1,3)
        if flag==1:
            req=[source,des,NULL ,reqkeyrate]
        elif flag==2:
            req=[source,des,reqkeynum[j],NULL]
        else:
            req=[source,des,reqkeynum[j],reqkeyrate]
        #req=[source,des,600,reqkeyrate[j]]
        

        #算法运行
        print("请求：",req,"kb/s")
        path1=Alg1().ada(copy.deepcopy(topo),req)
        print(path1)
        if path1 is not NULL:
            sraqa[j]+=1
            if Cost().timecost(topo,path1,req)!=-1:
                ctimeaqa[j]+=1
                timeaqa[j]+=Cost().timecost(topo,path1,req)
            if Cost().th(topo,path1,req)>0:
                cthaqa[j]+=1
                thaqa[j]+=Cost().th(topo,path1,req)
            if Cost().keycon(topo,path1,req)>0:
                ckeyconaqa[j]+=1
                keyconaqa[j]+=Cost().keycon(topo,path1,req)

        path0=Alg1().kod(copy.deepcopy(topo),req)
        print(path0)
        if path0 is not NULL:
            srkod[j]+=1
            if Cost().timecost(topo,path0,req)!=-1:
                ctimekod[j]+=1
                timekod[j]+=Cost().timecost(topo,path0,req)
            if Cost().th(topo,path0,req)>0:
                cthkod[j]+=1
                thkod[j]+=Cost().th(topo,path0,req)
            if Cost().keycon(topo,path0,req)>0:
                ckeyconkod[j]+=1
                keyconkod[j]+=Cost().keycon(topo,path0,req)

        path2=Alg2().alg2(copy.deepcopy(topo),req)
        print(path2)
        if path2 is not NULL:
            sr2[j]+=1
            if Cost().timecost(topo,path2,req)!=-1:
                ctime2[j]+=1
                time2[j]+=Cost().timecost(topo,path2,req)
            if Cost().th(topo,path2,req)>0:
                cth2[j]+=1
                th2[j]+=Cost().th(topo,path2,req)
            if Cost().keycon(topo,path2,req)>0:
                ckeycon2[j]+=1
                keycon2[j]+=Cost().keycon(topo,path2,req)

for i in range(len(reqkeynum)):
    sraqa[i]/=run_round
    srkod[i]/=run_round
    sr2[i]/=run_round

    if ctimeaqa[i]>0:
        timeaqa[i]/=ctimeaqa[i]
    if ctimekod[i]>0:
        timekod[i]/=ctimekod[i]
    if ctime2[i]>0:
        time2[i]/=ctime2[i]
    
    if cthaqa[i]>0:
        thaqa[i]/=cthaqa[i]
    if cthkod[i]>0:
        thkod[i]/=cthkod[i]
    if cth2[i]>0:
        th2[i]/=cth2[i]

    if ckeyconaqa[i]>0:
        keyconaqa[i]/=ckeyconaqa[i]
    if ckeyconkod[i]>0:
        keyconkod[i]/=ckeyconkod[i]
    if ckeycon2[i]>0:
        keycon2[i]/=ckeycon2[i]

    ws.append([reqkeynum[i],sraqa[i],srkod[i],sr2[i],timeaqa[i],timekod[i],time2[i],keyconaqa[i],keyconkod[i],keycon2[i],thaqa[i],thkod[i],th2[i]])

wb.save(filename)
fig = plt.figure()
plt.plot(reqkeynum,sraqa,color='red')
plt.plot(reqkeynum,srkod,color='green')
plt.plot(reqkeynum,sr2,color='blue')
plt.title("req sastify rate")
plt.xlabel('reqkeynum')
plt.ylabel('sastify rate')
plt.show()
#资源利用率
fig = plt.figure()
plt.plot(reqkeynum,timeaqa,color='red')
plt.plot(reqkeynum,timekod,color='green')
plt.plot(reqkeynum,time2,color='blue')
plt.title("req finish time")
plt.xlabel('reqkeynum')
plt.ylabel('finish time')
plt.show()