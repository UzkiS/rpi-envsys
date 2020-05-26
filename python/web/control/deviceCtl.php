<?php
function get_client_ip()
{
    $data = json_decode(shell_exec('ip -4 -j a'), TRUE);
    $ip = array();
    $count = 0;
    foreach ($data as $dataItem) {
        $ipAddr = $dataItem['addr_info'][0]['local'];
        $ipHead = substr($ipAddr, 0, 3);
        if ($ipHead != '169' & $ipHead != '127') {
            $ip[$count] = $ipAddr;
            $count++;
        }
    }
    return json_encode($ip);
}
// $_SERVER['SERVER_NAME'] 
switch ($_GET['mode']) {
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
