import razorpay
from application.controller.__init__ import calculate_insurance,request,jsonify,session

razorpay_client = razorpay.Client(auth=('rzp_test_WgaCObsDzKY0Uj', '2NBTrbPCTOt3ZxuOnCpyhV3K'))


def create_payment():
    data = request.get_json()
    insurance_selected = data['insurance_selected']  # Assuming insurance selection is provided in the request data
    insurance_amount = calculate_insurance(insurance_selected)
    Published_Fare = session.get('Published_Fare')
    meal_price = session.get('meal_price')
    seat_price = session.get('seat_price')
    print("meal_price",meal_price)
    print("seat_price",seat_price)

    # Add insurance amount to the payment amount
    total_amount =  insurance_amount  + Published_Fare + meal_price + seat_price
    print(total_amount)
    amount = int(total_amount * 100)  # Payment amount in paise as an integer (e.g., 1000 paise = ₹10)
    currency = 'INR'  # Currency code

    # Create a Razorpay order
    order = razorpay_client.order.create({'amount': amount, 'currency': currency})

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
        return jsonify({'status': 'failure'})









 

   



