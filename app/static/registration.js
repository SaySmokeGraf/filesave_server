

const login_form = document.getElementById('login_form');
login_form.addEventListener('submit', handleFormSubmit)

function handleFormSubmit(event) {
    event.preventDefault();
    const form = event.target;
    const formData = serializeForm(form);


    if (formData.get('username') != null && formData.get('password') != null) {
        const user = {
            username: formData.get('username'),
            password: formData.get('password')
        }
        console.log(user);
        fetch('/auth/token', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                const accessToken = data.access_token;
                setSecureCookie('auth_token', accessToken, 7, false);
            }) // и})
            .catch(error => console.error('Ошибка запроса:', error));
    }

    function serializeForm(formNode) {

        return new FormData(formNode);
    }



}
