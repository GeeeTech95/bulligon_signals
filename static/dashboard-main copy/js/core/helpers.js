
//makes 

//shows loading when a form is to be submitted via ajax
function changeToLoading(_object,loadingText="loading"){
    //reset all field erro to empty
    $(".field-error").html('')
    
    //_object is the button object
    loadingText = " " + loadingText  
    loading = "" +
    "<center>" +
        '<span style="text-align:center" class="spinner-border spinner-border-sm me-05" role="status" aria-hidden="true">' +
        '</span>' +
    loadingText  +
    "</center>"

    _object.attr("disabled","")
    _object.attr("type","button")
    _object.html(loading)

}


function transactionSuccessPopUp(text){
    modal = $("#transactionSuccessDialog")
    modalContent = modal.find(".modal-dialog .modal-content .modal-body")
    modalContent.html(text)
    modal.modal("toggle")

}


function popUp(text,form_object = null,title = "Error !"){
        
        errorModal = $("#DialogIconedDanger")

        if(form_object != null){
            try{
                formModal = $("#" + form_object.attr("modal-parent"))
                formModal.modal("hide")
                errorModal.attr("referrer-form-modal",form_object.attr("modal-parent"))

            }
            catch{

            }
            
        }
     

        errorModalTitle = errorModal.find(".modal-dialog .modal-content .modal-header .modal-title")
        errorModalContent = errorModal.find(".modal-dialog .modal-content .modal-body")
        errorModalContent.html(text)
        errorModalTitle.html(title)

        errorModal.modal("toggle")
  
     
    }





function normalizeLoadingButton(_object,buttonText="Submit"){
    //_object is the button object
    
    _object.removeAttr("disabled")
    _object.attr("type","submit")
    _object.html(buttonText)

}


function handleFormError(form_object,error_response,buttonText="Submit"){
    //apply error
    
    for(const [field,error] of Object.entries(error_response)){
       $(".field-error[input-name=" + field + "]").html(error)
    
    }
    dangerText = "please correct the form errors"
    
    //check for general errors
    if (error_response.non_field_errors){
        dangerText = error_response.non_field_errors
    }
 
    popUp(dangerText,form_object)
}

//when the error modal closes, it brings back the form modal which reffered it
$(document).on("click","#closeDialogIconedDangerButton",function(){
    parentModal = $("#DialogIconedDanger")
    //incase referrer is not set

    referrerFormModalId = parentModal.attr("referrer-form-modal")
    referrerFormModal = $("#"+ referrerFormModalId)
    parentModal.modal("toggle")
    console.log(referrerFormModal)
    referrerFormModal.modal("toggle")
   


})

/*-- @v1.0.1-s */
// Copyto clipboard
function feedback (el, state) {
    if (state==='success'){
        $(el).parent().find('.copy-feedback').text('Copied to Clipboard').fadeIn().delay(1000).fadeOut();
    } else {
        $(el).parent().find('.copy-feedback').text('Faild to Copy').fadeIn().delay(1000).fadeOut();
    }
}
var clipboard = new ClipboardJS('.copy-clipboard');
clipboard.on('success', function(e) {
    feedback(e.trigger, 'success'); e.clearSelection();
}).on('error', function(e) {
    feedback(e.trigger, 'fail');
});

// Copyto clipboard In Modal
var clipboardModal = new ClipboardJS('.copy-clipboard-modal', {
    container: document.querySelector('.modal')
});
clipboardModal.on('success', function(e) {
    feedback(e.trigger, 'success'); e.clearSelection();
}).on('error', function(e) {
    feedback(e.trigger, 'fail');
});

