<?php
function get_client_ip() {
    if ($_SERVER['REMOTE_ADDR']) {
        $cip = $_SERVER['REMOTE_ADDR'];
    } elseif (getenv("REMOTE_ADDR")) {
        $cip = getenv("REMOTE_ADDR");
    } elseif (getenv("HTTP_CLIENT_IP")) {
        $cip = getenv("HTTP_CLIENT_IP");
    } else {
        $cip = "unknown";
    }
    return $cip;
}

switch ($_GET['mode'])
{
    case 'ip':
        echo get_client_ip();
        break;
    case 'reload':
        shell_exec('sudo reboot');
        break;
    case 'reboot':
        shell_exec('sudo reboot');
        break;  
    case 'poweroff':
        shell_exec('sudo poweroff');
        break;
}
?>
