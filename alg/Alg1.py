#对比对象AQAN算法
from Dijkstra import *
from Cost import *
from Topo import *

class Alg1:
    def __init__(self):
        self.path=[] #储存找到的路径
        self.sp=[] #储存路径安全概率
        

    def alg1(self,topo,req):#找到满足请求的路径req=(s,d,keyvo,keyrate)
        
        g=topo
        #筛选路径先根据密钥量再根据密钥速率
        Topo().TopoFilter(g,req,0)
        #寻找可用路径
        feasiblepath=Dijkstra().kspf(g,req[0],req[1])
        #找出最小代价的路径
        if feasiblepath==[]:
            Topo().TopoFilter(g,req,1)
            feasiblepath=Dijkstra().kspf(g,req[0],req[1])
        if feasiblepath==[]:
            return NULL
        mincost=0
        
        for i in range(len(feasiblepath)):
            if i==0:
                mincost= Cost().cost1(feasiblepath[i])
                path= feasiblepath[i]
            else:
                if Cost().cost1(feasiblepath[i])< mincost:
                    mincost= Cost().cost1(feasiblepath[i])
                    path= feasiblepath[i]
        #返回最优路径
        

        return path
