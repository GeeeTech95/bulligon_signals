
$(document).on("submit", ".login-form", function (e) {
    e.preventDefault()
  
    form = $(this)
    data = new FormData(form[0])
  
    buttonObj = $(this).find(".login-submit-btn")
    origText = buttonObj.html()
    changeToLoading(buttonObj, "Logging on")
 
    $.ajax({

        type: "POST",
        url: form.attr("action"),
        data: form.serialize(),
      
        timeout: 3000,
        success: function (response) {
            url = response.success_url
            window.location.href = form.attr("dashboard_link")
        },

        /*error : function(){
            normalizeLoadingButton(buttonObj,"Pay From Bank")
            popUp("Request timed out, please retry")
        },*/

        statusCode: {

            400 : function (response) {
                normalizeLoadingButton(buttonObj,origText)
                handleFormError(form, response.responseJSON)
            },

            500 : function (response) {
                normalizeLoadingButton(buttonObj, origText)
                popUp("Request timed out, please retry", form_object = form)
            }
        }

    })
})





$(document).on("submit", ".registration-form", function (e) {
    e.preventDefault()
    buttonObj = $("#signup-btn")

    changeToLoading(buttonObj, "Creating Account")

    //send ajax
    form = $(this)
    data =   form.serialize(),
  
    //crfToken = document.querySelector('[name = csrfmiddlewaretoken]').value,
     
    $.ajax({

        type: "POST",
        url: form.attr("action"),
        data: data,
        success: function (response) {
            normalizeLoadingButton(buttonObj,"Register Account")
            Swal.fire({
                  
                icon: "success",
                html:"Registration was successful",
                showCloseButton: true,
                showCancelButton: false,
                focusConfirm: true,
                willClose: () => {
                    url = response.success_url
                    window.location.href = form.attr("email_confirm_link")
                },
                confirmButtonAriaLabel: 'Verify Email',
            
            });
           
            
        },
        error : function(response){

            normalizeLoadingButton(buttonObj,"Register Account")
            Swal.fire({
                icon : "error",
                //title:"<i class=' fas fa-exclamation-circle' style='font-size:38px;color:red' ></i>",
                text:"An error occured , please retry or contact support. " + response.responseJSON['detail'],
                showCloseButton: true,
                showCancelButton: false,
                focusConfirm: false,
                confirmButtonAriaLabel: 'Close!',
           
            });
           
        },
        statusCode: {
            400: function (response) {
                normalizeLoadingButton(buttonObj,"Register Account")
                handleFormError(form, response.responseJSON)
                Swal.fire({
                    icon : "error",
                    title:"<i class=' fas fa-exclamation-circle' style='font-size:38px;color:red' ></i>",
                    text:"Please correct the form errors",
                    showCloseButton: true,
                    showCancelButton: false,
                    focusConfirm: false,
                    confirmButtonAriaLabel: 'Close!',
               
                });
              
               
            },

            500: function (response) {
             
                normalizeLoadingButton(form.find(".form-group button"), "Register Account")
                Swal.fire({
                    icon : "error",
                   
                    text:"Request timed out, please retry",
                    showCloseButton: true,
                    showCancelButton: false,
                    focusConfirm: false,
                    confirmButtonAriaLabel: 'Close!',
               
                });
               
            }
        }

    })
})


$(document).on("submit", ".verify-email-form", function (e) {
    e.preventDefault()
    buttonObj = $("#verify-email-btn")
    const inputs = document.querySelectorAll(".otp-field input");

    let otp = "";
    inputs.forEach((input) => {
        otp += input.value;
        input.disabled = true;
        input.classList.add("disabled");
    })
    changeToLoading(buttonObj, "Verifying")

    //send ajax
    form = $(this)
    data =  {
        "otp" : otp,
        "csrfmiddlewaretoken": document.querySelector('[name = csrfmiddlewaretoken]').value
    },
  
    //crfToken = document.querySelector('[name = csrfmiddlewaretoken]').value,
     
    $.ajax({

        type: "POST",
        url: form.attr("action"),
        data: data,
        timeout: 3000,
        success: function (response) {
            normalizeLoadingButton(buttonObj, "Verify")
             if(response.success){
                Swal.fire({
                    //title:"<i class='fas fa-hourglass-half' style='font-size:50px;color:#6d4afe' ></i>",
                    icon: 'success',
                    html:"Your email address has been verified successfully!",
                    showCloseButton: true,
                    showCancelButton: false,
                    focusConfirm: true,
                    willClose: () => {
                        url = response.success_url
                        window.location.href = form.attr("dashboard_link")
                    },
                    confirmButtonAriaLabel: 'Back To Dasboard',
                
                });
               
                
             }
             else {
                Swal.fire({
                    //title:"<i class='fas fa-hourglass-half' style='font-size:50px;color:#6d4afe' ></i>",
                    icon: 'error',
                    html:response.error,
                    showCloseButton: true,
                    showCancelButton: false,
                    focusConfirm: true,
                  
                    confirmButtonAriaLabel: 'OK!',
                
                });

             }
    
        },
      

    })


})




$(document).on("submit", ".kyc-form", function (e) {

    e.preventDefault()
    buttonObj = $(this).find("#kyc-submit-btn")

    changeToLoading(buttonObj, "Uploading")
    
    var formData = new FormData(this); 
    //send ajax
    form = $(this)
    data =   form.serialize(),

    //crfToken = document.querySelector('[name = csrfmiddlewaretoken]').value,
     
    $.ajax({
        data: formData,
        contentType: false,  // Important: Do not set content type, it will be set by FormData
        processData: false, 
        type: "POST",
        url: form.attr("action"),
        data: formData,
        timeout: 3000,
        success: function (response) {
            normalizeLoadingButton(buttonObj, "Submit")
             if(response.success){
        
                Swal.fire({
                  
                    title:"<i class='fas fa-hourglass-half' style='font-size:50px;color:#6d4afe' ></i>",
                    html:"Your KYC request was submitted successfully. It's currently in review!, you will be notified when it's completed.",
                    showCloseButton: true,
                    showCancelButton: false,
                    focusConfirm: true,
                    willClose: () => {
                        url = response.success
                        window.location.href = url
                    },
                    confirmButtonAriaLabel: 'OK!',
                
                });
           
          
               
                
             }
             else if(response.error){
              
                Swal.fire({
                    icon : "error",
                    title:"<i class=' fas fa-exclamation-circle' style='font-size:38px;color:red' ></i>",
                    text:response.error,
                    showCloseButton: true,
                    showCancelButton: false,
                    focusConfirm: false,
                    confirmButtonAriaLabel: 'Close!',
               
                });
               
             }

             else if(response.form_errors){
                //customize
                //handleFormError(form,response.form_errors)
                Swal.fire({

                    title:"<i class=' fas fa-exclamation-circle' style='font-size:38px;color:red' ></i><br><span style='font-family:normal;margin-right:10px'>Correct Form Errors</span>",
                    icon: 'error',
                    html:response.form_errors,
                    showCloseButton: true,
                    showCancelButton: false,
                    focusConfirm: false,
                    confirmButtonAriaLabel: 'OK!',
                
                });
              
              }
    
        },
   
         
         
 
        error : function(response){

            normalizeLoadingButton(buttonObj,"Submit")
            Swal.fire({


                icon: 'error',
                html:"An error occured , please retry or contact support.",
                showCloseButton: true,
                showCancelButton: false,
                focusConfirm: false,
                confirmButtonAriaLabel: 'OK!',
            
            });
             
        },

        

    })
})





