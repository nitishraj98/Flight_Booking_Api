from application.controller.user_controller import *
from application.controller.flight_controller import *
from application.controller.payment_controller import *





# Registration API
@app.route('/api/v1/user/create', methods=['POST'])
def register_route():
    return register()


# OTP verification API
@app.route('/api/v1/user/mobile-verify', methods=['POST'])
def verify_register_route():
    return verify_otp_for_registration()


# Resend OTP API
@app.route('/api/v1/user/resend-otp', methods=['POST'])
def resend_otp_route():
    return resend_otp()


# Login API through otp
@app.route('/api/v1/user/login-by-mobile', methods=['POST'])
def login_route():
    return login_by_otp()

# OTP verification API for login
@app.route('/api/v1/user/login/verify-mobile-for-login', methods=['POST'])
def verify_login_route():
    return verify_login_otp()

# Password reset API through otp
@app.route('/api/v1/user/reset-password', methods=['POST'])
def reset_password_by_otp_route():
    return reset_password_by_otp()

# OTP verification API for password reset
@app.route('/api/v1/user/verify-reset-password-otp', methods=['POST'])
def verify_reset_password_route():
    return verify_reset_otp()

# Password reset API
@app.route('/api/v1/user/reset-password-copy', methods=['POST'])
def reset_password_route():
    return reset_password()



#  API for login using password
@app.route('/api/v1/user/login-using-password', methods=['POST'])
def login_using_password_route():
    return login_using_password()

#  API for logout
@app.route('/api/v1/user/logout', methods=['POST'])
def logout_route():
    return logout()

# API for flight search
@app.route('/api/v1/flight-search', methods=['POST'])
def flight_search_route():
    return flight_search()

# API for flight search farerules
@app.route('/api/v1/flight-search-farerules', methods=['POST'])
def flight_search_farerules_route():
    return flight_search_farerules()


# API for flight search farequote
@app.route('/api/v1/flight-search-farequote', methods=['POST'])
def flight_search_farequote_route():
    return flight_search_fareQuote()


# API for flight search SSR
@app.route('/api/v1/flight-search-ssr', methods=['POST'])
def flight_search_SSR_route():
    return flight_search_SSR()

# API for flight search SSR
@app.route('/api/v1/add-on-ssr', methods=['POST'])
def add_on_ssr_route():
    return add_on_ssr()

# API for calendar fare
@app.route('/api/v1/flight-search-getcalendarfare', methods=['POST'])
def calendar_fare_route():
    return get_fare_calendar()

# API for calendar fare update
@app.route('/api/v1/flight-search-calendarfare-update', methods=['POST'])
def calendar_fare_update_route():
    return update_fare_calendar()

# API for process ticket
@app.route('/api/v1/process-ticket', methods=['POST'])
def process_ticket_route():
    return process_ticket()


# API for authenticate
@app.route('/api/v1/authenticate', methods=['POST'])
def authenticate_route():
    return GetTokenId()


# API for booking details
@app.route('/api/v1/booking-details', methods=['GET'])
def book_deatails_route():
    return booking_details()


# API for release pnr request
@app.route('/api/v1/release-pnr-request', methods=['GET'])
def release_pnr_request_route():
    return release_pnr_request()

# API for send change request
@app.route('/api/v1/send-change-request', methods=['POST'])
def change_request_route():
    return send_change_request()  


# API for send change request status
@app.route('/api/v1/send-change-request-status', methods=['GET'])
def change_request_status_route():
    return send_change_request_status()  


# API for cancellation charge
@app.route('/api/v1/cancellation-charge', methods=['POST'])
def cancellation_charge_route():
    return cancellation_charge() 


# API for city details
@app.route('/api/v1/citydetails', methods=['GET'])
def city_details_route():
    return Airport_Details() 

# API for create payment
@app.route('/api/v1/create-payment', methods=['GET'])
def create_payment_route():
    return create_payment() 

# API for confirm payment
@app.route('/api/v1/confirm-payment', methods=['POST'])
def confirm_payment_route():
    return confirm_payment() 




