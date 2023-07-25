from application.controller import *
from datetime import datetime




def flight_search():
    # Get the request payload
    payload = request.get_json()

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
            

            return jsonify(result)
    else: 
        return jsonify({'error': 'An error occurred'}) 







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
        return jsonify(result)
    else:
        return jsonify({'error': 'An error occurred'})

    


def flight_search_fareQuote():
    # Get the request payload
    payload = request.get_json()
    # print(payload)

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
        # print("&&&&&&&&&&&&&&&&&&&&",result)

        # Get the value of IsLCC
        is_lcc = result['Response']['Results']['IsLCC']
        Published_Fare = result['Response']['Results']['Fare']['PublishedFare']

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

                # print("Adult_BaseFare", Adult_BaseFare, "\nAdult_Tax", Adult_Tax, "\nAdult_othercharge", Adult_othercharge, "\nAdult_yqtax", Adult_yqtax,
                #       "\nAdult_AdditionalTxnFeeOfrd", Adult_AdditionalTxnFeeOfrd, "\nAdult_AdditionalTxnFeePub", Adult_AdditionalTxnFeePub)
                Adult = {"Adult_BaseFare": Adult_BaseFare, "Adult_Tax": Adult_Tax, "Adult_othercharge": Adult_othercharge, "Adult_yqtax": Adult_yqtax,"Adult_AdditionalTxnFeeOfrd":Adult_AdditionalTxnFeeOfrd,"Adult_AdditionalTxnFeePub":Adult_AdditionalTxnFeePub}
                session['Adult'] = Adult
            if pas_type == 2:
                Child_BaseFare = passenger_type['BaseFare'] / passenger_type['PassengerCount']
                Child_Tax = passenger_type['Tax'] / passenger_type['PassengerCount']
                Child_othercharge = passenger_type.get('Fare', {}).get('OtherCharges', 0) / passenger_type['PassengerCount']
                Child_yqtax = passenger_type['YQTax'] / passenger_type['PassengerCount']
                Child_AdditionalTxnFeeOfrd= passenger_type['AdditionalTxnFeeOfrd'] / passenger_type['PassengerCount']
                Child_AdditionalTxnFeePub = passenger_type['AdditionalTxnFeePub'] / passenger_type['PassengerCount']

                # print("Child_BaseFare", Child_BaseFare, "\nChild_Tax", Child_Tax, "\nChild_othercharge", Child_othercharge, "\nChild_yqtax", Child_yqtax,
                #       "\nChild_AdditionalTxnFeeOfrd", Child_AdditionalTxnFeeOfrd, "\nChild_AdditionalTxnFeePub", Child_AdditionalTxnFeePub)
                Child = {"Child_BaseFare":Child_BaseFare, "Child_Tax":Child_Tax, "Child_othercharge":Child_othercharge, "Child_yqtax":Child_yqtax,"Child_AdditionalTxnFeeOfrd": Child_AdditionalTxnFeeOfrd,"Child_AdditionalTxnFeePub":Child_AdditionalTxnFeePub}
                session['Child'] = Child
                
            if pas_type == 3:
                Infant_BaseFare = passenger_type['BaseFare'] / passenger_type['PassengerCount']
                Infant_Tax = passenger_type['Tax'] / passenger_type['PassengerCount']
                Infant_othercharge = passenger_type.get('Fare', {}).get('OtherCharges', 0)/ passenger_type['PassengerCount']
                Infant_yqtax = passenger_type['YQTax'] / passenger_type['PassengerCount'] 
                Infant_AdditionalTxnFeeOfrd = passenger_type['AdditionalTxnFeeOfrd'] / passenger_type['PassengerCount']
                Infant_AdditionalTxnFeePub = passenger_type['AdditionalTxnFeePub'] / passenger_type['PassengerCount']

                # print("Infant_BaseFare", Infant_BaseFare, "\nInfant_Tax", Infant_Tax, "\nInfant_othercharge", Infant_othercharge, "\nInfant_yqtax", Infant_yqtax,
                #       "\nInfant_AdditionalTxnFeeOfrd", Infant_AdditionalTxnFeeOfrd, "\nInfant_AdditionalTxnFeePub", Infant_AdditionalTxnFeePub)
                
            
            
                Infant = {"Infant_BaseFare":Infant_BaseFare, "Infant_Tax":Infant_Tax,"Infant_othercharge":Infant_othercharge, "Infant_yqtax":Infant_yqtax,"Infant_AdditionalTxnFeeOfrd":Infant_AdditionalTxnFeeOfrd, "Infant_AdditionalTxnFeePub":Infant_AdditionalTxnFeePub}
                session['Infant'] = Infant

        
            return jsonify(result)
    else:
        return jsonify({'error': 'An error occurred'})

    
    


def flight_search_SSR():
    # Get the request payload 
    payload = request.get_json()
    # print(payload)

    # # Fetch values from the database
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
        return jsonify({'error': 'An error occurred'})
    


def add_on_ssr():
    payload = request.get_json()
    print(payload)
    meal_selected = payload.get('Meal', [{}])[0].get('Code')
    seat_selected = payload.get('Seats', [{}])[0].get('SeatNo')

    # Retrieve the meal and seat prices from the SSR response
    meal_price = None
    seat_price = None

    # Find the selected meal in the payload
    for meal in payload.get('Meal', []):
        if meal['Code'] == meal_selected:
            meal_price = meal.get('Price')
            print(meal_price)
            break

    # Find the selected seat in the SSR response
    for seat in payload.get('Seats', []):
        if seat['SeatNo'] == seat_selected:
            seat_price = seat.get('Price')
            print(seat_price)
            break

    # Store the meal and seat prices in the session
    session['meal_price'] = meal_price
    session['seat_price'] = seat_price

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
        return jsonify({'error': 'An error occurred'})
    


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
        return jsonify({'error': 'An error occurred'})
    


    
def booking_details():
    # Get the request payload
    payload = request.get_json()
    Adult = session.get('Adult')
    Child = session.get('Child')
    Infant = session.get('Infant')
    # print(payload)
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
        return jsonify({"Adultfare_for_one":Adult,"Childfare_for_one":Child,"Infantfare_for_one":Infant,"Result":result})
    else:
        return jsonify({'error': 'An error occurred'})
    


def process_ticket():
    is_lcc = session.get('is_lcc')
    payload = request.get_json()

    if is_lcc is False:
        # Call the book() function to make the booking request
        book_response = book(payload)
        search_details = db.session.query(SearchDetails).order_by(SearchDetails.id.desc()).first()
        tob_api_details = db.session.query(TobApiDetails).first()
        token_id = tob_api_details.tokenId if tob_api_details else None
        end_user_ip = search_details.ip if search_details else None


        # Check if the book() function succeeded
        if 'Response' in book_response:
            # print("****************",book_response)
            # Obtain the PNR and BookingId from the book_response
            if book_response['Response']['Response'] is None:
                return json.jsonify({"msg":book_response['Response']['Error']['ErrorMessage']}),400

            pnr = book_response['Response']['Response']['PNR']
            booking_id = book_response['Response']['Response']['BookingId']
            trace_id = book_response['Response']['TraceId']
            # Construct the payload for the ticket() function using the obtained values
            ticket_payload = {
                "PNR": pnr,
                "BookingId": booking_id,
                "TraceId":trace_id,
                "TokenId":token_id,
                "EndUserIp":end_user_ip
            }
            print("ticket_payload",ticket_payload)

            

                # Call the ticket() function again with the updated payload
            ticket_response = ticket(ticket_payload)

                # Return the responses
            return jsonify({"Data": {"book": book_response, "ticket": ticket_response}})
            
        else:
            # Handle the case where the book() function failed
            return jsonify({'error': 'Book function failed'})
    elif is_lcc is True:
        # Call the ticket() function directly
        ticket_response = ticket(payload)
        # Return the ticket response
        return jsonify({"Data": {"ticket": ticket_response}})
    else:
        return jsonify({'error': 'Invalid'})


 
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
        return jsonify({'error': 'An error occured'})  
    



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
        return jsonify({'error': 'An error occured'})   




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
        return jsonify({'error': 'An error occured'})  
    




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
        return jsonify({'error': 'An error occured'})  
    


def City_Details():
    city_details = AirportCityCountryDetails.query.all()

    # if not city_details:
    #     # Handle the case when there are no records found
    #     return jsonify([])

    schema = AirportCityCountryDetailsSchema(many=True)
    result = schema.dump(city_details)
    
    return jsonify(result)

        



     



   


    









    




     





        
        
 
        
        







    
    

