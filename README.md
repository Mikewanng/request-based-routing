# request-based-routing


实验参数设置：请求R(s,d,keyvo,keyrate)

自变量： 请求的密钥速率、请求的密钥量需求

因变量：请求满足率、吞吐量、请求完成时间、密钥消耗量

将请求分为三个类型分别进行实验
R(s,d,keyvo,null) 对比对象: ada spf
实验1：链路上的密钥生成速率和密钥池容量随机变化
自变量：密钥量上升
因变量：请求满足率、请求完成时间、资源消耗量、吞吐量

R(s,d,null,keyrate)  对比对象: ada 
实验2：链路上的密钥生成速率和密钥池容量随机变化
自变量：密钥供应率上升
因变量：请求满足率、资源消耗量

R(s,d,keyvo,keyrate)  对比对象: ada
实验3：链路上的密钥生成速率和密钥池容量随机变化
自变量：密钥量上升，密钥速率不变
因变量：请求满足率、资源消耗量

R(s,d,keyvo,keyrate)  对比对象: ada 
实验4：链路上的密钥生成速率和密钥池容量随机变化
自变量：密钥量不变，密钥速率上升
因变量：请求满足率、资源消耗量 
