# PTT_KCM_API (使用KCM當作PTT文章查詢索引的API)[![Build Status](https://travis-ci.org/UDICatNCHU/PTT_KCM_API.svg?branch=master)](https://travis-ci.org/UDICatNCHU/PTT_KCM_API)

使用 **jwline** 實作的[PTT爬蟲](https://github.com/jwlin/ptt-web-crawler)  
實作初一個可以用get協定去查詢的API，若關鍵字不存在  
則使用KCM（實作中）找出最相關的字去做查詢

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

```
git clone https://github.com/UDICatNCHU/PTT_KCM_API.git
make install
```


## Running & Testing

## Run


1. 初次啟動需要先爬PTT資料：`make firstRunCrawler`
  * `python manage.py insertArticles`：把載下來的PTT匯入到mongodb
2. `翔宇`：這邊給你補充步驟，理論上執行 `python manage.py buildIP` 就會把IP通通都匯進去，不過目前好像怪怪的
3. `翔宇`：這邊給你補充步驟，理論上執行 `python manage.py cache` 就會透過 `PTT_KCM_API/management/commands/issue.txt` 裏面的名詞去做查詢，並且在伺服器建立 cache。
4. 啟動django專案：`./manage.py runserver`
5. 開啟瀏覽器，檢查一下API是否正常產出json資料

### Break down into end to end tests


1. 執行全部的測試：`make test`
2. 分別測試：
  * 測試ptt爬蟲：`cd ptt-web-crawler; python test.py`
  * 測試PTT_KCM_API：`python manage.py test --setting=project.settings_test
`

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
