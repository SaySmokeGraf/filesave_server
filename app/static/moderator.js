const username_field_label = document.getElementById("username_field_label");
const status_field_label = document.getElementById("status_field_label");
const searchForm = document.querySelector('.search_form');
// Находим инпут, куда пользователь вводит текст
const searchInput = document.querySelector('.search_form_input');
const filterBtn = document.querySelector('.search_form_filter_btn');

const resetBtn = document.querySelector('.reset');

document.addEventListener('DOMContentLoaded', () => {
    const filterBtn = document.getElementById('filterBtn');
    const filterDropdown = document.getElementById('filterDropdown');
    filterBtn.addEventListener('click', () => {
        filterDropdown.classList.toggle('active');
    });
});

resetBtn.addEventListener('click', () => {
    resetPagination();

})
searchForm.addEventListener('submit', function (event) {
    event.preventDefault();

    // 1. Получаем текст из инпута поиска
    const query = searchInput ? searchInput.value.trim() : "";
    const formData = new FormData(searchForm);
    const limitValue = formData.get('filter_limit');
    if (limitValue) {
        paginationConfing.limit = parseInt(limitValue, 10);
    }
    // 2. Создаем FormData прямо в момент отправки формы!
    // Она автоматически соберет значения всех <select> и <input> внутри этой формы


    // 3. Забираем значения выпадающих списков по их атрибуту name
    // Если в селекте выбрано "Все равно", formData.get() вернет пустую строку ""
    const bannedStatus = formData.get('filter_banned') || "";
    const verifiedStatus = formData.get('filter_verified') || "";
    const moderatorStatus = formData.get('filter_is_moderator') || "";

    // Выводим в консоль для проверки, что прилетает ("true", "false" или "")
    console.log("Поиск:", query);
    console.log("Бан:", bannedStatus);
    console.log("Верификация:", verifiedStatus);
    console.log("Модератор:", moderatorStatus);
    //async function updateUserListContent(page = "", limit = "", username = "", is_verified = "", is_banned = "", is_moderator = "")
    // 4. Вызываем ваш итоговый метод и передаем туда чистые данные
    updateUserListContent("", limitValue, query, verifiedStatus, bannedStatus, moderatorStatus);
});
// const exit_from_profile_btn = document.querySelector('.exit_From_Moder_Btn');

document.addEventListener('DOMContentLoaded', () => {
    const exit_from_profile_btn = document.querySelector('.exit_From_Moder_Btn');

    if (exit_from_profile_btn) {
        exit_from_profile_btn.addEventListener('click', () => {
            cleanCookie('auth_token');
            window.location.href = 'registration.html';
        });
    } else {
        console.error('ОШИБКА: Кнопка .exit_From_Moder_Panel не найдена в HTML!');
    }
});
// Запускаем асинхронные функции последовательно или параллельно
initPage();

async function initPage() {
    try {
        // Ждем проверку статуса и отрисовку списка пользователей
        await updateModeratorStatus();
        await updateUserListContent();
        //  updateUserListContent();
    } catch (error) {
        console.error("Ошибка при инициализации страницы:", error);
    }
}

// ВАЖНО: Добавили ключевое слово async
async function updateModeratorStatus() {
    let queries = "/auth/user-info";
    try {
        const response = await apiRequest(queries, {}, "GET", "application/json");

        if (response.status !== 200) {
            throw new Error(`Ошибка загрузки профиля. Статус: ${response.status}`);
        }

        const data = await response.json();

        if (data) {
            if (username_field_label) {
                username_field_label.textContent = data.username;
            }

            if (status_field_label) {
                if (data.is_moderator) {
                    status_field_label.textContent = "Модератор";
                } else {
                    status_field_label.textContent = "Пользователь";
                }
            }
        }
    } catch (error) {
        console.error("Не удалось обновить статус модератора:", error);
    }
}