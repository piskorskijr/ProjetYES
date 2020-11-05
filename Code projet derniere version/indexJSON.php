<?php
 $bdd = new PDO('mysql:host=localhost;dbname=comptage', 'root', 'pass');

 $req = $bdd->prepare("SELECT * FROM comptage");
 $req->execute();
 $data = $req->fetch();
?>

<!DOCTYPE html>

<html lang="en">

<head>
  <meta charset="utf-8" name="viewport" initial-scale="1.0">
  <link rel="stylesheet" href="style2.css">
  <script type="text/javascript" src="dataAPI2.js"></script>
  <script type="text/javascript" src="getDataAPI.js"></script>
  <script src="https://code.jquery.com/jquery-3.5.0.js"></script>
</head>
<body id="body">
  <div class="wrapper">
    <div class="block" id="zero">
      <div id="dateDisplay" class="numbers"></div>
      <div id="clockDisplay" class="numbers"></div>
    </div>
    <div class="block" id="one">
      <div class="bikeNumber">
        <img id="images_bike" src="images/blackBike.png">
        <div class="numbers" style="font-size : 140px"><?php echo $data['cycliste'];?></div>
      </div>
    </div>
    <div class="block" id="three">
      <img id="images_cloudy" style="width: 140%;" src="">
      <div class="numbers" id="temperature"></div>
    </div>
    <div class="block_2" id="two">
      <div class="numbers" id="air" style="font-size: 70px">Qualité de l'air</div>
      <div class="numbers" id="air-quality"></div>
    </div>
    <div class="block" id="four">
      <div class="column">
        <div id="route1" class="numbers">Grand Palais - 3km</div>
        <img id="images_right" src="images/arrow.png">
        <img id="images_front" src="images/arrow.png">
        <div id="route2" class="numbers">Citadelle - 1km</div>
      </div>
    </div>
    <div class="block" id="five">
      <img id="images_careful" src="images/message_rouge.png">
      <div class="numbers" style="font-size:70px; text-align:center; margin-top: 0.5em">CHAUSSÉE GLISSANTE SUR 500M</div>
    </div>

  </div>
</body>

<script type="text/javascript">

//auto refresh de la page toute les 10 secondes
  setTimeout(function(){
    window.location.reload(1);
  }, 4000);


function showTime(){
  var time = new Date();
  var h = time.getHours();
  var m = time.getMinutes();
  var s = time.getSeconds();

  h = (h < 10) ? "0" +h : h;
  m = (m < 10) ? "0" +m : m;
  s = (s < 10) ? "0" +s : s;

  var time = h + ":" + m + ":" + s;
  document.getElementById("clockDisplay").innerText = time;

  setTimeout(showTime, 1000)

// Mode nuit
  if (h >= 12){
    document.getElementById("body").style.backgroundColor = "black"

    for(var i=0; i< document.getElementsByClassName("block").length; i++) {
      document.getElementsByClassName("block")[i].style.backgroundColor = "rgb(59,57,59)";
    }

    for(var i=0; i< document.getElementsByClassName("numbers").length; i++) {
      document.getElementsByClassName("numbers")[i].style.color = "white";
    }

    document.getElementById("images_bike").src = "images/whiteBike.png"

  }
}

function showDate(){
  var today = new Date();

  var date = today.getDate();
  var day = today.getDay();
  var month = today.getMonth();
  var year = today.getFullYear();
  var monthNames = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"];
  var dayNames = ["Dimanche", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"];
  var values = ["month"]

  var currentDate = dayNames[day]+ " " + date + " " + monthNames[month];

  document.getElementById("dateDisplay").innerText = currentDate;

}
showDate();

showTime();


</script>

</html>
