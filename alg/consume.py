# 计算密钥消耗

class Con:
    def __init__(self):
        pass

    def CalCon(self,pathset):
        sum=0
        for i in pathset:
            for j in i[0]:
                sum+=len(j)-1
        return sum