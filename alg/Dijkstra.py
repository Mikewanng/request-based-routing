import sys,heapq

import copy

class Dijkstra:
    def __init__(self):
        self._passed=[]
        self._nopass=[]
        self._prev=[]  #记录从源点V0到终点Vi的当前最短路径上终点Vi的直接前驱顶点序号，若V0到Vi之间有边前驱为V0否则为-1 
        self._cost=[]  #记录源点到终点之间最短路径的代价，存在记V0到Vi的边的安全概率，否则记为0
        self._path=[]  #源点到目的点的路径

   

    def getpath(self,u):   #获取到当前点u的路径
        tmp=u
        li=[]
        while u!=-1:
            li.append(u)
            u=self._prev[u]

        li.reverse()
        return li

    def hopdijkstra(self,topo,source,des):#最短路径
        #初始化起点
        if source==des:
            return [des]
        self._passed.append(source)
        self.topo=topo
        self._visited=[0]*len(topo)
        self._cost=[]
        self._prev=[]
        self._visited[source]=1
        #初始化前驱列表以及代价
        for i in range(len(topo)):
            if i==source:
                self._cost.append(0)
            else:
                self._cost.append(sys.maxsize/2)
            self._prev.append(-1)
        
        heap=[]
        for i in self.topo[source]:
            self._prev[i[0]]=source
            self._cost[i[0]]=i[1]
            heapq.heappush(heap,(i[1],i[0]))  #跳数作为cost
        while heap!=[]:
            #弹出最小cost节点
            tmpe=heapq.heappop(heap)
            
            if self._visited[tmpe[1]]==1:#如果该点已到过，就进行下一次循环
                continue
            self._visited[tmpe[1]]=1
            for i in self.topo[tmpe[1]]:
                if self._cost[tmpe[1]]+i[1]<self._cost[i[0]]:
                    self._cost[i[0]]=self._cost[tmpe[1]]+i[1]
                    self._prev[i[0]]=tmpe[1]
                    heapq.heappush(heap,(self._cost[i[0]],i[0]))
        #确定路径
        path=self.getpath(des)
        if path[0]==source and len(path)>=2:
            return path
        else:
            return []

    def kspf(self,g,source,des,maxk=20): #搜索多路径
        ng=g
        self.aset=[]
        self.bset=[]
        li=self.hopdijkstra(copy.deepcopy(ng),source,des)
        if len(li):
            self.aset.append(li)
        else:
            return self.bset
        for k in range(1,maxk):
            for i in range(len(self.aset[-1])-1):
                tmpg=copy.deepcopy(ng)
                curnode=self.aset[-1][i]
                curroot=self.aset[-1][i+1]
                pathahead=self.aset[-1][0:i]
		        #将当前边cost设为无穷大
                for listi in tmpg[self.aset[-1][i]]:
                    if listi[0]==self.aset[-1][i+1]:
                        listi[1]=sys.maxsize/2
                        break
                for listi in tmpg[self.aset[-1][i+1]]:
                    if listi[0]==self.aset[-1][i]:
                        listi[1]=sys.maxsize/2
                        break
                #tmpg[self.aset[-1][i]][self.aset[-1][i+1]]=sys.maxsize/2
                #tmpg[self.aset[-1][i+1]][self.aset[-1][i]]=sys.maxsize/2
                path=self.hopdijkstra(tmpg,curnode,des)
                if len(path):
                    sumpath=pathahead+path
                    if sumpath  not in self.bset and sumpath not in self.aset and self.noring(sumpath):#无环路
                        self.bset.append(sumpath)

            if len(self.bset):
                #找出bset中cost最小的长度最短的
                f=0
                mincost=5000
                for i in range(len(self.bset)):
                    if len(self.bset[i])<mincost:
                        mincost=len(self.bset[i])
                        f=i
                if self.bset[f]  not in self.aset:
                    self.aset.append(self.bset[f])
                self.bset.remove(self.bset[f])
            else:
                break
        return self.aset



		        


    def noring(self,path):#判断是否有环
        for i in range(len(path)):
            for j in range(i+1,len(path)):
                if path[i]==path[j]:
                    return False
        return True
		