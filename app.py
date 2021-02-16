import os
from iqoptionapi.stable_api import IQ_Option
from flask import Flask

app = Flask(__name__)


    
@app.route('/')
def hello():
    return 'Hello World!'

# GET
@app.route('/balance')
def balance():
    from iqoptionapi.stable_api import IQ_Option
    Iq=IQ_Option("elamparuthik1991@gmail.com","Chennai@1991")
    Iq.connect()
    Iq.change_balance("REAL")
    return str(Iq.get_balance())

# GET
@app.route('/close/<order_id>/<mode>')
def close(order_id,mode):
    from iqoptionapi.stable_api import IQ_Option
    Iq=IQ_Option("elamparuthik1991@gmail.com","Chennai@1991")
    Iq.connect()
    
    Iq.change_balance(mode)
    return str(Iq.close_position(order_id))

# GET
@app.route('/open/<mode>/<instrument_type>/<instrument_id>/<side>/<amount>/')
def open(mode,instrument_type,instrument_id,side,amount):
    from iqoptionapi.stable_api import IQ_Option
    Iq=IQ_Option("elamparuthik1991@gmail.com","Chennai@1991")
    Iq.connect()
    
    Iq.change_balance(mode)
    instrument_type=instrument_type
    instrument_id=instrument_id
    side=side#input:"buy"/"sell"
    amount=amount#input how many Amount you want to play
    
    #"leverage"="Multiplier"
    leverage=3#you can get more information in get_available_leverages()
    
    type="market"#input:"market"/"limit"/"stop"
    
    #for type="limit"/"stop"
    
    # only working by set type="limit"
    limit_price=None#input:None/value(float/int)
    
    # only working by set type="stop"
    stop_price=None#input:None/value(float/int)
    
    #"percent"=Profit Percentage
    #"price"=Asset Price
    #"diff"=Profit in Money
    
    stop_lose_kind="percent"#input:None/"price"/"diff"/"percent"
    stop_lose_value=200#input:None/value(float/int)
    
    take_profit_kind=None#input:None/"price"/"diff"/"percent"
    take_profit_value=None#input:None/value(float/int)
    
    #"use_trail_stop"="Trailing Stop"
    use_trail_stop=True#True/False
    
    #"auto_margin_call"="Use Balance to Keep Position Open"
    auto_margin_call=False#True/False
    #if you want "take_profit_kind"&
    #            "take_profit_value"&
    #            "stop_lose_kind"&
    #            "stop_lose_value" all being "Not Set","auto_margin_call" need to set:True
    
    use_token_for_commission=False#True/False
    
    check,order_id=Iq.buy_order(instrument_type=instrument_type, instrument_id=instrument_id,
                side=side, amount=amount,leverage=leverage,
                type=type,limit_price=limit_price, stop_price=stop_price,
                stop_lose_value=stop_lose_value, stop_lose_kind=stop_lose_kind,
                take_profit_value=take_profit_value, take_profit_kind=take_profit_kind,
                use_trail_stop=use_trail_stop, auto_margin_call=auto_margin_call,
                use_token_for_commission=use_token_for_commission)
    print(Iq.get_order(order_id))
    print(Iq.get_positions(instrument_type))
    print(Iq.get_position_history(instrument_type))
    print(Iq.get_available_leverages(instrument_type,instrument_id))
    #print(Iq.close_position(order_id))
    print(Iq.get_overnight_fee(instrument_type,instrument_id))

    return str(order_id)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
