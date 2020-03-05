<?php
$shellCmd = array(
    'cpuTemp' => 'cat /sys/class/thermal/thermal_zone0/temp | awk \'{print $1/1000}\'',
    'memUsed' => 'free | awk \'/Mem/\' | awk \'{print $3/$2*100}\'',
    'sysUpTime' => 'cat /proc/uptime| awk -F. \'{run_days=$1 / 86400;run_hour=($1 % 86400)/3600;run_minute=($1 % 3600)/60;run_second=$1 % 60;printf("%d天%d时%d分%d秒",run_days,run_hour,run_minute,run_second)}\''
);

function getShellData($shellCmd)
{
    return shell_exec($shellCmd);
}
// $cpuTemp = shell_exec(); 
// $memUsed = shell_exec();
// $sysUpTime = shell_exec();
foreach ($shellCmd as $key => $value) {
    $arr[$key] = getShellData($value);
}

echo json_encode($arr);
