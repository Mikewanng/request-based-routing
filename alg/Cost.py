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
    def cost2(self,g,path,pathset,a=0.4,b=0.6):
         #找到最小的链路密钥量
        minkeyvo= MAXINT
        for i in range(len(path)-1):
            minkeyvo = min (minkeyvo , g[path[i]][path[i+1]].c)
        #找到最小的链路密钥生成速率
        minkeyrate= MAXINT
        for i in range(len(path)-1):
            minkeyrate = min (minkeyrate , g[path[i]][path[i+1]].rate)
        
        cost=(b* minkeyrate+a*minkeyvo)*(len(path)-1)/(len(pathset[0])-1)

        return 0