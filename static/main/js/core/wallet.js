


$(document).on("submit", ".deposit-form", function (e) {

    e.preventDefault()
    buttonObj = $(this).find("#submit-deposit-btn")

    changeToLoading(buttonObj, "Processing")
    
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
        timeout: 20000,
        success: function (response) {
            normalizeLoadingButton(buttonObj, "Submit")
             if(response.success){
              
                Swal.fire({
                  
                    title:"<i class='fas fa-hourglass-half' style='font-size:50px;color:#00d094' ></i>",
                    html:"Deposit Processing!, you will be notified when it's completed.",
                    showCloseButton: true,
                    showCancelButton: false,
                    focusConfirm: true,
                    willClose: () => {
                        url = response.success_url
                        window.location.href = url
                    },
                    confirmButtonAriaLabel: 'OK!',
                    customClass: {
                        confirmButton: 'my-confirm-button' // Add your custom class here
                    }
                
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


 $(document).ready(function (e) {
        $("#deposit-amount").val(5000)

        $("#pay-amount").html("5000")
    })
    $(".payment-check").on("change", function () {
        //fill in the wallet address for selected method
        var add = $(this).attr("wallet_address")
        $("input[name=wallet_address]").val(add)
        $("#wallet-address-copy").attr("data-clipboard-text", add)
        $("#address_name").html($(this).attr("value"))

    })

    $(".copy-clipboard").click(function (e) {
        e.preventDefault()
        swal({
            title: "",
            text: "Copied to clipboard !",
            icon: "",
            button: "close"
        });
       
    })

$(document).on("submit", ".withdrawal-form", function (e) {
        e.preventDefault()
        buttonObj = $(this).find("div button")
        const inputs = document.querySelectorAll(".otp-field input");
    
        let otp = "";
        inputs.forEach((input) => {
            otp += input.value;
            input.disabled = true;
            input.classList.add("disabled");
        })
        changeToLoading(buttonObj, "Processing")
    
        //send ajax
        form = $(this)
        form.append('<input type="hidden" name="otp" value="' + otp + '">');
        form.append('<input type="hidden" name="csrfmiddlewaretoken" value="' + document.querySelector('[name = csrfmiddlewaretoken]').value + '">');
        data = form.serialize()
     
    
      
        $.ajax({
    
            type: "POST",
            url: form.attr("action"),
            data: data,
            timeout: 3000,
            success: function (response) {
                normalizeLoadingButton(buttonObj, "WIthdraw")
                 if(response.success){
                    Swal.fire({
                        title:"<i class='fas fa-hourglass-half' style='font-size:50px;color:#00d094' ></i>",
                        icon: 'primary',
                        html:"WIthdrawal Processing.",
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
                 else if(response.wallet_address_error){
                    //customize
                    Swal.fire({
                        icon : "error",
                        title:"<i class=' fas fa-exclamation-circle' style='font-size:38px;color:red' ></i>",
                        text:response.wallet_address_error,
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
                        title:"<i class=' fas fa-exclamation-circle' style='font-size:38px;color:red' ></i>",
                        icon: 'error',
                        html:response.form_errors,
                        showCloseButton: true,
                        showCancelButton: false,
                        focusConfirm: false,
                    
                        confirmButtonAriaLabel: 'OK!',
                    
                    });
                  
                  }
        
            },
          
    
        })
    
    
    })
    
    



    $("input[name=deposit-amount]").on("keyup keydown", function () {
        $("#pay-amount").html($(this).val())
        correctAmount($(this).val())
    })


    function correctAmount(entered_value) {
   
        entered_value = parseInt(entered_value)
        max_cost = "500000"
        min_cost = "2000"

        max_cost = parseInt(max_cost)
        min_cost = parseInt(min_cost)

        if (entered_value > max_cost) {
            $("input[name=deposit-amount]").val(max_cost)
        } else if (entered_value < min_cost) {
            $("input[name=deposit-amount]").val(min_cost)
        }

    }

