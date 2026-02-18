<?php
require "auth.php"; // Načte soubor auth.php

$error = ""; // Proměnná pro chybovou hlášku

// Když je odeslaný formulář metodou POST
if ($_SERVER["REQUEST_METHOD"] === "POST") {
   // Vezme hodnoty z formuláře (pokud existují)
  $user = $_POST["username"] ?? "";
  $pass = $_POST["password"] ?? "";


  if ($user === "admin" && $pass === "1234") { // Kontrola přihlašovacích údajů (natvrdo napsané)
    $_SESSION["admin"] = true;  // Nastaví session, že je uživatel admin
    header("Location: admin.php");  // Přesměruje na admin panel
    exit; // Ukončí skript (aby se už nic dalšího nevykreslovalo)
  } else {
    $error = "Špatné jméno nebo heslo."; // Nastaví chybovou hlášku, pokud login nesedí
  }
}
?>
<!doctype html>
<html lang="cs">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="styly.css">
  <title>Admin login</title>
</head>
<body>
  <main class="hlavni">
    <div class="container_leaderboard">
      <div class="ramec">
        <div class="ramec-obsah">
          <h1>Přihlášení admina</h1>

          <?php if ($error): ?> 
             <!-- Pokud je v proměnné $error text, zobrazí se -->
            <div class="okno"><?= htmlspecialchars($error) ?></div>
             <!-- htmlspecialchars zajistí, že by se nespustil žádný HTML kód -->
          <?php endif; ?>

          <!-- Přihlašovací formulář -->
          <form method="post">
            <div class="okno">
              <strong>Jméno</strong><br>
              <input name="username" required style="width:95%; margin-top:8px; padding:10px; border-radius:10px;">
            </div>

            <div class="okno">
              <strong>Heslo</strong><br>
              <input type="password" name="password" required style="width:95%; margin-top:8px; padding:10px; border-radius:10px;">
            </div>

            <div style="margin-top:12px;">
              <button class="nav-link" type="submit">Přihlásit</button>
               <!-- Tlačítko odešle formulář -->
            </div>
          </form>

        </div>
      </div>
    </div>
  </main>
</body>
</html>