<?php
require "auth.php";  #nacte soubor 

if (!is_admin()) { #zavola funkci, pokud vrati false, ucivatel neni admin a stranka ho nepusti
  header("Location: login.php"); #presperovani na jinou stranku
  exit; // ukončí skript, aby se admin stránka vůbec nevykreslila
}

$servername = "dbs.spskladno.cz";
$username   = "student14";
$password   = "spsnet";
$database   = "vyuka14";

$conn = new mysqli($servername, $username, $password, $database); // vytvoří připojení na DB
$conn->set_charset("utf8mb4"); // nastaví kódování (aby fungovala čeština + emoji)

if ($conn->connect_error) {
  die("DB error: " . $conn->connect_error);   // když se nepřipojí DB, ukončí skript a vypíše chybu
}

# delete hrace
if ($_SERVER["REQUEST_METHOD"] === "POST" && isset($_POST["delete_id"])) { // pokud přišel POST request a obsahuje delete_id -> chceš smazat hráče
  $id = (int)$_POST["delete_id"]; // převede na int (aby tam nebyl bordel / text)
 
  // 1) smaže všechny hry (score záznamy) daného hráče
  $stmt1 = $conn->prepare("DELETE FROM games WHERE player_id = ?");
  $stmt1->bind_param("i", $id);
  $stmt1->execute();
  $stmt1->close();
 
  // 2) smaže samotného hráče
  $stmt2 = $conn->prepare("DELETE FROM players WHERE player_id = ?");
  $stmt2->bind_param("i", $id);
  $stmt2->execute();
  $stmt2->close();
  
  header("Location: admin.php");  // refresh stránky aby se neodeslal POST znovu
  exit;
}

# update hrace
if ($_SERVER["REQUEST_METHOD"] === "POST" && isset($_POST["update_id"])) { // pokud přišel POST request a obsahuje update_id -> chceš změnit jméno
  $id = (int)$_POST["update_id"]; // id hráče jako číslo
  $new_username = trim($_POST["new_username"] ?? ""); // vezme new_username z formuláře, odstraní mezery, když není -> dá ""

  if ($id > 0 && $new_username !== "") { // kontrola že id je ok a jméno není prázdné
    $stmt = $conn->prepare("UPDATE players SET username = ? WHERE player_id = ?"); // připravený UPDATE dotaz
    $stmt->bind_param("si", $new_username, $id);
    $stmt->execute();     // provede update
    $stmt->close();
  }

  header("Location: admin.php");   // refresh aby se neodesílal POST znovu
  exit;
}

 // SQL dotaz pro načtení seznamu her a hráčů
$sql = "  
SELECT p.player_id, p.username -- vybere ID hráče a jeho jméno z tabulky players
FROM games g -- vybere tabulku games, pocet radku se odviji od toho kolik tam bude her
JOIN players p ON p.player_id = g.player_id -- ke každé hře připojí hráče podle shodného player_id, ziskame jmeno hrace ke konkretni hre
ORDER BY g.player_id ASC -- seřadí výsledky podle ID hráče vzestupně (od nejmenšího)
LIMIT 50
";
$res = $conn->query($sql); // spustí SELECT a uloží výsledky do $res

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
              <th>Hráč (Změna jména)</th>
              <th>Akce</th>
            </tr>

            <?php if ($res): ?>
              <?php while($row = $res->fetch_assoc()): ?>  <!-- fetch_assoc() = vezme 1 řádek z výsledků jako pole (sloupec => hodnota) -->
                <tr>
                  <td><?= (int)$row["player_id"] ?></td>  <!-- vypíše id jako číslo -->

                  <td>
                     <!-- UPDATE form: pošle update_id + new_username -->
                    <form method="post" style="margin:0; display:flex; gap:8px; align-items:center; justify-content:center;">
                      <input type="hidden" name="update_id" value="<?= (int)$row["player_id"] ?>">   <!-- hidden input = pošle id hráče -->
                      <input
                        type="text"
                        name="new_username"
                        value="<?= htmlspecialchars($row["username"]) ?>"  
                        required 
                        style="padding:8px 10px; border-radius:10px; width: 220px;">  <!-- value je vyplněné současným jménem, htmlspecialchars = aby se nerozbilo HTML -->
                      <button class="nav-link" type="submit">Uložit</button> <!-- submit = odešle formulář -->
                    </form>
                  </td>

                  <td>
                     <!-- DELETE form: pošle delete_id -->
                    <form method="post" style="margin:0;">
                      <input type="hidden" name="delete_id" value="<?= (int)$row["player_id"] ?>">
                      <button class="nav-link" type="submit">Smazat</button>
                    </form>
                  </td>
                </tr>
              <?php endwhile; ?>
            <?php endif; ?>
          </table>

        </div>
      </div>
    </div>
  </main>
</body>
</html>