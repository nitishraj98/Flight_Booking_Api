from application.controller import *
from datetime import datetime




def flight_search():
    # Get the request payload
    payload = request.get_json()
    journeytype = payload['JourneyType']
    session['journeytype']=journeytype

    tob_api_details = db.session.query(TobApiDetails).first()
    token_id = tob_api_details.tokenId if tob_api_details else None
    if token_id:
        payload['TokenId'] = token_id
        payload['EndUserIp'] = request.headers.get('X-Forwarded-For', request.remote_addr)
        total_count = int(payload['AdultCount'])+int(payload['ChildCount'])+int(payload['InfantCount'])
        session['total_count'] = total_count
    
    
    if int(payload['AdultCount'])>0 and total_count<10:
     # Construct the API URL 
        base_url = app.config['BASE_URL']
        api_url = f"{base_url}/Search"

        response = requests.post(api_url, json=payload) 
    

        # Process the response and return the result
        if response.status_code == 200:
            result = response.json()
            
            result_index = result.get('ResultIndex')
            trace_id = result.get('TraceId')
            ip = payload['EndUserIp']
            origin = payload.get('Origin')
            destination = payload.get('Destination')
            current_datetime = datetime.now()
            created_at = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            updated_at = created_at
            is_active= True

            search_details = SearchDetails(result_index=result_index, trace_id=trace_id, ip=ip, origin=origin, destination=destination, is_active=is_active,created_at=created_at, updated_at=updated_at)
            
            db.session.add(search_details)
            db.session.commit()
            db.session.flush()

            return jsonify(result)
    else:
        return jsonify({'message':'Adult count must be 1 or more than 1 and total count must be less than 10'})







def flight_search_farerules():
    # Get the request payload
    payload = request.get_json()

    # Fetch values from the database
    search_details = db.session.query(SearchDetails).order_by(SearchDetails.id.desc()).first()
    tob_api_details = db.session.query(TobApiDetails).first()
    token_id = tob_api_details.tokenId if tob_api_details else None
    end_user_ip = search_details.ip if search_details else None
    
    # Update the payload with the fetched values
    if end_user_ip:
        payload['EndUserIp'] = end_user_ip
    if token_id:
        payload['TokenId'] = token_id

    # Construct the API URL
    base_url = app.config['BASE_URL'] 
    api_url = f"{base_url}/FareRule"

    response = requests.post(api_url, json=payload)               

    # Process the response and return the result
    if response.status_code == 200:
        result = response.json() 
        uid = str(uuid.uuid4())
        current_datetime = datetime.now()
        create_at = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        update_at = create_at
        is_active= True
        result_index = payload['ResultIndex']
        trace_id = payload['TraceId']
        journey_type =session.get('journeytype')
        fare_rule = json.dumps(result)
        flight_details = FlightDetails(uuid=uid,is_active=is_active,create_at=create_at, update_at=update_at,result_index=result_index,trace_id=trace_id,fare_rules=fare_rule,journey_type=journey_type)
        db.session.add(flight_details)
        db.session.commit()
        db.session.flush()
    
        return jsonify(result)
    else:
        return jsonify({'error':'Something went wrong'})
    

    


def flight_search_fareQuote():
    payload = request.get_json()
    # Fetch values from the database
    search_details = db.session.query(SearchDetails).order_by(SearchDetails.id.desc()).first()
    tob_api_details = db.session.query(TobApiDetails).first()
    token_id = tob_api_details.tokenId if tob_api_details else None
    end_user_ip = search_details.ip if search_details else None

    # Update the payload with the fetched values
    if end_user_ip:
        payload['EndUserIp'] = end_user_ip
    if token_id:
        payload['TokenId'] = token_id
    

    # Construct the API URL
    base_url = app.config['BASE_URL']
    api_url = f"{base_url}/FareQuote"

    response = requests.post(api_url, json=payload)

    # Process the response and return the result
    if response.status_code == 200:
        result = response.json()
        flight_details = db.session.query(FlightDetails).order_by(FlightDetails.id.desc()).first()
        is_lcc = result['Response']['Results']['IsLCC']
        Published_Fare = result['Response']['Results']['Fare']['PublishedFare']
        fare_quote = json.dumps(result)
        if flight_details:
            flight_details.fare_quote = fare_quote
            flight_details.is_lcc = is_lcc
            db.session.commit()
            db.session.flush()

        # Store the value in a session variable
        session['is_lcc'] = is_lcc
        session['Published_Fare'] = Published_Fare
        
        print("is_lcc",is_lcc)
        print("published_fare",Published_Fare)   
    
        fare_breakdown = result['Response']['Results']['FareBreakdown']
        Adult,Child,Infant = {},{},{}
        for passenger_type in fare_breakdown:
            pas_type = passenger_type['PassengerType']
            if pas_type == 1:
                Adult_BaseFare = passenger_type['BaseFare'] / passenger_type['PassengerCount']
                Adult_Tax = passenger_type['Tax'] / passenger_type['PassengerCount']
                Adult_othercharge = passenger_type.get('Fare', {}).get('OtherCharges', 0)/ passenger_type['PassengerCount']
                Adult_yqtax = passenger_type['YQTax'] / passenger_type['PassengerCount']
                Adult_AdditionalTxnFeeOfrd = passenger_type['AdditionalTxnFeeOfrd'] / passenger_type['PassengerCount']
                Adult_AdditionalTxnFeePub = passenger_type['AdditionalTxnFeePub'] / passenger_type['PassengerCount']
                Adult = {"Adult_BaseFare": Adult_BaseFare, "Adult_Tax": Adult_Tax, "Adult_othercharge": Adult_othercharge, "Adult_yqtax": Adult_yqtax,"Adult_AdditionalTxnFeeOfrd":Adult_AdditionalTxnFeeOfrd,"Adult_AdditionalTxnFeePub":Adult_AdditionalTxnFeePub}
                session['Adult'] = Adult
            elif pas_type == 2:
                Child_BaseFare = passenger_type['BaseFare'] / passenger_type['PassengerCount']
                Child_Tax = passenger_type['Tax'] / passenger_type['PassengerCount']
                Child_othercharge = passenger_type.get('Fare', {}).get('OtherCharges', 0) / passenger_type['PassengerCount']
                Child_yqtax = passenger_type['YQTax'] / passenger_type['PassengerCount']
                Child_AdditionalTxnFeeOfrd= passenger_type['AdditionalTxnFeeOfrd'] / passenger_type['PassengerCount']
                Child_AdditionalTxnFeePub = passenger_type['AdditionalTxnFeePub'] / passenger_type['PassengerCount']
                Child = {"Child_BaseFare":Child_BaseFare, "Child_Tax":Child_Tax, "Child_othercharge":Child_othercharge, "Child_yqtax":Child_yqtax,"Child_AdditionalTxnFeeOfrd": Child_AdditionalTxnFeeOfrd,"Child_AdditionalTxnFeePub":Child_AdditionalTxnFeePub}
                session['Child'] = Child
                
            elif pas_type == 3:
                Infant_BaseFare = passenger_type['BaseFare'] / passenger_type['PassengerCount']
                Infant_Tax = passenger_type['Tax'] / passenger_type['PassengerCount']
                Infant_othercharge = passenger_type.get('Fare', {}).get('OtherCharges', 0)/ passenger_type['PassengerCount']
                Infant_yqtax = passenger_type['YQTax'] / passenger_type['PassengerCount'] 
                Infant_AdditionalTxnFeeOfrd = passenger_type['AdditionalTxnFeeOfrd'] / passenger_type['PassengerCount']
                Infant_AdditionalTxnFeePub = passenger_type['AdditionalTxnFeePub'] / passenger_type['PassengerCount']
            
                Infant = {"Infant_BaseFare":Infant_BaseFare, "Infant_Tax":Infant_Tax,"Infant_othercharge":Infant_othercharge, "Infant_yqtax":Infant_yqtax,"Infant_AdditionalTxnFeeOfrd":Infant_AdditionalTxnFeeOfrd, "Infant_AdditionalTxnFeePub":Infant_AdditionalTxnFeePub}
                session['Infant'] = Infant

        
        return jsonify(result)
    else:
        return jsonify({'error': 'Something went wrong'})

    
    


def flight_search_SSR(): 
    payload = request.get_json()
    # Fetch values from the database
    search_details = db.session.query(SearchDetails).order_by(SearchDetails.id.desc()).first()
    tob_api_details = db.session.query(TobApiDetails).first()
    token_id = tob_api_details.tokenId if tob_api_details else None
    end_user_ip = search_details.ip if search_details else None
    
    # Update the payload with the fetched values
  
    if end_user_ip:
         payload['EndUserIp'] = end_user_ip
    if token_id:
        payload['TokenId'] = token_id
   
     # Construct the API URL
    base_url = app.config['BASE_URL']
    api_url = f"{base_url}/SSR"

    response = requests.post(api_url, json=payload)


    # Process the response and return the result
    if response.status_code == 200:
        result = response.json()
        return jsonify(result)
    else:
        return jsonify({'error': 'Something went wrong'})
    


def add_on_ssr():
    payload = request.get_json()
    if not payload:
        return jsonify({'success':False})
    
    meal_price = None
    seat_price = None

    # Find the selected meal in the payload
    for meal in payload.get('Meal', []):
            meal_price = meal.get('Price')
            print(meal_price)
            break
  
    # Find the selected seat in the SSR response
    for seat in payload.get('Seats', []):
            seat_price = seat.get('Price')
            print(seat_price)
            break
    
    # Find the selected seat in the SSR response
    for baggage in payload.get('Baggage', []):
            baggage_price = baggage.get('Price')
            print(baggage_price)
            break
    user_uuid = str(uuid.uuid4())
    flightuuid = str(uuid.uuid4())
    current_datetime = datetime.now()
    create_at = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    update_at = create_at
    userid = session.get('userid')
    amount = int(meal_price+seat_price+baggage_price)
    ssr = json.dumps(payload)
    ssr_details = SSRDetails(uuid=user_uuid,ssr_details=ssr,user_id=userid,flight_uuid=flightuuid,create_at=create_at, update_at=update_at,amount=amount)
    db.session.add(ssr_details)
    db.session.commit()
    db.session.flush()

    # Store the meal and seat prices in the session
    session['meal_price'] = meal_price
    session['seat_price'] = seat_price
    session['baggage_price'] = baggage_price

    return jsonify({'success': True})

    
    
    
def get_fare_calendar():
    # Get the request payload
    payload = request.get_json()
     # Fetch values from the database
    search_details = db.session.query(SearchDetails).order_by(SearchDetails.id.desc()).first()
    tob_api_details = db.session.query(TobApiDetails).first()
    token_id = tob_api_details.tokenId if tob_api_details else None
    end_user_ip = search_details.ip if search_details else None

    # Update the payload with the fetched values
    if end_user_ip:
         payload['EndUserIp'] = end_user_ip
    if token_id:
        payload['TokenId'] = token_id 
    

     # Construct the API URL  
    base_url = app.config['BASE_URL']
    api_url = f"{base_url}/GetCalendarFare"

    response = requests.post(api_url, json=payload)

    # Process the response and return the result
    if response.status_code == 200:
        result = response.json()
        return jsonify(result)
    else:
        return jsonify({'error': 'Something went wrong'})
    


def update_fare_calendar():
    # Get the request payload
    payload = request.get_json()
     # Fetch values from the database
    search_details = db.session.query(SearchDetails).order_by(SearchDetails.id.desc()).first()
    tob_api_details = db.session.query(TobApiDetails).first()
    token_id = tob_api_details.tokenId if tob_api_details else None
    end_user_ip = search_details.ip if search_details else None

    # Update the payload with the fetched values
    if end_user_ip:
         payload['EndUserIp'] = end_user_ip
    if token_id:
        payload['TokenId'] = token_id 
    

     # Construct the API URL 
    base_url = app.config['BASE_URL']
    api_url = f"{base_url}/UpdateCalendarFareOfDay"

    response = requests.post(api_url, json=payload)

    # Process the response and return the result
    if response.status_code == 200:
        result = response.json()
        return jsonify(result)
    else:
        return jsonify({'error': 'Something went wrong'})
    


    
def booking_details():
    # Get the request payload
    payload = request.get_json()
    # Fetch values from the database
    search_details = db.session.query(SearchDetails).order_by(SearchDetails.id.desc()).first()
    tob_api_details = db.session.query(TobApiDetails).first()
    token_id = tob_api_details.tokenId if tob_api_details else None
    end_user_ip = search_details.ip if search_details else None

    # Update the payload with the fetched values
    if end_user_ip:
         payload['EndUserIp'] = end_user_ip
    if token_id:
        payload['TokenId'] = token_id 

     # Construct the API URL
    base_url = app.config['BASE_URL']
    api_url = f"{base_url}/GetBookingDetails"

    response = requests.post(api_url, json=payload)

    # Process the response and return the result
    if response.status_code == 200:
        result = response.json()
        return jsonify({"Result":result})
    else:
        return jsonify({'error': 'Something went wrong'})
    


def process_ticket():
    payload = request.get_json()
    flight_details = db.session.query(FlightDetails).order_by(FlightDetails.id.desc()).first()
    is_lcc = flight_details.is_lcc if flight_details else None

    if is_lcc == 0:
        ticket_respons = ticket_for_false_lcc(payload)
        userid = session.get('userid')

        current_datetime = datetime.now()
        create_at = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        update_at = create_at
        is_active= True
        pid = db.session.query(PaymentInformation).order_by(PaymentInformation.id.desc()).first()
        paymentid = pid.id if pid else None
        bookinghistory = json.dumps(ticket_respons)
        bookingid = ticket_respons['book']['Response']['Response']['BookingId']
        pnr = ticket_respons['book']['Response']['Response']['PNR']
        booking_information = BookingInformation(user_id=userid,is_active=is_active,created_at=create_at, updated_at=update_at,booking_history=bookinghistory,pnr=pnr,booking_id=bookingid,payment_id=paymentid)
        db.session.add(booking_information)
        db.session.commit()
        db.session.flush()
        session.clear()
        return jsonify({"Data": ticket_respons})
        
    elif is_lcc == 1:
        ticket_response = ticket_for_true_lcc(payload)
        userid = session.get('userid')

        current_datetime = datetime.now()
        create_at = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        update_at = create_at
        is_active= True
        pid = db.session.query(PaymentInformation).order_by(PaymentInformation.id.desc()).first()
        paymentid = pid.id if pid else None
        bookinghistory = json.dumps(ticket_response)
        bookingid = ticket_response['Response']['Response']['BookingId']
        pnr = ticket_response['Response']['Response']['PNR']
        booking_information = BookingInformation(user_id=userid,is_active=is_active,created_at=create_at, updated_at=update_at,booking_history=bookinghistory,pnr=pnr,booking_id=bookingid,payment_id=paymentid)
        db.session.add(booking_information)
        db.session.commit()
        db.session.flush()
        session.clear()
        # Return the ticket response
        return jsonify({"Data": {"ticket": ticket_response}})
    

 
def release_pnr_request():
    payload = request.get_json()
    # Fetch values from the database
    search_details = db.session.query(SearchDetails).order_by(SearchDetails.id.desc()).first()
    tob_api_details = db.session.query(TobApiDetails).first()
    token_id = tob_api_details.tokenId if tob_api_details else None
    end_user_ip = search_details.ip if search_details else None

    # Update the payload with the fetched values
    if end_user_ip:
         payload['EndUserIp'] = end_user_ip
    if token_id:
        payload['TokenId'] = token_id 

     # Construct the API URL
    base_url = app.config['BASE_URL']
    api_url = f"{base_url}/ReleasePNRRequest"

    response = requests.post(api_url, json=payload) 

    if response.status_code == 200:
        result = response.json()
        return jsonify(result)
    else:
        return jsonify({'error': 'Something went wrong'})  
    



def send_change_request():
    payload = request.get_json()
    # Fetch values from the database
    search_details = db.session.query(SearchDetails).order_by(SearchDetails.id.desc()).first()
    tob_api_details = db.session.query(TobApiDetails).first()
    token_id = tob_api_details.tokenId if tob_api_details else None
    end_user_ip = search_details.ip if search_details else None

    # Update the payload with the fetched values
    if end_user_ip:
         payload['EndUserIp'] = end_user_ip
    if token_id:
        payload['TokenId'] = token_id 

     # Construct the API URL
    base_url = app.config['BASE_URL']
    api_url = f"{base_url}/SendChangeRequest"

    response = requests.post(api_url, json=payload)

    if response.status_code == 200:
        result = response.json()
        return jsonify(result)
    else:
        return jsonify({'error': 'Something went wrong'})   




def send_change_request_status():
    payload = request.get_json()
    # Fetch values from the database
    search_details = db.session.query(SearchDetails).order_by(SearchDetails.id.desc()).first()
    tob_api_details = db.session.query(TobApiDetails).first()
    token_id = tob_api_details.tokenId if tob_api_details else None
    end_user_ip = search_details.ip if search_details else None

    # Update the payload with the fetched values
    if end_user_ip:
         payload['EndUserIp'] = end_user_ip
    if token_id:
        payload['TokenId'] = token_id 

     # Construct the API URL
    base_url = app.config['BASE_URL']
    api_url = f"{base_url}/GetChangeRequestStatus"

    response = requests.post(api_url, json=payload)

    if response.status_code == 200:
        result = response.json()
        return jsonify(result)
    else:
        return jsonify({'error': 'Something went wrong'})  
    




def cancellation_charge():
    payload = request.get_json()
    # Fetch values from the database
    search_details = db.session.query(SearchDetails).order_by(SearchDetails.id.desc()).first()
    tob_api_details = db.session.query(TobApiDetails).first()
    token_id = tob_api_details.tokenId if tob_api_details else None
    end_user_ip = search_details.ip if search_details else None

    # Update the payload with the fetched values
    if end_user_ip:
         payload['EndUserIp'] = end_user_ip
    if token_id:
        payload['TokenId'] = token_id 

     # Construct the API URL
    base_url = app.config['BASE_URL']
    api_url = f"{base_url}/GetCancellationCharges  "
    response = requests.post(api_url, json=payload)

    if response.status_code == 200:
        result = response.json()
        return jsonify(result)
    else:
        return jsonify({'error': 'Something went wrong'})  
    


def City_Details():
    city_details = AirportCityCountryDetails.query.all()
    schema = AirportCityCountryDetailsSchema(many=True)
    result = schema.dump(city_details)
    
    return jsonify(result)

        



     



   


    









    




     





        
        
 
        
        







    
    