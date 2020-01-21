<?php
  /**
   * @descGet system run time value script
  */
  $arRuntime =explode(",  ", exec('uptime'));
  echo $arRuntime[2];
?>