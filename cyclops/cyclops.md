# cyclops

## 1. Code
```php
<?php
  include "./config.php";
  login_chk();
  $db = dbconnect();
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~");
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");
  $query = "select id,pw from prob_cyclops where id='{$_GET[id]}' and pw='{$_GET[pw]}'";
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  $result = @mysqli_fetch_array(mysqli_query($db,$query));
  if(($result['id'] === "first") && ($result['pw'] === "second")) solve("cyclops");//must use union select
  highlight_file(__FILE__);
?>
```

## 2. Condition
- `prob _ . ( )`를 필터링 한다.
- 이전 문제들과 같이 웹 방화벽이 존재한다.

## 3. Solution
구글링을 통해 우회법을 찾아 해결하였다.   
https://github.com/SpiderLabs/owasp-modsecurity-crs/issues/1181   


위 참고링크에서 볼 수 있듯이 `<@`를 이용하여 문제를 해결하였다.   
공격 코드는 다음과 같다.   

변수명 | 값
---|---:
`pw` | ' <@ union/**/select 'first','second



`<@`이 무슨 역할인지는 다음을 참고했다.   
https://stackoverflow.com/questions/36985926/what-does-the-operator-in-postgres-do   


그 뒤, union select 사이에 주석 /**/을 통해 우회를 해주었다.   