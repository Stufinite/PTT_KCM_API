# PTT_KCM_API (使用KCM當作PTT文章查詢索引的API)[![Build Status](https://travis-ci.org/Stufinite/PTT_KCM_API.svg?branch=master)](https://travis-ci.org/Stufinite/PTT_KCM_API)

一個透過[Swinger](https://github.com/UDICatNCHU/Swinger)去判斷鄉民留言情緒的api，藉由蒐集大量文章並且判斷情緒，達到迅速調查網路民調的效果。

### API usage and Results

API使用方式（下面所寫的是api的URL pattern）  
(Usage of API (pattern written below is URL pattern))：

##### parameter

* `issue`：Api will search and calculate on specific issue.
* `date`(optional)：You get results from specified Month or Year. e.g. `/PTT_KCM_API/api/locations/?issue=馬英九&date=2016-3` means return locations result which happened from `2016-3-01` to `2016-03-31` (Default：`All information on this issue`)

##### url pattern

API使用方式（下面所寫的是api的URL pattern）：

1. *`PTT_KCM_API/api/articles/?issue=<>`*  
  取得特定主題的`PTT文章`：    
  * 範例：`PTT_KCM_API/api/articles/?issue=燈迷`
  * reeulst：

    ```
    [
      {
        "content": "國民黨產終於漏出破口，兆豐銀洗錢被美國抓包，再扯出巴拿馬文件中出現八個 國民黨的洗錢帳戶，其中四個的地址就設在國民黨中央黨部。 此案馬在任時便已爆發，隱瞞了好幾個月，終於紙包不住火，兆豐金準備人事 大地震吧。 國民黨繼續再坳嘛，將8000億變成200億，然後說快破產，原來是在五鬼搬運，洗錢 案的地雷將一一爆開，200億將再變回8000億。 此案特偵組請靠邊站，你們遇到國民黨就只會牽結，已被看破手腳了，何況這也不 是特偵組的轄區，請其他單為來辦。 電視上將會再看到，子兀夜半仍啼熊，不信黨產喚不回，一時興起來一段燈迷。 迷題: 子兀夜啼......打一俗語。 . . . . . . . . . . 迷底: 靠腰 (要吃奶了) ",
        "article_title": "[討論] 洗錢案與國民黨黨產的破口",
        "author": "fashionjack (神奇傑克)",
        "board": "HatePolitics",
        "message_conut": {
          "all": 12,
          "count": -1,
          "neutral": 11,
          "push": 0,
          "boo": 1
        },
        "ip": "122.116.198.5",
        "date": "Tue Aug 23 09:18:26 2016",
        "messages": [
          {
            "push_content": "黨工：崩潰～我的錢",
            "push_userid": "WTF55665566",
            "push_tag": "噓",
            "push_ipdatetime": "08/23 09:19"
          },
          {
            "push_content": "美國果然資本主義，等你不當黨產條例過了，賺個吹哨子錢",
            "push_userid": "vyjssm",
            "push_tag": "→",
            "push_ipdatetime": "08/23 09:34"
          },
        ],
        "article_id": "M.1471915108.A.11D"
      }
    ]
    ```

2. *`PTT_KCM_API/api/ip/?issue=<>`*  
  取得特定主題文章的參與者他們的`IP`與對議題的`支持程度`：
  * 範例：`/PTT_KCM_API/api/ip/?issue=燈迷`
  * result：

    ```
    {
      "attendee": [
        {
          "ip": '140.120.4.13',
          "push_userid": "WTF55665566",
          "score": -1,
          "push_ipdatetime": "08/23 09:19"
        },
        {
          "ip": null,
          "push_userid": "vyjssm",
          "score": 0,
          "push_ipdatetime": "08/23 09:34"
        },
      ],
      "author": [
        {
          "ip": "122.116.198.5",
          "date": "Tue Aug 23 09:18:26 2016",
          "author": "fashionjack (神奇傑克)",
          "score": -1.0
        }
      ],
      "issue": "燈迷"
    }
    ```

3. *`PTT_KCM_API/api/locations/?issue=<>`*   
取得特定主題文章的參與者其`地理位置`與對議題的`支持程度`：
  * 範例：`/PTT_KCM_API/api/ip/?issue=燈迷`
  * result：

    ```
        {
      "map": {
        "Taiwan": {
          "Taipei": {
            "attendee": 664,
            "positive": 428.34357561722715,
            "negative": -166.3100122100122
          },
          "Kaohsiung": {
            "attendee": 89,
            "positive": 59.07366233697503,
            "negative": -22.174242424242426
          },
          "Taitung": {
            "attendee": 1,
            "positive": 0,
            "negative": -1
          }
          ...
        }
      }
    }
    ```







## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisities

1. OS：Ubuntu / OSX would be nice
2. environment：need python3 `sudo apt-get update; sudo apt-get install; python3 python3-dev`
3. 使用虛擬環境去安裝本套件 ( recommended ) ：`pip install virtualenv`
  * 建立虛擬環境，取名叫作venv：`virtualenv venv`
  *  啟動虛擬環境，這樣套件就會裝在目錄底下的venv資料夾：`. venv/bin/activate`

### Installing

`pip install -r requirements.txt`


## Running & Testing

## Run

1. 初次啟動需要先爬PTT資料：
  * `python manage.py crawler 看板名稱 起始索引 結束索引 (設為 -1 則自動計算最後一頁)`
  * `python manage.py insertArticles ./XXX.json`：把載下來的PTT匯入到mongodb
    * optional args: `--append True` 每次插入文章都會把mongoDB清空，--append則不會清空
2. （For windows）請將/PTT_KCM_API/venv/lib/python3.4/site-packages/mysql/connector/django/operations.py內的def bulk_insert_sql修改成
```
def bulk_insert_sql(self, fields, placeholder_rows):
    """
    Format the SQL for bulk insert
    """
    placeholder_rows_sql = (", ".join(row) for row in placeholder_rows)
    values_sql = ", ".join("(%s)" % sql for sql in placeholder_rows_sql)
    return "VALUES " + values_sql
```
3. 建立並寫入 model 到 mysql 資料庫 :
  * `python manage.py makemigrations`
  * `python manage.py migrate`
4. 將PTT文章內的發文者IP匯入資料庫 : `python manage.py buildIP`
5. 透過 `PTT_KCM_API/management/commands/issue.txt` 裏面的名詞去做查詢，並在伺服器建立 cache : `python manage.py cache`
6. 啟動django專案：`./manage.py runserver`
7. 開啟瀏覽器，檢查一下API是否正常產出json資料

### Break down into end to end tests

1. 先插入測試用文集(注意：此舉會先清空本地端的MongoDB)：`python manage.py insertArticles testData testData/Hate-1000-1001.json`
2. run test：`python manage.py test`

### And coding style tests

目前沒有coding style tests...

## Deployment


目前只是一般的 **django** 程式，使用gunicorn或者uwsgi佈署即可

## Built With

* Django 1.10.2
* python3.5

## Versioning

For the versions available, see the [tags on this repository](https://github.com/david30907d/KCM/releases).

## Contributors

* **張泰瑋** [david](https://github.com/david30907d)

## License

This project is licensed under the **GNU 3.0** License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* 感謝 **jwline** 實作的[PTT爬蟲](https://github.com/jwlin/ptt-web-crawler)
