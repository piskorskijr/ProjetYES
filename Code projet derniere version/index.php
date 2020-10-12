<?php
 $bdd = new PDO('mysql:host=localhost;dbname=TestProjetYES', 'root', 'pass');

 $req = $bdd->prepare("SELECT * FROM comptage");
 $req->execute();
 $data = $req->fetch();



?>
<!DOCTYPE html>

<html lang="en">

<head>
  <meta charset="utf-8" name="viewport" content="device-width, initial-scale=1.0">
  <link rel="stylesheet" href="style3.css">
</head>
<meta http-equiv="refresh" content="10">
<body>
  <div class="wrapper">
    <div class="one">
      <div class="text">Cyclistes</div>
      <div class="numbers"><?php echo $data['cycliste'];?></div>
    </div>

    <div class="two" id="toto">
      <div class="text">Qualité de l'air</div>
      <div class="numbers"><?php echo $data['valeur_air'];?> /10</div>
    </div>
    <div class="three">
      <div class="text">Température</div>
      <div class="numbers"><?php echo $data['qualif_air'];?></div>
    </div>
    <div class="four">
      <div class="text">Itinéraires</div>
      <div class="numbers"></div>
    </div>
    <div class="five">
      <div class="text">Alertes Mairie</div>
      <div class="numbers"></div>
    </div>
  </div>
</body>

<script type="text/javascript">
  setTimeout(function(){
    window.location.reload(10);
  }, 30000);
  var couleur= "<?php echo $data['COULEUR_AIR'];?>";
  document.getElementById('toto').style.backgroundColor = couleur;
</script>


</html>
