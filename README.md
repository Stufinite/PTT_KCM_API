# PTT_KCM_API (ʹ��KCM����PTT���²�ԃ������API)[![Build Status](https://travis-ci.org/UDICatNCHU/PTT_KCM_API.svg?branch=master)](https://travis-ci.org/UDICatNCHU/PTT_KCM_API)

ʹ�� **jwline** ������[PTT���x](https://github.com/jwlin/ptt-web-crawler)

������һ��������get�f��ȥ��ԃ��API�����P�I�ֲ�����

�tʹ��KCM�ҳ������P����ȥ����ԃ

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisities

1. OS��Ubuntu / OSX would be nice
2. environment��need python3 `sudo apt-get update; sudo apt-get install; python3 python3-dev`
3. ʹ��̓�M�h��ȥ���b���׼� ( recommended ) ��`pip install virtualenv`
  * ����̓�M�h����ȡ������venv��`virtualenv venv`
  *  ����̓�M�h�����@���׼��͕��b��Ŀ䛵��µ�venv�Y�ϊA��`. venv/bin/activate`

### Installing

```
git clone https://github.com/UDICatNCHU/PTT_KCM_API.git
make install
```


## Running & Testing

## Run


1. ���Ά�����Ҫ����PTT�Y�ϣ�`make firstRunCrawler`
2. ����django������`./manage.py runserver`
3. �_���g�[����ݔ�룺 `http://127.0.0.1:8000/PTT_KCM_API/build_IpTable/`
  * ����Ptt�Ñ��c�l�ĵ�IP���ձ�
4. �_���g�[�����z��һ��API�Ƿ������a��json�Y��

### Break down into end to end tests


1. ����ȫ���Ĝyԇ��`make test`
2. �քe�yԇ��
  * �yԇptt���x��`cd ptt-web-crawler; python test.py`
  * �yԇPTT_KCM_API��**�Пo**

### And coding style tests

Ŀǰ�]��coding style tests...

### API usage and Results

APIʹ�÷�ʽ��������������api��URL pattern����

1. ȡ���ض����}��PTT���£� `PTT_KCM_API/api/articles/?issue={���}���Q}`
  * ������`PTT_KCM_API/api/articles/?issue=��͹�`
  * reeulst��
    ```
    [
      {
        "article_id": "M.1477366093.A.CF0",
        "article_title": "[ӑՓ] ������̨����͹�&�Ō��^���ۼo����",
        "author": "McCain (�L��Rβ��)",
        "board": "HatePolitics",
        "content": "������̨����͹� ��λ�зżن�?...",
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
            "push_content": "��͹�? �@���~�䌍�U�ࠎ�h��",
            "push_ipdatetime": "10/25 11:33",
            "push_tag": "��",
            "push_userid": "Antler5566"
          },
          ...
        ]
      },
    ```

2. ȡ���ض����}���µą��c��������IP�c���h�}��֧�̶ֳȣ�`PTT_KCM_API/api/ip/?issue={���}���Q}`
  * ������`/PTT_KCM_API/api/ip/?issue=��͹�`
  * result��
    ```
    {
      "issue": "��͹�",
      "author": [
        {
          "date": "Tue Oct 25 11:28:08 2016",
          "author": "McCain (�L��Rβ��)",
          "ip": "114.45.182.54",
          "score": -1
        },
        ...
      ]
      "attendee": [
        {
          "push_userid": "Antler5566",
          "score": 1,
          "ip": "140.120.4.13",
          "push_ipdatetime": "10/25 11:33"
        }
        ...
      ],
    }
    ```

## Deployment


Ŀǰֻ��һ��� **django** ��ʽ��ʹ��gunicorn����uwsgi���𼴿�

## Built With

* Django 1.10.2
* python3.5

## Versioning

For the versions available, see the [tags on this repository](https://github.com/david30907d/KCM/releases).

## Contributors

* **��̩�|** [david](https://github.com/david30907d)

## License

This project is licensed under the **GNU 3.0** License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* ���x **jwline** ������[PTT���x](https://github.com/jwlin/ptt-web-crawler)
