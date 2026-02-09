<?php
require "auth.php";  #nacte soubor 

if (!is_admin()) { #zavola funkci, pokud vrati false, ucivatel neni admin a stranka ho nepusti
  header("Location: login.php"); #presperovani na jinou stranku
  exit; #ukonci aby se dal nevykreslovala stranka admin panelu
}

$servername = "dbs.spskladno.cz";
$username   = "student14";
$password   = "spsnet";
$database   = "vyuka14";
$conn = new mysqli($servername, $username, $password, $database);
$conn->set_charset("utf8mb4");


if ($_SERVER["REQUEST_METHOD"] === "POST" && isset($_POST["delete_id"])) {
  $id = (int)$_POST["delete_id"];
 
 
  $stmt1 = $conn->prepare("DELETE FROM games WHERE player_id = ?");
  $stmt1->bind_param("i", $id);
  $stmt1->execute();

 
  $stmt2 = $conn->prepare("DELETE FROM players WHERE player_id = ?");
  $stmt2->bind_param("i", $id);
  $stmt2->execute();

  header("Location: admin.php");
  exit;
}


$sql = "
SELECT p.player_id, p.username, MAX(g.score) AS best_score
FROM players p
LEFT JOIN games g ON g.player_id = p.player_id
GROUP BY p.player_id, p.username
ORDER BY best_score DESC
LIMIT 200
";
$res = $conn->query($sql);
?>
<!doctype html>
<html lang="cs">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="styly.css">
  <title>Admin</title>
</head>
<body>
  <main class="hlavni">
    <div class="container_leaderboard">
      <div class="ramec">
        <div class="ramec-obsah leaderboard">
          <h1>Admin panel</h1>

          <div style="margin: 12px 0;">
            <a class="nav-link" href="leaderboard.php">Leaderboard</a>
            <a class="nav-link" href="logout.php">Odhlásit</a>
          </div>

          <table>
            <tr>
              <th>ID</th>
              <th>Hráč</th>
              <th>Best score</th>
              <th>Akce</th>
            </tr>

            <?php while($row = $res->fetch_assoc()): ?>
              <tr>
                <td><?= (int)$row["player_id"] ?></td>
                <td><?= htmlspecialchars($row["username"]) ?></td>
                <td><?= (int)($row["best_score"] ?? 0) ?></td>
                <td>
                  <form method="post" style="margin:0;">
                    <input type="hidden" name="delete_id" value="<?= (int)$row["player_id"] ?>">
                    <button class="nav-link" type="submit">Smazat</button>
                  </form>
                </td>
              </tr>
            <?php endwhile; ?>
          </table>

        </div>
      </div>
    </div>
  </main>
</body>
</html>