install:
	- git clone https://github.com/UDICatNCHU/ptt-web-crawler.git; cd ptt-web-crawler; pip install -r requirements.txt
	- pip install -r requirements.txt

test:
	- python manage.py test --setting=project.settings_test
	- cd ptt-web-crawler; python test.py

firstRunCrawler:
	# 把政黑版的文章爬完
	- cd ptt-web-crawler; python crawler.py -b HatePolitics -i 1 3499

trigger_cache:
	- cd PTT_KCM_API/init/;python trigger_cache.py