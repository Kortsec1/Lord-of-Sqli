# zombie_assassin

## 1. Code
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  $db = dbconnect();
  $_GET['id'] = strrev(addslashes($_GET['id']));
  $_GET['pw'] = strrev(addslashes($_GET['pw']));
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~"); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  $query = "select id from prob_zombie_assassin where id='{$_GET[id]}' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysqli_fetch_array(mysqli_query($db,$query)); 
  if($result['id']) solve("zombie_assassin"); 
  highlight_file(__FILE__); 
?>
```

## 2. Condition
- GET 파라미터 `id`와 `pw`를 `strrev`, `addslashes`함수를 거치게 한다.

함수명 | 설명
---|---
`strrev` | 문자열을 뒤집는 함수.
`addslashes` | `'`, `"`, `공백`, `\`등앞에 백슬래쉬`\`를 붙여 문자취급 이스케이핑을 시키는 함수.


## 3. Solution

`"`가 `addslashes`함수를 거치면 앞에 백슬래쉬 `\`(%5c)가 붙게된다.<br>
즉, `"` &rarr; `\"`인 것이다.


하지만, `strrev`함수를 거치면서 `\"`는 `"\`로 바뀌게 된다. (...?)
`addslashes`가 친절하게 붙여준 `\`는 쿼리문속 id 정상 따옴표를 문자로 만들어버린다.


이후, `pw`값에 참을 뒤집어 넣어주면 문제가 해결된다.


변수명 | 값
---|---:
`id` | `"`
`pw` | `#1=1 ro`


