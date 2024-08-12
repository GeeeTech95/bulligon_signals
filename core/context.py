from django.core.exceptions import ObjectDoesNotExist
from Users.models import Country, KYC


def core(request):
    prepend = "https://" if request.is_secure() else "http://"
    host = request.get_host()
    # reg_link  = prepend + host + request.user.user_admin.reg_link
    ctx = {"site_url" : prepend + host}
    print(prepend + host)
    ctx['liquidity'] = 53199180

    ctx['site_name_verbose'] = "Bulligon SIgnals"
    ctx['site_name'] = "Bulligon SIgnals"
    ctx['site_name_full'] = "Bulligon SIgnals"
    ctx['support_email'] = "support@bitcoinvoyager.finance"
    ctx['site_email'] = "support@bitcoinvoyager.finance"
    ctx['site_phone'] = "+3594858"
    ctx['site_whatsapp_no'] = "+66658656fg6"
    ctx['site_address'] = "No 23 winston road new york"
    ctx['ltc_wallet_address'] = "ltc1quehe6rnusjv4e8jhcsnryq5pxt00qpetdwgkyd"
    ctx['usdt_bep20_wallet_address'] = "0x5DAaDBc326896104Cd0fF517Dc572fA74d8D22A0"
    ctx['usdt_trc20_wallet_address'] = "TUZa6KazwmQt294XtybQTUL4cw3qyesoC9"
    ctx['eth_wallet_address'] = "0x5DAaDBc326896104Cd0fF517Dc572fA74d8D22A0"
    ctx['btc_wallet_address'] = "bc1q6ks696dlm4gkcex99qcz0kph8k3ua4cws7s9h0"
    ctx['bnb_wallet_address'] = "0x5DAaDBc326896104Cd0fF517Dc572fA74d8D22A0"
    ctx['COUNTRIES'] = Country.objects.all()

    return ctx
