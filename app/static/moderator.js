const username_field_label = document.getElementById("username_field_label");
const status_field_label = document.getElementById("status_field_label");

// Запускаем асинхронные функции последовательно или параллельно
initPage();

async function initPage() {
    try {
        // Ждем проверку статуса и отрисовку списка пользователей
        await updateModeratorStatus();
        await updateUserListContent();
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