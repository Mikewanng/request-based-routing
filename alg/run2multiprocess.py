#随机可信中继，随机拓扑，随机请求  可信中继数量

from Topo import *
from Net import *
from Alg1 import *
from RandomRouting import *
from Alg2 import *
from Securitylevel import *
from consume import *
import copy,random,time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import threading
from multiprocessing import Process


def run(self,a=0.3,b=3,nodenum=50):
    run_time=10  #运行次数


    filename='MaxSp_vs_TrNode'+str(run_time)+'time='+str(time.time())+'a='+str(a)+"b="+str(b)+"nodenum="+str(nodenum)+'.txt'
    fp = open(filename, 'w')
    fp.write('Trnode    aveMaxSp_random    aveMaxSp_sgr    资源利用率_random    资源利用率_sgr    重构0.9后密钥量_random    重构0.9后密钥量_sgr    重构0.7后密钥量_random    重构0.7后密钥量_sgr    重构0.9后密钥量_random    重构0.9后密钥量_sgr    重构0.5后密钥量_random    重构0.5后密钥量_sgr\n')
    trnode=np.arange(1,10,1)

    #最大安全性
    avemaxsp_random=[0]*len(trnode)
    avemaxsp_sgr=[0]*len(trnode)
    #资源利用率
    resource_consume_random=[0]*len(trnode)
    resource_consume_sgr=[0]*len(trnode)
    #重构后密钥量0.9
    keynum_9_random=[0]*len(trnode)
    keynum_9_sgr=[0]*len(trnode)

    keynum_7_random=[0]*len(trnode)
    keynum_7_sgr=[0]*len(trnode)

    keynum_5_random=[0]*len(trnode)
    keynum_5_sgr=[0]*len(trnode)

    #记录分段的次数
    segnum=[0]*len(trnode)
    start_time=time.time()
    for count in range(run_time):
        print("running process:",count*100/run_time,"%")
        if count!=0:
            print("预计剩余时间为：",(time.time()-start_time)*(run_time-count)/count/60,"min")

        random_topo=Topo().create_random_topology(nodenum,a,b) #随机拓扑生成：点边集合
        source=random.randint(0,len(random_topo[0])-1)
        des=random.randint(0,len(random_topo[0])-1)
        while des==source:
            des=random.randint(0,len(random_topo[0])-1)
    

        for j in range(len(trnode)):
            #更改可信节点数量
            NodeEdgeSet=Topo().CreatNodeEdgeSet(random_topo,10,trnode[j],0.9)
            topo=Topo().CreatTopo(NodeEdgeSet)
        

            #算法运行
            print("可信节点数量：",trnode[j])
            tr=Rr().rrmaxs(copy.deepcopy(topo),source,des)
            print(tr)
            avemaxsp_random[j]+=tr[0][2]
            resource_consume_random[j]+=Con().CalCon(tr)*2/len(random_topo[1])
            keynum_9_random[j]+=Seclev().sl(tr,0.9)
            keynum_7_random[j]+=Seclev().sl(tr,0.7)
            keynum_5_random[j]+=Seclev().sl(tr,0.5)
        
            t2=Alg2().alg2max(copy.deepcopy(topo),source,des)
            if len(t2)>1:
                segnum[j]+=1
            print(t2)
            totalsp=1
            for i in t2:
                totalsp*=i[2]
            avemaxsp_sgr[j]+=totalsp
            resource_consume_sgr[j]+=Con().CalCon(t2)*2/len(random_topo[1])
            keynum_9_sgr[j]+=Seclev().sl(t2,0.9)
            keynum_7_sgr[j]+=Seclev().sl(t2,0.7)
            keynum_5_sgr[j]+=Seclev().sl(t2,0.5)

    for j in range(len(trnode)):
        avemaxsp_random[j]/=run_time
        avemaxsp_sgr[j]/=run_time
   
        resource_consume_random[j]/=run_time
        resource_consume_sgr[j]/=run_time
   
        keynum_9_random[j]/=run_time
        keynum_9_sgr[j]/=run_time

        keynum_7_random[j]/=run_time
        keynum_7_sgr[j]/=run_time

        keynum_5_random[j]/=run_time
        keynum_5_sgr[j]/=run_time


    for j in range(len(trnode)):
        fp.write(str(trnode[j])+'    '+str(avemaxsp_random[j])+'    '+str(avemaxsp_sgr[j])+'    '+str(resource_consume_random[j])+'    '+str(resource_consume_sgr[j])+'    '+str(keynum_9_random[j])+'    '+str(keynum_9_sgr[j])+'    '+str(keynum_7_random[j])+'    '+str(keynum_7_sgr[j])+'    '+str(keynum_5_random[j])+'    '+str(keynum_5_sgr[j])+'\n')

    for j in segnum:
        fp.write(str(j)+"    ")
    fp.close()
    #最大安全概率
    fig = plt.figure()
    plt.plot(trnode,avemaxsp_random,color='red')
    plt.plot(trnode,avemaxsp_sgr,color='green')
    plt.title("Max Security probability")
    plt.xlabel('nodesp')
    plt.ylabel('max Security probability')
    plt.show()
    #资源利用率
    fig = plt.figure()
    plt.plot(trnode,resource_consume_random,color='red')
    plt.plot(trnode,resource_consume_sgr,color='green')
    plt.title("Resource utilization")
    plt.xlabel('nodesp')
    plt.ylabel('Resource utilization')
    plt.show()
    #不同安全概率阈值下的密钥分发速率
    fig = plt.figure()
    plt.plot(trnode,keynum_9_random,color='red')
    plt.plot(trnode,keynum_9_sgr,color='green')
    plt.plot(trnode,keynum_7_random,color='red')
    plt.plot(trnode,keynum_7_sgr,color='green')
    plt.plot(trnode,keynum_5_random,color='red')
    plt.plot(trnode,keynum_5_sgr,color='green')
    plt.title("Key rate")
    plt.xlabel('trnode')
    plt.ylabel('Key rate')
    plt.show()



if __name__ == '__main__':

    p1 = Process(target=run, args=(0.3,4,50))
    p1.start()
    #p1.join()
    p2 = Process(target=run, args=(0.35,4,50))
    p2.start()
    #p2.join()
    p3 = Process(target=run, args=(0.4,4,50))
    p3.start()
    #p3.join()
    p4 = Process(target=run, args=(0.45,4,50))
    p4.start()
    #p4.join()

    p1.join()
    p2.join()
    p3.join()
    p4.join()