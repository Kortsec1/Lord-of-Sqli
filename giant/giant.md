# giant

## 1. Code
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  $db = dbconnect(); 
  if(strlen($_GET[shit])>1) exit("No Hack ~_~"); 
  if(preg_match('/ |\n|\r|\t/i', $_GET[shit])) exit("HeHe"); 
  $query = "select 1234 from{$_GET[shit]}prob_giant where 1"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysqli_fetch_array(mysqli_query($db,$query)); 
  if($result[1234]) solve("giant"); 
  highlight_file(__FILE__); 
?>
```

## 2. Condition
- GET 파라미터 shit을 받아온다.
- 공백, 개행, 캐리지 리턴, 탭 등을 필터링한다.

## 3. Solution
query를 정상 실행하려면, GET 파라미터 shit에 공백을 입력해야한다.
&rarr; 공백우회 문제.


변수명 | 값
---|---:
`shit` | `%0b`


`%0b`를 통해 공백으로 인식시킬 수 있다.