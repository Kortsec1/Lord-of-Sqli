# chupacabra

## 1. Code
```php
<?php
  include "./config.php";
  login_chk();
  $db = sqlite_open("./db/chupacabra.db");
  $query = "select id from member where id='{$_GET[id]}' and pw='{$_GET[pw]}'";
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  $result = sqlite_fetch_array(sqlite_query($db,$query));
  if($result['id'] == "admin") solve("chupacabra");
  highlight_file(__FILE__);
?>
```

## 2. Condition
- sqlite를 사용한다.   
- 별다른 방어책이 없다.   

## 3. Solution
sqlite로 바뀐것을 제외하곤, 유심히 볼 것이 없다.   

공격 코드는 다음과 같다.   

변수명 | 값
---|---:
`pw` | ' or id='admin