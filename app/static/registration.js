const login_form = document.getElementById('login_form');
const main_text = document.getElementById('mainText');
const regDialog = document.getElementById('registration_dialog');
const registrationDialog = document.getElementById('registration_dialog');
const registrationForm = document.getElementById('registration_form');
const exitBtn = document.getElementById('exitBtn');

const create_account_link = document.getElementById('create-account-link');
login_form.addEventListener('submit', handleFormSubmit);
registrationForm.addEventListener('submit', handleFormRegistration);

create_account_link.addEventListener('click', function (event) {
    event.preventDefault();
    console.log('Пользователь нажал на ссылку "Создать аккаунт"');
    if (create_account_link) {
        registrationDialog.showModal();
        console.log('на месте');
    }
});

function closeModal() {
    console.log("модальное окно закрыто");
    registrationDialog.close();

}

exitBtn.addEventListener('click', closeModal);

async function handleFormSubmit(event) {
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

                        checkUserStatus().then(isValid => {
                            if (isValid) {
                                window.location.href = '/site/';
                                console.log(data);
                            }
                        })
                        // if (checkUserStatus()) {
                        //      window.location.href = '/site/';
                        //     console.log(data);

                        // }
                    });
                } else {
                    main_text.textContent = 'Неправильный логин или пароль';
                    main_text.style.color = '#ff0000';

                }

            }) // и})
            .catch(error => console.error('Ошибка запроса:', error));
    }




}

async function handleFormRegistration(event) {
    console.log("Должен был отправить форму");
    event.preventDefault();
    const form = event.target;
    // if (form != null) {
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
        fetch('/auth/register', {
            method: 'POST',
            body: formData
        })
            .then(response => {
                if (response.status == 201) {
                    return response.json().then(data => {
                        console.log(data);
                        console.log(`${user.username} зарегистрирован`);
                    });
                }
                // } else {
                //     main_text.textContent = 'Неправильный логин или пароль';
                //     main_text.style.color = '#ff0000';

                // }

            }) // и})
            .catch(error => console.error('Ошибка запроса:', error));
    }
    // }
}



async function checkUserStatus() {
    const userProfileData = await checkUserProfileRequest();
    if (userProfileData.is_banned) {
        console.log('Забанен');
        main_text.textContent = 'Вы забанены';
        main_text.style.color = '#ff0000';
        return false;
    } else if (!userProfileData.is_verified) {
        main_text.textContent = 'Вы не верифицированы'
        main_text.style.color = '#00ff15';
        return false;
    }
    return true;
}

function checkUserProfileRequest() {
    return window.apiRequest('/auth/user-info', {}, 'GET', 'application/json', {})
        .then(data => {
            if (data != null) {
                return data.json();
            } else {
                throw new Error('Нет данных');
            }
        })
        .then(jsonData => {
            // здесь jsonData — уже распарсенный объект JSON
            console.log(jsonData);
            return jsonData; // можно вернуть дальше, если нужно
        })
        .catch(error => {
            console.error('Ошибка запроса:', error);
        });
}
// function checkUserIsModerator(isModerator) {
//     return isModerator;
// }


function serializeForm(formNode) {

    return new FormData(formNode);
}
