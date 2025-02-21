<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bate-Papo</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&display=swap">
    <link rel="stylesheet" type="text/css" href="/static/css/bate_papo.css">
</head>
<body>
    <div class="main-container">
        <nav class="navbar">
            <h1>TikTube</h1>
            <ul>
                <li><a href="/home">Home</a></li>
                <li><a href="/profile">Perfil</a></li>
                <li><a href="/chat-{{info['usuario_id']}}">Chat</a></li>
                <li><a href="/logout">Sair</a></li>
            </ul>
        </nav>
        <main class="main-content">
            <div class="chat-container">
                <h2>Chat com {{info['usuario'].nome}}</h2>
                <div id="messages" class="messages"></div>
                <input type="text" id="messageInput" placeholder="Digite sua mensagem...">
                <button onclick="sendMessage()">Enviar</button>
            </div>
        </main>
    </div>
    <script>
        let ws;

        function connect() {
            ws = new WebSocket('ws://localhost:6789');

            ws.onopen = function() {
                console.log('Connected to WebSocket');
            };

            ws.onmessage = function(event) {
                const messages = document.getElementById('messages');
                const messageData = JSON.parse(event.data);
                const message = document.createElement('div');
                message.textContent = `${messageData.autor}: ${messageData.mensagem}`;
                messages.appendChild(message);
            };

            ws.onclose = function() {
                console.log('WebSocket connection closed. Reconnecting...');
                setTimeout(connect, 1000); // Tentar reconectar após 1 segundo
            };

            ws.onerror = function(error) {
                console.error('WebSocket error:', error);
                ws.close();
            };
        }

        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value;
            if (message.trim() === '') {
                return;
            }

            fetch('/send-message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    mensagem: message,
                    destinatario_id: {{info['usuario_id']}}
                })
            })
            .then(response => {
                if (!response.ok) {
                    console.error('Network response was not ok:', response.status, response.statusText);
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({ type: 'message', mensagem: data.mensagem, autor: data.autor }));
                }
                input.value = '';
            })
            .catch(error => {
                console.error('Error sending message:', error);
            });
        }

        function loadMessages() {
            fetch(`/get-messages/{{info['usuario_id']}}`)
                .then(response => response.json())
                .then(data => {
                    const messages = document.getElementById('messages');
                    data.mensagens.forEach(mensagem => {
                        const message = document.createElement('div');
                        message.textContent = `${mensagem.autor}: ${mensagem.conteudo}`;
                        messages.appendChild(message);
                    });
                })
                .catch(error => {
                    console.error('Error loading messages:', error);
                });
        }

        connect();
        loadMessages();
    </script>
</body>
</html>