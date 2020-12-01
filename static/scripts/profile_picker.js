object.addEventListener("click", myScript);

window.addEventListener("DOMContentLoaded", function() {
	// attach a listener to call increment when Up button is clicked
	let pic1 = document.getElementById("up");
	upbtn.addEventListener("click", increment);
	// attach a listener to call decrement when Down button is clicked
	let downbtn = document.getElementById("down");
	downbtn.addEventListener("click", decrement);
});