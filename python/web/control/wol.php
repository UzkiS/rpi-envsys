<?php
class MyDB extends SQLite3
{
    function __construct()
    {
        $this->open('../envsys.db');
    }
}
function add(){
    $mac = $_GET['mac'];
    $name = $_GET['name'];

    $db = new MyDB();
    if(!$db){
       echo $db->lastErrorMsg();
    } else {
    //    echo "Opened database successfully\n";
    }
    $sql =  "INSERT INTO wol (name, mac) VALUES ('".$name."','".$mac."');";
    echo $sql;
    // die;
    $ret = $db->exec($sql);
    if(!$ret){
       echo $db->lastErrorMsg();
    } else {
    //    echo "Records created successfully\n";
    }
    $db->close();
}
function listItem(){
    $db = new MyDB();
    if(!$db){
       echo $db->lastErrorMsg();
    } else {
    //    echo "Opened database successfully\n";
    }
 
    $sql = "SELECT * from wol;";
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

function del(){
    $uid = $_GET['uid'];
    $db = new MyDB();
    if(!$db){
       echo $db->lastErrorMsg();
    } else {
    //    echo "Opened database successfully\n";
    }
 
    $sql = "DELETE from wol where uid=".$uid.";";
    $ret = $db->exec($sql);
    if(!$ret){
      echo $db->lastErrorMsg();
    } else {
    //    echo $db->changes(), " Record deleted successfully\n";
    }
}

function boot(){
    $mac = $_GET['mac'];
    // echo $mac;
    $rst='';
    $p = array("1", "3", "5", "7", "9");
    for ($i=0; $i < strlen($mac) ; $i++) {
        
        $rst.=$mac[$i];
        if(in_array($i, $p)){
            $rst.=":";
        }
    }
    $cmd = "wakeonlan ".$rst;
    echo $cmd;
    shell_exec($cmd);
}

switch ($_GET['mode']) {
    case 'add':
        add();
        break;
    case 'del':
        del();
        break;
    case 'list':
        listItem();
        break;
    case 'boot':
        boot();
        break;
}
