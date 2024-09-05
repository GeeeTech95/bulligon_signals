
//subscribe to notifications
$(document).ready(
    function () {
        cookieConsent()
        getPriceUpdates()

    }
)

$("#accept-cookies").on("click",function(e){
    localStorage.setItem('accepted_cookie', 'True');
    $("#cookiePermissionModal").modal("hide") 
})


function cookieConsent(){
    var value = localStorage.getItem('accepted_cookie');
    if(value != "True"){
        $("#cookiePermissionModal").modal("show")
    }
    
}

window.OneSignalDeferred = window.OneSignalDeferred || [];
OneSignalDeferred.push(async function (OneSignal) {
    await OneSignal.init({
        appId: "8bf9716f-f42c-4617-aea1-3c42e57a83b2",
    });
});



function getPriceUpdates() {
    coinMarketCapToken = "d8b53a16-98eb-4971-80f3-d426acfdd646"
    crytptoAlertingToken = "e1kw1WoNHbT0dogNm9gmW0RDqKniK1y"
   
    $.ajax({
        headers: {
            'Authorization': 'Bearer e1kw1WoNHbT0dogNm9gmW0RDqKniK1y',
            'Content-Type': 'application/json'
        },
      
        type: "POST",
        url: "https://api.cryptocurrencyalerting.com/v1/alert-conditions",
        data:  {
            type: 'price',
            currency: 'ETH',
            target_currency: 'USD',
            price: '400.00',
            direction: 'above',
            channel: { 'name': 'telegram' },
            exchange: 'Gemini'
          },

        timeout: 3000,
        success: function (response) {
            alert('sd')
           console.log(response.data)
        },

        error : function(response){
            console.log(response)
        },

        statusCode: {

            400: function (response) {
                normalizeLoadingButton(buttonObj, origText)
                handleFormError(form, response.responseJSON)
            },

            500: function (response) {
                normalizeLoadingButton(buttonObj, origText)
                popUp("Request timed out, please retry", form_object = form)
            }
        }

    })
}