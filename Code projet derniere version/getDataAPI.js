window.onload = function() {
	console.log(data);
	console.log(meteo);
	console.log(couleur);
	console.log(quality);
  document.getElementById("air-quality").innerText = quality;
  document.getElementById("temperature").innerText = temp + "°C";
  document.getElementById("two").style.backgroundColor = couleur;
	console.log(temp);
var list_weather = ["broken clouds", "scattered clouds", "fog", "mist", "overcast clouds","clear sky", "few clouds", "snow", "rain", "heavy rain" , "moderate rain", "thunderstorm"]
if (list_weather.includes(meteo) == true){

	if (meteo == 'broken clouds'){
		document.getElementById("images_cloudy").src = "images/weather/lightgray.jpg"
	}

	if (meteo == 'scattered clouds'){
		document.getElementById("images_cloudy").src = "images/weather/lightgray.jpg"
	}

	if (meteo == 'fog'){
		document.getElementById("images_cloudy").src = "images/weather/cloudy.jpg"
	}

	if (meteo == 'mist'){
		document.getElementById("images_cloudy").src = "images/weather/cloudy.jpg"
	}

	if (meteo == 'overcast clouds'){
		document.getElementById("images_cloudy").src = "images/weather/cloudy.jpg"
	}

	if (meteo == 'clear sky'){
		document.getElementById("images_cloudy").src = "images/weather/soleil.jpg"
	}

	if (meteo == 'few clouds'){
		document.getElementById("images_cloudy").src = "images/weather/few_clouds.jpg"
	}

	if (meteo.includes('snow')){
		document.getElementById("images_cloudy").src = "images/weather/snow.gif"
	}

	if (meteo == ('rain')){
		document.getElementById("images_cloudy").src = "images/weather/rain.gif"
	}

	if (meteo == ('heavy rain')){
		document.getElementById("images_cloudy").src = "images/weather/rain.gif"
	}

        if (meteo == ('moderate rain')){
		document.getElementById("images_cloudy").src = "images/weather/rain.gif"
	}
        
        if (meteo == 'thunderstorm'){
		document.getElementById("images_cloudy").src = "images/weather/thunder.gif"
	}


}

else {
	document.getElementById("images_cloudy").src = "images/weather/lightgray.jpg"
}




}
