
window.addEventListener("DOMContentLoaded", function() {
	//attach listeners for all of the profile images you can choose from
	let pic1 = document.getElementById("king");
	pic1.addEventListener("click", switching);

	let pic2 = document.getElementById("queen");
	pic2.addEventListener("click", switching);

	let pic3 = document.getElementById("rook");
	pic3.addEventListener("click", switching);

	let pic4 = document.getElementById("bishop");
	pic4.addEventListener("click", switching);

	let pic5 = document.getElementById("knight");
	pic5.addEventListener("click", switching);

	let pic6 = document.getElementById("pawn");
	pic6.addEventListener("click", switching);

	let pic7 = document.getElementById("pikachu");
	pic7.addEventListener("click", switching);

	let pic8 = document.getElementById("cat");
	pic8.addEventListener("click", switching);

	let pic9 = document.getElementById("dog");
	pic9.addEventListener("click", switching);

	let pic10 = document.getElementById("elephant");
	pic10.addEventListener("click", switching);

	let pic11 = document.getElementById("penguin");
	pic11.addEventListener("click", switching);

	let pic12 = document.getElementById("fish");
	pic12.addEventListener("click", switching);
});

//change the profile image to the one clicked on in the selector box
function switching(event) {
	let current = document.getElementById("profile_pic");
	current.src = event.target.src;
	let hidden = document.getElementById("picture-holder");
	hidden.value = event.target.src;
}

