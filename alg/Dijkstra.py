from Sp import *
import sys,heapq
class Dijkstra:
    def __init__(self):
        self._passed=[]
        self._nopass=[]
        self._prev=[]  #记录从源点V0到终点Vi的当前最短路径上终点Vi的直接前驱顶点序号，若V0到Vi之间有边前驱为V0否则为-1 
        self._cost=[]  #记录源点到终点之间最短路径的代价，存在记V0到Vi的边的安全概率，否则记为0
        self._path=[]  #源点到目的点的路径

    def dijkstra(self,topo,source,des):
        #初始化起点
        if source==des:
            return [des],1
        self._passed.append(source)
        self.topo=topo
        self._visited=[0]*len(topo[0])

        #初始化前驱列表以及代价
        for i in range(len(topo[0])):
            if i==source:
                self._cost.append(1)
            else:
                self._cost.append(0)
            self._prev.append(-1)
        
        heap=[]
        for i in self.topo[0][source]:
            self._prev[i[0]]=source
            self._cost[i[0]]=i[1]
            heapq.heappush(heap,(1-i[1],i[0]))  #要将高安全概率的节点优先级提高，将sp值转化为1-f
        while heap!=[]:
            #弹出最大安全概率节点
            tmpe=heapq.heappop(heap)
            tmp=list(tmpe)
            tmp[0]=1-tmp[0] #重新转化为安全概率p
            tmpe=tuple(tmp)
            if self._visited[tmpe[1]]==1:#如果该点已到过，就进行下一次循环
                continue
            self._visited[tmpe[1]]=1
            for i in self.topo[0][tmpe[1]]:
                if Sp().pathsp(topo,self.getpath(tmpe[1])+[i[0]])>self._cost[i[0]]:
                    self._cost[i[0]]=Sp().pathsp(topo,self.getpath(tmpe[1])+[i[0]])
                    self._prev[i[0]]=tmpe[1]
                    heapq.heappush(heap,(1-self._cost[i[0]],i[0]))
        #确定路径
        path=self.getpath(des)
        if path[0]==source and len(path)>=2:
            return path,Sp().pathsp(topo,path)
        else:
            return [],0
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
        self._visited=[0]*len(topo[0])

        #初始化前驱列表以及代价
        for i in range(len(topo[0])):
            if i==source:
                self._cost.append(0)
            else:
                self._cost.append(sys.maxsize/2)
            self._prev.append(-1)
        
        heap=[]
        for i in self.topo[0][source]:
            self._prev[i[0]]=source
            self._cost[i[0]]=i[1]
            heapq.heappush(heap,(i[1],i[0]))  #跳数作为cost
        while heap!=[]:
            #弹出最小cost节点
            tmpe=heapq.heappop(heap)
            
            if self._visited[tmpe[1]]==1:#如果该点已到过，就进行下一次循环
                continue
            self._visited[tmpe[1]]=1
            for i in self.topo[0][tmpe[1]]:
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