<?php

function get_conf_arr($src)
{
    $f_src = $src;
    $f = fopen($f_src, 'r');
    $size = filesize($f_src);
    // if ($size <= 1) {
    //     return [];
    // }
    $f_rst = explode("\n\n", fread($f, $size));
    fclose($f);
    $rst_arr = [];
    foreach ($f_rst as $x) {
        $mkey="";
        $conf_rst = explode("\n", $x);
        // var_dump($conf_rst);
        // die;
        if (count($conf_rst) != 1) {
            foreach ($conf_rst as $line) {
                $conf_rst_line = explode("=", $line);
                if(substr($conf_rst_line[0],0,1) == "#" or $conf_rst_line[0] == ""){
                    
                }elseif ($conf_rst_line[1] == NULL and substr($conf_rst_line[0],0,1)=="[" and  substr($conf_rst_line[0],-1)=="]"){
                    $mkey=substr($conf_rst_line[0],1,-1);
                }else{
                        $rst_arr[$mkey][trim($conf_rst_line[0])] = trim($conf_rst_line[1]);
                }
            }
        }
        // echo json_encode($rst_arr) ;
        // die;
    }
    
    return json_encode($rst_arr) ;
}

function write_conf($arr, $src)
{
    // var_dump($arr);
    $f_src = $src;
    $f = fopen($f_src, 'w');
    $arr=json_decode($arr);
    // echo $arr;
    // die;
    foreach ($arr as $key => $val) {
        // echo "[" . $key . "]</br>";
        // die;
        fwrite($f, "[" . $key . "]\n");
        foreach ($val as $k => $v) {
            // echo $k." = ".$v."</br>";
            fwrite($f, $k . " = " . $v . "\n");
            // echo $key;
        }
        fwrite($f, "\n");
    }
    fclose($f);
}

$src='../../config.conf';
switch ($_GET['mode']) {
    case 'list':
        echo get_conf_arr($src);
        break;
    case 'save':
        write_conf($_GET['conf'],$src);
        break;
}

// write_conf(get_conf_arr($src),'../../a.conf');