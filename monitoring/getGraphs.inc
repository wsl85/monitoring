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
        $query = "SELECT * FROM `graph` WHERE `visible`=1 ORDER BY options";
        $graphs = $conn->query($query);
        foreach($graphs as $graph){
		echo '<div class="demo-container">
			<p class="graphName">'. $graph['graph_name'] .'</p>
			<div id="placeholder_'. $graph['name'] .'" class="demo-placeholder" style="float:left; width:620px;"></div>
			<p id="choices_'. $graph['name'] .'" style="float:right; width:180px;"></p>
			</div>
			';
	}
}
catch(PDOException $e) {
    echo "Błąd pobierania danych: " . $e->getMessage();
}
$conn = null;
?>


