from Alg1 import *
import copy,sys,queue
class Alg2:
    def __init__(self):
        self.path=[] #储存找到的路径
        self.sp=[] #储存路径安全概率
        self.fsp=0 #最终安全概率
        self.finalpath=[]

    def alg2(self,topo,source,des,sth):#找到满足安全概率阈值的路径
        #先调用alg1找出普通多路径的数量
        tmp=Alg1().alg1(copy.deepcopy(topo),source,des,sth)
        fsp=tmp[0][2]
        #如果alg1能够满足那么确定路径数量
        if fsp>=sth:
            path_num=len(tmp[0][0])
            if path_num==1:#不需要分段
                return tmp
            return self.alg2n(copy.deepcopy(topo),source,des,path_num)
            
        else:#算法1不能满足，那么依次递增路径数量直到满足sth
            for n in range(2,100):
                t=self.alg2n(copy.deepcopy(topo),source,des,n)
                #判断返回路径是否为空
                for i in t:
                    if i[0]==[]:#无法找到足够路径数量
                        return [[[],[],0]]
                #判断能否满足安全性需求
                sp=Sp().segsp(t)
                if sp>=sth:
                    
                    return t
                    
    def alg2n(self,topo,source,des,n):#找出n条路径并返回
        sumlen=1000000
        #找出最近的可信点且距离起点更近
        relaynode=sys.maxsize
        topotable=Topo().Toporeducehop(topo)
        for i in range(len(topo[0])):
            if topo[1][i]==1 and i!=source and i!=des:#是可信节点
                path1=Dijkstra().hopdijkstra(topotable,source,i)
                if path1!=[]:
                    len1=len(path1)-1
                else:
                    continue
                path2=Dijkstra().hopdijkstra(topotable,i,des)
                if path1!=[]:
                    len2=len(path2)-1
                else:
                    continue

                if len1+len2<sumlen:
                    sumlen=len1+len2
                    relaynode=i

        #判断是否分段
        if relaynode==sys.maxsize:
            return Alg1().alg1n(copy.deepcopy(topo),source,des,n)
        t=Alg1().alg1n(copy.deepcopy(topo),source,des,n)
        t1=Alg1().alg1n(topo,source,relaynode,n)
        tmptopo=copy.deepcopy(topo)
        t2=Alg1().alg1n(topo,relaynode,des,n)

        if len(t1[0][0])==n and len(t2[0][0])==n and t1[0][2]*t2[0][2]>t[0][2]:
                return t1+self.alg2n(tmptopo,relaynode,des,n)
        
        else:
            return t
        

    def alg2maxs(self,topo,source,des,sth=1):#找到最大安全性的路径,分段的路径数量尽量接近。
        
             
        t=[]
        curnode=source
        #找出当前最近中继距离sd
        #minrelay=self.findminrelay(topo,source,des)
        while curnode!=des:
            minrelay=self.findminrelay(topo,source,des)
            
            nseg=Alg1().alg1maxs(copy.deepcopy(topo),curnode,des)
            if minrelay==-1:
                t+=nseg
                break
            for i in range(2,6):
                tmp=[]
                seg1=Alg1().alg1maxn(topo,curnode,minrelay,i)
                tmptopo=copy.deepcopy(topo)
                seg2=Alg1().alg1maxn(tmptopo,minrelay,des,i)
                if seg1[0][2]*seg2[0][2]>nseg[0][2]:
                    
                    tmp=seg1
            if tmp!=[]:
                curnode=minrelay
                t+=seg1
            else:
                t+=nseg
                break
        return t
    def alg2max(self,topo,source,des,sth=1):
        t=[] #返回值
        pathchain=[source]
        curnode=source
        #先找出两条的分段路径然后在每一段上增加
        while curnode!=des:
            minrelay=self.findminrelay(topo,source,des)
            g1=copy.deepcopy(topo)
            nseg=Alg1().alg1maxn(g1,curnode,des,2)
            if minrelay==-1:
                t+=nseg
                topo=g1
                break
            
            tmp=[]
            seg1=Alg1().alg1maxn(topo,curnode,minrelay,2) #找出当前节点到最近可信中继节点
            g2=copy.deepcopy(topo)
            seg2=Alg1().alg1maxn(topo,minrelay,des,2) #找出最近可信中继节点到目的节点
            if seg1[0][2]*seg2[0][2]>nseg[0][2]: #如果分段后带来更大的安全性
                curnode=minrelay
                pathchain.append(curnode)
                t+=seg1
                topo=g2
            else:
                t+=nseg
                topo=g1
                break
        pathchain.append(des)   #源节点与可信中继节点以及目的节点的链用以查找一段路径
        #tmpsd=[]
        tt=[]
        for i in range(len(pathchain)-1):
            tt.append([pathchain[i],pathchain[i+1]])
        #每一段单独找路
        while True:
            tmpsd=copy.deepcopy(tt)
            while tmpsd!=[]:
                p=queue.PriorityQueue()
                for i in tmpsd:
                    topotable=Topo().Toporeduce(copy.deepcopy(topo))
                    tmp_path,tmp_sp=Dijkstra().dijkstra(topotable,i[0],i[1])
                    if tmp_path!=[]:
                        p.put((1-tmp_sp,tmp_path))
                    if p.empty():
                        return t
                chosed_path=p.get()
                for i in t:
                    if i[0][0][0]==chosed_path[1][0] and i[0][0][-1]==chosed_path[1][-1]:
                        i[0].append(chosed_path[1])
                        i[1].append(1-chosed_path[0])
                        i[2]=Sp().CalSumSecurityProbability(i[2],1-chosed_path[0])
                        Topo().TopoUpdate(topo,chosed_path[1])
                        tmpsd.remove([chosed_path[1][0],chosed_path[1][-1]])
                        break


            


        return t
                    
                    
               
            

            
            
            
            
            
            
            
        
    def findminrelay(self,topo,source,des):#找出最近relay
        sumlen=1000000
        #找出最近的可信点且距离起点更近
        relaynode=sys.maxsize
        topotable=Topo().Toporeducehop(topo)
        for i in range(len(topo[0])):
            if topo[1][i]==1 and i!=source and i!=des:#是可信节点
                path1=Dijkstra().hopdijkstra(topotable,source,i)
                if path1!=[]:
                    len1=len(path1)-1
                else:
                    continue
                path2=Dijkstra().hopdijkstra(topotable,i,des)
                if path1!=[]:
                    len2=len(path2)-1
                else:
                    continue

                if len1+len2<sumlen:
                    sumlen=len1+len2
                    relaynode=i
        if relaynode==sys.maxsize:
            return -1
        return relaynode