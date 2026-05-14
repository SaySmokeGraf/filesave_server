const renameFileOptionOverlay = document.getElementById('renameFileOptionOverlay');
const renameFilePopupOkButton = document.getElementById('rename_file_btn_ok');
const renameFilePopupNoButton = document.getElementById('rename_file_btn_no');
const file_already_exists = document.getElementById('file_already_exists');
const file_bad_name = document.getElementById('file_bad_name');
const empty_alert = document.getElementById('empty_alert');
const renameFileTextArea = document.getElementById('newFileName');
const renameCloseOptionBtn = document.getElementById('option-close-btn');
const rewriteFileWithNewNameBtn = document.getElementById('rewriteFileWithNewNameBtn');
const makeCopyWithName = document.getElementById('makeCopyWithName');
const alert_btn_copy_or_rewrite_cancel = document.getElementById('alert_btn_copy_or_rewrite_cancel');
const copyOrRewriteOverlay_close_btn = document.getElementById('copyOrRewriteOverlay-close-btn');
const copyOrRewriteOverlay = document.getElementById('copyOrRewriteOverlay');


renameFilePopupNoButton.addEventListener('click', () => {
    renameFileOptionOverlay.style.display = 'none';
})

renameCloseOptionBtn.addEventListener('click', () => {
    renameFileOptionOverlay.style.display = 'none';
})

alert_btn_copy_or_rewrite_cancel.addEventListener('click', () => {
    copyOrRewriteOverlay.style.display = ' none';
})

copyOrRewriteOverlay_close_btn.addEventListener('click', () => {
    copyOrRewriteOverlay.style.display = ' none';
})

