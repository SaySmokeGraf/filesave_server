const login_form = document.getElementById('login_form');
login_form.addEventListener('submit', handleFormSubmit)

function handleFormSubmit(event) {
    event.preventDefault();
    const form = event.target;
    const formData = serializeForm(form);

    if (formData.get('username') != null && formData.get('password') != null) {
        const user = {
            name: formData.get('username'),
            password: formData.get('password')
        }
        console.log(user);
        fetch('/auth/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(user)
        })
            .then(response => {
                const token = response.json()
                setSecureCookie('auth_token', token, 7, false)
            })
            .catch(error => console.error('Ошибка запроса:', error));
    }
}

function serializeForm(formNode) {
    return new FormData(formNode);
}



function setSecureCookie(name, value, days, isSecure = false) {
    let cookieString = `${name}=${encodeURIComponent(value)}; path=/`;

    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        cookieString += `; expires=${date.toUTCString()}`;
    }

    if (isSecure && window.location.protocol === 'http:') {
        cookieString += '; Secure';
    }

    cookieString += '; SameSite=Strict'; // или Lax, в зависимости от требований

    document.cookie = cookieString;
}



