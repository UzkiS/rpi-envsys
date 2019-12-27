<?php
$address = '127.0.0.1';
$port = 16868;
$sock = socket_create(AF_INET, SOCK_STREAM, 0);
if(socket_connect($sock, $address, $port)){
    socket_recv ($sock , $buf , 1024 , MSG_WAITALL );
} else{
    $buf='0';
};
echo $buf
?>