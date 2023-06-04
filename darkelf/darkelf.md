# darkelf

## 1. Code
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  $db = dbconnect();  
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  if(preg_match('/or|and/i', $_GET[pw])) exit("HeHe"); 
  $query = "select id from prob_darkelf where id='guest' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysqli_fetch_array(mysqli_query($db,$query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
  if($result['id'] == 'admin') solve("darkelf"); 
  highlight_file(__FILE__); 
?>
```

## 2. Condition
- `or`, `and`를 필터링 한다.

## 3. Solution
`or`, `and` 연산자 우회를 통해 문제를 해결할 수 있다.



변수명 | 값
---|:---:
`pw` | 1234' || id='admin



`or`과 `and`는 각각 `||`, `&&`로 우회해 주면 된다.