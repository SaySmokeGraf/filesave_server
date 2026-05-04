

const login_form = document.getElementById('login_form');
const main_text = document.getElementById('mainText');
login_form.addEventListener('submit', handleFormSubmit)

function handleFormSubmit(event) {
    event.preventDefault();
    const form = event.target;
    const formData = serializeForm(form);
    // if (!formData || !password) {
    //     // Можно показывать сообщение пользователю
    //     alert('Пожалуйста, заполните оба поля: логин и пароль.');
    //     return; // Выходим, не отправляя запрос
    // }

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
            .then(response => {
                if (response.status !== 401) {
                    return response.json().then(data => {
                        console.log('Access Token:', data.access_token);
                        setSecureCookie('auth_token', data.access_token, 7, false);
                        console.log('Редирект на /site/');
                        window.location.href = '/site/';
                    });
                } else {
                    main_text.textContent = 'Неправильный логин или пароль';
                    main_text.style.color = '#ff0000';

                }

            }) // и})
            .catch(error => console.error('Ошибка запроса:', error));
    }

    function serializeForm(formNode) {

        return new FormData(formNode);
    }



}
