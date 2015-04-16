var setExtension = function() {
    firstRequest = document.getElementById('id_form-0-first_request');
    extension = document.getElementById('id_form-0-extension');
    if(firstRequest.selectedIndex == 1){
        // YES value
        extension.value = '0';
        extension.readOnly = true;
    }
    if(firstRequest.selectedIndex == 2){
        // NO value
        extension.value = '';
        extension.readOnly = false;
    }
}


function bindSelectFirstRequest(){
    firstRequest = document.getElementById('id_form-0-first_request');
    if (firstRequest.addEventListener) {
        firstRequest.addEventListener('change', setExtension ,false);
    }
    else {
        firstRequest.attachEvent('onchange', setExtension);
    }
}







