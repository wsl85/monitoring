<?php                        
require 'config.inc';

function getColors($graph_name) {
	return "var i = 0;
                $.each(".$graph_name.", function(key, val) {
                	val.color = i;
                        ++i;
                });
		";
}

function getCheckboxes($dane) {
	return 'var choiceContainer_'. $dane.
		' = $("#choices_'. $dane.
		'");$.each('. $dane.
		', function(key, val) {	choiceContainer_'. $dane.
		'.append("<br/><input type='. "'".
		'checkbox'. "'".
		' name='. "'".
		'" + key +"'. "'".
		' checked='. "'".
		'checked'. "'".
		' id='. "'".
		'id" + key + "'. "'".
		'></input>" + "<label for='. "'".
		'id" + key + "'. "'".
		'>" + val.label + "</label>");}); ';
}

function GetTooltip() {
	return '$("<div id='."'".'tooltip'."'".'></div>").css({
			position: "absolute",
			display: "none",
			border: "1px solid #fdd",
			padding: "2px",
			"background-color": "#fee",
			opacity: 0.80
		}).appendTo("body"); ';
}

function getGraph($name) {
	return 'function plotAccordingToChoices_'. $name .'() {
                        var data = [];
                        choiceContainer_'. $name . '.find("input:checked").each(function () {
                                var key = $(this).attr("name");
                                if (key && '. $name .'[key]) {
                                        data.push('. $name .'[key]);
                                }
                        });
                        var plot = $.plot("#placeholder_'. $name .'", data, options);
                        var placeholder_'. $name .' = $("#placeholder_'. $name .'");
                        placeholder_'. $name .'.bind("plotselected", function (event, ranges) {
                        	plot = $.plot("#placeholder_'. $name .'", data, $.extend(true, {}, options, {
                        		xaxis: {
                                		min: ranges.xaxis.from,
                                        	max: ranges.xaxis.to
                                	}
                                }));
                        });
			placeholder_'. $name .'.bind("plothover", function (event, pos, item) {
				if (item) {
					var x = item.datapoint[0].toFixed(2);
					var y = item.datapoint[1].toFixed(2);
					$("#tooltip").html(y)
						.css({top: item.pageY+5, left: item.pageX+5})
						.fadeIn(200);
				} else {
					$("#tooltip").hide();
				}
			});
                }
                plotAccordingToChoices_'. $name .'();
                choiceContainer_'. $name .'.find("input").click(plotAccordingToChoices_'. $name .');
		';
}

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
		echo "var ".$graph['name']." = { \n";
		$query = "SELECT * FROM `sensors_view`,`sensors` WHERE `sensors_view`.`sensor_id` = `sensors`.`id` AND `sensors_view`.`graph_id`=".$graph['id'];
		$sensors = $conn->query($query);
		$i = 0;
		foreach($sensors as $sensor){
			if($i) {
				echo ",\n";
			}
			echo '"'.$sensor['name'].'": { label: "'.$sensor['graph_name'].'", data: [';
                	$query = "SELECT * FROM `values` WHERE `sensor_id`=". $sensor['id'];
			$values = $conn->query($query);
			$j = 0;
			$value['value'] = NULL;
			foreach($values as $value){
				if($j){
					echo ",";
				}
				echo "[". strtotime($value['time'])*1000 .",". $value['value'] ."]";
				$j++;
			}
			echo ",[". strtotime(date('Y-m-d H:i:s'))*1000 .",". $value['value'] ."]";
			echo "]}\n";
			$i++;
		}
		echo "};\n";
		//echo getTooltip();
		echo "\n";
		//javascript generowanie kolorow wykresow
		echo getColors($graph['name']);	
		echo "\n";
		//javascript generowanie checkboxow
		echo getCheckboxes($graph['name']);		
		echo "\n";
		//javascript generowanie wykresow
		echo getGraph($graph['name']);
	}

}
catch(PDOException $e) {
    echo "Błąd pobierania danych: " . $e->getMessage();
}
$conn = null;
?>
