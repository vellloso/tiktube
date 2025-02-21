<!DOCTYPE html>
<html lang="pt-BR">
<head>
   <meta charset="UTF-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>Administração</title>
   <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&display=swap">
   <link rel="stylesheet" type="text/css" href="/static/css/admin.css">
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
            <h2>Gerenciar Usuários</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nome</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    % for usuario in info['usuarios']:
                        <tr>
                            <td>{{usuario.id}}</td>
                            <td>{{usuario.nome}}</td>
                            <td>
                                <form action="/delete-user" method="post" style="display:inline;">
                                    <input type="hidden" name="usuario_id" value="{{usuario.id}}">
                                    <button type="submit" class="btn-delete">Excluir</button>
                                </form>
                            </td>
                        </tr>
                    % end
                </tbody>
            </table>
            <h2>Gerenciar Vídeos</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Título</th>
                        <th>Autor</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    % for video in info['videos']:
                        <tr>
                            <td>{{video.id}}</td>
                            <td>{{video.titulo}}</td>
                            <td>{{video.usuario.nome}}</td>
                            <td>
                                <form action="/delete-video-admin" method="post" style="display:inline;">
                                    <input type="hidden" name="video_id" value="{{video.id}}">
                                    <button type="submit" class="btn-delete">Excluir</button>
                                </form>
                            </td>
                        </tr>
                    % end
                </tbody>
            </table>
        </main>
    </div>
</body>
</html>