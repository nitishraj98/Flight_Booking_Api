import razorpay
import uuid
from datetime import datetime
from application.controller.__init__ import calculate_insurance,request,jsonify,session
from application.models.payment import *

razorpay_client = razorpay.Client(auth=('rzp_test_WgaCObsDzKY0Uj', '2NBTrbPCTOt3ZxuOnCpyhV3K'))


def create_payment():
    data = request.get_json()
    insurance_selected = data['insurance_selected']   
    insurance_amount = calculate_insurance(insurance_selected)
    Published_Fare = session.get('Published_Fare')
    meal_price = session.get('meal_price')
    seat_price = session.get('seat_price')
    baggage_price = session.get('baggage_price')

    print("meal_price",meal_price)
    print("seat_price",seat_price)
    print("baggage_price",baggage_price)

    
 
    # Add insurance amount to the payment amount
    total_amount =  insurance_amount  + Published_Fare + meal_price + seat_price + baggage_price
    session['total_amount'] = total_amount
    print(total_amount)
    amount = int(total_amount * 100)  # Payment amount in paise as an integer (e.g., 1000 paise = ₹10)
    currency = 'INR'  # Currency code

    # Create a Razorpay order
    order = razorpay_client.order.create({'amount': amount, 'currency': currency})
    order_id = order['id']
    transaction = 'Testing'
    Amount = total_amount
    gateway_name = 'razorpay'
    gateway_status = 'Pending'
    flightuuid = str(uuid.uuid4())
    userid = session.get('userid')
    current_datetime = datetime.now()
    create_at = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    update_at = create_at
    payment_details = PaymentInformation(user_id=userid,flight_uuid=flightuuid,created_at=create_at, updated_at=update_at,gateway_name=gateway_name,gateway_status=gateway_status,orderid=order_id,transaction=transaction,amount=Amount)
    db.session.add(payment_details)
    db.session.commit()
    db.session.flush()


    return jsonify({'amount': total_amount, 'order_id': order['id']})



def confirm_payment():
    data = request.get_json()  
    order_id = data['order_id']  # Order ID received from the frontend 
    
    # Fetch the order details from Razorpay
    order = razorpay_client.order.fetch(order_id)
    
    # Verify the payment signature 
    signature = data['signature']
    params_dict = {
        'razorpay_order_id': order['id'], 
        'razorpay_payment_id': data['payment_id'],
        'razorpay_signature': signature
    }
    try:
        razorpay_client.utility.verify_payment_signature(params_dict)
        # Payment signature is valid, you can proceed with order fulfillment
        
        return jsonify({'status': 'success'})
    except razorpay.errors.SignatureVerificationError:
        # Payment signature is invalid
        return jsonify({'status': 'Failure'})









 

   



