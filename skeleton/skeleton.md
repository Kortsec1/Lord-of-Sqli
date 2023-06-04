# skeleton

## 1. Code
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  $db = dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  $query = "select id from prob_skeleton where id='guest' and pw='{$_GET[pw]}' and 1=0"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysqli_fetch_array(mysqli_query($db,$query)); 
  if($result['id'] == 'admin') solve("skeleton"); 
  highlight_file(__FILE__); 
?>
```

## 2. Condition
- query의 조건문 속 거짓값, `1=0`이 들어있다.

## 3. Solution
주석을 이용하여 `and 1=0`부분을 없애면 해결되는 문제이다.

변수명 | 값
---|:---:
`id` | 1234' or id='admin' #
