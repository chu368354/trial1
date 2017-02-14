import numpy as np
import pandas as pd
import feedparser
from time import mktime
import datetime
from subprocess import check_output
import sys

excel1=pd.ExcelFile("D:\Dropbox\Fat Ton\Python\Financial_Statement_Download\HKEX_Stock_List.xlsx")
excel2=excel1.parse("list")

#len(excel2.index)

NewsSummary1=pd.DataFrame()

for i in range(0,len(excel2.index)):
    symbol1=excel2["Google_Symbol"][i]
    print(symbol1)
    url1="".join(["https://www.google.com.hk/finance/company_news?q=",symbol1,"&output=rss"])
    feed=feedparser.parse(url1).entries

    for j in range(0,len(feed)):
        try:
            newstitle = feed[j]["title"]

            newslink=feed[j]["links"][0].href

            newstime = datetime.fromtimestamp(mktime(feed[j].updated_parsed))

            NewsDummy=pd.DataFrame({"Symbol":[symbol1],
                                      "NewsTitle":[newstitle],
                                    "NewsLink": [newslink],
                                    "NewsTime": [newstime]})

            NewsSummary1=pd.concat([NewsSummary1,NewsDummy])
            Log = "".join([symbol1])
            print(Log)
        except:
            ErrLog = "".join(["Error:",symbol1])
            print(ErrLog)
            continue



NewsSummary2=NewsSummary1.sort_values(["NewsTime","Symbol"],ascending=[0,1])
#Keyword filter
NewsSummary2["Keyword1"]=NewsSummary2["NewsTitle"].str.contains("趁")
NewsSummary2["Keyword2"]=NewsSummary2["NewsTitle"].str.contains("低")
NewsSummary2["Keyword3"]=NewsSummary2["NewsTitle"].str.contains("吸")
NewsSummary2["Keyword4"]=NewsSummary2["NewsTitle"].str.contains("評級")

#Filter latest 3 month data
month3=datetime.datetime.now()-datetime.timedelta(days=92)
NewsSummary3=NewsSummary2[NewsSummary2.NewsTime>month3]

#NewsSummary1.to_csv("D:\R\stock\GoogleNews.csv",  sep=',', index=False)

Dataexportpath = "".join(["D:\Dropbox\Fat Ton\R\FS_analytic\GoogleNews.xlsx"])
DataWriter = pd.ExcelWriter(Dataexportpath, engine='xlsxwriter',options={'strings_to_urls': False})
NewsSummary3.to_excel(DataWriter, "Sheet1", index=False)
DataWriter.save()

print(NewsSummary3)
