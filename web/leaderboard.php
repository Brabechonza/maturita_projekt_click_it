<?php
require "auth.php";
$servername = "dbs.spskladno.cz";
$username   = "student14";
$password   = "spsnet";
$database   = "vyuka14";

$conn = new mysqli($servername, $username, $password, $database);
if ($conn->connect_error) { die("DB error"); }

$sql = "
SELECT
  p.username AS name,
  m.mode_name AS mode,
  g.score AS score
FROM games g
JOIN players p ON p.player_id = g.player_id
JOIN modes   m ON m.mode_id   = g.mode_id
ORDER BY g.score DESC
LIMIT 50
";
$result = $conn->query($sql);
?>

<!DOCTYPE html>
<html lang="cs">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" type="text/css" href="styly.css">
	<title>CLICK IT WEB</title>
</head>


<body>					   
		<header class="hlava"> <!-- vsechno co je nahore, oddeleni od obsahu -->
			
			<!-- navigace -->
			<!-- nav-icon je ramecek kolem emoji -->
			<!-- nav-link dela vzhled tlacitka -->
			<nav class="navigace"> <!-- cely ramecek s navigaci -->
				<div class="container">
					<ul class="nav-list"> <!-- seznam polozek navigace, home...-->
						 <li><a class="nav-link" href="index.html"><span class="nav-icon">🏠</span>Home</a></li>
          				 <li><a class="nav-link" href="about.html"><span class="nav-icon">🎮</span>About</a></li>
				         <li><a class="nav-link" href="contact.html"><span class="nav-icon">💬</span>Contact</a></li>
				         <li><a class="nav-link" href="popis.html"><span class="nav-icon">📖</span>Seznam</a></li>     
					</ul>
				</div>
			</nav>
				
			<!-- logo click it -->	
			<div class="logo-bar"> <!-- pozadi pod logem, -->
			  <div class="container"> <!-- centrovani obsahu -->
			  	<a class="logo" href="index.html">
			  		<span class="icon-logo"></span> <!-- ctverecek loga -->
		  			<span class="text-logo">CLICK IT!</span>
		  			</a>
		  			<a class="leaderboard" href="leaderboard.php">🏆 Leaderboard</a>
		  	   </div>
			</div>

		</header>
v
		<main class="hlavni">
			<div class="container_leaderboard">
				<div class="ramec">
					<div class="ramec-obsah leaderboard">
							<h1>Leaderboard<br>🏆</h1>
						    <table>
						      <tr>
							   		 <th>Position</th>
							   		 <th>Name</th>
							   		 <th>Mode</th>
							   		 <th>Score</th> 	
							    </tr>
							  
							    <?php
							    if (is_admin()): ?>
									  <a class="nav-link" href="admin.php">Admin panel</a>
									<?php else: ?>
									  <a class="nav-link" href="login.php">Admin login</a>
									<?php endif;
								$pos = 1;
								if ($result && $result->num_rows > 0) {
								  while ($row = $result->fetch_assoc()) {
								    echo "<tr>";
								    echo "<td>" . $pos++ . "</td>";
								    echo "<td>" . htmlspecialchars($row["name"]) . "</td>";
								    echo "<td>" . htmlspecialchars($row["mode"]) . "</td>";
								    echo "<td>" . (int)$row["score"] . "</td>";
								    echo "</tr>";
								  }
								} else {
								  echo "<tr><td colspan='4'>No data</td></tr>";
								}
								$conn->close();
								?>

								</table>
					</div>
				</div>
			</div>
		</main>


		<footer class="footer">
			<div class="container">
				<p class="footer-text">© 2026 CLICK IT!</p>
			</div>
		</footer>
				
</body>
</html> 