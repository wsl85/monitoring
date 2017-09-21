<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<meta http-equiv="Content-Language" content="pl">
	<meta http-equiv="refresh" content="60">
        <title>Monitoring wilgotnosci</title>
	<link href="style.css" rel="stylesheet" type="text/css">
</head>
<body>
<div id="header">
	<h2>Konfiguracja</h2>
</div>
<div id="content">

<?php
	require 'config.inc';
	try {
        	$conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
        	// set the PDO error mode to exception
        	$conn->setAttribute( PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION );
        	if($debug)
                	echo "Połączono z bazą danych";

	}
	catch(PDOException $e){
        	if($debug)
                	echo "Błąd połączenie z bazą danych: " . $e->getMessage();
	}



	try {
        	$query = "SET NAMES 'utf8'";
        	$conn->query($query);
        	$query = "SET CHARACTER SET utf8";
        	$conn->query($query);
        	$query = "SELECT * FROM `graph` WHERE `visible`=1";
        	$graphs = $conn->query($query);
        	foreach($graphs as $graph){
                	echo "<div id='".$graph['name']."'>".$graph['graph_name']."</div>";
			echo "\n";
                	$query = "SELECT * FROM `sensors_view`,`sensors` WHERE `sensors_view`.`sensor_id` = `sensors`.`id` AND `sensors_view`.`graph_id`=".$graph['id'];
                	$sensors = $conn->query($query);
                	foreach($sensors as $sensor){
				echo "<div id='".$sensor['name']."'>&emsp;&emsp;".$sensor['graph_name']."</div>";
				echo "\n";
			}
		}
	}
        catch(PDOException $e){
                if($debug)
                        echo "Błąd pobierania danych z bazy danych: " . $e->getMessage();
	}

?>

</div>
</body>
</html>
