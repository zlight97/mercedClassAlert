<?php

    $class = $_GET["class"];
    $email = $_GET["email"];
    $jsObj->email=$email;
    $jsObj->sent=false;
    $class = strtoupper($class);
    $class = trim($class);

    $split = array();
    $split = str_split($class);
    if($split[0]>='0' and $split[0]<='9')
    {
        $jsObj->usesCRN=true;
        $jsObj->crn=$class;
    }
    else {
        $jsObj->usesCRN=false;
        $count = 0;
        foreach($split as $st)
        {
            if($st>='0' and $st<='9')
                break;
            $count++;
        }
        $subj = substr($class, 0, $count);
        $code = substr($class, strlen($class)-3,3);
        $jsObj->subj=$subj;
        $jsObj->code=$code;
    }
    // $jsonObj = json_encode($jsObj);
    // echo json_encode($jsObj);

    $string = file_get_contents("jsonLayout.json");
    $json_a = json_decode($string, true);
    array_push($json_a['classes'],$jsObj);
    $jsonObj = json_encode($json_a,JSON_PRETTY_PRINT);
    $file = fopen( "jsonLayout.json", "w" );
    if( $file == false ) {
        echo ( "Error in opening file" );
        exit();
    }
    fwrite($file,$jsonObj);
    fclose($file);
    // echo $json_a[];
    exit();
?>