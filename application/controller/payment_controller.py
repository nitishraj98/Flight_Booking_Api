import razorpay
import uuid
from datetime import datetime
from application.controller.__init__ import calculate_insurance,request,jsonify,session,jwt_required
from application.models.payment import *
from flask_jwt_extended import get_jwt

razorpay_client = razorpay.Client(auth=('rzp_test_WgaCObsDzKY0Uj', '2NBTrbPCTOt3ZxuOnCpyhV3K'))

@jwt_required()
def create_payment():
    data = request.get_json()
    usrid = get_jwt()["sub"]["userid"] 
    insurance_selected = data['insurance_selected']   
    insurance_amount = calculate_insurance(insurance_selected,usrid)
    Published_Fare = session.get('Published_Fare')
    meal_price = session.get('meal_price')
    seat_price = session.get('seat_price')
    baggage_price = session.get('baggage_price')

    print("meal_price",meal_price)
    print("seat_price",seat_price)
    print("baggage_price",baggage_price)
    print("insurance_amount",insurance_amount)

    InsuranceAmount = insurance_amount if insurance_amount is not None else 0
    MealAmount = meal_price if meal_price is not None else 0
    SeatAmount = seat_price if seat_price is not None else 0
    BaggageAmount = baggage_price if baggage_price is not None else 0
 
    total_amount =  InsuranceAmount  + Published_Fare + MealAmount + SeatAmount + BaggageAmount
    
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
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    flightuuid = str(uuid.uuid4())
    userid = usrid
    current_datetime = datetime.now()
    create_at = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    update_at = create_at
    payment_details = PaymentInformation(user_id=userid,flight_uuid=flightuuid,created_at=create_at, updated_at=update_at,gateway_name=gateway_name,gateway_status=gateway_status,orderid=order_id,transaction=transaction,amount=Amount,ip=ip)
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
        payment_details = db.session.query(PaymentInformation).order_by(PaymentInformation.id.desc()).first()
        gateway_status = 'success'
        
        if payment_details:
            payment_details.gateway_status = gateway_status
            db.session.commit()
            db.session.flush()
        
        return jsonify({'status': 'success'})
    except razorpay.errors.SignatureVerificationError:
        # Payment signature is invalid
        return jsonify({'status': 'Failure'})









 

   



