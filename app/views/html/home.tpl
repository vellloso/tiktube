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
                % if info['info']['logado'] == 'SIM':
                    <li><a href="/profile">Perfil</a></li>
                    <li><a href="/chat-{{info['info']['usuario_id']}}">Chat</a></li>
                % end
                % if info['info'].get('is_admin', False):
                    <li><a href="/admin">Admin</a></li>
                % end
                <li><a href="/logout">Sair</a></li>
            </ul>
        </nav>
        <main class="main-content">
            <div class="user-info">
                % if info['info']['logado'] == 'SIM':
                    <h2>Bem-vindo, {{info['info']['nome']}}</h2>
                    <a href="/home/following" class="btn">Seguindo</a>
                    <a href="/home" class="btn">Tudo</a>
                % else:
                    <a href="/login" class="btn">Logar</a>
                    <a href="/register" class="btn">Registrar</a>
                % end
            </div>
            <div class="video-list">
                % if info['videos']:
                    % for video in info['videos']:
                        <div class="video-container">
                            <video controls>
                                <source src="/static/videos/{{video['caminho']}}" type="video/mp4">
                                Seu navegador não suporta o elemento de vídeo.
                            </video>
                            <div class="video-right">
                                <div class="video-info">
                                    <h2>{{video['titulo']}}</h2>
                                    <p>Por <strong>{{video['autor']}}</strong></p>
                                    <a href="/profile/{{video['autor_id']}}" class="btn">Visitar Perfil</a>
                                </div>
                                <div class="video-actions">
                                    % if not info['verificar_like'](info['db'], info['info']['usuario_id'], video['id']):
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
                % else:
                    <p>Nenhum vídeo encontrado.</p>
                % end
            </div>
        </main>
    </div>
</body>
</html>