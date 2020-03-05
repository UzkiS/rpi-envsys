<?php
$address = '127.0.0.1';
$port = 16868;
$sock = socket_create(AF_INET, SOCK_STREAM, 0);


$msg = 'getWeather';
if (socket_connect($sock, $address, $port)) {
    socket_send($sock, $msg, strlen($msg), 0);
    socket_recv($sock, $buf, 5120, MSG_WAITALL);
} else {
    $buf = '-1';
};
socket_close($sock);
echo $buf;