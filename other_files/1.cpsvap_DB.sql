/* Δημιουργία Βάσης Δεδομένων "cpsv_ap" */

set character_set_client='utf8';
set character_set_connection='utf8';
set character_set_database='utf8';
set character_set_filesystem='utf8';
set character_set_results='utf8';
set character_set_server='utf8';

SET GLOBAL time_zone = '+2:00';


/* Δημιουργία και χρήση Database */
/* ----------------------------- */
DROP DATABASE IF EXISTS cpsv_ap;
create database cpsv_ap DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
use cpsv_ap;

