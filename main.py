import ascii_magic
import os
import time
from PIL import Image

# Fonction pour extraire les frames d'un GIF et les sauvegarder en tant que fichiers temporaires
def extract_gif_frames(gif_path, temp_dir='temp_frames', fill_empty=False):
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    gif = Image.open(gif_path)
    frames = []
    try:
        frame_idx = 0
        while True:
            gif.seek(gif.tell() + 1)
            frame_filename = os.path.join(temp_dir, f"frame_{frame_idx}.png")
            gif.save(frame_filename)
            frames.append(frame_filename)
            frame_idx += 1
    except EOFError:
        pass  # Fin de la séquence
    return frames

# Convertir les frames en représentation ASCII
def convert_frames_to_ascii(frames):
    ascii_frames = []
    for frame in frames:
        # Convertir chaque frame en ASCII en utilisant ascii_magic à partir du fichier image
        ascii_art = ascii_magic.from_image(frame)  # Convertir l'image en ASCII
        ascii_frames.append(ascii_art)
    return ascii_frames

# Animer les frames ASCII dans le terminal

def ascii_GIF_to_php(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    php_code = """
    <?php
// Spécifier le répertoire où les fichiers HTML sont stockés
$directory = 'output_gif_php/';
$frames = [];

// Ouvrir le répertoire
if ($handle = opendir($directory)) {
    // Lire tous les fichiers .html dans le répertoire
    while (false !== ($file = readdir($handle))) {
        // Vérifier si le fichier est un fichier HTML
        if (strpos($file, '.html') !== false) {
            // Ajouter le chemin complet du fichier dans un tableau
            $frames[] = $directory . $file;
        }
    }
    // Fermer le répertoire
    closedir($handle);
}

// Vérifier si le tableau de fichiers HTML n'est pas vide
if (!empty($frames)) {
    // Générer une structure HTML de base
    echo "<html><head><title>Gif ASCII Animation</title>";
    echo "<style>body {text-align: center; font-family: monospace;}</style>";
    echo "</head><body>";
    
    // Créer une fonction JavaScript pour afficher les fichiers HTML successivement
    echo "
    <script type='text/javascript'>
        var frames = " . json_encode($frames) . ";
        var currentFrame = 0;
        var totalFrames = frames.length;
        
        function showNextFrame() {
            // Effacer le contenu de la page

            
            // Charger le fichier HTML du prochain frame
            fetch(frames[currentFrame])
                .then(response => response.text())
                .then(data => {
                     document.body.innerHTML = '';
                    // Afficher le contenu du fichier HTML
                    document.body.innerHTML = '<div>' + data + '</div>';
                });

            // Passer au frame suivant
            currentFrame = (currentFrame + 1) % totalFrames;
        }
        
        // Afficher un frame toutes les 500ms (ajustez la vitesse de l'animation)
        setInterval(showNextFrame, 200);
    </script>
    ";

    echo "</body></html>";
}
?>
    """



    # Créer le fichier PHP et y écrire le code
    with open("output_gif_php/index.php", "w", encoding="utf-8") as file:
        file.write(php_code)

    print("Le fichier PHP a été généré avec succès !")


def generate_html_files(ascii_frames, output_dir="frames"):

    # Parcourir chaque frame et créer un fichier HTML pour chaque frame
    for i, frame in enumerate(ascii_frames):
        frame_html = frame.to_html(columns=200)  # Convertir le frame ASCII en HTML

        # Nom du fichier pour chaque frame, par exemple "frame_0.html", "frame_1.html", etc.
        filename = f"{output_dir}/frame_{i}.html"

        # Générer le contenu du fichier HTML
        html_content = f"""<!DOCTYPE html>
                                <html lang="fr">
                                <head>
                                    <meta charset="UTF-8">
                                    <title>Frame {i}</title>
                                </head>
                                <body>
                                    {frame_html}
                                </body>
                                </html>
                                """

        # Écrire le contenu HTML dans le fichier
        with open(filename, "w") as file:
            file.write(html_content)
        print(f"Frame {i} sauvegardée dans {filename}")


def animate_ascii(ascii_frames, frame_pause=0.05, num_iterations=15, clear_prev_frame=True, i=0):
    # Initialiser la liste htmlascigif pour stocker tous les frames HTML
    htmlascigif = []

    for _ in range(num_iterations):
        for i, ascii_art in enumerate(ascii_frames):
            #ascii_art.to_terminal()  # Afficher l'art ASCII dans le terminal

            # Ajouter la version HTML du frame actuel à la liste htmlascigif
            htmlascigif.append(ascii_art.to_html_file(f"output_gif_php/frame{i}.html"))

            time.sleep(frame_pause)

            # Effacer l'écran si clear_prev_frame est True
            if clear_prev_frame:
                os.system('cls' if os.name == 'nt' else 'clear')  # Effacer l'écran pour chaque frame

    # Retourner la liste complète après toutes les itérations
    return htmlascigif
# Fonction principale pour gérer l'animation
def main():
    gif_path = "sarah-cameron.gif"  # Remplace par le chemin de ton GIF
    temp_dir = 'temp_frames'  # Répertoire temporaire pour les frames extraites
    output_dir = 'output_gif_php'
    # Créer le répertoire de sortie s'il n'existe pas
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Extraire les frames et les sauvegarder
    frames = extract_gif_frames(gif_path, temp_dir=temp_dir)

    # Convertir les frames en ASCII
    ascii_frames = convert_frames_to_ascii(frames)

    # Attendre avant de démarrer l'animation
    time.sleep(11)  # Délai avant le début de l'animation

    # Démarrer l'animation ASCII
    test=animate_ascii(ascii_frames, num_iterations=2)
    print(test)
    ascii_GIF_to_php(output_dir)

    # Nettoyer les fichiers temporaires après l'animation
    for frame in frames:
        os.remove(frame)
    os.rmdir(temp_dir)

# Lancer le programme
if __name__ == "__main__":
    main()
