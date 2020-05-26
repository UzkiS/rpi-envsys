<?php
class MyDB extends SQLite3
{
    function __construct()
    {
        $this->open('../envsys.db');
    }
}

function listItem(){
    $db = new MyDB();
    if(!$db){
       echo $db->lastErrorMsg();
    } else {
    //    echo "Opened database successfully\n";
    }
    
    $sql = "SELECT uid, lowVar, highVar, method, alarmMode, cname, useEmail, useWatcher, recVal from sensor;";
    $rst=[];
    $i=0;
    $ret = $db->query($sql);
    while($row = $ret->fetchArray(SQLITE3_ASSOC) ){
        $rst[$i]=$row;
        $i++;
        // var_dump($row);
    //    die;
    }
    // var_dump($rst);
    echo json_encode($rst);
    // echo "Operation done successfully\n";
    $db->close();
}

function save()
{
    $data=json_decode($_GET['data'], true);
    $db = new MyDB();
    if(!$db){
        echo $db->lastErrorMsg();
     } else {
     //    echo "Opened database successfully\n";
     }
    //  {"uid":2,"lowVar":16,"highVar":32,"method":0,"alarmMode":0,"cname":"温度","useEmail":0,"useWatcher":1,"recVal":5}
    $sql = "UPDATE sensor set lowVar = ". $data['lowVar'] .", highVar = ". $data['highVar'] .", useEmail = ". $data['useEmail'] .", useWatcher = ". $data['useWatcher'] .", recVal = ". $data['recVal'] ." where uid = ". $data['uid'] .";";
    $ret = $db->exec($sql);
    if(!$ret){
       echo $db->lastErrorMsg();
    } else {
    //    echo $db->changes(), " Record updated successfully\n";
    }
    $db->close();
}

switch ($_GET['mode']) {
    case 'save':
        save();
        break;
    case 'list':
        listItem();
        break;
}