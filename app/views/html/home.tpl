<!DOCTYPE html>
<html lang="pt-BR">
<head>
   <meta charset="UTF-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>Home</title>
   <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&display=swap">
   <link rel="stylesheet" type="text/css" href="/static/css/home.css">
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
            <div class="user-info">
                % if info['logado'] == 'SIM':
                    <h2>Bem-vindo, {{info['nome']}}</h2>
                % else:
                    <h2>Bem-vindo, você não está logado, caso queira logar <a href="/login">clique aqui</a>.</h2>
                % end
            </div>
            <div class="video-list">
                <div class="video-container">
                    <video controls>
                        <source src="/static/videos/sample.mp4" type="video/mp4">
                        Seu navegador não suporta o elemento de vídeo.
                    </video>
                    <div class="video-right">
                        <div class="video-info">
                            <h2>Nome do Vídeo</h2>
                            <p>Descrição do vídeo...</p>
                        </div>
                        <div class="video-actions">
                            <button class="like-button">Curtir</button>
                        </div>
                        <div class="comments-section">
                            <h3>Comentários</h3>
                            <ul class="comments-list">
                                <li>Comentário 1...</li>
                                <li>Comentário 2...</li>
                            </ul>
                            <form class="comment-form">
                                <input type="text" placeholder="Adicione um comentário..." required>
                                <button type="submit">Enviar</button>
                            </form>
                        </div>
                    </div>
                </div>
                <!-- Adicione mais vídeos aqui -->
            </div>
        </main>
    </div>
</body>
</html>