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
    if (!firstRequest)
        return;
    if (firstRequest.addEventListener) {
        firstRequest.addEventListener('change', setExtension ,false);
    }
    else {
        firstRequest.attachEvent('onchange', setExtension);
    }
}



function setFocusFirstElemForm(){
  if(document.forms){
     form = document.forms[0];
     if(form){
        if(form.elements){
            for(i=0; i<form.length;i++){
               if(form[i].readOnly == false && form[i].type != 'hidden'){
                        form[i].focus();
                        return;
               }
            }
        }
     }
  }
}

function setUploadButtonRequest(){
  sendToSupervisorElement = document.getElementById("id_form-0-send_to_supervisor");
  if(sendToSupervisorElement)
    sendToSupervisorElement.style.display='none';

  projectDocument = document.getElementById("id_form-0-project_document")
  if(projectDocument){
      labelFile = document.getElementById("labelFile")
      projectDocument.onchange = function () {
        labelFile.value = projectDocument.value;
        document.getElementById("linkFile").style.display='none';
        labelFile.style.display='inline';
      };
      document.getElementById("chooseFile").onclick = function() {
        projectDocument.click();
      }
  }
}


function setUploadButtonExpert(){
  file_name_element = document.getElementById("id_form-0-file_name")
  if (file_name_element){
      document.getElementById("id_form-0-file_name").onchange = function () {
        document.getElementById("labelFile").value = file_name_element.value;
        document.getElementById("linkFile").style.display='none';
        document.getElementById("labelFile").style.display='inline';
      };
      document.getElementById("chooseFile").onclick = function() {
        file_name_element.click();
      }
  }
}

function sendToSupervisorAndSave(){
    document.getElementById('id_form-0-send_to_supervisor').checked=true;
    if(document.forms){
        form = document.forms[0];
        if(form){
            form.submit();
        }
    }
}

function rejectRequest(SMT_URL, expert_request_id){
    location.href= SMT_URL + "reject_request/" + expert_request_id;
}

function rejectUser(){
    document.getElementById('id_form-0-rejected').checked=true
    if(document.forms){
        form = document.forms[0];
        if(form){
            form.submit();
        }
    }
}






