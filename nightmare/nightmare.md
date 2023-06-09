# nightmare

## 1. Code
```php
<?php 
  include "./config.php"; 
  login_chk(); 
  $db = dbconnect(); 
  if(preg_match('/prob|_|\.|\(\)|#|-/i', $_GET[pw])) exit("No Hack ~_~"); 
  if(strlen($_GET[pw])>6) exit("No Hack ~_~"); 
  $query = "select id from prob_nightmare where pw=('{$_GET[pw]}') and id!='admin'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysqli_fetch_array(mysqli_query($db,$query)); 
  if($result['id']) solve("nightmare"); 
  highlight_file(__FILE__); 
?>
```

## 2. Condition
- `prob`, `_`, `.`, `()`, `#`, `-`등을 필터링한다.
- `strlen`함수를 통해, 파라미터 `pw`의 길이를 6까지 제한한다.


## 3. Solution

sql에서 문자와 숫자의 비교는 문자&rarr;숫자 형변환 이후에 이루어 진다.<br>
여기서 문자열에 값이 없다면 0으로 형변환되는데, 이를 이용한다.


변수명 | 값
---|---:
`pw` | `')=0;%00`



`#`과 `-`가 필터링 되어 `;%00`를 통해 주석처리 해주었다.
이렇게 되면, 길이도 6으로 딱이다.