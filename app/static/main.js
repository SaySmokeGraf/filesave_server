const fileInput = document.getElementById('fileInput');
const selectionFileBtn = document.getElementById('upload_btn');
const fileListContainer = document.querySelector('.uploader_file_list');
const dropZone = document.getElementById('drop-zone');
const myFiles = document.getElementById('loaded-file-list');
const overlay = document.getElementById('messageOverlay');
const renameFileOverlay = document.getElementById('renameFileOverlay');
const renameBtnManually = document.getElementById('rename_btn_manually');
const renameOkAutomatic = document.getElementById('alert_btn_rename_automat');
const renameBtnCancel = document.getElementById('alert_btn_rename_no');
const renameCloseBtn = document.getElementById('renameCloseBtn');
const alert_ok_btn = document.getElementById('alert_btn_ok');
const alert_btn_close = document.getElementById('alert_btn_no');
const closeAlertBtn = document.getElementById('closeBtn');

let currentUploadContext = null;// { file, uploadBtn, progressBar }

renameFilePopupOkButton.addEventListener('click', () => {
    if (!currentUploadContext) return;
    if (renameFileTextArea.value.trim() !== '') {
        const orig = currentUploadContext.file; // native File
        const newFile = new File([orig], renameFileTextArea.value.trim(), { type: orig.type });
        currentUploadContext.file.file = newFile;
        uploadFileOnServer(currentUploadContext.file, currentUploadContext.uploadBtn, currentUploadContext.progressBar, false);
    } else {
        renameFileOptionOverlayInformationEmptyAlertNotice();
    }
});
renameBtnManually.addEventListener('click', () => {
    if (!currentUploadContext) return;
    console.log('открыть дополнительное окно загрузки вручную');
    // renameFile.style.display = 'block';
    renameFileOptionOverlay.style.display = 'block';

    renameFilePopupNoButton.addEventListener('click', () => {
        if (!currentUploadContext) return;
        renameFileOptionOverlay.style.display = 'none';
    })
}
);

rewriteFileWithNewNameBtn.addEventListener('click', () => {
    if (!currentUploadContext) return;
    uploadFileOnServer(currentUploadContext.file, currentUploadContext.uploadBtn, currentUploadContext.progressBar, true, true);
});

makeCopyWithName.addEventListener('click', () => {
    if (!currentUploadContext) return;
    uploadFileOnServer(currentUploadContext.file, currentUploadContext.uploadBtn, currentUploadContext.progressBar, false, false);
})
console.trace('attach listener');
renameOkAutomatic.addEventListener('click', () => {
    if (!currentUploadContext) return;
    console.log('кнопка');
    uploadFileOnServer(currentUploadContext.file, currentUploadContext.uploadBtn, currentUploadContext.progressBar, true, false);
});

window.getProfile();
window.loadLibraryData();
let fileToUpload = [];
// renameFileOptionOverlay.style.display = 'none';
// renameFileOverlay.style.display = 'none';
// overlay.style.display = 'none';

closeAlertBtn.addEventListener('click', () => {
    overlay.style.display = 'none';

});

renameCloseBtn.addEventListener('click', () => {
    renameFileOverlay.style.display = 'none';
});

renameBtnCancel.addEventListener('click', () => {
    renameFileOverlay.style.display = 'none';
});

window.addEventListener('click', (e) => {
    if (e.target === overlay) {
        overlay.style.display = 'none';

    }
});


window.exit_profile_btn.addEventListener('click', () => {
    window.location.href = '/site/registration.html';
    window.cleanCookie('auth_token');
})


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
    li.id = file.key;

    const progressBarContainer = document.createElement('div');
    progressBarContainer.className = 'progress-container';
    progressBarContainer.id = `progress-container${file.key}`;
    const progressBar = document.createElement('div');
    progressBar.className = 'progress-bar';
    progressBar.id = `progress-bar-${file.key}`;
    progressBarContainer.appendChild(progressBar);
    const uploadedFileInfoDiv = document.createElement('div');
    uploadedFileInfoDiv.className = 'upload_file-info';
    uploadedFileInfoDiv.id = `upload_file-info_${file.key}`;

    const upload_fileLink = document.createElement('a');
    upload_fileLink.href = '#';
    upload_fileLink.className = 'upload_file-link';
    upload_fileLink.id = `upload_file-linl${file.key}`;

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
    fileActionsDiv.id = `upload_file-actions_${file.key}`;

    const uploadBtn = document.createElement('button');
    uploadBtn.className = 'upload_download-btn';
    uploadBtn.id = `upload_btn_${file.key}`;
    uploadBtn.textContent = 'Загрузить';

    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'upload_delete-btn';
    deleteBtn.id = `delete_btn_${file.key}`;
    deleteBtn.textContent = 'Удалить';

    fileActionsDiv.appendChild(uploadBtn);
    fileActionsDiv.appendChild(deleteBtn);

    li.appendChild(uploadedFileInfoDiv);
    li.appendChild(progressBarContainer);
    li.appendChild(fileActionsDiv);


    fileListContainer.appendChild(li);

    deleteBtn.addEventListener('click', () => {
        deleteUploadFile(file);
    },);

    uploadBtn.addEventListener('click', () => {
        uploadFileOnServer(file, uploadBtn, progressBar);
    })

    // currentUploadContext.file = file.file;
    // currentUploadContext.uploadBtn = uploadBtn;
    // currentUploadContext.progressBar = progressBar;
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
async function uploadFileOnServer(file, btn, progressBar, renameQuery = undefined, rewriteQuery = undefined) {
    console.log(`получен файл${file}`);
    const xhr = new XMLHttpRequest();
    btn.disabled = true;
    url = '/files/upload/single';
    const params = [];

    // if (option) {
    if (rewriteQuery == true) {
        params.push('overwrite=true');
    } else if (rewriteQuery == false) {
        params.push('overwrite=false');
    }

    if (renameQuery == true) {
        params.push('rename=true');
    } else if (renameQuery == false) {
        params.push('rename=false');
    }

    if (params.length > 0) {
        url += '?' + params.join('&');
    }
    // }
    console.log(url);
    // Создаем FormData и добавляем файл
    const formData = new FormData();
    formData.append('file', file.file); // 'file' - имя поля, которое ожидает сервер

    xhr.open('POST', url, true);

    // Устанавливаем заголовок авторизации (не нужно устанавливать для FormData)
    xhr.setRequestHeader('Authorization', `Bearer ${getCookie('auth_token')}`);
    // const progressBar = document.getElementById('progress-bar');
    // Отслеживание прогресса
    // const progressResult;
    xhr.upload.onprogress = function (event) {
        if (event.lengthComputable) {
            const percentComplete = (event.loaded / event.total) * 100;
            console.log(`Загружено: ${percentComplete.toFixed(2)}%`);
            // progressResult = percentComplete;
            progressBar.style.width = `${percentComplete.toFixed(2)}%`;
        }
    };

    // Обработка успешного ответа
    xhr.onload = () => {
        btn.disabled = false;
        currentUploadContext = { file: file, uploadBtn: btn, progressBar: progressBar };
        if (xhr.status === 201) {
            // успешно
            console.log('201');
            if (progressBar) progressBar.style.width = '100%';
            deleteUploadFile(file);
            disableAllAlertWindow();
        } else if (xhr.status === 401) {
            console.log('401');
            if (progressBar) {
                console.log('прогрессбар должен быть в ноль');
                progressBar.style.width = '0%';
            }
            window.location.href = '/site/registration.html';
        } else if (xhr.status === 400) {

            console.log('400');
            if ((getComputedStyle(renameFileOverlay).display === 'none')) {
                showRenameFileOverlay();
            } else {
                renameFileOptionOverlayInformationBadFileNameNotice();
            }
            if (progressBar) {
                console.log('прогрессбар должен быть в ноль');
                progressBar.style.width = '0%';
            }
        }
        else if (xhr.status == 409) {
            // if (getComputedStyle(renameFileOptionOverlay).display === 'block') {
            //     // renameFileOptionOverlayInformationAlreadyExistsNotice();
            //     copyOrRewriteOverlay.style.display = 'block';
            // } else {

            // }
            copyOrRewriteOverlay.style.display = 'block';
            // else {
            //     console.log('меню переименования тут будет. ')
            //     copyOrRewriteOverlay.style.display = 'block';
            // }
            if (progressBar) {
                progressBar.style.width = '0%';
            }
        } else {
            console.error('Ошибка при загрузке:', xhr.status, xhr.statusText);
        }

    }
    xhr.onerror = () => {
        console.error('Ошибка сети');
        btn.disabled = false;
    };


    //  Отправляем запрос с файлом
    xhr.send(formData);
}

function disableAllAlertWindow() {
    if (getComputedStyle(renameFileOverlay).display === 'block' ||
        getComputedStyle(copyOrRewriteOverlay).display === 'block' ||
        getComputedStyle(renameFileOptionOverlay).display === 'block') {
        copyOrRewriteOverlay.style.display = 'none';
        renameFileOverlay.style.display = 'none';
        renameFileOptionOverlay.style.display = 'none';
    }

}


function showRenameFileOverlay() {
    empty_alert.hidden = true; file_already_exists.hidden = true; file_bad_name.hidden = true;
    renameFileOverlay.style.display = 'block';
}

function renameFileOptionOverlayInformationBadFileNameNotice() {
    file_bad_name.hidden = false;
    file_already_exists.hidden = true;
    empty_alert.hidden = true;
}
function renameFileOptionOverlayInformationAlreadyExistsNotice() {
    file_bad_name.hidden = true;
    file_already_exists.hidden = false;
    empty_alert.hidden = true;
}
function renameFileOptionOverlayInformationEmptyAlertNotice() {
    file_bad_name.hidden = true;
    file_already_exists.hidden = true;
    empty_alert.hidden = false;
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
            } else {
                return response.json();
            }
        }).then(data => {
            if (data != null) {
                updateContent(data);
            }
        }).catch(error => console.error('Ошибка запроса:', error));
}

function updateContent(data) {
    // document.getElementById('content-container').innerHTML = data.html;
    console.log(data);
    myFiles.innerHTML = ''
    data.forEach(element => {

        // const closeBtn = document.getElementById('closeBtn');
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
            overlay.style.display = 'block';
            alert_ok_btn.addEventListener('click', () => {
                apiRequest(`/files/delete?filename=${element.filename}`, {}, 'DELETE',
                    'application/json').then(response => {
                        if (response.status == 404) {
                            // window.location.href = '/site/error.html';
                            fileNotFoundAlert.style.display = 'block';
                        }
                        return response;
                    }).then(() => loadLibraryData());
                overlay.style.display = 'none';
                alert_btn_close.addEventListener('click', () => {
                    overlay.style.display = 'none';
                })
            });
        });

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
                    // if (!response.ok) throw new Error('Ошибка при загрузке файла');
                    if (response.status == 401) {
                        window.location.href = '/site/registration.html';
                        return response;
                    } else if (response.status == 404) {
                        // window.location.href = '/site/error.html';
                        fileNotFoundAlert.style.display = 'block';
                        return response;
                    }
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