# WSM Project 1: Ranking by Vector Space Models

執行
python3.9 main.py --query "Taiwan YouTube COVID-19" --query2 "烏克蘭 大選"
執行後會回傳Question1～4的所有結果
(很抱歉8000筆資料跑不太動)

# Question1
function getQ1answer(searchlist, files, n, mode ) 
n為跑出前n筆資料，mode為cosine模式及euclidean模式
cosine模式會依照老師提供的util.py算出cosine分數
並在util.py中新增加function Euclidean(vector1, vector2)計算euclidean分數

圖Q1為跑資料461至資料695的結果
![image](https://github.com/changwen922/WSM-project1/blob/0560c485c909e988ae5b13e17d5d12da47627171/Q1.png)

# Question2
抓取上一題得到的最相關（第一筆）資料
並把此筆資料去執行 function getQ2query(searchlist, q1answer) 得到新query
q1answer為第一題排序後的第一筆文件

圖Q2為跑資料461至資料695的結果
![image](https://github.com/changwen922/WSM-project1/blob/0560c485c909e988ae5b13e17d5d12da47627171/Q2.png)

# Question3
將資料分類成中文及英文
使用jieba對中文進行斷句
此題程式碼在chi_VecctorSpace.py中

輸出結果如圖Q3
![image](https://github.com/changwen922/WSM-project1/blob/5183c96b48da1f5800b1634f77f12113fba63178/Q3.png)


# Question4
function getQ4answer(searchlist, files,n, mode='cos', h = int)
n為前n筆資料，h為第h筆query
將資料和query做cosine相似後得到的前10筆文件和rel.tsv裡的正確對應文件數做recall,MAP,MRR

輸出結果如圖Q4
![image](https://github.com/changwen922/WSM-project1/blob/5183c96b48da1f5800b1634f77f12113fba63178/Q4.png)