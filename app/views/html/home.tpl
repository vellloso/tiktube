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
                % for video in videos:
                    <div class="video-container">
                        <video controls>
                            <source src="static/videos/{{video['caminho']}}" type="video/mp4">
                            Seu navegador não suporta o elemento de vídeo.
                        </video>
                        <div class="video-right">
                            <div class="video-info">
                                <h2>{{video['titulo']}}</h2>
                                <p>Por <strong>{{video['autor']}}</strong></p>
                            </div>
                            <div class="video-actions">
                                % if not verificar_like(db, info['usuario_id'], video['id']):
                                    <form action="/like-video" method="post">
                                        <input type="hidden" name="video_id" value="{{video['id']}}">
                                        <button type="submit" class="like-button">Curtir</button>
                                    </form>
                                % else:
                                    <button class="like-button" disabled>Curtido</button>
                                % end
                                <p>{{video['likes']}} curtidas</p>
                            </div>
                            <div class="comments-section">
                                <h3>Comentários</h3>
                                <ul class="comments-list">
                                    % for comentario in video['comentarios']:
                                        <li><strong>{{comentario['autor']}}:</strong> {{comentario['conteudo']}}</li>
                                    % end
                                </ul>
                                <form class="comment-form" action="/comentar-video" method="post">
                                    <input type="hidden" name="video_id" value="{{video['id']}}">
                                    <input type="text" name="conteudo" placeholder="Adicione um comentário..." required>
                                    <button type="submit">Enviar</button>
                                </form>
                            </div>
                        </div>
                    </div>
                % end
            </div>
        </main>
    </div>
</body>
</html>