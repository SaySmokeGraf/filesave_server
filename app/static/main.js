const fileInput = document.getElementById('fileInput');
const selectionFileBtn = document.getElementById('upload_btn');
const fileListContainer = document.querySelector('.uploader_file_list');
const dropZone = document.getElementById('drop-zone');
const myFiles = document.getElementById('loaded-file-list');
window.loadLibraryData();
let fileToUpload = [];

/**
 * Выгрузка куки из базы куки браузера.
 * */


const token = getCookie('auth_token');

/**
 * 
 * Метод выполняет действие когда файлы драг-энд-дропом сброшены
 */
function handleDropFiles(files) {
    addFilesInCollections(files);
    updateUploaderFileList();
}

/**
 * 
 * Обновляет список файлов в разделе Upload.
 */
function updateUploaderFileList() {
    fileListContainer.innerHTML = '';
    fileToUpload.forEach((file) => {
        createUploadElement(file);
    });
}

/**
 * 
 * Создание одного элемента в списке upload
 */
function createUploadElement(file) {
    const li = document.createElement('li');
    li.className = 'upload_file_item';

    const uploadedFileInfoDiv = document.createElement('div');
    uploadedFileInfoDiv.className = 'upload_file-info';

    const upload_fileLink = document.createElement('a');
    upload_fileLink.href = '#';
    upload_fileLink.className = 'upload_file-link';

    let lastDotIndex = file.name.lastIndexOf('.');
    let filename = lastDotIndex !== -1 ? file.name.substring(0, lastDotIndex) : file.name;
    let extension = lastDotIndex !== -1 ? file.name.substring(lastDotIndex) : '';

    if (filename.length >= 18) {
        filename = filename.slice(0, 18) + "...";
    }

    upload_fileLink.textContent = filename + extension;
    uploadedFileInfoDiv.appendChild(upload_fileLink);

    const fileActionsDiv = document.createElement('div');
    fileActionsDiv.className = 'upload_file-actions';

    const uploadBtn = document.createElement('button');
    uploadBtn.className = 'upload_download-btn';
    uploadBtn.textContent = 'Upload';

    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'upload_delete-btn';
    deleteBtn.textContent = 'Delete';

    fileActionsDiv.appendChild(uploadBtn);
    fileActionsDiv.appendChild(deleteBtn);

    li.appendChild(uploadedFileInfoDiv);
    li.appendChild(fileActionsDiv);

    fileListContainer.appendChild(li);

    deleteBtn.addEventListener('click', () => {
        deleteUploadFile(file);
    });

    uploadBtn.addEventListener('click', () => {
        uploadFileOnServer(file, uploadBtn);
    })
}
/**
 * 
 * Удаляет Upload элемент из списка Upload.
 */
function deleteUploadFile(file) {
    const index = fileToUpload.findIndex(f => f.key === file.key);
    if (index !== -1) {
        fileToUpload.splice(index, 1);
        updateUploaderFileList();
        loadLibraryData();
    }
}
/**
 * 
 * Загрузка файла на сервер из списка Upload.
 */
function uploadFileOnServer(file, btn) {
    const xhr = new XMLHttpRequest();
    btn.disabled = true;

    // Создаем FormData и добавляем файл
    const formData = new FormData();
    formData.append('file', file.file); // 'file' - имя поля, которое ожидает сервер

    xhr.open('POST', '/files/upload/single', false);

    // Устанавливаем заголовок авторизации (не нужно устанавливать для FormData)
    xhr.setRequestHeader('Authorization', `Bearer ${getCookie('auth_token')}`);

   // Отслеживание прогресса
    xhr.upload.onprogress = function (event) {
        if (event.lengthComputable) {
            const percentComplete = (event.loaded / event.total) * 100;
            console.log(`Загружено: ${percentComplete.toFixed(2)}%`);
        }
    };

    // Обработка успешного ответа
    xhr.onload = () => {
        if (xhr.status === 200) {
            console.log('Успешно:', xhr.responseText);
            deleteUploadFile(file);
        } else {
            console.error('Ошибка при загрузке:', xhr.status, xhr.statusText);
        }
        btn.disabled = false; // Разблокируем кнопку после завершения
    };

    // Обработка ошибок сети
    xhr.onerror = () => {
        console.error('Ошибка сети');
        btn.disabled = false;
    };

  //  Отправляем запрос с файлом
    xhr.send(formData);
}


function addFilesInCollections(files) {
    Array.from(files).forEach(file => {
        const key = `${file.name}_${file.size}_${file.type}`;
        const exists = fileToUpload.some(existingFile => existingFile.key === key);
        if (!exists) {
            fileToUpload.push({
                file: file,
                name: file.name,
                size: file.size,
                type: file.type,
                key: key
            });
        }
    });
}

fileInput.addEventListener('change', () => {
    addFilesInCollections(fileInput.files);
    updateUploaderFileList();
    fileInput.value = '';
});


selectionFileBtn.addEventListener('click', () => {
    fileInput.click();
});


['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, e => {
        e.preventDefault();
        e.stopPropagation();
    }, false);
});


dropZone.addEventListener('dragover', () => dropZone.style.borderColor = 'green');
dropZone.addEventListener('dragleave', () => dropZone.style.borderColor = '#ccc');


dropZone.addEventListener('drop', e => {
    dropZone.style.borderColor = '#ccc';
    const files = e.dataTransfer.files; // Получаем список файлов
    handleDropFiles(files); // Функция обработки
});


function loadLibraryData() {



    apiRequest('/files', {}, 'GET', 'application/json', {})
        .then(response => {
            if (response.status === 401) {
                window.location.href = '/site/registration.html';
                return null;
            }
            return response.json();
        })
        .then(data => {
            if (data != null) {
                updateContent(data);
            }
        })
        .catch(error => console.error('Ошибка запроса:', error));
}

function updateContent(data) {
    // document.getElementById('content-container').innerHTML = data.html;
    console.log(data);
    myFiles.innerHTML = ''
    data.forEach(element => {

        const li = document.createElement('li');
        li.className = 'file-item';
        const myFileInfoDiv = document.createElement('div');
        myFileInfoDiv.className = 'file-info';
        const myfileLink = document.createElement('a');
        myfileLink.href = '#';
        myfileLink.className = 'file-link';
        myfileLink.textContent = element.filename;
        myFileInfoDiv.appendChild(myfileLink);
        const fileactions = document.createElement('div');
        fileactions.className = 'file-actions';
        const downloadButton = document.createElement('button');
        downloadButton.className = 'download-btn';
        downloadButton.textContent = 'Скачать';
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'delete-btn';
        deleteBtn.textContent = 'Удалить';
        // const file-actio
        li.appendChild(myFileInfoDiv);
        fileactions.appendChild(downloadButton);
        fileactions.appendChild(deleteBtn);
        li.appendChild(fileactions);
        myFiles.appendChild(li);
        // myFiles.appendChild(myFileInfoDiv);

        deleteBtn.addEventListener('click', () => {
            apiRequest(`/files/delete?filename=${element.filename}`, {}, 'DELETE',
                'application/json').then(() => loadLibraryData());
        })

        downloadButton.addEventListener('click', () => {
            // Создаем спиннер или иное индикатор загрузки
            const spinner = document.createElement('span');
            spinner.className = 'spinner'; // добавьте стили для класса spinner
            spinner.innerHTML = '⏳'; // или используйте любой другой символ или SVG

            // Сохраняем текущий текст кнопки, чтобы вернуть после
            const originalText = downloadButton.textContent;

            // Показываем спиннер внутри кнопки
            downloadButton.textContent = '';
            downloadButton.appendChild(spinner);
            apiRequest('/files/download/?filename=' + encodeURIComponent(element.filename), {}, 'GET',
                'multipart/file').then(response => {
                    if (!response.ok) throw new Error('Ошибка при загрузке файла');
                    return response.blob();
                })
                .then(blob => {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = element.filename; // укажите нужное имя
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                    window.URL.revokeObjectURL(url);
                })
                .catch(error => {
                    console.error('Ошибка запроса:', error);
                })
                .finally(() => {
                    // Восстановить исходный текст кнопки
                    downloadButton.textContent = originalText;
                });
        });

    })
}
const obj = document.getElementById('flyingObject');

// Задаем зону перемещения (например, центральная часть окна)
const zone = {
    xMin: 100,
    yMin: 100,
    xMax: window.innerWidth - 150, // учитываем ширину картинки
    yMax: window.innerHeight - 150 // учитываем высоту картинки
};

// Начальные координаты
let position = {
    x: Math.random() * (zone.xMax - zone.xMin) + zone.xMin,
    y: Math.random() * (zone.yMax - zone.yMin) + zone.yMin
};

// Целевая точка
let target = {
    x: 0,
    y: 0
};

// Скорость перемещения
const speed = 1.5; // пикселей за кадр, можно регулировать

// Функция для выбора новой цели внутри зоны
function setNewTarget() {
    target.x = Math.random() * (zone.xMax - zone.xMin) + zone.xMin;
    target.y = Math.random() * (zone.yMax - zone.yMin) + zone.yMin;
}

// Изначально задаем первую цель
setNewTarget();

function animate() {
    // Вычисляем разницу до цели
    const dx = target.x - position.x;
    const dy = target.y - position.y;
    const distance = Math.hypot(dx, dy);

    if (distance < speed) {
        // Достигли цели, выбираем новую
        setNewTarget();
    } else {
        // Двигаемся к цели
        position.x += (dx / distance) * speed;
        position.y += (dy / distance) * speed;
    }

    // Обновляем позицию картинки
    obj.style.left = position.x + 'px';
    obj.style.top = position.y + 'px';

    requestAnimationFrame(animate);
}

// Обновляем зону при изменении размера окна
window.addEventListener('resize', () => {
    zone.xMax = window.innerWidth - 150;
    zone.yMax = window.innerHeight - 150;
});

// Запускаем анимацию
animate();

async function apiRequest(url, options = {}, method = 'GET', contentType = 'application/json') {
    const token = getCookie('auth_token');
    if (!token) {
        return {
            error: 'No authentication token found. Please log in.',
            status: 401,
            body: null
        };
    } else {
        const config = {
            method: method,
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': contentType,
                ...options.headers
            },
            ...options
        };

        const response = await fetch(url, config);

        if (!response.ok) {
            return {
                error: `HTTP error! status: ${response.status}`,
                status: response.status,
                body: await response.text()
            };
        }

        return response;
    }
}
