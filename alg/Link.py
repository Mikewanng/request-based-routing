class Link(object):#定义边
    def __init__(self,fr=None,to=None,capacity=0,rate=0,Is_connected=False):
        self.fr=fr
        self.to=to
        self.c=capacity #密钥池
        self.rate=rate  #密钥速率
        self.Is_connected=Is_connected
        if self.c>0 or self.rate >0:
            self.Is_connected=True
        


    def dellink(self):
        self.fr=None
        self.to=None
        self.c=0    
        self.rate=0
        self.Is_connected=False





