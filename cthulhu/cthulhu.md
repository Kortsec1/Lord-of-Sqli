# cthulhu

## 1. Code
```php
<?php
  include "./welcome.php";
  include "./config.php";
  login_chk();
  $db = dbconnect();
  if(preg_match('/prob|_|\.|\(\)|admin/i', $_GET[id])) exit("No Hack ~_~");
  if(preg_match('/prob|_|\.|\(\)|admin/i', $_GET[pw])) exit("No Hack ~_~");
  $query = "select id from prob_cthulhu where id='{$_GET[id]}' and pw='{$_GET[pw]}'";
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  $result = @mysqli_fetch_array(mysqli_query($db,$query));
  if($result['id']) solve("cthulhu");
  highlight_file(__FILE__);
?>
```

## 2. Condition
- 상단에 다음과 같은 메세지가 떠있다.   
>    modsec.rubiya.kr server is running ModSecurity Core Rule Set v3.1.0 with paranoia level 1(default).
It is the latest version now.(2019.05)
Can you bypass the WAF?
- `prob _ . () admin`을 필터링 한다.   
- 쿼리가 실행되어, id값이 불러진다면 문제가 해결된다.   

## 3. Solution   

웹방화벽(WAF)을 우회하는 문제이다.   
상세 버전과 정보는 위에 나와있듯이 `ModSecurity Core Rule Set v3.1.0 (level 1)`이다.   

구글링을 통해 해당 버전의 취약점을 찾아보았다.   
https://github.com/SpiderLabs/owasp-modsecurity-crs/issues/1181   

``{`a`b}``을 이용한다.   
backtick속 `a`에는 특정 함수 이름, `b`에는 실행된 sql구문이 들어간다.   

실제로, ``pw=1' or {`if`1}%23``를 입력하면 문제가 해결된다.   

변수 | 값
---|---
pw | ``1' or {`if`1}%23``