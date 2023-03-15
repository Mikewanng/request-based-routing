from asyncio.windows_events import NULL
from xmlrpc.client import MAXINT


class Cost(object):#定义边

    def __init__(self):
        pass

    def cost1(self,g,path,a=0.4,b=0.5):
        #找到最小的链路密钥量
        minkeyvo= MAXINT
        for i in range(len(path)-1):
            minkeyvo = min (minkeyvo , g[path[i]][path[i+1]].c)
        #找到最小的链路密钥生成速率
        minkeyrate= MAXINT
        for i in range(len(path)-1):
            minkeyrate = min (minkeyrate , g[path[i]][path[i+1]].rate)

        cost=(1/minkeyvo)+(1/minkeyrate)
        return cost
    def timecost(self,g,path,req):
        #找到最小的链路密钥量
        minkeyvo= MAXINT
        for i in range(len(path)-1):
            minkeyvo = min (minkeyvo, g[path[i]][path[i+1]].c)
        #找到最小的链路密钥生成速率
        minkeyrate= MAXINT
        for i in range(len(path)-1):
            minkeyrate = min (minkeyrate, g[path[i]][path[i+1]].rate)
        t=0
        if req[2]==NULL:
            return -1
        elif req[3]==NULL:
            return (req[2]-minkeyvo)/minkeyrate
        else:
            return (req[2]-minkeyvo)/req[3]
            
        

    def cost2(self,g,path,pathset,req,a=0.4,b=0.6):
         #找到最小的链路密钥量
        minkeyvo= MAXINT
        for i in range(len(path)-1):
            minkeyvo = min (minkeyvo, g[path[i]][path[i+1]].c)
        #找到最小的链路密钥生成速率
        minkeyrate= MAXINT
        for i in range(len(path)-1):
            minkeyrate = min (minkeyrate , g[path[i]][path[i+1]].rate)
        
        if req[2]==NULL:
            cost=minkeyrate*(len(path)-1)/(len(pathset[0])-1)
        else:
            cost=(req[2]-minkeyvo)*(len(path)-1)/(len(pathset[0])-1)

        
        return cost

    def issastify(self,g,path,req):
         #找到最小的链路密钥量
        minkeyvo= MAXINT
        for i in range(len(path)-1):
            minkeyvo = min (minkeyvo, g[path[i]][path[i+1]].c)
        
        if req[3]!=NULL: #如果请求中包含速率则无法满足
            return False
        else: #否则只看密钥池
            if minkeyvo >= req[2]:
                return True
        
        return False

    def th(self,g,path,req):
         #找到最小的链路密钥量
        minkeyvo= MAXINT
        for i in range(len(path)-1):
            minkeyvo = min (minkeyvo, g[path[i]][path[i+1]].c)

        minkeyrate= MAXINT
        for i in range(len(path)-1):
            minkeyrate = min (minkeyrate , g[path[i]][path[i+1]].rate)

        if req[2]==NULL: #如果请求中只包含速率
            return req[3]
        elif req[3]==NULL: #否则只看密钥池数量，此时不计算吞吐量
            return 0
        else:
            return req[3]

    def keycon(self,g,path,req):
         #找到最小的链路密钥量
        minkeyvo= MAXINT
        for i in range(len(path)-1):
            minkeyvo = min (minkeyvo, g[path[i]][path[i+1]].c)

        minkeyrate= MAXINT
        for i in range(len(path)-1):
            minkeyrate = min (minkeyrate , g[path[i]][path[i+1]].rate)

        if req[2]==NULL: #如果请求中只包含速率
            return 0
        elif req[3]==NULL: #否则只看密钥量
            return req[2]*(len(path)-1)
        else:
            return req[2]*(len(path)-1)
        
        