from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# Initialisation de l'application Ursina
app = Ursina()
window.title = 'Optimized 3D Game'
window.fullscreen = False  # Désactiver le plein écran pour de meilleures performances
window.borderless = False

# Chargement de la carte à partir d'un fichier .obj et application de la texture avec colliders
map = Entity(model='spawn.obj', texture='texture.png', collider='mesh', scale=1)
map.model.generate_normals()  # Génération des normales pour les ombres

# Création de deux personnages pour le multijoueur
player1 = FirstPersonController()
player2 = FirstPersonController()
player2.position = (3, 0, 0)  # Position initiale du deuxième joueur

# Création du sol (au cas où la carte n'a pas de sol)
ground = Entity(model='plane', collider='box', scale=(100, 1, 100), texture='white_cube', texture_scale=(100, 100))

# Ajout de lumières
sun = DirectionalLight()
sun.look_at(Vec3(1, -1, -1))
sun.shadows = True

# Lumière ambiante
ambient_light = AmbientLight(color=color.rgba(100, 100, 100, 0.3))

# Création du menu de paramètres
def toggle_settings_menu():
    if settings_menu.enabled:
        settings_menu.disable()
        player1.enable()
        player2.enable()
        mouse.locked = True
        mouse.visible = False
    else:
        settings_menu.enable()
        player1.disable()
        player2.disable()
        mouse.locked = False
        mouse.visible = True

settings_menu = Entity(parent=camera.ui, enabled=False)
settings_menu_background = Entity(parent=settings_menu, model='quad', scale=(0.5, 0.5), color=color.gray, position=(0, 0, 0.1))
settings_text = Text(parent=settings_menu, text='Settings Menu', scale=2, position=(-0.1, 0.05))

# Désactiver le menu au démarrage
settings_menu.disable()

def update():
    if held_keys['escape']:
        toggle_settings_menu()
        held_keys['escape'] = False  # Empêche le menu de s'ouvrir et de se fermer instantanément

    if not settings_menu.enabled:
        # Contrôles pour le joueur 2 (utiliser d'autres touches que celles de joueur 1)
        player2.speed = 5
        if held_keys['i']:
            player2.position += player2.forward * time.dt * player2.speed
        if held_keys['k']:
            player2.position -= player2.forward * time.dt * player2.speed
        if held_keys['j']:
            player2.position -= player2.right * time.dt * player2.speed
        if held_keys['l']:
            player2.position += player2.right * time.dt * player2.speed
        if held_keys['u']:
            player2.position += Vec3(0, 1, 0) * time.dt * player2.speed
        if held_keys['o']:
            player2.position -= Vec3(0, 1, 0) * time.dt * player2.speed

# Lancement de l'application
app.run()
