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
    
    def check_current_directory():
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
                print("File is updated")
            else:
                print("File is not updated")
                upstox_url = Upstox_auth.generate_upstox_url()
                print("Generated URL:", upstox_url)
                code = input("Enter the code from the redirect URL: ")
                token = Upstox_auth.get_upstox_token(code)
                


                # Write code to the file
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






Upstox_auth.check_current_directory()
