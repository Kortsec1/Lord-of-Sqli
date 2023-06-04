# troll

## 1. Code
```php
<?php  
  include "./config.php"; 
  login_chk(); 
  $db = dbconnect(); 
  if(preg_match('/\'/i', $_GET[id])) exit("No Hack ~_~");
  if(preg_match("/admin/", $_GET[id])) exit("HeHe");
  $query = "select id from prob_troll where id='{$_GET[id]}'";
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  $result = @mysqli_fetch_array(mysqli_query($db,$query));
  if($result['id'] == 'admin') solve("troll");
  highlight_file(__FILE__);
?>
```

## 2. Condition
- 'admin'을 필터링 한다.

## 3. Solution
GET 파라미터에 'admin'만을 전달하면 풀리는 간단한 문제이다.

필터링 구문 속 정규표현식 `/admin/`을 보면 마지막에 i가 없는것을 볼 수 있다.<br>
이는 대소문자를 구분한다는 의미이다.

하지만, 기본적으로 mysql은 대소문자를 구분하지 않는다.<br>
&rarr; 정확히는 정렬값이 같은 문자는 같은 문자로 취급한다.   ex. ä=a
```
mysql> select * from user where id='adMIn';
+----+-------+---------+
| no | id    | pw      |
+----+-------+---------+
|  2 | admin | 1711697 |
+----+-------+---------+
1 row in set (0.00 sec)
```

`adMin`, `AdMin`, `Admin`과 같은 방법으로 대문자를 섞어서 보낸다면<br>
php에서는 필터링에 걸리지 않지만 mysql에서는 대소문자 상관없이 처리된다.

변수명 | 값
---|:---:
`id` | Admin
