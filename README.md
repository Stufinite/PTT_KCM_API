# PTT_KCM_API (使用KCM當作PTT文章查詢索引的API)[![Build Status](https://travis-ci.org/UDICatNCHU/PTT_KCM_API.svg?branch=master)](https://travis-ci.org/UDICatNCHU/PTT_KCM_API)

使用 **jwline** 實作的[PTT爬蟲](https://github.com/jwlin/ptt-web-crawler)

實作初一個可以用get協定去查詢的API，若關鍵字不存在

則使用KCM找出最相關的字去做查詢

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
git clone https://david30907d@bitbucket.org/udiclab/term_classification.git
make install
```


## Running & Testing

## Run


1. 初次啟動需要先爬PTT資料：`make firstRunCrawler`
2. 啟動django專案：`./manage.py runserver`
3. 開啟瀏覽器，輸入： `127.0.0.1:8000/PTT_KCM_API/api/ip/?issue={想要查詢的關鍵字}`
4. EX：[連結](http://127.0.0.1:8000/PTT_KCM_API/api/ip/?issue=光復節)

### Break down into end to end tests


1. 執行全部的測試：`make test`
2. 分別測試：
  * 測試ptt爬蟲：`cd ptt-web-crawler; python test.py`
  * 測試PTT_KCM_API：**尚無**

### And coding style tests

目前沒有coding style tests...

### Results

```
[
  {
    "article_id": "M.1477366093.A.CF0",
    "article_title": "[討論] 今天是台灣光復節&古寧頭戰役紀念日",
    "author": "McCain (長髮馬尾控)",
    "board": "HatePolitics",
    "content": "今天是台灣光復節 各位有放假嗎? 自從進入職場之後 今天我是第一次在非周末的情況下 還能放到這個節日 不過應該也是唯一的一次了 因為不久後就要修法 ...2004 2010 R McCain 1505372 77% McCain 1005615 59% D Starky 404507 20% Glassman 592011 35% L Hancock 51798 3% Libertarian 80097 5% ",
    "date": "Tue Oct 25 11:28:08 2016",
    "ip": "114.45.182.54",
    "message_conut": {
      "all": 10,
      "boo": 0,
      "count": 5,
      "neutral": 5,
      "push": 5
    },
    "messages": [
      {
        "push_content": "光復節? 這個詞其實蠻多爭議的",
        "push_ipdatetime": "10/25 11:33",
        "push_tag": "→",
        "push_userid": "Antler5566"
      },
      ...
    ]
  },
```

## Deployment


目前只是一般的 **django** 程式，使用gunicorn或者uwsgi佈署即可

## Built With

* python3.2
* python3.3
* python3.4
* python3.5

## Versioning

For the versions available, see the [tags on this repository](https://github.com/david30907d/KCM/releases).

## Contributors

* **張泰瑋** [david](https://github.com/david30907d)

## License

This project is licensed under the **GNU 3.0** License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* 感謝 **jwline** 實作的[PTT爬蟲](https://github.com/jwlin/ptt-web-crawler)
