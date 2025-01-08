import requests
class Upstox_auth:
    client_id_input = 'a3c35f85-5ba0-4e4b-bde5-44c56d60c0ce'
    redirect_uri_input = 'https://127.0.0.1:5000/'
    client_secret_input = '10arbpucj2'

    def generate_upstox_url():
        base_url = "https://api.upstox.com/v2/login/authorization/dialog"
        params = {
            'response_type': 'code',
            'client_id': Upstox_auth.client_id_input,
            'redirect_uri': Upstox_auth.redirect_uri_input ,
            'state': 'state'
        }
        url = f"{base_url}?response_type={params['response_type']}&client_id={params['client_id']}&redirect_uri={params['redirect_uri']}&state={params['state']}"
        return url

    def get_upstox_token(code):
        token_url = "https://api.upstox.com/v2/login/authorization/token"
        client_id = Upstox_auth.client_id_input
        client_secret = Upstox_auth.client_secret_input  # Replace with your actual client secret
        redirect_uri = Upstox_auth.redirect_uri_input
        grant_type = 'authorization_code'
        
        # Prepare the data for the POST request (matching curl parameters)
        data = {
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': grant_type
        }

        # Prepare headers
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # Make the POST request to get the token
        response = requests.post(token_url, headers=headers, data=data)

        if response.status_code == 200:
            token_info = response.json()
            access_token = token_info.get('access_token')
            print(f"Access Token: {access_token}")
            return access_token
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
    
    def getToken():
        import os
        from datetime import datetime

        # Set the working directory
        os.chdir(r"C:\Users\prasa\Music\Algo Trading-Environment\AlgoTradeHub")

        # Current directory and file path
        current_directory = os.getcwd()
        file_path = os.path.join(current_directory, "token.txt")

        # Check if the file exists
        if os.path.exists(file_path):            
            # Check the last updated date
            last_modified_date = datetime.fromtimestamp(os.path.getmtime(file_path)).date()
            today_date = datetime.today().date()

            if last_modified_date == today_date:
                
                with open(file_path, 'r') as file:
                    token = file.read()
            else:
                print("File is not updated")
                upstox_url = Upstox_auth.generate_upstox_url()
                print("Generated URL:", upstox_url)
                code = input("Enter the code from the redirect URL: ")
                token = Upstox_auth.get_upstox_token(code)
                # Create and write to the file
                with open(file_path, 'w') as file:
                    file.write(token)
        else:
            upstox_url = Upstox_auth.generate_upstox_url()
            print("Generated URL:", upstox_url)
            code = input("Enter the code from the redirect URL: ")
            token = Upstox_auth.get_upstox_token(code)
            # Create and write to the file
            with open(file_path, 'w') as file:
                file.write(token)

        return token

    #To check the data

    def Profile_check(token):
        url = 'https://api.upstox.com/v2/user/profile'
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        response = requests.get(url, headers=headers)

        return (response.json())    

    def Fund_margin_check(token):
        url = 'https://api.upstox.com/v2/user/get-funds-and-margin'
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        response = requests.get(url, headers=headers)

        return (response.json())

        #if need to get only equity margin
        #return (response.json()['data']['equity'])

        #if need to get only commodity margin
        #return (response.json()['data']['commodity'])

    def Brokerage_check(instrument_token, quantity, product, transaction_type, price,token):
        url = 'https://api.upstox.com/v2/charges/brokerage'
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        params = {
            'instrument_token': instrument_token,
            'quantity': quantity,
            'product': product,
            'transaction_type': transaction_type,
            'price': price
        }
        response = requests.get(url, headers=headers, params=params)

        return response.json()

    def Margin_check(instrument_key, quantity, transaction_type, product, token):
        url = "https://api.upstox.com/v2/charges/margin"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        data = {
            "instruments": [
                {
                    "instrument_key": instrument_key,
                    "quantity": quantity,
                    "transaction_type": transaction_type,
                    "product": product
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data)

        
        return (response.json())

    #to do actions
    def place_order(quantity:int, product, validity, price, tag, instrument_token, order_type, transaction_type, disclosed_quantity, trigger_price, is_amo, token):

        url = 'https://api-hft.upstox.com/v2/order/place'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
        }

        data = {
            'quantity': quantity,                           #Numerical Quantity expected
            'product': product,                             #D for Delivery &  I for Intraday
            'validity': validity,                           #Day or IOC 
            'price': price,                                 #Numerical Price expected
            'tag': tag,                                     #String expected no definition
            'instrument_token': instrument_token,           #IN value with prefix of NSE_EQ or BSE_EQ
            'order_type': order_type,                       #MARKET, LIMIT, SL, SL-M
            'transaction_type': transaction_type,           #BUY or SELL
            'disclosed_quantity': disclosed_quantity,       #Numerical Quantity expected 0 for no disclosure
            'trigger_price': trigger_price,                 #Numerical Price expected 0 for no trigger price
            'is_amo': is_amo,                               #Boolean value expected True or False
            #'slice': True                                  #add if needed to Slice the order
        }

        try:
            # Send the POST request
            response = requests.post(url, json=data, headers=headers)

            # Print the response status code and body
            print('Response Code:', response.status_code)
            return response.json()
            return (response.json()['data']['order_id'])

        except Exception as e:
            # Handle exceptions
            print('Error:', str(e))

    def modify_order(quantity,validaty,price,order_id,order_type,disclosed_quantity,trigger_price,token):

        url = 'https://api-hft.upstox.com/v2/order/modify'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        data = {
            'quantity': quantity,
            'validity': validaty,
            'price': price,
            'order_id': order_id,
            'order_type': order_type,
            'disclosed_quantity': disclosed_quantity,
            'trigger_price': trigger_price
        }

        response = requests.put(url, headers=headers, json=data)
        return response.text

    def get_order_details(order_id,token):

        url = 'https://api.upstox.com/v2/order/details'
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        params = {'order_id': order_id}

        response = requests.get(url, headers=headers, params=params)

        return (response.text)

    def get_orderbook(token):
        url = 'https://api.upstox.com/v2/order/retrieve-all'
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        response = requests.get(url, headers=headers)
        return response.text

    def get_order_history(order_id,token):
        url = 'https://api.upstox.com/v2/order/history'
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        params = {'order_id': order_id}

        response = requests.get(url, headers=headers, params=params)

        return response.text

    def cancel_order(order_id,token):
        import requests

        url = f'https://api-hft.upstox.com/v2/order/cancel?order_id={order_id}'
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        response = requests.delete(url, headers=headers)

        return response.text

    def exit_all_positions(token):
        url = 'https://api.upstox.com/v2/order/positions/exit'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
        }

        data = {}

        try:
            # Send the POST request
            response = requests.post(url, json=data, headers=headers)

            # Print the response status code and body
            print('Response Code:', response.status_code)
            return response.json()

        except Exception as e:
            # Handle exceptions
            print('Error:', str(e))

    def cancel_all_orders(token):
        url = 'https://api.upstox.com/v2/order/multi/cancel'
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        response = requests.delete(url, headers=headers)
        return response.text

    def get_today_trade(token):
    
        url = 'https://api.upstox.com/v2/order/trades/get-trades-for-day'
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        response = requests.get(url, headers=headers)
        return response.text

    def get_old_trade(segment,start_date,end_date,page_number,page_size,token):
        url = 'https://api.upstox.com/v2/charges/historical-trades'
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        params = {
            'segment': segment,
            'start_date': start_date,
            'end_date': end_date,
            'page_number': str(page_number),
            'page_size': str(page_size)
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            return (data)
        else:
            print(f"Error: {response.status_code} - {response.text}")

    def get_trade_ordernum(order_id,token):
        url = f'https://api.upstox.com/v2/order/trades?order_id={order_id}'
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        response = requests.get(url, headers=headers)
        return response.text

    def get_holdings(token):
        
        url = 'https://api.upstox.com/v2/portfolio/long-term-holdings'
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        response = requests.get(url, headers=headers)

        print(response.json())

    def get_positions(token):
        url = 'https://api.upstox.com/v2/portfolio/short-term-positions'
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        response = requests.get(url, headers=headers)

        print(response.json())

    def convert_position(instrument_token, older_product, transaction_type, quantity, token):
        

        url = 'https://api.upstox.com/v2/portfolio/convert-position'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',  # Replace {your_access_token} with your actual access token
        }

        if older_product == 'I':
            data = {
                "instrument_token": instrument_token,
                "new_product": "D",
                "old_product": "I",
                "transaction_type": transaction_type,
                "quantity": quantity
            }
        else:
            data = {
                "instrument_token": instrument_token,
                "new_product": "I",
                "old_product": "D",
                "transaction_type": transaction_type,
                "quantity": quantity
            }

        response = requests.put(url, headers=headers, json=data)


        return(response.json())

    def get_metadata(from_date, to_date, segment, financial_year, token):

        url = 'https://api.upstox.com/v2/trade/profit-loss/metadata'
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        params = {
            'from_date': from_date, #'05-11-2023'
            'to_date': to_date, #'19-12-2023'
            'segment': segment, #'EQ','FO'
            'financial_year': financial_year, #'2324'
        }

        response = requests.get(url, headers=headers, params=params)

        print(response.status_code)
        return (response.json())

    def getPLreport(from_date, to_date, segment, financial_year, page_number, page_size, token):
        
        url = 'https://api.upstox.com/v2/trade/profit-loss/data'
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        params = {
            'from_date': from_date, #'05-11-2023',
            'to_date': to_date, #'19-12-2023',
            'segment': segment, #'EQ',
            'financial_year': financial_year, #'2324',
            'page_number': page_number, #'1',
            'page_size': page_size #'4'
        }

        response = requests.get(url, headers=headers, params=params)

        print(response.status_code)
        return (response.json())

    def trade_charges(from_date, to_date, segment, financial_year, token):
        

        url = 'https://api.upstox.com/v2/trade/profit-loss/charges'
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        params = {
            'from_date': from_date, #'05-11-2023',
            'to_date': to_date, #'19-12-2023',
            'segment': segment, #'EQ',
            'financial_year': financial_year #'2324'
        }

        response = requests.get(url, headers=headers, params=params)

        print(response.status_code)
        return (response.json())


token = Upstox_auth.getToken()
print(Upstox_auth.trade_charges('01-05-2024','31-12-2024','EQ','2425',token))



    