import http.server
import socketserver
import urllib.parse

# Define chatbot responses
responses = {
    "hello": "Hi there! How can I assist you today?",
    "how are you": "I'm just a bot, but I'm doing fine! How can I help you?",
    "your name": "I'm ChatBot 101, your friendly assistant.",
    "bye": "Goodbye! Have a great day!",
    "default": "I'm sorry, I didn't understand that. Could you rephrase?"
}

# Chatbot logic
def chatbot_response(user_input):
    user_input = user_input.lower()
    for pattern, response in responses.items():
        if pattern in user_input:
            return response
    return responses["default"]

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>ChatBot</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 50px; }
        .chat-box { width: 50%; margin: auto; }
        input { width: 80%; padding: 10px; margin: 10px 0; }
        button { padding: 10px 20px; }
        .response { font-weight: bold; margin: 20px 0; }
    </style>
</head>
<body>
    <h1>ChatBot</h1>
    <div class="chat-box">
        <form method="GET">
            <input type="text" name="user_input" placeholder="Type your message here..." required>
            <button type="submit">Send</button>
        </form>
        {% if response %}
        <div class="response">
            <p><strong>You:</strong> {{ user_input }}</p>
            <p><strong>ChatBot:</strong> {{ response }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

# HTTP request handler
class ChatBotHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the query parameters
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        user_input = query_params.get("user_input", [None])[0]

        # Generate the chatbot response
        response = chatbot_response(user_input) if user_input else None

        # Generate the HTML response
        html = HTML_TEMPLATE
        if response:
            html = html.replace("{% if response %}", "")
            html = html.replace("{% endif %}", "")
            html = html.replace("{{ user_input }}", user_input)
            html = html.replace("{{ response }}", response)
        else:
            html = html.replace("{% if response %}.*?{% endif %}", "", 1)

        # Respond to the HTTP request
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

# Start the server
PORT = 8000
with socketserver.TCPServer(("", PORT), ChatBotHandler) as httpd:
    print(f"ChatBot is running on http://127.0.0.1:{PORT}")
    httpd.serve_forever()
