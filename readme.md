# Pinboard manager
Gestion locale d'images, navigation, système de tags, recherche.

`Django` + `SQLite`

# Ajouter des images
```bash
python manage.py add_images
```

# Styles, JS
Les styles sont gérés par Tailwind. Une commande est présente pour collecter automatiquement les fichiers statiques
```bash
$ cd images/static
$ npm start # génère les styles w/ Tailwind
```
Côté Django, la commande `images/management/commands/watch_files.py`
```bash
python manage.py watch_static & python manage.py runserver
```

Les deux démons doivent être lancés en même temps

# Recherche
Pour rechercher un tag, on entoure le terme de `:`

```bash
:typographie: :couleur:
```

Pour rechercher un terme dans le nom, on ne met rien devant
```bash
gerstner
```

Et on peut bien sûr croiser les deux
```bash
:typographie: :couleur: gerstner
```

> La recherche est de type AND. on recherche : 
> tag contient 'typographie' AND tag contient 'couleur' AND name contient 'gerstner'
