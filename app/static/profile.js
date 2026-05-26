const userNameLabel = document.querySelector('.username_label');
const exit_profile_btn = document.getElementById('exit_profile_btn');


async function getProfile() {
    apiRequest('/auth/user-info', {}, 'GET', 'application/json', {})
        .then(response => {
            if (response.status === 401) {
                window.location.href = '/site/registration.html';
                return null;
            } else {
                return response.json();
            }
        }).then(data => {
            if (data != null) {
                updateProfileName(data);
            }
        }).catch(error => console.error('Ошибка запроса:', error));
}




async function updateProfileName(data) {
    console.log(data);
    userNameLabel.textContent = data.username;
    if (data.is_moderator) {
        document.getElementById('moderator_btn').removeAttribute('hidden');
    }
}



