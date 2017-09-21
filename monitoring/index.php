<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<meta http-equiv="Content-Language" content="pl">
	<meta http-equiv="refresh" content="60">
        <title>Monitoring wilgotnosci</title>
	<link href="style.css" rel="stylesheet" type="text/css">
        <script language="javascript" type="text/javascript" src="javascript/flot/jquery.js"></script>
        <script language="javascript" type="text/javascript" src="javascript/flot/jquery.flot.js"></script>
        <script language="javascript" type="text/javascript" src="javascript/flot/jquery.flot.time.js"></script>
        <script language="javascript" type="text/javascript" src="javascript/flot/jquery.flot.selection.js"></script>
	<script type="text/javascript">
	$(function() {
		var options = {
			legend: {
				position: "nw",
				noColumns: 0
			},
			xaxis: {
				mode: "time",
				tickLength: 5,
				timezone: "browser"
			},
            		yaxis: {
				autoscaleMargin: 0.2
			},
			selection: {
				mode: "x"
			},
			points: {
				show: true,
				radius: 1
			},
			lines: {
				show: true,
				steps: true
			},
			grid: {
				hoverable: true,
				clickable: true
			}

		};

		var formatTime = function(unixTimestamp) {
    			var dt = new Date(unixTimestamp*1);

    			var hours = dt.getHours();
    			var minutes = dt.getMinutes();
    			var seconds = dt.getSeconds();

    			// the above dt.get...() functions return a single digit
    			// so I prepend the zero here when needed
    			if (hours < 10) 
     				hours = '0' + hours;

    			if (minutes < 10) 
     				minutes = '0' + minutes;

    			if (seconds < 10) 
     				seconds = '0' + seconds;

    			return hours + ":" + minutes + ":" + seconds;
		}       
	
		//wyswietlanie wartosci po najechaniu na punkt
		$("<div id='tooltip'></div>").css({
			position: "absolute",
			display: "none",
			border: "1px solid #fdd",
			padding: "2px",
			"background-color": "#fee",
			opacity: 0.80
		}).appendTo("body");	
		
		<?php
			require 'getValues.inc';
		?>
	
	});
	</script>
</head>
<body>
<div id="header">
	<h2>Monitoring</h2>
</div>
<div id="content">

<?php
	require 'getGraphs.inc';
?>

</div>

</body>
</html>
