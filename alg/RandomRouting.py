#随机路由算法
from Dijkstra import *
from Sp import *
from Topo import *
import random

class Rr:
    def __init__(self):
        self.path=[] #储存找到的路径
        self.sp=[] #储存路径安全概率
        self.fsp=0 #最终安全概率

    def rr(self,topo,source,des,sth):#找到满足安全概率阈值的路径
        g=topo
        cur_sp=0
        while cur_sp<sth:
            #转为邻接表
            topotable=Topo().Toporeducehop(g)
            path,path_sp=self.randompath(topotable,source,des)#返回找到的路径和安全概率
            if path==[]: #意味着没有足够的路径来保证安全概率
                return [[[],[],0]] #拒绝服务返回0
            else:
                self.path.append(path)
                self.sp.append(path_sp)
            cur_sp=Sp().CalSumSecurityProbability(cur_sp,path_sp)
            self.fsp=cur_sp
            #移除拓扑上的边
            Topo().TopoUpdater(g,path)
        return [[self.path,self.sp,self.fsp]]
    def rrmaxs(self,topo,source,des,sth=5):#找到最大安全性
        g=topo
        cur_sp=0
        while cur_sp<sth:
            #转为邻接表
            topotable=Topo().Toporeducehop(g)
            path,path_sp=self.randompath(topotable,source,des)#返回找到的路径和安全概率
            if path==[]: #意味着没有路径了
                break
            else:
                self.path.append(path)
                self.sp.append(path_sp)
            cur_sp=Sp().CalSumSecurityProbability(cur_sp,path_sp)
            self.fsp=cur_sp
            #移除拓扑上的边
            Topo().TopoUpdater(g,path)
        return [[self.path,self.sp,self.fsp]]
    def randompath(self,g,source,des):
        count=0
        path=[source]
        curnode=source
        dis=[]
        w=[]
        pr=[]
        while curnode != des:
            count+=1
            #if count>10000:
                #return [],0
            dis=[]
            w=[]
            pr=[]
            prtable=[]
            sumw=0
            #找出下一跳距目的节点距离不能有环,不能回头
            for i in g[0][curnode]:
                if i[0] !=path[-1]:
                    tmppath=Dijkstra().hopdijkstra(g,i[0],des)
                    if tmppath!=[]:
                        dis.append([len(tmppath)-1,i[0]])
                
            #如果dis为空，那么意味着进入死胡同，如果还能找到其他路径,需要重随机
            if dis==[]:
                if Dijkstra().hopdijkstra(g,source,des)!=[]:
                    return self.randompath(self,g,source,des)
                else:
                    return [],0
            #降序
            dis=sorted(dis,key=lambda distance: distance[0],reverse = True)
            #计算权重
            for i in range(len(dis)):
                if i ==0:
                    w.append(1)
                    sumw+=1
                elif i>0 and dis[i][0]==dis[i-1][0]:
                    w.append(w[i-1])
                    sumw+=w[i-1]
                elif i>0 and dis[i][0]<dis[i-1][0]:
                    w.append(w[i-1]+1)
                    sumw+=w[i-1]+1
            #概率确定
            for i in w:
                pr.append(i/sumw)
            for i in range(len(pr)):
                if i==0:
                    prtable.append(0)
                else:
                    prtable.append(prtable[i-1]+pr[i-1])
            prtable.append(1)
            #选择
            randnum=random.random()
            for i in range(len(dis)):
                if randnum>prtable[i] and randnum<=prtable[i+1]:
                    curnode=dis[i][1]
                    path.append(curnode)
        #消除环路
        
        t=Sp().checkring(path)
        while t!=[0,0]:
            path=path[:t[0]]+path[t[1]:]
            t=Sp().checkring(path)
        

        return path ,Sp().pathsp(g,path)

