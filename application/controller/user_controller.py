from application.controller import *
import re



def generate_otp():  
    return random.randint(100000, 999999)

def is_valid_mobile(mobile_no):
    # Regular expression for mobile number format validation
    mobile_pattern = r'^\d{10}$'  # Assumes 10-digit mobile numbers
    return re.match(mobile_pattern, mobile_no)

def is_valid_email(email):
    # Regular expression for email format validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email)


def is_strong_password(password):
    # Define password strength criteria
    min_length = 8
    has_uppercase = re.search(r'[A-Z]', password)
    has_lowercase = re.search(r'[a-z]', password)
    has_digit = re.search(r'\d', password)
    has_special_char = re.search(r'[!@#$%^&*(),.?":{}|<>]', password)

    # Check if all criteria are met
    if (len(password) >= min_length and
        has_uppercase and
        has_lowercase and
        has_digit and
        has_special_char):
        return True
    else:
        return False
 

def register():
    data = request.get_json()
    if data["password"] != data["password_confirmation"]:
        return jsonify({'message': 'Password and Confirm Password do not match'}), 400
    #Validate email format
    if not is_valid_email(data["email"]):
        return jsonify({'message': 'Invalid email format'}), 400
    
    # Validate mobile number format
    if not is_valid_mobile(data["mobile_no"]):
        return jsonify({'message': 'Invalid mobile number format'}), 400
    
    # Validate strong password
    if not is_strong_password(data["password"]):
        return jsonify({'message': 'Password must be at least 8 characters long and contain uppercase, lowercase, digit, and special character'}), 400
   
    
    
    # Check if email or mobile number already exists
    existing_email = User.query.filter(User.email==data["email"]).first()
    existing_mob = User.query.filter(User.mobile_no == data["mobile_no"]).first()
    if existing_email and existing_mob:
        return jsonify({'message': 'Email and Phone number already exists'}), 406
    elif existing_email:
        return jsonify({'message': 'Email already exists'}), 406
    elif existing_mob:
        return jsonify({'message': 'Phone number already exists'}), 406


    # Hash the password
    data['password'] = Bcrypt().generate_password_hash(data["password"]).decode('utf-8')
    
    # Generate OTP
    otp = generate_otp()

    db.session.query(GenOtp).delete()
    db.session.commit()
    db.session.flush()

    ins = GenOtp(otp=otp,name=data["name"],email=data["email"], mobile_no=data["mobile_no"], password=data["password"])
    db.session.add(ins)
    db.session.commit()
    db.session.flush()

    mobile_no = data['mobile_no']
   # Construct the SMS URL
    sms_url = app.config['SMS_URL']
    sms_url = f"{sms_url}&receiver={mobile_no}&route=TA&msgtype=1&sms=Your+Rirabh+Login+OTP+is+{otp}"
    
    response = requests.get(sms_url)
    
    user = GenOtp.query.filter(GenOtp.mobile_no==data['mobile_no']).first()
    user = GenOtpSchema().dump(user)
    
    user['reference_id'] = str(user.pop('id'))
    
    
    if response.status_code != 200:
        return jsonify({'message': 'Failed to send OTP'}), 406
    
    return jsonify({'message':'Otp has been sent!','reference_id':user['reference_id']}),200



def verify_otp_for_registration():  
    data = request.get_json()
    
    
    add_otp = GenOtp.query.filter(GenOtp.otp==data['otp']).first()
    if not add_otp or (add_otp.otp != data["otp"]):
        return json.jsonify({"message":"Please, Enter a valid otp!"}), 406
    add_otp = GenOtpSchema().dump(add_otp)
    
    GenOtp.query.filter(GenOtp.otp==data['otp']).delete()
    db.session.commit()
    db.session.flush()

    add_otp.pop("id")
    add_otp.pop('otp')
    #print(add_otp)

    ins = User(**add_otp)
    db.session.add(ins)
    db.session.commit()
    db.session.flush()

    # Check if the OTP exists in the database
    user = User.query.filter(User.email==add_otp["email"]).first()
    user2 = UserSchema().dump(user)
    
    send_registration_email(user2["email"], user2["name"]) 
    
    # Generate an access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({'access_token': access_token,'username': user.name,
                'id': user.id, 'message': 'Registration Successful','status':True})

def resend_otp_for_registration():
    data = request.get_json()

    # Check if the mobile number exists in the database
    user = GenOtp.query.filter(GenOtp.mobile_no == data['mobile_no']).first()

    if not user:
        return jsonify({'message': 'Mobile number not found'}), 404

    # Generate a new OTP
    otp = generate_otp()

    # Update the OTP in the database
    user.otp = otp
    db.session.commit()
 
    mobile_no = data['mobile_no']
    # Construct the SMS URL
    sms_url = app.config['SMS_URL']
    sms_url = f"{sms_url}&receiver={mobile_no}&route=TA&msgtype=1&sms=Your+Rirabh+Login+OTP+is+{otp}"

    response = requests.get(sms_url)

    if response.status_code != 200:
        return jsonify({'message': 'Failed to send OTP'}), 406

    return jsonify({'message': 'OTP has been resent'}), 200





def login_by_otp():
    mobile_no = request.json.get('phoneno')

    user = User.query.filter(User.mobile_no==mobile_no).first()
    
    if not user:
        return jsonify({'message': 'User not found','status':False}), 401

    otp = generate_otp()

    user.otp = otp
    
    db.session.commit()
 
   # Construct the SMS URL
    sms_url = app.config['SMS_URL']
    sms_url = f"{sms_url}&receiver={mobile_no}&route=TA&msgtype=1&sms=Your+Rirabh+Login+OTP+is+{otp}"
   
    response = requests.get(sms_url)

    user_data = UserSchema().dump(user) 
    user_data['reference_id'] = user_data.pop('id')
    

    if response.status_code != 200:
        return jsonify({'message': 'Failed to send OTP'}), 406

    return jsonify({'message':'OTP has been sent','status':True,'reference_id':user_data['reference_id']}), 200


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
    session['access_token'] = access_token
    session['username'] = user.name
    session['userid'] = user.id

    return jsonify({'access_token': access_token,'username': user.name,
                'id': user.id, 'message': 'Login Successful','status':True})


def reset_password_by_otp():
    mobile_no = request.json.get('phoneno')
    session['mobile_no'] = mobile_no

    user = User.query.filter_by(mobile_no=mobile_no).first()
    user = UserSchema().dump(user)
    user.pop('is_active')

    if not user:
        return jsonify({'message': 'User not found','status':False}), 404

    db.session.query(GenOtp).delete()
    db.session.commit()
    db.session.flush()

    otp = generate_otp()

    user['otp'] = otp

    ins = GenOtp(**user)
    db.session.add(ins)
    db.session.commit()
    db.session.flush()

    # Construct the SMS URL
    sms_url = app.config['SMS_URL']
    sms_url = f"{sms_url}&receiver={mobile_no}&route=TA&msgtype=1&sms=Your+Rirabh+Login+OTP+is+{otp}"

    response = requests.get(sms_url)
    user_data = UserSchema().dump(user)
    user_data['reference_id'] = user_data.pop('id')
    

    if response.status_code != 200:
        return jsonify({'message': 'Failed to send OTP'}), 500

    return jsonify({'message': 'OTP has been sent','status':True,'reference_id':user_data['reference_id']})




def verify_reset_otp():
    otp = request.json.get('otp')

    user = GenOtp.query.filter_by(otp=otp).first()
 
    if not user:
        return jsonify({'message': 'Invalid OTP'}), 404

    if user.otp != otp:
        return jsonify({'message': 'Invalid OTP'}), 400

    return jsonify({ 'message': 'OTP Verified','status':True,'reference_id': user.id})
    


def reset_password():
    password = request.json.get('password')
    password_confirmation = request.json.get('password_confirmation')

    if password != password_confirmation:
        return jsonify({'message': 'New Password and Confirm Password do not match'}), 406
    #Validate strong password
    if not is_strong_password(password):
        return jsonify({'message': 'Password must be at least 8 characters long and contain uppercase, lowercase, digit, and special character'}), 406

    bcrypt = Bcrypt(app)
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
 
    user_mob = GenOtp.query.filter_by().first()

    user = User.query.filter(User.mobile_no==user_mob.mobile_no).first()

    if not user:
        return json.jsonify({"message":'unverified user'}), 406

    user.password = hashed_password
    db.session.commit()
    access_token = create_access_token(identity=hashed_password)
    user_data = UserSchema().dump(user)
    user_data['reference_id'] = user_data.pop('id')
    
    return json.jsonify({'access_token': access_token,"message":'Password Reset Successfully','status':True,'reference_id':user_data['reference_id']})


def login_using_password():
    email = request.json['email']
    password = request.json['password']

    # Find the user by email
    user = User.query.filter_by(email=email).first()

    if user:
        # Check if the password matches
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            access_token = create_access_token(identity=email)
            session['access_token'] = access_token
            session['username'] = user.name
            session['userid'] = user.id
            
            return jsonify({'access_token': access_token,'username': user.name,
                'id': user.id,'Email':user.email,'message': 'Login successful','status':True})
        else:
            return jsonify({'message': 'Invalid password'})
    else:
        return jsonify({'message': 'User not found','status':False}), 404 
     


def logout():
    # print(session)
    if 'username' in session:
        session.pop('username', None)
        session.pop('access_token', None)
    # print(session)
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
    












    





        

        

        

         

   











