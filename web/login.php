<?php
require "auth.php";

$error = "";

if ($_SERVER["REQUEST_METHOD"] === "POST") {
  $user = $_POST["username"] ?? "";
  $pass = $_POST["password"] ?? "";


  if ($user === "admin" && $pass === "1234") {
    $_SESSION["admin"] = true;
    header("Location: admin.php");
    exit;
  } else {
    $error = "Špatné jméno nebo heslo.";
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
            <div class="okno"><?= htmlspecialchars($error) ?></div>
          <?php endif; ?>

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
            </div>
          </form>

        </div>
      </div>
    </div>
  </main>
</body>
</html>