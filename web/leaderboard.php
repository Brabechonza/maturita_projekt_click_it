<?php
// připojení k databázi
$servername = "dbs.spskladno.cz";
$username   = "student14";
$password   = "spsnet";
$database   = "vyuka14";

$conn = new mysqli($servername, $username, $password, $database);

// kontrola připojení
if ($conn->connect_error) {
    die("Connection failed");
}

// SQL dotaz
$sql = "SELECT name, score FROM scores ORDER BY score DESC";
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
							    	
							    </td>
							    	<th>Position</th>
							        <th>Name</th>
							        <th>Score</th>
							    </tr>

							    <?php
							     $poradi = 1;
							     if ($result->num_rows > 0) {
							        while ($row = $result->fetch_assoc()) {
							            echo "<tr>";
										echo "<td>" . $poradi . "</td>";
										echo "<td>" . $row["name"] . "</td>";
										echo "<td>" . $row["score"] . "</td>";
										echo "</tr>";
										$poradi++;
							        }
							    } else {
							        echo "<tr><td colspan='2'>No data</td></tr>";
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