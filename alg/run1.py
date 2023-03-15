#请求的密钥量增加

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
run_round=50  #运行次数
a=0.28
b=3
nodenum=50 #节点数量

#请求响应率 随着请求的密钥量增加

reqkeyvol=np.arange(150,250,10)
#数据统计
#请求满足
sraqa=[0]*len(reqkeyvol)
srkod=[0]*len(reqkeyvol)
sr2=[0]*len(reqkeyvol)
#吞吐量
thaqa=[0]*len(reqkeyvol)
thkod=[0]*len(reqkeyvol)
th2=[0]*len(reqkeyvol)
cthaqa=[0]*len(reqkeyvol)
cthkod=[0]*len(reqkeyvol)
cth2=[0]*len(reqkeyvol)
#请求完成时间
timeaqa=[0]*len(reqkeyvol)
timekod=[0]*len(reqkeyvol)
time2=[0]*len(reqkeyvol)
ctimeaqa=[0]*len(reqkeyvol)
ctimekod=[0]*len(reqkeyvol)
ctime2=[0]*len(reqkeyvol)
#密钥消耗量
keyconaqa=[0]*len(reqkeyvol)
keyconkod=[0]*len(reqkeyvol)
keycon2=[0]*len(reqkeyvol)
ckeyconaqa=[0]*len(reqkeyvol)
ckeyconkod=[0]*len(reqkeyvol)
ckeycon2=[0]*len(reqkeyvol)
#创建excel表

#filename='1.xlsx'
filename='keyvol'+str(run_round)+'a-'+str(a)+"b-"+str(b)+"nodenum-"+str(nodenum)+'.xlsx'
wb = Workbook()
ws = wb.active



head=["reqkeyvol","SRaqa","SRkod","SR2","finishtimeaqa","finishtimekod","finishtime2","keyconaqa","keyconkod","keycon2","thaqa","thkod","th2"]
ws.append(head)


start_time=time.time()
for count in range(run_round):
    print("running:",count,"round")
    if count!=0:
        print("预计剩余时间为：",(time.time()-start_time)*(run_round-count)/count/60,"min")
    random_topo=Topo().create_random_topology(nodenum,a,b) #随机拓扑生成：点边集合
    NodeEdgeSet=Topo().CreatNodeEdgeSet(random_topo)
    topo=Topo().CreatTopo(NodeEdgeSet)
    Topo().Changelrate(topo,20,50)  #链路生成速率
    Topo().Changelc(topo,100,200)     #链路密钥池容量
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

    for j in range(len(reqkeyvol)):
        #更改请求的密钥速率
        
        req=[source,des,reqkeyvol[j],NULL]
        

        #算法运行
        print("请求：",req,"kb/s")
        path1=Alg1().ada(copy.deepcopy(topo),req)
        print(path1)
        
        if path1 is not NULL:
            p1=[]
            for index in range(len(path1)-1):
                p1.append([topo[path1[index]][path1[index+1]].c,topo[path1[index]][path1[index+1]].rate])
            print(p1)
            sraqa[j]+=1
            if Cost().timecost(topo,path1,req)!=-1:
                print("time:",Cost().timecost(topo,path1,req))
                ctimeaqa[j]+=1
                timeaqa[j]+=Cost().timecost(topo,path1,req)
                thaqa[j]+=req[2]
                
            
            if Cost().keycon(topo,path1,req)>0:
                ckeyconaqa[j]+=1
                keyconaqa[j]+=Cost().keycon(topo,path1,req)

        path0=Alg1().spf(copy.deepcopy(topo),req)
        print(path0)
        if path0 is not NULL:
            srkod[j]+=1
            if Cost().timecost(topo,path0,req)!=-1:
                print("time:",Cost().timecost(topo,path0,req))
                ctimekod[j]+=1
                timekod[j]+=Cost().timecost(topo,path0,req)
                thkod[j]+=req[2]
            
            if Cost().keycon(topo,path0,req)>0:
                ckeyconkod[j]+=1
                keyconkod[j]+=Cost().keycon(topo,path0,req)

        path2=Alg2().alg2(copy.deepcopy(topo),req)
        print(path2)
        if path2 is not NULL:
            p2=[]
            for index in range(len(path2)-1):
                p2.append([topo[path2[index]][path2[index+1]].c,topo[path2[index]][path2[index+1]].rate])
            print(p2)
            sr2[j]+=1
            if Cost().timecost(topo,path2,req)!=-1:
                print("time:",Cost().timecost(topo,path2,req))
                ctime2[j]+=1
                time2[j]+=Cost().timecost(topo,path2,req)
                th2[j]+=req[2]
            
             
            if Cost().keycon(topo,path2,req)>0:
                ckeycon2[j]+=1
                keycon2[j]+=Cost().keycon(topo,path2,req)

for i in range(len(reqkeyvol)):
    sraqa[i]/=run_round
    srkod[i]/=run_round
    sr2[i]/=run_round
    
    if timeaqa[i]>0:
        thaqa[i]/=timeaqa[i]
    if timekod[i]>0:
        thkod[i]/=timekod[i]
    if time2[i]>0:
        th2[i]/=time2[i]
    timeaqa[i]/=run_round
    timekod[i]/=run_round
    time2[i]/=run_round
    
    
    

    if ckeyconaqa[i]>0:
        keyconaqa[i]/=ckeyconaqa[i]
    if ckeyconkod[i]>0:
        keyconkod[i]/=ckeyconkod[i]
    if ckeycon2[i]>0:
        keycon2[i]/=ckeycon2[i]

    ws.append([reqkeyvol[i],sraqa[i],srkod[i],sr2[i],timeaqa[i],timekod[i],time2[i],keyconaqa[i],keyconkod[i],keycon2[i],thaqa[i],thkod[i],th2[i]])

wb.save(filename)
fig = plt.figure()
plt.plot(reqkeyvol,sraqa,color='red')
plt.plot(reqkeyvol,srkod,color='green')
plt.plot(reqkeyvol,sr2,color='blue')
plt.title("req sastify rate")
plt.xlabel('reqkeyrate')
plt.ylabel('sastify rate')
plt.show()
#资源利用率
fig = plt.figure()
plt.plot(reqkeyvol,timeaqa,color='red')
plt.plot(reqkeyvol,timekod,color='green')
plt.plot(reqkeyvol,time2,color='blue')
plt.title("req finish time")
plt.xlabel('reqkeyrate')
plt.ylabel('finish time')
plt.show()