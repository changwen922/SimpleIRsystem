# Simple IR System : Ranking by Vector Space Models

執行
`python3.9 main.py --query "English key words" --query2 "中文關鍵字"`
執行後會回傳以下結果：
* 分別用Cosine及Euclidean計算出來的英文關鍵字推薦結果
* 使用Relevance Feedback後得到的英文關鍵字推薦結果
* 使用Jieba分詞後的中文關鍵字推薦結果
* 計算推薦結果的Recall@10/MAP@10/MRR@10

# Data Resources
* 上述第一二點使用的資料為8,000筆從reuters.com搜集來的英文文章
* 第三點為2,000筆從chinatimes.com及setn.com搜集來的中文文章
* 第四點為另一筆有標註過的小型英文文章（1460筆文章, 76組關鍵字）

# Example
* 為節省時間以資料461至資料695進行測試
* 圖一為分別用Cosine及Euclidean計算出來的英文關鍵字推薦結果
![image](https://github.com/changwen922/WSM-project1/blob/0560c485c909e988ae5b13e17d5d12da47627171/Q1.png)

* 圖二為使用Relevance Feedback後得到的英文關鍵字推薦結果
![image](https://github.com/changwen922/WSM-project1/blob/0560c485c909e988ae5b13e17d5d12da47627171/Q2.png)

* 圖三為使用Jieba分詞後的中文關鍵字推薦結果
![image](https://github.com/changwen922/WSM-project1/blob/5183c96b48da1f5800b1634f77f12113fba63178/Q3.png)

* 圖四在計算推薦結果的Recall@10/MAP@10/MRR@10
![image](https://github.com/changwen922/WSM-project1/blob/5183c96b48da1f5800b1634f77f12113fba63178/Q4.png)
