from openpyxl import Workbook

wb = Workbook()
ws = wb.active

head=["reqkeyrate","SR1","SR2","finishtime1","finishtime2"]
ws.append(head)

ns=[0]*10
for i in range(10):
    ns[i]=i
for j in range(10):
    ws.append([ns[j],ns[9-j],ns[j],ns[9-j],ns[j],ns[9-j]])
ws.append(['a','b','c','d'])
ws.append([1,2,3,4])
ws.append([5,6,7,8])

wb.save('1.xlsx')