<?php

/**
 * @descGet system run time value script
 */
// $arRuntime =explode(",  ", exec('uptime'));
// echo $arRuntime[2];
$data = json_decode(shell_exec('ip -4 -j a'), TRUE);
$ip = array();
$count = 0;
foreach ($data as $dataItem) {

  // var_dump($v['addr_info'][0]['local']);
  $ipAddr = $dataItem['addr_info'][0]['local'];
  $ipHead = substr($ipAddr, 0, 3);
  // $ip[$count] = $dataItem['addr_info'][0]['local'];
  if ($ipHead != '169') {
    $ip[$count] = $ipAddr;
    $count++;
  }

  // foreach($v as $b){
  //     var_dump($b);
  //     echo '==============';
  // }
}
//   var_dump($ip);
echo json_encode($ip);
    // var_dump($data);
    // echo shell_exec('ip -4 -j a');
