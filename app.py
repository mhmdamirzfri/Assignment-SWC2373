from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Replace with your Webex API base URL
WEBEX_API_URL = "https://webexapis.com/v1"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        access_token = request.form['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        user_info = requests.get(f'{WEBEX_API_URL}/people/me', headers=headers).json()
        if 'errors' in user_info:
            return "Invalid Token. Please try again."
        else:
            return render_template('user_info.html', user_info=user_info, access_token=access_token)
    return render_template('index.html')

@app.route('/rooms/<access_token>', methods=['GET', 'POST'])
def rooms(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Fetch rooms
    rooms_data = requests.get(f'{WEBEX_API_URL}/rooms', headers=headers).json()
    
    if request.method == 'POST':
        # If the user submits a message form, sned a message to the selected room
        room_id = request.form['room_id']
        message = request.form['message']
        message_data = {'roomId': room_id, 'text': message}
        
        # Send the message to the specified room
        send_message_response = requests.post(f'{WEBEX_API_URL}/messages', headers=headers, json=message_data)
        
        if send_message_response.status_code == 200:
            return f"Message sent to room {room_id} successfully!"
        else:
            return "Failed to send the message. Please try again."
    
    # Display rooms for selection and message sending
    return render_template('rooms.html', rooms=rooms_data['items'], access_token=access_token)

if __name__ == '__main__':
    app.run(debug=True)

