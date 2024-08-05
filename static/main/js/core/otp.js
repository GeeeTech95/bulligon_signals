const inputs = document.querySelectorAll(".otp-field input");

inputs.forEach((input, index) => {
    input.dataset.index = index;
    input.addEventListener("keyup", handleOtp);
    input.addEventListener("paste", handleOnPasteOtp);
});

function handleOtp(e) {
    /**
     * <input type="text" 👉 maxlength="1" />
     * 👉 NOTE: On mobile devices `maxlength` property isn't supported,
     * So we to write our own logic to make it work. 🙂
     */
    const input = e.target;
    let value = input.value;
    let isValidInput = value.match(/[0-9a-z]/gi);
    input.value = "";
    input.value = isValidInput ? value[0] : "";

    let fieldIndex = input.dataset.index;
    if (fieldIndex < inputs.length - 1 && isValidInput) {
        input.nextElementSibling.focus();
    }

    if (e.key === "Backspace" && fieldIndex > 0) {
        input.previousElementSibling.focus();
    }

    if (fieldIndex == inputs.length - 1 && isValidInput) {
        //submit();
    }
}

function handleOnPasteOtp(e) {
    const data = e.clipboardData.getData("text");
    const value = data.split("");
    if (value.length === inputs.length) {
        inputs.forEach((input, index) => (input.value = value[index]));
        submit();
    }
}


$("#resend-otp").click(function () {
    //set timeout


    $.ajax({
        type: "GET",
        url: $(this).attr('url'),
   
        success: function (data) {

            if (data.success) {
                
                //show success modal
                Swal.fire({
                    title: '',
                    icon: 'success',
                    text:"An OTP has been sent, please check your mail.",
                    showCloseButton: true,
                    showCancelButton: false,
                    focusConfirm: false,
                    confirmButtonAriaLabel: '    OK!    ',
               
                });
              
            
            } else if (data.error) {
            
            }
        }
    });
})
