function setTheme() {
	var now = new Date();
	var hour = now.getHours();
	var body = document.body;

	if (hour >= 6 && hour < 18) {
		body.classList.remove('night');
		body.classList.add('day');
	} else {
		body.classList.remove('day');
		body.classList.add('night');
	}
}

document.addEventListener('DOMContentLoaded', setTheme);
