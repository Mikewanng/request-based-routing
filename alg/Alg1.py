#对比对象AQAN算法
from copy import deepcopy
from Dijkstra import *
from Cost import *
from Topo import *

class Alg1:
    def __init__(self):
        self.path=[] #储存找到的路径
        self.sp=[] #储存路径安全概率
        

    def ada(self,topo,req,a=2/3,b=1/3):#找到满足请求的路径req=(s,d,keyvo,keyrate)
        
        g=topo
        #筛选路径先根据密钥量再根据密钥速率
        if req[2]==NULL: #如果只对密钥速率有需求
            Topo().TopoFilter(g,req,1)
            #转为邻接表
            glist=Topo().Toporeduce(g)
            #寻找可用路径
            feasiblepath=Dijkstra().kspf(glist,req[0],req[1])
        elif req[3]==NULL:  #如果只对密钥量有需求,先将
            ng=copy.deepcopy(topo)
            Topo().TopoFilter(ng,req,0)
            #转为邻接表
            glist=Topo().Toporeduce(ng)
            #寻找可用路径
            feasiblepath=Dijkstra().kspf(glist,req[0],req[1])
            #找出最小代价的路径
            if feasiblepath==[]:
                glist=Topo().Toporeduce(g)
                feasiblepath=Dijkstra().kspf(glist,req[0],req[1])
        else:
            ng=copy.deepcopy(topo)
            Topo().TopoFilter(ng,req,0)
            #转为邻接表
            glist=Topo().Toporeduce(ng)
            #寻找可用路径
            feasiblepath=Dijkstra().kspf(glist,req[0],req[1])
            #找出最小代价的路径
            if feasiblepath==[]:

                Topo().TopoFilter(g,req,1)
                #转为邻接表
                glist=Topo().Toporeduce(g)
                #寻找可用路径
                feasiblepath=Dijkstra().kspf(glist,req[0],req[1])


        
        #找出最小代价的路径
        """
        if feasiblepath==[]:
            Topo().TopoFilter(g,req,1)
            feasiblepath=Dijkstra().kspf(glist,req[0],req[1])
            """
        if feasiblepath==[]:
            return NULL


        mincost=0
        Costpmh=Cost().cost1(g,feasiblepath[0])
        nmin=len(feasiblepath[0])-1
        ACostpmh=Costpmh/nmin
        for i in range(len(feasiblepath)):
            if i==0:
                mincost= a*Cost().cost1(g,feasiblepath[i])+b*ACostpmh*(len(feasiblepath[i])-1-nmin)
                path= feasiblepath[i]
            else:
                c=a*Cost().cost1(g,feasiblepath[i])+b*ACostpmh*(len(feasiblepath[i])-1-nmin)
                if c< mincost:
                    mincost=c
                    path= feasiblepath[i]
        #返回最优路径
        

        return path

    def kod(self,topo,req):#找到满足请求的路径req=(s,d,keyvo,keyrate)
        if req[2]==NULL:
            return NULL
        g=topo
        #转为邻接表
        glist=Topo().Toporeduce(g)
        #寻找可用路径
        feasiblepath=Dijkstra().kspf(glist,req[0],req[1])
        for path in feasiblepath:
            if Cost().issastify(g,path,req):
                return path

        return NULL

    def spf(self,topo,req):#最短路径
        if req[2]==NULL:
            return NULL
        g=topo
        #转为邻接表
        glist=Topo().Toporeduce(g)
        #寻找可用路径
        feasiblepath=Dijkstra().hopdijkstra(glist,req[0],req[1])
       

        return feasiblepath