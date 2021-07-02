<?php
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);
$link = mysqli_connect("localhost", "root", "password", "rocket_news");
if ($link == false){
    print("Ошибка: Невозможно подключиться к MySQL <br>" . mysqli_connect_error());
}
else {
    print("Соединение установлено успешно <br>");
}
//mysqli_set_charset($con, "utf8");
$sql = 'SELECT title FROM news WHERE author = "Иванов И.И."';
$result = mysqli_query($link, $sql);
$rows = mysqli_fetch_all($result, MYSQLI_ASSOC);

foreach ($rows as $row) {
    print("Заголовок: " . $row['title']. "<br>");
}
?>