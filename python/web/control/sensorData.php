<?php
$address = '127.0.0.1';
$port = 16868;
$sock = socket_create(AF_INET, SOCK_STREAM, 0);

switch ($_GET['mode']) {
    case 'data':
        $msg = 'getAllSensorDataWithStatus';
        if (socket_connect($sock, $address, $port)) {
            socket_send($sock, $msg, strlen($msg), 0);
            socket_recv($sock, $buf, 5120, MSG_WAITALL);
        } else {
            $buf = '-1';
        };
        socket_close($sock);
        echo $buf;
        break;
    case 'status':
        $msg = 'getDefaultSensorStatus';
        if (socket_connect($sock, $address, $port)) {
            socket_send($sock, $msg, strlen($msg), 0);
            socket_recv($sock, $buf, 5120, MSG_WAITALL);
        } else {
            $buf = '-1';
        };
        socket_close($sock);

        $data = json_decode($buf, TRUE);
        class MyDB extends SQLite3
        {
            function __construct()
            {
                $this->open('../envsys.db');
            }
        }
        $db = new MyDB();
        if (!$db) {
            echo $db->lastErrorMsg();
        } else {
            // echo "Opened database successfully\n";
        }
        $count = 0;
        foreach ($data as $key => $status) {
            // 下面为0
            if ($status > 0) {
                $count = $count + 1;
                $sql = 'SELECT cname, suggest from sensor WHERE name = "' . $key . '"';


                // echo $sql;
                $ret = $db->query($sql);
                // var_dump($ret);
                while ($row = $ret->fetchArray(SQLITE3_ASSOC)) {
                    // var_dump($row['cname']);
                    if ($row['suggest'] != NULL) {
                        $comma = ',';
                    } else {
                        $comma = '。';
                    }
                    if ($status == 1) {
                        $topic = $row['cname'] . '达到警戒值' . $comma . $row['suggest'];
                    } elseif ($status == 2) {
                        $topic = $row['cname'] . '超过安全范围' . $comma . $row['suggest'];
                    }
                }

                $arr[$key] = $topic;
                // echo $topic;
                // var_dump($arr);

            }
        }
        if ($count == 0) {
            echo '0';
        } else {
            echo json_encode($arr);
        }

        break;
}
