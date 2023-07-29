# manticore

## 1. Code
```php
<?php
  include "./config.php";
  login_chk();
  $db = sqlite_open("./db/manticore.db");
  $_GET['id'] = addslashes($_GET['id']);
  $_GET['pw'] = addslashes($_GET['pw']);
  $query = "select id from member where id='{$_GET[id]}' and pw='{$_GET[pw]}'";
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  $result = sqlite_fetch_array(sqlite_query($db,$query));
  if($result['id'] == "admin") solve("manticore");
  highlight_file(__FILE__);
?>
```

## 2. Condition
- mysql이 아닌, sqlite를 이용한다.   
- get 파라미터, id와 pw가 addslashes 함수를 거친다.   
- 쿼리 결과의 id값이 'admin'이라면 문제가 해결된다.   

## 3. Solution
sqlite에 대한 사소한 배경지식이 있다면, 어렵지 않게 해결할 수 있는 문제였다.   




중요한 특징은 다음과 같다.   
- sqlite는 `\`를 escape 문자로 취급하지 않는다.   
- 주석은 `-- `와 `/**/`를 사용한다.   



backslash 이슈는 아래 문서를 확인해 보면 알 수 있다.   
https://www.sqlite.org/lang_expr.html
```
C-style escapes using the backslash character are not supported because they are not standard SQL
```   


그렇다면 addslashes 함수를 신경쓰지 않고, 그대로 진행시키면 된다.   

변수명 | 값
---|---:
`pw` | ' or id = char(97,100,109,105,110)-- 