import os
#import sched 
import time
import pytz
from iqoptionapi.stable_api import IQ_Option
from flask import Flask, request, jsonify

app = Flask(__name__)
#scheduler = sched.scheduler(time.time, time.sleep)

@app.route('/')
def hello():
    return 'Hello World!'

# GET
@app.route('/balance/<email1>/<pass1>/<mode1>')
def balance(email1,pass1,mode1):
    from iqoptionapi.stable_api import IQ_Option
    Iq=IQ_Option(str(email1),str(pass1))
    Iq.connect()
    Iq.change_balance(mode1)
    return str(Iq.get_balance())

# GET
@app.route('/close/<email1>/<pass1>/<order_id>/<mode>')
def close(email1,pass1,order_id,mode):
    from iqoptionapi.stable_api import IQ_Option
    Iq=IQ_Option(str(email1),str(pass1))
    Iq.connect()
    
    Iq.change_balance(mode)
    return str(Iq.close_position(order_id))

# GET /open/email/pass/PRACTICE/crypto/ETHUSD/buy/10
@app.route('/open/<email1>/<pass1>/<mode>/<instrument_type>/<instrument_id>/<side>/<amount>')
def open(email1,pass1,mode,instrument_type,instrument_id,side,amount):
    from iqoptionapi.stable_api import IQ_Option
    Iq=IQ_Option(str(email1),str(pass1))
    Iq.connect()
    
        
    Iq.change_balance(mode)
    instrument_type=instrument_type
    instrument_id=instrument_id
    side=side#input:"buy"/"sell"
    amount=amount#input how many Amount you want to play
    order_id =0
    
    leverage =3
    
    leverages1 = str(Iq.get_available_leverages(instrument_type,instrument_id))
    if (leverages1.find("1000") != -1): 
        leverage =1000
    elif(leverages1.find("500") != -1): 
        leverage =500
    elif(leverages1.find("300") != -1): 
        leverage =300
    elif(leverages1.find("200") != -1): 
        leverage =200
        
    #leverage =500
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
    
    try:
        check,order_id=Iq.buy_order(instrument_type=instrument_type, instrument_id=instrument_id,
                    side=side, amount=amount,leverage=leverage,
                    type=type,limit_price=limit_price, stop_price=stop_price,
                    stop_lose_value=stop_lose_value, stop_lose_kind=stop_lose_kind,
                    take_profit_value=take_profit_value, take_profit_kind=take_profit_kind,
                    use_trail_stop=use_trail_stop, auto_margin_call=auto_margin_call,
                    use_token_for_commission=use_token_for_commission)
    except:
        order_id=0
        
    print(Iq.get_order(order_id))
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
