<!DOCTYPE html>
<html>
	<!--#########################################################
	# Created by the Semi Autonomous Rescue Team				#
	#															#
	# Author: Jack Williams, Connor Kneebone					#
	#															#
	# Licensed under GNU General Public License 3.0				#
	##########################################################-->

	<title>S.A.R.T. Interface</title><!--The title displayed in the browser tab bar-->
	<head>
		<!--Link CSS and scripts-->
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="shortcut icon" href="css/favicon.ico" type="image/x-icon" />
		<link rel="stylesheet" href="css/bootstrap.css">
		<link rel="stylesheet" href="css/circle.css">
		<script src="js/jquery.min.js"></script>
		<script src="js/jquery-ui.min.js"></script>
		<script src="js/bootstrap.min.js"></script>
		<script src="js/Chart.bundle.js"></script>
		<!-- S.A.R.T. Scripts -->
		<script src="js/sart.gamepad.js"></script>

		<script>
		$(document).ready(function(){
			$("#btm_view_sensors" ).toggle(false);
			$(".modal-dialog").draggable({
				handle: ".modal-header"
			});
			$("#sensorToggle" ).click(function() {
			  $("#btm_view_camera" ).toggle();
			  $("#btm_view_sensors" ).toggle();
			});
		});
		</script>
		<style>
		@media (min-width: 768px) {
			.abs-center-x {
				position: absolute;
				left: 50%;
				transform: translateX(-50%);
			}
		}
		table {
		  width: 100%;
		}
		td {
		  width: 12.5%;
		  position: relative;
		}
		td:after {
		  content: '';
		  display: block;
		  margin-top: 100%;
		}
		td .content {
		  position: absolute;
		  top: 0;
		  bottom: 0;
		  left: 0;
		  right: 0;
		  background: gold;
		}
		</style>
	</head>
	<body>
		<div class="modal fade top" id="sshModal" role="dialog" data-backdrop="true">
			<div class="modal-dialog modal-lg">
				<div class="modal-content">
					<div class="modal-header dragHeader" id="sshDrag">
						<h4 class="modal-title">SSH</h4>
						<button type="button" class="close" data-dismiss="modal" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>
					<div class="modal-body">
					
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-warning btn-default" onclick="refreshSSH();">Refresh</button>
						<button type="button" class="btn btn-danger btn-default" data-dismiss="modal">&times; Close</button>
					</div>
				</div>
			</div>
		</div>

		<div class="modal fade top" id="logModal" role="dialog" data-backdrop="true">
			<div class="modal-dialog modal-lg" >
				<div class="modal-content">
					<div class="modal-header dragHeader" id="logDrag">
						<h4 class="modal-title">Logs</h4>
						<button type="button" class="close" data-dismiss="modal" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>
					<div class="modal-body">
					
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-warning btn-default" onclick="refreshSSH();">Clear</button>
						<button type="button" class="btn btn-danger btn-default" data-dismiss="modal">&times; Close</button>
					</div>
				</div>
			</div>
		</div>
		
		<!--   _                 _           _                   
			  | |               | |         | |                  
			  | |_   _ _ __ ___ | |__   ___ | |_ _ __ ___  _ __  
		  _   | | | | | '_ ` _ \| '_ \ / _ \| __| '__/ _ \| '_ \ 
		 | |__| | |_| | | | | | | |_) | (_) | |_| | | (_) | | | |
		  \____/ \__,_|_| |_| |_|_.__/ \___/ \__|_|  \___/|_| |_|-->
		<nav class="navbar navbar-toggleable-sm navbar-fixed-top navbar-light bg-light main-nav">
			<div class="container-fluid">
				<ul class="nav navbar-nav">
					<li class="nav-item">
						<a class="nav-link"  href="#" id="start">
							Press a button on your controller to start
						</a>
					</li>
				</ul>
				<ul class="nav navbar-nav abs-center-x">
					<li class="nav-item">
						<a class="nav-link" href="#">
							<span style="color: #FF5A00">S.A.R.T.</span> Control Interface
						</a>
					</li>
				</ul>
				<!--ul class="nav navbar-nav ml-auto">
					<li class="nav-item"-->	
					<div class="inline">
						<button type="button" class="btn btn-outline-dark" id="sensorToggle">
							Toggle Sensors
						</button>
						<button type="button" class="btn btn-outline-dark" data-toggle="modal" data-target="#sshModal" >
							SSH
						</button>
						<button type="button" class="btn btn-outline-dark" data-toggle="modal" data-target="#logModal" >
							Logs
						</button>
						<div class="btn-group dropleft" role="group">
							<button id="powerButtonDropdown" type="button" class="btn btn-outline-danger dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
								Power
							</button>
							<div class="dropdown-menu" aria-labelledby="btnGroupDrop1">
								<a class="dropdown-item" href="#">Shutdown</a>
								<a class="dropdown-item" href="#">Reboot</a>
							</div>
						</div>
					</div>
					<!--/li>
				</ul-->
			</div>
		</nav>
		<div class="container-fluid">
			<br/>
			<div class="row justify-content-md-center">
				<div class="col-md-auto">
					
					<div class="row">
						<div class="col">
							<div class="card">
								<div class="card-body">
									<div id="cputemp_graph" class="c100 p5 med orange">
										<span id="cputemp_level">5°C</span>
										<div class="slice">
											<div class="bar"></div>
											<div class="fill"></div>
										</div>
									</div>
								</div>
								<div class="card-header">
									<span>CPU Temp.</span><br/>
								</div>
							</div>
						</div>
						<div class="col">
							<div class="card">
								<div class="card-body">
									<div id="charge_graph" class="c100 p75 med orange">
										<span id="charge_level">75%</span>
										<div class="slice">
											<div class="bar"></div>
											<div class="fill"></div>
										</div>	
									</div>
								</div>
								<div class="card-header">
									<span>Charge Level</span><br/>
								</div>
							</div>
						</div>
					</div>
				</div>
				<div class="col-md-auto">
					<div class="card" style="border: 0px">
						<!--img id="camera_back" width="480" src="images/test.png"/-->
						<img id="camera_back" src="http://10.0.2.4:8084"/>
					</div>
				</div>
				<div class="col-md-auto">
					<div class="row">
						<div class="col">
							<div class="card">
								<div class="card-body">
									<div id="co2_graph" class="c100 p55 med orange">
										<span id="co2_level">55 ppm</span>
										<div class="slice">
											<div class="bar"></div>
											<div class="fill"></div>
										</div>
									</div>
								</div>
								<div class="card-header">
									<span>CO<sub>2</sub> Level</span><br/>
								</div>
							</div>
						</div>
						<div class="col">
							<div class="card">
								<div class="card-body">
									<div id="tvoc_graph" class="c100 p69 med orange">
										<span id="tvoc_level">69 ppb</span>
										<div class="slice">
											<div class="bar"></div>
											<div class="fill"></div>
										</div>
									</div>
								</div>
								<div class="card-header">
									<span>TVOC Level</span><br/>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
			
			<div class="row justify-content-md-center" id="btm_view_sensors" style="padding-top:20px">
				<div class="col-md-auto">
					<div class="card">
						<div class="card-header">
							Distance
						</div>
						<div class="card-body">
							<canvas id="distChart" width="400" height="200"></canvas>
						</div>
					</div>
				</div>
				<div class="col-md-auto">
					<div class="card">
						<div class="card-header">
							Thermal Camera
						</div>
						<div class="">
							<table>
								<tr>
									<td><div class="content" id="p1"></div></td>
									<td><div class="content" id="p2"></div></td>
									<td><div class="content" id="p3"></div></td>
									<td><div class="content" id="p4"></div></td>
									<td><div class="content" id="p5"></div></td>
									<td><div class="content" id="p6"></div></td>
									<td><div class="content" id="p7"></div></td>
									<td><div class="content" id="p8"></div></td>
								</tr>
								<tr>
									<td><div class="content" id="p9"></div></td>
									<td><div class="content" id="p10"></div></td>
									<td><div class="content" id="p11"></div></td>
									<td><div class="content" id="p12"></div></td>
									<td><div class="content" id="p13"></div></td>
									<td><div class="content" id="p14"></div></td>
									<td><div class="content" id="p15"></div></td>
									<td><div class="content" id="p16"></div></td>
								</tr>
								<tr>
									<td><div class="content" id="p17"></div></td>
									<td><div class="content" id="p18"></div></td>
									<td><div class="content" id="p19"></div></td>
									<td><div class="content" id="p20"></div></td>
									<td><div class="content" id="p21"></div></td>
									<td><div class="content" id="p22"></div></td>
									<td><div class="content" id="p23"></div></td>
									<td><div class="content" id="p24"></div></td>
								</tr>
								<tr>
									<td><div class="content" id="p25"></div></td>
									<td><div class="content" id="p26"></div></td>
									<td><div class="content" id="p27"></div></td>
									<td><div class="content" id="p28"></div></td>
									<td><div class="content" id="p29"></div></td>
									<td><div class="content" id="p30"></div></td>
									<td><div class="content" id="p31"></div></td>
									<td><div class="content" id="p32"></div></td>
								</tr>
								<tr>
									<td><div class="content" id="p33"></div></td>
									<td><div class="content" id="p34"></div></td>
									<td><div class="content" id="p35"></div></td>
									<td><div class="content" id="p36"></div></td>
									<td><div class="content" id="p37"></div></td>
									<td><div class="content" id="p38"></div></td>
									<td><div class="content" id="p39"></div></td>
									<td><div class="content" id="p40"></div></td>
								</tr>
								<tr>
									<td><div class="content" id="p41"></div></td>
									<td><div class="content" id="p42"></div></td>
									<td><div class="content" id="p43"></div></td>
									<td><div class="content" id="p44"></div></td>
									<td><div class="content" id="p45"></div></td>
									<td><div class="content" id="p46"></div></td>
									<td><div class="content" id="p47"></div></td>
									<td><div class="content" id="p48"></div></td>
								</tr>
								<tr>
									<td><div class="content" id="p49"></div></td>
									<td><div class="content" id="p50"></div></td>
									<td><div class="content" id="p51"></div></td>
									<td><div class="content" id="p52"></div></td>
									<td><div class="content" id="p53"></div></td>
									<td><div class="content" id="p54"></div></td>
									<td><div class="content" id="p55"></div></td>
									<td><div class="content" id="p56"></div></td>
								</tr>
								<tr>
									<td><div class="content" id="p57"></div></td>
									<td><div class="content" id="p58"></div></td>
									<td><div class="content" id="p59"></div></td>
									<td><div class="content" id="p60"></div></td>
									<td><div class="content" id="p61"></div></td>
									<td><div class="content" id="p62"></div></td>
									<td><div class="content" id="p63"></div></td>
									<td><div class="content" id="p64"></div></td>
								</tr>
							</table>
						</div>
					</div>
				</div>
				<div class="col-md-auto">
					<div class="card">
						<div class="card-header">
							Temperature
						</div>
						<div class="card-body">
							<canvas id="tempChart" width="400" height="200"></canvas>
						</div>
					</div>
				</div>
			</div>
			<div class="row justify-content-md-center no-gutters" style="" id="btm_view_camera">
				<div class="col-md-auto ">
					<div class="card" style="border: 0px">
						<img width="" id="camera_left" class="img-fluid" src="http://10.0.2.4:8083"/>
						<!--img id="camera_left" width="420" src="images/test.png"/-->
					</div>
				</div>
				
				<div class="col-md-auto">
					<div class="card" style="border: 0px">
						<img width="" id="camera_front" class="img-fluid" src="http://10.0.2.4:8081"/>
						<!--img id="camera_front" width="420" src="images/test.png"/-->
					</div>
				</div>
				
				<div class="col-md-auto">
					<div class="card" style="border: 0px">
						<img width="" id="camera_right" class="img-fluid" src="http://10.0.2.4:8082"/>
						<!--img id="camera_right" width="420" src="images/test.png"/-->
					</div>
				</div>
			</div>
		</div>
		<script src="js/sart.sensors.js"></script>
	</body>
</html>
