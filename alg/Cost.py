from asyncio.windows_events import NULL
from xmlrpc.client import MAXINT


class Cost(object):#�����

    def __init__(self):
        pass

    def cost1(self,g,path,a=0.4,b=0.5):
        cost=0
        #�ҵ���С����·��Կ��
        minkeyvo= MAXINT
        for i in range(len(path)-1):
            minkeyvo = min (minkeyvo , g[path[i]][path[i+1]].c)
            cost+=1/g[path[i]][path[i+1]].c
        #�ҵ���С����·��Կ��������
        minkeyrate= MAXINT
        for i in range(len(path)-1):
            minkeyrate = min (minkeyrate , g[path[i]][path[i+1]].rate)
            cost+=1/g[path[i]][path[i+1]].rate
        #cost=(1/minkeyvo)+(1/minkeyrate)
        return cost
    def timecost(self,g,path,req):
        #�ҵ���С����·��Կ��
        minkeyvo= MAXINT
        for i in range(len(path)-1):
            minkeyvo = min (minkeyvo, g[path[i]][path[i+1]].c)
        #�ҵ���С����·��Կ��������
        minkeyrate= MAXINT
        for i in range(len(path)-1):
            minkeyrate = min (minkeyrate, g[path[i]][path[i+1]].rate)
        t=0
        if req[2]==NULL:
            return 10
        elif req[3]==NULL:
            return max((req[2]-minkeyvo)/minkeyrate,0)
        else:
            return (req[2]-minkeyvo)/req[3]
            
        

    def cost2(self,g,path,pathset,req,a=0.4,b=0.6):
         #�ҵ���С����·��Կ��
        minkeyvo= MAXINT
        for i in range(len(path)-1):
            minkeyvo = min (minkeyvo, g[path[i]][path[i+1]].c)
        #�ҵ���С����·��Կ��������
        minkeyrate= MAXINT
        for i in range(len(path)-1):
            minkeyrate = min (minkeyrate , g[path[i]][path[i+1]].rate)
        
        if req[2]==NULL:
            cost=1/minkeyrate*(len(path)-1)/(len(pathset[0])-1)
        else:
            cost=(req[2]-minkeyvo)/minkeyrate*(len(path)-1)/(len(pathset[0])-1)

        
        return cost

    def issastify(self,g,path,req):
         #�ҵ���С����·��Կ��
        minkeyvo= MAXINT
        for i in range(len(path)-1):
            minkeyvo = min (minkeyvo, g[path[i]][path[i+1]].c)
        
        if req[3]!=NULL: #��������а����������޷�����
            return False
        else: #����ֻ����Կ��
            if minkeyvo >= req[2]:
                return True
        
        return False

    def th(self,g,path,req):
         #�ҵ���С����·��Կ��
        minkeyvo= MAXINT
        for i in range(len(path)-1):
            minkeyvo = min (minkeyvo, g[path[i]][path[i+1]].c)

        minkeyrate= MAXINT
        for i in range(len(path)-1):
            minkeyrate = min (minkeyrate , g[path[i]][path[i+1]].rate)

        if req[2]==NULL: #���������ֻ��������
            return req[3]
        elif req[3]==NULL: #����ֻ����Կ����������ʱ������������
            return 0
        else:
            return req[3]

    def keycon(self,g,path,req):
         #�ҵ���С����·��Կ��
        minkeyvo= MAXINT
        for i in range(len(path)-1):
            minkeyvo = min (minkeyvo, g[path[i]][path[i+1]].c)

        minkeyrate= MAXINT
        for i in range(len(path)-1):
            minkeyrate = min (minkeyrate , g[path[i]][path[i+1]].rate)

        if req[2]==NULL: #���������ֻ��������
            return req[3]*10*(len(path)-1)
        elif req[3]==NULL: #����ֻ����Կ��
            return req[2]*(len(path)-1)
        else:
            return req[2]*(len(path)-1)
        
        