<?php
$address = '127.0.0.1';
$port = 16868;
$sock = socket_create(AF_INET, SOCK_STREAM, 0);
if(socket_connect($sock, $address, $port)){
    $msg = 'getAllSensorDataWithStatus';
    socket_send ($sock , $msg , strlen($msg) , 0) ;
    // socket_write($sock,$msg);
    socket_recv ($sock , $buf , 5120 , MSG_WAITALL );




    // socket_send($sock, $msg, strlen($msg), MSG_DONTROUTE);
    // socket_write($sock,$msg);
    // socket_recv ($sock , $buf , 1024 , MSG_WAITALL );
} else{
    $buf='-1';
};
socket_close($sock);
echo $buf;
?>