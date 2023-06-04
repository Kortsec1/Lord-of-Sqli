# vampire

## 1. Code
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  $db = dbconnect(); 
  if(preg_match('/\'/i', $_GET[id])) exit("No Hack ~_~");
  $_GET[id] = strtolower($_GET[id]);
  $_GET[id] = str_replace("admin","",$_GET[id]); 
  $query = "select id from prob_vampire where id='{$_GET[id]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysqli_fetch_array(mysqli_query($db,$query)); 
  if($result['id'] == 'admin') solve("vampire"); 
  highlight_file(__FILE__); 
?>
```

## 2. Condition
- 입력받은 id값을 소문자로 변환 한다.
- 입력받은 id값속 'admin'문자열을 ''으로 교체한다.

## 3. Solution
GET 파라미터에 'admin'만을 전달하면 풀리는 간단한 문제이다.

`admin`속에 또 하나의 `admin`을 집어 넣으면 해결된다.<br>
&rarr; ad`admin`min


변수명 | 값
---|:---:
`id` | adadminmin


약간의 센스가 필요한 문제였다.
