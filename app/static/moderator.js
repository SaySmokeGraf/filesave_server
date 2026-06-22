const moderator_table = document.getElementById("moderator_table");

// alert_ok_btn.addEventListener('click', () => {
//     apiRequest(`/files/delete?filename=${currentFilename}`, {}, 'DELETE',
//         'application/json').then(response => {
//             if (response.status == 404) {
//                 // window.location.href = '/site/error.html';
//                 console.log('1234');
//                 fileNotFoundAlert.style.display = 'block';
//             }
//             return response;
//         }).then(() => loadLibraryData());
//     overlay.style.display = 'none';
// });

// alert_btn_close.addEventListener('click', () => {
//     overlay.style.display = 'none';
// })
// renameFilePopupOkButton.addEventListener('click', () => {
//     if (!currentUploadContext) return;
//     if (renameFileTextArea.value.trim() !== '') {
//         const orig = currentUploadContext.file; // native File
//         const newFile = new File([orig], renameFileTextArea.value.trim(), { type: orig.type });
//         currentUploadContext.file.file = newFile;
//         uploadFileOnServer(currentUploadContext.file, currentUploadContext.uploadBtn, currentUploadContext.progressBar, false);
//     } else {
//         renameFileOptionOverlayInformationEmptyAlertNotice();
//     }
// });

function updateUserListContent() {
  apiRequest("/moder/users", {}, "GET", "application/json")
    .then((response) => {
      if (response.status == 200) {
        console.log("1234");
        return response;
      }
    })
    .then((data) => {
      getUserListByRequest(data);
    });
}

function getUserListByRequest(data) {
  const data = JSON.parse(data.items);
  console.log(Array.isArray(data)); // true
  console.log(objectArray.length); // 3
  console.log(typeof data[0]); // "object"
  if (Array.isArray(data)) {
    data.array.forEach((element) => {
      row = table.insertRow(-1);
      row.id = `user_row${element.id}`;
      user_name_cell = row.insertCell(0);
      is_verified_cell = row.insertCell(1);
      is_banned_cell = row.insertCell(2);
      is_moderator_cell = row.insertCell(3);
      action_bar_cell = row.insertCell(4);
      // 4. Заполняем ячейки
      user_name_cell = element.username;
      is_verified_cell.className = "checkbox-container";
      is_banned_cell.className = "checkbox-container";
      is_moderator_cell.className = "checkbox-container";
      action_bar_cell.className = "action-buttons";
      addUserRowCheckBoxes(element,isVerifiedCell,isBannedCell,isModeratorCell,actionBarCell);
    });
  }
}

function addUserRowCheckBoxes(user,isVerifiedCell,isBannedCell,isModeratorCell,actionBarCell) {
  isVerifiedCell.appendChild(addVerifiedCheckBox(user));
  isBannedCell.appendChild(addIsBannedCheckBox(user));
  isModeratorCell.appendChild(addIsModeratorCheckBox(user));
}

function addVerifiedCheckBox(user) {
  checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.id = "verified_checkbox";
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
  if (user.is_moderator) {
    checkbox.checked = true;
  } else {
    checkbox.checked = false;
  }
  return checkbox;
}

function updatePagination(limit,total,page){

}
