<?php
require "auth.php";
$servername = "dbs.spskladno.cz";
$username   = "student14";
$password   = "spsnet";
$database   = "vyuka14";

$conn = new mysqli($servername, $username, $password, $database); // Vytvoří připojení k MySQL
if ($conn->connect_error) { die("DB error"); } // Když se nepřipojí, skript se ukončí a vypíše chybu

$sql = "
SELECT -- jmena v tabulce se zobrazi vicekrat, jedno jmeno muze mit vice her 
  p.username AS name, -- vezme username z tabulky players a pojmenuje ho jako 'name'
  m.mode_name AS mode, -- vezme název módu z tabulky modes a pojmenuje ho jako 'mode'
  g.score AS score -- vezme skóre z tabulky games
FROM games g -- hlavní tabulka games
JOIN players p ON p.player_id = g.player_id -- propojí hráče podle player_id
JOIN modes   m ON m.mode_id   = g.mode_id -- propojí mód podle mode_id
ORDER BY g.score DESC -- seřadí od největšího skóre po nejmenší, desc = sestupne
LIMIT 50 -- vezme jen top 50 záznamů
";
$result = $conn->query($sql); // Spustí SQL dotaz a uloží výsledek do $result
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
				         <li><a class="nav-link" href="popis.html"><span class="nav-icon">📖</span>Algorithms</a></li>     
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
							    if (is_admin()): ?> <!-- Admin tlačítko: když je user admin, ukáže admin panel, jinak login -->
									  <a class="nav-link" href="admin.php">Admin panel</a>
									<?php else: ?>
									  <a class="nav-link" href="login.php">Admin login</a>
									<?php endif; 
								$pos = 1; // Pořadí v tabulce (1. místo, 2. místo...)
								if ($result && $result->num_rows > 0) { // Pokud dotaz vrátil nějaká data, projde je cyklem
								  while ($row = $result->fetch_assoc()) { // fetch_assoc = vezme jeden řádek jako asociativní pole
								    echo "<tr>";
								    echo "<td>" . $pos++ . "</td>"; // Vypíše pořadí a pak ho zvýší o 1
								    echo "<td>" .  htmlspecialchars($row["name"]) . "</td>"; // Vypíše jméno hráče + htmlspecialchars chrání proti XSS = ochrana proti vlozeni skodliveho skriptu 
								    echo "<td>" .  htmlspecialchars($row["mode"]) . "</td>"; // Vypíše mód
								    echo "<td>" .  (int)$row["score"] . "</td>";  // Vypíše score
								    echo "</tr>";
								  }
								} else {
								  echo "<tr><td colspan='4'>No data</td></tr>"; // Když nejsou žádná data v DB, vypíše hlášku
								}
								$conn->close();   // Zavře připojení k databázi
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