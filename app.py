import os
#import sched 
import time
from iqoptionapi.stable_api import IQ_Option
from flask import Flask

app = Flask(__name__)
#scheduler = sched.scheduler(time.time, time.sleep)

    
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
@app.route('/open/<mode>/<instrument_type>/<instrument_id>/<side>/<amount>/<sleep>')
def open(mode,instrument_type,instrument_id,side,amount,sleep):
    from iqoptionapi.stable_api import IQ_Option
    Iq=IQ_Option("elamparuthik1991@gmail.com","Chennai@1991")
    Iq.connect()
    
    Iq.change_balance(mode)
    instrument_type=instrument_type
    instrument_id=instrument_id
    side=side#input:"buy"/"sell"
    amount=amount#input how many Amount you want to play
    
    leverage =300
    
    leverages1 = Iq.get_available_leverages(instrument_type,instrument_id)
    if (leverages1.find("1000") != -1): 
        leverage =1000
    elif(leverages1.find("500") != -1): 
        leverage =500
    elif(leverages1.find("300") != -1): 
        leverage =300
    elif(leverages1.find("200") != -1): 
        leverage =200
    
    
    #"leverage"="Multiplier"
    #leverage=3#you can get more information in get_available_leverages()
    
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
    Iq.get_order(order_id)
    #print(Iq.get_positions(instrument_type))
    #print(Iq.get_position_history(instrument_type))
    
    #scheduler.enter(sleep*60, 1, Iq.close_position(order_id), (' 2nd', ))
    # executing the events 
    #scheduler.run()
    
    #print(Iq.get_overnight_fee(instrument_type,instrument_id))

    return str(order_id)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
