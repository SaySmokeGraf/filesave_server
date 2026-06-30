const moderator_table = document.getElementById("moderator_table");
const tbody = moderator_table.querySelector("tbody");
// const searchForm = document.querySelector('.search_form');
const paginationConfing = {
    limit: "",
    username: "",
    is_verified: "",
    is_banned: "",
    is_moderator: ""
}

function resetPagination() {
    paginationConfing.limit = "";
    paginationConfing.username = "";
    paginationConfing.is_verified = "";
    paginationConfing.is_banned = "";
    paginationConfing.is_moderator = "";
    // const formData = new FormData(searchForm);
    searchForm.reset();
}
async function updateUserListContent(page = "", limit = "", username = "", is_verified = "", is_banned = "", is_moderator = "") {
    try {
        if (tbody) {
            tbody.innerHTML = "";
        }

        let baseUrl = "/moder/users";
        const params = new URLSearchParams();
        if (page !== "") {
            params.append('page', page)

        }
        if (limit !== "") {
            params.append('limit', limit);
            paginationConfing.limit = limit;
        } else {
            paginationConfing.limit = "";
        }
        // Добавляем параметры ТОЛЬКО если они не пустые
        if (username !== "") {
            params.append('username', username)
            paginationConfing.username = username;
        }
        else {
            paginationConfing.username = "";
        }


        if (is_verified !== "") {
            params.append('is_verified', is_verified);
            paginationConfing.is_verified = is_verified;
        } else {
            paginationConfing.is_verified = "";
        }

        if (is_banned !== "") {
            params.append('is_banned', is_banned);
            paginationConfing.is_banned = is_banned;
        } else {
            paginationConfing.is_banned = "";
        }
        if (is_moderator !== "") {
            params.append('is_moderator', is_moderator);
            paginationConfing.is_moderator = is_moderator;
        } else {
            paginationConfing.is_moderator = "";
        }

        // Формируем итоговый URL
        let queries = baseUrl;
        if (params.toString()) {
            queries += "?" + params.toString();
        }
        // -------------------------------

        console.log("Отправляем запрос:", queries);

        // 1. Ждем ответ от сервера
        const response = await apiRequest(queries, {}, "GET", "application/json");

        if (response.status !== 200) {
            throw new Error(`Ошибка сервера. Статус: ${response.status}`);
        }

        // 2. Ждем парсинг JSON
        const data = await response.json();
        console.log("Данные успешно получены с сервера:", data);

        // 3. Ждем, пока отрисуется список пользователей
        await getUserListByRequest(data);
        console.log("Список пользователей отрисован. Переходим к пагинации...");

        // 4. Запускаем пагинацию
        await renderPagination(data);

    } catch (error) {
        // Если что-то сломается на любом этапе, мы увидим точную причину здесь
        console.error("Произошла ошибка в updateUserListContent:", error);
    }
}

async function getUserListByRequest(data) {
    console.log("Данные внутри getUserListByRequest:", data);
    const userData = data.items;

    if (!Array.isArray(userData)) {
        console.warn("Поле items не является массивом или отсутствует");
        return data;
    }

    // Заменили .forEach на обычный цикл for...of, который корректно работает в async-функциях
    for (const element of userData) {
        const row = tbody.insertRow(-1);
        row.id = `user_row${element.id}`;

        const user_name_cell = row.insertCell(0);
        const is_verified_cell = row.insertCell(1);
        const is_banned_cell = row.insertCell(2);
        const is_moderator_cell = row.insertCell(3);
        const action_bar_cell = row.insertCell(4);

        user_name_cell.innerText = element.username;
        is_verified_cell.className = "checkbox-container";
        is_banned_cell.className = "checkbox-container";
        is_moderator_cell.className = "checkbox-container";
        action_bar_cell.className = "action-buttons";

        const saveBtn = document.createElement('button');
        saveBtn.className = 'action-btn save-btn';
        saveBtn.textContent = 'Сохранить';

        saveBtn.addEventListener('click', async (event) => {
            const button = event.target;
            const row = button.closest('tr');

            const verifiedCheckbox = row.querySelector('#verified_checkbox');
            const bannedCheckbox = row.querySelector('#banned_checkbox');
            const moderatorCheckbox = row.querySelector('#is_moderator_checkbox');

            if (!verifiedCheckbox || !bannedCheckbox || !moderatorCheckbox) {
                console.error('Не все чекбоксы найдены в строке');
                return;
            }

            const payload = {
                is_verified: verifiedCheckbox.checked,
                is_banned: bannedCheckbox.checked,
                is_moderator: moderatorCheckbox.checked
            };

            try {
                const res = await apiRequest(`/moder/users/update?username=${element.username}`, { body: payload }, 'PATCH', 'application/json');
                console.log(`Статус обновления пользователя ${element.username}:`, res.status);
            } catch (err) {
                console.error("Ошибка при обновлении пользователя:", err);
            }
        });

        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'action-btn delete-btn';
        deleteBtn.textContent = 'Удалить';
        deleteBtn.addEventListener('click', async (event) => {
            try {
                const res = await apiRequest(`/moder/users/delete?username=${element.username}`, {}, 'DELETE', 'application/json');
                console.log(`Статус обновления пользователя ${element.username}:`, res.status);
                if (res.status !== 403 && res.status !== 401 && res.status !== 409 && res.status !== 422 && res.status !== 404) {
                    console.log("Статус не связан с доступом, удаляем строку");
                    row.remove();
                }
                // updateUserListContent();
            } catch (err) {
                console.error("Ошибка при обновлении пользователя:", err);
            }

        })


        action_bar_cell.appendChild(saveBtn);
        action_bar_cell.appendChild(deleteBtn);

        // Ждем выполнения  сторонней функции, если она асинхронная
        await addUserRowCheckBoxes(element, is_verified_cell, is_banned_cell, is_moderator_cell, action_bar_cell);
    }

    return data;
}

async function renderPagination(data) {
    console.log("Отрисовка пагинации. Данные:", data);

    const total = data.total || 0;
    const limit = data.limit || 10;
    const page = data.page || 1;
    const totalPages = Math.ceil(total / limit) || 1;

    // 1. Обновляем текстовую информацию о страницах
    const paginationInfoContainer = document.querySelector('.pagination-info');
    if (paginationInfoContainer) {
        paginationInfoContainer.innerHTML = `Страница <span id="current-page">${page}</span> из 
        <span id="total-pages">${totalPages}</span> (<span id="total-users">${total}</span> пользователей всего)`;
    }

    // 2. Находим элементы управления
    const prevBtn = document.getElementById('prev-page');
    const nextBtn = document.getElementById('next-page');
    const pageNumbersContainer = document.getElementById('page-numbers');

    if (!pageNumbersContainer) {
        console.warn("Элемент #page-numbers не найден в HTML!");
        return data;
    }

    // Очищаем старые номера страниц перед созданием новых
    pageNumbersContainer.innerHTML = '';

    // 3. Логика генерации номеров страниц с троеточиями (как в макете)
    const range = [];
    const delta = 2; // Сколько страниц показывать слева и справа от текущей

    for (let i = 1; i <= totalPages; i++) {
        if (i === 1 || i === totalPages || (i >= page - delta && i <= page + delta)) {
            range.push(i);
        }
    }

    let l;

    for (const i of range) {
        if (l) {
            if (i - l === 2) {
                pageNumbersContainer.appendChild(createPageButton(l + 1, page, limit));
            } else if (i - l > 2) {
                const ellipsis = document.createElement('span');
                ellipsis.className = 'ellipsis';
                ellipsis.textContent = '...';
                pageNumbersContainer.appendChild(ellipsis);
            }
        }
        pageNumbersContainer.appendChild(createPageButton(i, page, limit));
        l = i;
    }

    // 4. Настраиваем кнопку "Назад"
    if (prevBtn) {
        // Удаляем старые слушатели, заменяя кнопку клоном (избегаем дублирования кликов)
        const newPrevBtn = prevBtn.cloneNode(true);
        prevBtn.parentNode.replaceChild(newPrevBtn, prevBtn);

        if (page <= 1) {
            newPrevBtn.disabled = true;
            newPrevBtn.classList.add('disabled'); // Если нужны стили для неактивной кнопки
        } else {
            newPrevBtn.disabled = false;
            newPrevBtn.classList.remove('disabled');
            newPrevBtn.addEventListener('click', () => updateUserListContent(page - 1, limit, paginationConfing.username,
                paginationConfing.is_verified, paginationConfing.is_banned, paginationConfing.is_moderator));
        }
    }

    // 5. Настраиваем кнопку "Вперёд"
    if (nextBtn) {
        const newNextBtn = nextBtn.cloneNode(true);
        nextBtn.parentNode.replaceChild(newNextBtn, nextBtn);

        if (page >= totalPages) {
            newNextBtn.disabled = true;
            newNextBtn.classList.add('disabled');
        } else {
            newNextBtn.disabled = false;
            newNextBtn.classList.remove('disabled');
            newNextBtn.addEventListener('click', () => updateUserListContent(page + 1, limit, paginationConfing.username,
                paginationConfing.is_verified, paginationConfing.is_banned, paginationConfing.is_moderator));
        }
    }

    return data;
}

// Вспомогательная функция для создания одной кнопки страницы
function createPageButton(pageNum, currentPage, limit) {
    const btn = document.createElement('button');
    btn.className = 'page-link';
    btn.textContent = pageNum;
    if (pageNum === currentPage) {
        btn.classList.add('active');
    } else {
        btn.addEventListener('click', () => {
            updateUserListContent(pageNum, limit, paginationConfing.username, paginationConfing.is_verified,
                paginationConfing.is_banned, paginationConfing.is_moderator);
        });
    }
    return btn;
}

function addUserRowCheckBoxes(user, isVerifiedCell, isBannedCell, isModeratorCell, actionBarCell) {
    isVerifiedCell.appendChild(addVerifiedCheckBox(user));
    isBannedCell.appendChild(addIsBannedCheckBox(user));
    isModeratorCell.appendChild(addIsModeratorCheckBox(user));
}

function addVerifiedCheckBox(user) {
    checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.id = "verified_checkbox";
    checkbox.className = "status-checkbox";
    if (user.is_verified) {
        checkbox.checked = true;
    } else {
        checkbox.checked = false;
    }
    return checkbox;
}

function addIsBannedCheckBox(user) {
    checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.id = "banned_checkbox";
    checkbox.className = "status-checkbox";
    if (user.is_banned) {
        checkbox.checked = true;
    } else {
        checkbox.checked = false;
    }
    return checkbox;
}

function addIsModeratorCheckBox(user) {
    checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.id = "is_moderator_checkbox";
    checkbox.className = "status-checkbox";
    if (user.is_moderator) {
        checkbox.checked = true;
    } else {
        checkbox.checked = false;
    }
    return checkbox;
}

