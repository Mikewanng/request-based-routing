#请求的密钥速率需求增加

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
run_round=100  #运行次数
a=0.5
b=0.5
nodenum=50  #节点数量

#请求响应率 随着请求的密钥速率增加

reqkeyrate=np.arange(50,500,50)
#数据统计
sr1=[0]*len(reqkeyrate)
sr2=[0]*len(reqkeyrate)
#创建excel表


filename='keyrate'+str(run_round)+'a='+str(a)+"b="+str(b)+"nodenum="+str(nodenum)+'time'+str(time.time())+'.xlsx'
#wb = Workbook()
#ws = wb.active



fp = open(filename, 'w')
fp.write('NodeSp    aveMaxSp_random    aveMaxSp_sgr    资源利用率_random    资源利用率_sgr    重构0.9后密钥量_random    重构0.9后密钥量_sgr    重构0.7后密钥量_random    重构0.7后密钥量_sgr    重构0.9后密钥量_random    重构0.9后密钥量_sgr    重构0.5后密钥量_random    重构0.5后密钥量_sgr\n')




start_time=time.time()
for count in range(run_round):
    print("running:",count,"round")
    if count!=0:
        print("预计剩余时间为：",(time.time()-start_time)*(run_round-count)/count/60,"min")
    random_topo=Topo().create_random_topology(nodenum,a,b) #随机拓扑生成：点边集合
    NodeEdgeSet=Topo().CreatNodeEdgeSet(random_topo)
    topo=Topo().CreatTopo(NodeEdgeSet)
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

    for j in range(len(reqkeyrate)):
        #更改请求的密钥速率
        req=[source,des,600 ,reqkeyrate[j]]
        

        #算法运行
        print("请求：",req,"kb/s")
        path1=Alg1().alg1(copy.deepcopy(topo),req)
        print(path1)
        if path1 is not NULL:
            sr1[j]+=1


        path2=Alg2().alg2(copy.deepcopy(topo),req)
        print(path2)
        if path2 is not NULL:
            sr2[j]+=1

for i in range(len(reqkeyrate)):
    sr1[i]/=run_round
    sr2[i]/=run_round

fig = plt.figure()
plt.plot(reqkeyrate,sr1,color='red')
plt.plot(reqkeyrate,sr2,color='green')
plt.title("req sastify rate")
plt.xlabel('reqkeyrate')
plt.ylabel('sastify rate')
plt.show()
#资源利用率
