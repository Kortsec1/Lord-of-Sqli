# succubus

## 1. Code
```php
<?php
  include "./config.php"; 
  login_chk();
  $db = dbconnect();
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~"); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");
  if(preg_match('/\'/',$_GET[id])) exit("HeHe");
  if(preg_match('/\'/',$_GET[pw])) exit("HeHe");
  $query = "select id from prob_succubus where id='{$_GET[id]}' and pw='{$_GET[pw]}'"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysqli_fetch_array(mysqli_query($db,$query)); 
  if($result['id']) solve("succubus"); 
  highlight_file(__FILE__); 
?>
```

## 2. Condition
- 작은 따옴표 `'`를 필터링 한다.
- 쿼리문에서, GET 파라미터 `id`와 `pw`는 작은 따옴표로 덮여있다.

## 3. Solution
`and pw='{$_GET[pw]}'` 부분을 무시하기 위해 앞의 `id='{$_GET[id]}'`와 묶어서 해결하였다.

GET 파라미터 `id`에 `\`를 넣어줌 으로서, `{$_GET[id]}' and pw=` 부분즉,<br>
다음번에 오는 작은따옴표까지가 쿼리문의 id로 인식되게 된다.
&rarr; 두 번쨰 따옴표는 이스케이프 `\`로 인해 문자취급된다.


이후, GET 파라미터 pw에 참 값을 넣어주면 결과적으로 DB에서 id를 가져오게 된다.


변수명 | 값
---|---:
`id` | `\`
`pw` | ` or 1=1#`


