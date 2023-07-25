from application.controller import *
from flask import session


def calculate_insurance(insurance_selected):
    total_count = session.get('total_count')
    
    
    # Check if total_count is None or not
    if total_count is None:
        total_count = 0  # Assign a default value of 0 if total_count is None
    
    insurance_amount = 199 * total_count if insurance_selected else 0
    # print(type(Published_Fare))
    # print(type(insurance_amount))
    total_amount = insurance_amount
    return total_amount   




def book(payload):
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
        api_url = f"{base_url}/Book"              
    
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            result = response.json()

            return (result)
        
    else:
        return jsonify({'error': 'An error occurred'})
            
            
    
def ticket(payload):
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
    api_url = f"{base_url}/Ticket"

    response = requests.post(api_url, json=payload)

    # Process the response and return the result
    if response.status_code == 200: 
        result = response.json()
        return (result)
    else: 
        return jsonify({'error': 'An Error Occurred'})
    



    





    



     




        
       
    