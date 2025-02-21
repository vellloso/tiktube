<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&display=swap">
    <link rel="stylesheet" type="text/css" href="/static/css/chat.css">
</head>
<body>
    <div class="main-container">
        <nav class="navbar">
            <h1>TikTube</h1>
            <ul>
                <li><a href="/home">Home</a></li>
                <li><a href="/profile">Perfil</a></li>
                <li><a href="/logout">Sair</a></li>
            </ul>
        </nav>
        <main class="main-content">
            <div class="chat-list">
                <h2>Contatos</h2>
                <ul>
                    % if info['contatos']:
                        % for contato in info['contatos']:
                            <li>
                                <p class="contact-name">{{contato.nome}}</p>
                                <a href="/bate-papo?usuario_id={{contato.id}}" class="btn">Conversar</a>
                            </li>
                        % end
                    % else:
                        <li>Nenhum contato encontrado.</li>
                    % end
                </ul>
            </div>
        </main>
    </div>
</body>
</html>