import http.server
import socketserver
import urllib.parse
import base64

# Shared chat log
chat_log = []

# HTML Template with Logo, Heading, Animation, and Chat Interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Green ChatBot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 0;
            background-color: #4CAF50;
            color: white;
            overflow: hidden;
        }

        .container {
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 10px;
        }

        .initial-page {
            display: block;
            animation: fadeIn 2s ease-out;
        }

        .chat-page {
            display: none;
        }

        .chat-box {
            height: 400px;
            overflow-y: scroll;
            padding: 10px;
            background-color: #f4f4f4;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }

        .input-box {
            display: flex;
            justify-content: space-between;
        }

        input[type="text"] {
            width: 80%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 14px;
        }

        button {
            padding: 10px 20px;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        button:hover {
            background-color: #218838;
        }

        .message {
            margin: 5px 0;
            padding: 10px;
            border-radius: 5px;
            display: inline-block;
            max-width: 70%;
        }

        .user {
            background-color: #e0f7fa;
            text-align: left;
        }

        .bot {
            background-color: #fff9c4;
            text-align: right;
        }

        .typing-indicator {
            font-style: italic;
            color: #888;
            display: none;
        }

        .emojis {
            font-size: 20px;
        }

        .emoji-button {
            cursor: pointer;
        }

        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(-50px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        @keyframes slideIn {
            0% { transform: translateX(100%); }
            100% { transform: translateX(0); }
        }

        .logo {
            animation: fadeIn 2s ease-out;
        }

        .heading {
            animation: fadeIn 2s ease-out 1s;
        }

        @media (max-width: 600px) {
            .container {
                width: 100%;
                padding: 10px;
            }
            .input-box {
                flex-direction: column;
            }
            input[type="text"] {
                width: 100%;
                margin-bottom: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container initial-page">
        <h1 class="heading">Green Chat</h1>
        <img src="data:image/png;base64,{{logo_base64}}" alt="Green Chat Logo" class="logo" width="200" height="200">
        <br><br>
        <button onclick="startChat()">Next</button>
    </div>

    <div class="container chat-page">
        <h1>Green Chat</h1>
        <div class="chat-box" id="chat-log"></div>
        <div id="typing-indicator" class="typing-indicator">Someone is typing...</div>
        <form method="GET" onsubmit="sendMessage(event)">
            <div class="input-box">
                <input type="text" id="user-message" name="message" placeholder="Type your message..." required>
                <button type="submit">Send</button>
            </div>
        </form>
        <div class="emojis">
            <span class="emoji-button" onclick="addEmoji('🙂')">🙂</span>
            <span class="emoji-button" onclick="addEmoji('😃')">😃</span>
            <span class="emoji-button" onclick="addEmoji('❤️')">❤️</span>
            <span class="emoji-button" onclick="addEmoji('😂')">😂</span>
        </div>
    </div>

    <script>
        // Function to show the chat page after clicking 'Next'
        function startChat() {
            document.querySelector('.initial-page').style.display = 'none';
            let chatPage = document.querySelector('.chat-page');
            chatPage.style.display = 'block';
            chatPage.style.animation = 'slideIn 1s ease-out';
        }

        // Function to handle new message submission
        function sendMessage(event) {
            event.preventDefault();
            let message = document.getElementById('user-message').value;
            let user = "User";
            if (message.trim() !== "") {
                // Add message to chat log
                updateChat(user, message);
                document.getElementById('user-message').value = '';
                document.getElementById('typing-indicator').style.display = 'inline-block'; // Show typing indicator
                simulateBotResponse();
            }
        }

        // Simulate bot response after a delay
        function simulateBotResponse() {
            setTimeout(function() {
                let botMessage = "Hello, I am your Green ChatBot! How can I assist you today?";
                updateChat("ChatBot", botMessage);
                document.getElementById('typing-indicator').style.display = 'none'; // Hide typing indicator
            }, 1500); // 1.5 seconds delay for bot response
        }

        // Update chat log dynamically
        function updateChat(sender, message) {
            let chatLog = document.getElementById('chat-log');
            let messageDiv = document.createElement('div');
            messageDiv.classList.add('message');
            if (sender === "ChatBot") {
                messageDiv.classList.add('bot');
            } else {
                messageDiv.classList.add('user');
            }
            messageDiv.textContent = sender + ": " + message;
            chatLog.appendChild(messageDiv);
            chatLog.scrollTop = chatLog.scrollHeight; // Auto scroll to bottom
        }

        // Function to add emoji to input box
        function addEmoji(emoji) {
            let messageInput = document.getElementById('user-message');
            messageInput.value += emoji;
            messageInput.focus();
        }
    </script>
</body>
</html>
"""

# Convert the logo image to Base64
def encode_logo_to_base64():
    with open("green_logo.png", "rb") as logo_file:
        encoded_logo = base64.b64encode(logo_file.read()).decode('utf-8')
    return encoded_logo

# HTTP request handler
class ChatHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global chat_log

        # Parse the query parameters
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)

        message = query_params.get("message", [None])[0]

        # If message is provided, add to the chat log
        if message:
            chat_log.append(("User", message))
            if len(chat_log) > 50:  # Limit chat log to 50 messages
                chat_log.pop(0)

        # Generate the chat log as HTML
        chat_html = ""
        for sender, msg in chat_log:
            chat_html += f'<div class="message {"user" if sender == "User" else "bot"}">{sender}: {msg}</div>'

        # Get the logo in base64 format
        logo_base64 = encode_logo_to_base64()

        # Replace placeholders in HTML template
        html = HTML_TEMPLATE.replace("{{logo_base64}}", logo_base64)
        html = html.replace("{% chat_log %}", chat_html)

        # Respond to the HTTP request
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

# Run the server
PORT = 8001  # Change port to 8001 to avoid conflicts
with socketserver.TCPServer(("", PORT), ChatHandler) as httpd:
    print(f"Interactive Green ChatBot is running on http://127.0.0.1:{PORT}")
    httpd.serve_forever()
