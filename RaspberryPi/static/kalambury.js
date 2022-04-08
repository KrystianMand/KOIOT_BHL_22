var przyslowia = [
	"Gdzie kucharek sześć tam nie ma co jeść",
	"Darowanemu koniowi w zęby się nie zagląda",
	"Nie mów hop póki nie przeskoczysz",
	"Dzieci i ryby głosu nie mają",
	"Człowiek człowiekowi wilkiem"
];

var obrazki = [
	"static/img/k0.jpg",
	"static/img/k1.jpg",
	"static/img/k2.jpg",
	"static/img/k3.jpg",
	"static/img/k4.jpg"
];


//losowanie hasła
var nr = Math.floor(Math.random() * przyslowia.length);
var haslo = przyslowia[nr];
haslo = haslo.toUpperCase();

var proby = 3;



function start()
{
	document.getElementById("obraz_kalambur").innerHTML = '<img src="'+obrazki[nr]+'" alt="" style="width:50%"/>';
}

window.onload = start;



function sprawdz() //sprawdzanie czy wpisana odpowiedz jest taka jak haslo
{
	var odpowiedz = document.getElementById("odpowiedz").value;
	odpowiedz = odpowiedz.toUpperCase();
	if(odpowiedz == haslo)
	{
		wygrana();
	}
	else{
		if (proby > 1)
		{
			nastepnaProba();
		}
		else
		{
			przegrana();
		}
	}
}



function wygrana()
{
	document.getElementById("wynik").innerHTML ="Brawo! Poprawna odpowiedź."
	+"<a class='reset' href='/win'> <u>Zakończ</u></a>";
	document.getElementById("odpowiedz").disabled = true;
	document.getElementById("sprawdz").disabled = true;
}

function przegrana()
{
	document.getElementById("wynik").innerHTML ="Niestety nie. Nie masz już więcej prób. Prawidłowa odpiwiedź to: "+haslo
	+"<br/><a class='reset' href='/play'> <u>Jeszcze raz?</u></a>   <a class='reset' href='/dashboard'> <u>Muszę odpocząć...</u></a>";
	document.getElementById("odpowiedz").disabled = true;
	document.getElementById("sprawdz").disabled = true;
}

function nastepnaProba()
{
	proby = proby -1;
	document.getElementById("wynik").innerHTML = "Niestety nie. Pozostało prób "+proby;
}