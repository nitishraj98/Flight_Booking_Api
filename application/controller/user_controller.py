from application.controller import *
import bcrypt


def generate_otp():  
    return random.randint(100000, 999999)
 

def register():
    data = request.get_json()
    
    # Validate user input using UserSchema
    errors = UserSchema().validate(data)
    if errors:
        return jsonify({'message': 'Validation errors', 'errors': errors}), 400
    
    if data["password"] != data["confirm_password"]:
        return jsonify({'message': 'Password and Confirm Password do not match'}), 400
    
    # Check if email or mobile number already exists
    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify({'message': 'Email already exists'}), 400
    
    existing_user = User.query.filter_by(mobile_no=data["mobile_no"]).first()
    if existing_user:
        return jsonify({'message': 'Mobile number already exists'}), 400
    
    # Generate OTP
    otp = generate_otp()
    
    # Hash the password
    hashed_password = Bcrypt().generate_password_hash(data["password"]).decode('utf-8')

    
    # Create a new user instance
    new_user = User(
        email=data["email"],
        name=data["name"],
        mobile_no=data["mobile_no"],
        password=hashed_password,    
        otp=otp
    )
    
    # Add the new user to the database session
    db.session.add(new_user)
    db.session.commit()
    
    mobile_no = data['mobile_no']
   # Construct the SMS URL
    sms_url = app.config['SMS_URL']
    sms_url = f"{sms_url}&receiver={mobile_no}&route=TA&msgtype=1&sms=Your+Rirabh+Login+OTP+is+{otp}"
    
    response = requests.get(sms_url)
    
    if response.status_code != 200:
        return jsonify({'message': 'Failed to send OTP'}), 500
    
    return jsonify({'message': 'OTP sent to your phone number'})



def verify_otp_for_registration():
    data = request.get_json()
    
    # Check if the OTP exists in the database
    user = User.query.filter(User.otp==data["otp"]).first()
    user2 = UserSchema().dump(user)
    if not user:
        return jsonify({'message': 'Invalid OTP'}), 404
    
    # Verify the OTP
    if user.otp != data["otp"]:
        return jsonify({'message': 'Invalid OTP'}), 400
    
    # Update the user's OTP field to NULL
    user.otp = None
    db.session.commit()

    print(data)
    send_registration_email(user2["email"], user2["name"]) 
    
    # Generate an access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({'access_token': access_token,'username': user.name,
                'id': user.id, 'msg': 'Registration Successful'})





def login_by_otp():
    mobile_no = request.json.get('mobile_no')

    user = User.query.filter_by(mobile_no=mobile_no).first()

    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    otp = generate_otp()

    user.otp = otp
    db.session.commit()
 
   # Construct the SMS URL
    sms_url = app.config['SMS_URL']
    sms_url = f"{sms_url}&receiver={mobile_no}&route=TA&msgtype=1&sms=Your+Rirabh+Login+OTP+is+{otp}"
   
    response = requests.get(sms_url)

    

    if response.status_code != 200:
        return jsonify({'message': 'Failed to send OTP'}), 500

    return jsonify({'message': 'OTP sent to your phone number'})


def verify_login_otp():
    otp = request.json.get('otp')

    user = User.query.filter_by(otp=otp).first()

    if not user:
        return jsonify({'message': 'Invalid OTP'}), 404

    if user.otp != otp:
        return jsonify({'message': 'Invalid OTP'}), 400

    user.otp = None
    db.session.commit()

    access_token = create_access_token(identity=otp)

    return jsonify({'access_token': access_token,'username': user.name,
                'id': user.id, 'msg': 'Login Successful'})


def reset_password_by_otp():
    mobile_no = request.json.get('mobile_no')

    user = User.query.filter_by(mobile_no=mobile_no).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    otp = generate_otp()

    user.otp = otp
    db.session.commit()

    # Construct the SMS URL
    sms_url = app.config['SMS_URL']
    sms_url = f"{sms_url}&receiver={mobile_no}&route=TA&msgtype=1&sms=Your+Rirabh+Login+OTP+is+{otp}"

    response = requests.get(sms_url)

    if response.status_code != 200:
        return jsonify({'message': 'Failed to send OTP'}), 500

    return jsonify({'message': 'OTP sent to your phone number'})




def verify_reset_otp():
    otp = request.json.get('otp')
    password = request.json.get('password')
    confirm_password = request.json.get('confirm_password')


    user = User.query.filter_by(otp=otp).first()

    if not user:
        return jsonify({'message': 'Invalid OTP'}), 404

    if user.otp != otp:
        return jsonify({'message': 'Invalid OTP'}), 400

    user.otp = None
    db.session.commit()

    
    if password != confirm_password:
        return jsonify({'message': 'New Password and Confirm Password do not match'}), 400

    bcrypt = Bcrypt(app)
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    user.password = hashed_password
    db.session.commit()

    access_token = create_access_token(identity=otp)

    return jsonify({'access_token': access_token, 'message': 'Password reset successful'})




def login_using_password():
    email = request.json['email']
    password = request.json['password']

    # Find the user by email
    user = User.query.filter_by(email=email).first()

    if user:
        # Check if the password matches
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            access_token = create_access_token(identity=email)
            
            return jsonify({'access_token': access_token,'username': user.name,
                'id': user.id,'Email':user.email,'message': 'Login successful'})
        else:
            return jsonify({'message': 'Invalid password'})
    else:
        return jsonify({'message': 'User not found'})
     


def logout():
    if 'name' in session:
        session.pop('name', None)
        session.pop('access_token', None)
    
    return jsonify({'message': 'You have successfully logged out.'})




def authenticate():
    payload = request.get_json()
    # print(payload)
    # Construct the API URL
    auth_url = app.config['AUTH_URL']
    api_url = f"{auth_url}/Authenticate"

    response = requests.post(api_url, json=payload)

    # Process the response and store the TokenId in the database
    if response.status_code == 200:
        result = response.json()
        token_id = result['TokenId']
        print(token_id)

        # Update the existing record with user_id 1 or insert a new record if it doesn't exist
        tob_api_details = TobApiDetails.query.filter(TobApiDetails.id==1).first()
        
        
        if tob_api_details is None:
            return jsonify({"msg":"error"}) 
        

        tob_api_details.tokenId = token_id

        # Commit the changes to the database
        db.session.add(tob_api_details)
        db.session.commit()

        return jsonify(result)

    else:
        return jsonify({'error': 'An error occurred'})
    








    





        

        

        

         

   











