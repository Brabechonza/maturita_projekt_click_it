<?php
require "auth.php";
session_destroy(); // Zničí aktuální session → smaže přihlášení
header("Location: index.html"); // Přesměruje uživatele na hlavní stránku
exit;