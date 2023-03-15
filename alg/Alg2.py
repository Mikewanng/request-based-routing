from Alg1 import *
import copy,sys,queue

class Alg2:
    def __init__(self):
        self.path=[] #储存找到的路径
        self.sp=[] #储存路径安全概率
        self.fsp=0 #最终安全概率
        self.finalpath=[]

    def alg2(self,topo,req):#找到满足请求的路径req=(s,d,keyvo,keyrate)
        
        g=topo
        #筛选路径先根据密钥量再根据密钥速率
        Topo().TopoFilter(g,req,3)
        #转为邻接表
        glist=Topo().Toporeduce(g)
        #寻找可用路径
        feasiblepath=Dijkstra().kspf(glist,req[0],req[1])
        #找出最小代价的路径
        
        if feasiblepath==[]:
            return NULL
        mincost=0
        
        for i in range(len(feasiblepath)):
            if i==0:
                mincost= Cost().cost2(g,feasiblepath[i],feasiblepath,req)
                path= feasiblepath[i]
            else:
                c=Cost().cost2(g,feasiblepath[i],feasiblepath,req)
                if c< mincost:
                    mincost= c
                    path= feasiblepath[i]
        #返回最优路径
        

        return path