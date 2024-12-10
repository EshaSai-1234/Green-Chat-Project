import http.server
import socketserver
import urllib.parse

# Shared chat log
chat_log = []

# HTML Template with green background
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Green Chat</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 50px; background-color: #4CAF50; }
        .chat-box { width: 50%; margin: auto; text-align: left; }
        input { width: 80%; padding: 10px; margin: 10px 0; }
        button { padding: 10px 20px; }
        .message { margin: 5px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        .user { background-color: #e0f7fa; }
        .bot { background-color: #fff9c4; }
    </style>
</head>
<body>
    <h1>Green Chat</h1>
    <div class="chat-box">
        <div id="chat-log">
            {% chat_log %}
        </div>
        <form method="GET">
            <input type="text" name="user" placeholder="Enter your username" required>
            <input type="text" name="message" placeholder="Type your message here..." required>
            <button type="submit">Send</button>
        </form>
    </div>
</body>
</html>
"""

# HTTP request handler
class ChatHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global chat_log

        # Parse the query parameters
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)

        user = query_params.get("user", [None])[0]
        message = query_params.get("message", [None])[0]

        # If user and message are provided, add to the chat log
        if user and message:
            # Add user's message to the global chat log
            chat_log.append((user, message))
            if len(chat_log) > 50:  # Limit chat log to 50 messages
                chat_log.pop(0)

        # Generate the chat log as HTML
        chat_html = ""
        for sender, msg in chat_log:
            chat_html += f'<div class="message user"><strong>{sender}:</strong> {msg}</div>'

        # Replace placeholders in HTML template
        html = HTML_TEMPLATE.replace("{% chat_log %}", chat_html)

        # Respond to the HTTP request
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

# Run the server
PORT = 8000
with socketserver.TCPServer(("", PORT), ChatHandler) as httpd:
    print(f"Green Chat is running on http://127.0.0.1:{PORT}")
    httpd.serve_forever()
