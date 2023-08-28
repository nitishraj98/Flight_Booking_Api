from application.controller import *
from flask import session
import uuid
from datetime import datetime
from application.models.insurance_details import *
from application.models.flight_details import FlightDetails,FlightDetails_schema
from application.models.passenger_details import PassengerDetails
from application.models.book_details import *
from application.models.ticket_details import * 




def calculate_insurance(insurance_selected):
    total_count = session.get('total_count')
    
    
    # Check if total_count is None or not
    if total_count is None:
        total_count = 0  # Assign a default value of 0 if total_count is None
    if insurance_selected:
        insurance_amount = 199 * total_count 
        Price = insurance_amount
        user_uuid = str(uuid.uuid4())
        flightuuid = str(uuid.uuid4())
        userid = session.get('userid')
        current_datetime = datetime.now()
        create_at = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        update_at = create_at
        insurance_details = InsuranceDetails(uuid=user_uuid,userid=userid,flight_uuid=flightuuid,price=Price,created_at=create_at, updated_at=update_at)
        db.session.add(insurance_details)
        db.session.commit()
        db.session.flush()
        total_amount = insurance_amount
        return total_amount   
  



def book(payload):
    # Fetch values from the database 
    search_details = db.session.query(SearchDetails).order_by(SearchDetails.id.desc()).first()
    tob_api_details = db.session.query(TobApiDetails).first()
    flight_details = db.session.query(FlightDetails).order_by(FlightDetails.id.desc()).first()
    token_id = tob_api_details.tokenId if tob_api_details else None
    end_user_ip = search_details.ip if search_details else None
    Trace_id = flight_details.trace_id if flight_details else None
    Result_index = flight_details.result_index if flight_details else None
    
    Adult = session.get('Adult')
    Child = session.get('Child')
    Infant = session.get('Infant')
    pasngr = payload["Passengers"]
    for i in range(len(pasngr)):
       
        if i==0:
            pasngr[i]['IsLeadPax']=True
        else:
            pasngr[i]['IsLeadPax']=False
    
 
    for passenger in pasngr:
        
        if passenger['PaxType'] == 1:
            fare = Adult
        elif passenger['PaxType'] == 2:
            fare = Child
        else:
            fare = Infant
        passenger['Fare'] = fare
        


    # Update the payload with the fetched values
    if end_user_ip:
        payload['EndUserIp'] = end_user_ip
    if token_id:
        payload['TokenId'] = token_id
    if Trace_id:
        payload['TraceId'] = Trace_id
    if Result_index:
        payload['ResultIndex'] = Result_index
    
        # Construct the API URL
        base_url = app.config['BASE_URL']  
        api_url = f"{base_url}/Book"              
    
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            result = response.json()
            user_uuid = str(uuid.uuid4())
            flightuuid = str(uuid.uuid4())
            current_datetime = datetime.now()
            create_at = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            update_at = create_at
            is_active= True
            userid = session.get('userid')
            passengerdetails = json.dumps(payload)
            Bookingdetails = json.dumps(result)
            total_amount = session.get('total_amount')
            passenger_details = PassengerDetails(uuid=user_uuid,passenger_details=passengerdetails,user_id=userid,flight_uuid=flightuuid,is_active=is_active,created_at=create_at, updated_at=update_at)
            booking_details = BookDetails(user_id=userid,is_active=is_active,create_at=create_at, update_at=update_at,total_amount=total_amount,booking_details=Bookingdetails)
            db.session.add(passenger_details)
            db.session.add(booking_details)
            db.session.commit()
            db.session.flush()
    
            return (result)
         
    else:
        return 'An error occurred in book response'

        
def ticket_for_false_lcc(payload):
    # Call the book() function to make the booking request
    book_response = book(payload)
    search_details = db.session.query(SearchDetails).order_by(SearchDetails.id.desc()).first()
    tob_api_details = db.session.query(TobApiDetails).first()
    token_id = tob_api_details.tokenId if tob_api_details else None
    end_user_ip = search_details.ip if search_details else None


    # Check if the book() function succeeded
    if 'Response' in book_response:
        # Obtain the PNR and BookingId from the book_response
        if book_response['Response']['Response'] is None:
            return book_response['Response']['Error']['ErrorMessage']

        pnr = book_response['Response']['Response']['PNR']
        booking_id = book_response['Response']['Response']['BookingId']
        trace_id = book_response['Response']['TraceId']
        # Construct the payload for the ticket() function using the obtained values
        ticket_payload = {
            "PNR": pnr,
            "BookingId": booking_id,
            "TraceId":trace_id,
            "TokenId":token_id,
            "EndUserIp":end_user_ip,
            
        } 

        # Construct the API URL
        base_url = app.config['BASE_URL']
        api_url = f"{base_url}/Ticket"

        ticket_response = requests.post(api_url, json=ticket_payload)
        if ticket_response.status_code == 200: 
            result = ticket_response.json()
            current_datetime = datetime.now()
            create_at = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            update_at = create_at
            is_active= True
            userid = session.get('userid')
            
            ticketdetails = json.dumps(result)
            
            booking_id = book_response['Response']['Response']
            
            if not booking_id:
                return result['Response']['Error']['ErrorMessage']
            booking_id = book_response['Response']['Response']['BookingId']
    
            
            ticket_details = TicketDetails(user_id=userid,is_active=is_active,created_at=create_at, updated_at=update_at,ticket_details=ticketdetails,booking_id=booking_id)
            db.session.add(ticket_details)
            db.session.commit()
            db.session.flush()
            
            # Return the responses
            return {"book": book_response, "ticket": result}
        
    else:
        # Handle the case where the book() function failed
        return {"msg":"Book function failed"}
  
        
        

             


def ticket_for_true_lcc(payload):  
    # Fetch values from the database
    search_details = db.session.query(SearchDetails).order_by(SearchDetails.id.desc()).first()
    tob_api_details = db.session.query(TobApiDetails).first()
    flight_details = db.session.query(FlightDetails).order_by(FlightDetails.id.desc()).first()
    token_id = tob_api_details.tokenId if tob_api_details else None
    end_user_ip = search_details.ip if search_details else None
    Trace_id = flight_details.trace_id if flight_details else None
    Result_index = flight_details.result_index if flight_details else None
    Adult = session.get('Adult')
    Child = session.get('Child')
    Infant = session.get('Infant')
    print(session)
    
    for i in range(len(payload['Passengers'])):
        if i==0:
            payload['Passengers'][i]['IsLeadPax']=True
        else:
            payload['Passengers'][i]['IsLeadPax']=False
    

    for passenger in payload['Passengers']:
        if passenger['PaxType'] == 1:
            fare = Adult 
        if passenger['PaxType'] == 2:
            fare = Child
        if passenger['PaxType'] == 3:
            fare = Infant
        passenger['Fare'] = fare

    # Update the payload with the fetched values
    if end_user_ip:
        payload['EndUserIp'] = end_user_ip
    if token_id:
        payload['TokenId'] = token_id 
    if Trace_id:
        payload['TraceId'] = Trace_id
    if Result_index:
        payload['ResultIndex'] = Result_index

    # Construct the API URL
    base_url = app.config['BASE_URL']
    api_url = f"{base_url}/Ticket"

    response = requests.post(api_url, json=payload)
 
    # Process the response and return the result
    if response.status_code == 200: 
        result = response.json()
        user_uuid = str(uuid.uuid4())
        flightuuid = str(uuid.uuid4())
        current_datetime = datetime.now() 
        create_at = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        update_at = create_at
        is_active= True
        userid = session.get('userid')
        passengerdetails = json.dumps(payload)
        ticketdetails = json.dumps(result)
        
        booking_id = result['Response']['Response']
        if not booking_id:
            return result['Response']['Error']['ErrorMessage']
        booking_id = result['Response']['Response']['BookingId']
    
        passenger_details = PassengerDetails(uuid=user_uuid,passenger_details=passengerdetails,user_id=userid,flight_uuid=flightuuid,is_active=is_active,created_at=create_at, updated_at=update_at)
        ticket_details = TicketDetails(user_id=userid,is_active=is_active,created_at=create_at, updated_at=update_at,ticket_details=ticketdetails,booking_id=booking_id)
        db.session.add(passenger_details)
        db.session.add(ticket_details)
        db.session.commit()
        db.session.flush()
        return result
    else: 
        return jsonify({'error': 'An Error Occurred'})
    
            

   

