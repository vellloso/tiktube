<!DOCTYPE html>
<html lang="pt-BR">
<head>
   <meta charset="UTF-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>Upload de Vídeo</title>
   <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&display=swap">
   <link rel="stylesheet" type="text/css" href="/static/css/upload.css">
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
            <h2>Upload de Vídeo</h2>
            <form action="/upload-video" method="post" enctype="multipart/form-data">
                <label for="titulo">Título do Vídeo:</label>
                <input type="text" id="titulo" name="titulo" required><br><br>
                <label for="video">Selecione o Vídeo:</label>
                <input type="file" id="video" name="video" accept="video/*" required><br><br>
                <input type="submit" value="Upload">
            </form>
        </main>
    </div>
</body>
</html>