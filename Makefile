install:
	- git clone https://github.com/UDICatNCHU/ptt-web-crawler.git; cd ptt-web-crawler; pip install -r requirements.txt
	- pip install -r requirements.txt

test:
	- cd ptt-web-crawler; python test.py