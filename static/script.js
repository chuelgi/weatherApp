function setTheme() {
	var now = new Date();
	var hour = now.getHours();
	var body = document.body;
	var mainIframe = document.getElementById('mainiframe');

	if (hour >= 6 && hour < 18) {
		body.classList.remove('night');
		body.classList.add('day');
		mainIframe.src =
			'https://my.spline.design/earthday-9d45310cde1d5aa5e7eafd5319e21a37/';
	} else {
		body.classList.remove('day');
		body.classList.add('night');
		mainIframe.src =
			'https://my.spline.design/untitled-314291d07ca525747f5d7034eda789d8/';
	}
}

document.addEventListener('DOMContentLoaded', setTheme);
