<?php
session_start();

function is_admin(): bool {
  return !empty($_SESSION["admin"]) && $_SESSION["admin"] === true;
}