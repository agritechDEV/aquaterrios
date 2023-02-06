/* GLOBALS */
// Response message
const _message = document.querySelector('#message')

/* Handle Login */
// Data from login input form
const loginForm = document.querySelector('#loginForm');
// Login function
async function login () {
   
    let response = await fetch('/login', {
        method: 'POST',
        body: new FormData(loginForm),
    });
    const result = await response.json();

    _message.innerHTML = result.detail;

    setTimeout(redirectToProfile, 2000)
};

/* Redirect functions */
function redirectToProfile (){
    location.href = '/profile';
};

function redirectToLogin (){
    location.href = '/';
};


/* Handle POST requests from FormData to JSON */
// Event handler for form submit event that MUST include action URL and type="submit" button
async function handleFormSubmit(event) {
	event.preventDefault();

	const form = event.currentTarget;
	const url = form.action;

	try {
		const formData = new FormData(form);
		const responseData = await postFormDataAsJson({ url, formData });

		console.log({ responseData });
	} catch (error) {
		console.error(error);
	}
}
// Helper function for Posting data
async function postFormDataAsJson({ url, formData }) {
	const plainFormData = Object.fromEntries(formData.entries());
	const formDataJsonString = JSON.stringify(plainFormData);

	const fetchOptions = {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			Accept: "application/json",
		},
		body: formDataJsonString,
	};

	const response = await fetch(url, fetchOptions);

	if (!response.ok) {
		const errorMessage = await response.text();
		throw new Error(errorMessage);
	}

	result = await response.json();
    _message.innerHTML = result.detail;

    setTimeout(redirectToLogin, 2000)
   
}

/* Post events from FormData */
// User registration
let signUpForm = document.getElementById("signUpForm");
signUpForm.addEventListener("submit", handleFormSubmit);














/* TO BE EDITED LATER */
// Data from input forms
const subscribeForm = document.querySelector('#subscribeForm');

//Buttons
const subscribeBtn = document.querySelector('#subscribeBtn');

subscribeBtn.addEventListener('click', (e) => {
    // prevent the form from submitting
    e.preventDefault();

    // show the form values
    const formData = new FormData(subscribeForm);
    const data = formData.values();
    console.log(data);
});





