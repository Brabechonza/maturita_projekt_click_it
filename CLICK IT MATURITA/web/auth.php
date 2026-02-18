<?php
session_start(); // Spustí session 

function is_admin(): bool {
  // Definuje funkci is_admin()
  // : bool znamená, že funkce vrací true nebo false
  return !empty($_SESSION["admin"]) // 1) Musí existovat hodnota $_SESSION["admin"]
  &&    //    A ZÁROVEŇ
  $_SESSION["admin"] === true; // 2) Ta hodnota musí být přesně true
}   /*
    Pokud obě podmínky platí → vrátí true
    Pokud některá neplatí → vrátí false
  */