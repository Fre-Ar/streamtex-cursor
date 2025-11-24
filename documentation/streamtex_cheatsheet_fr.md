# 📚 Streamtex Complete Cheatsheet

## 📥 Imports Essentiels

```python
from streamtex_package.src.streamtex import *
from streamtex_package.src.streamtex.styles import Style as ns, StyleGrid as sg
from streamtex_package.src.streamtex.streamtex_enums import Tags as t, ListTypes as l
```

## 🎨 Organisation des Styles

### Classe de Styles Personnalisés

```python
class BlockStyles:
    """Custom styles defined locally and used only for this block"""
    # Styles composés
    content = s.Large + s.center_txt
    lime_bold = s.text.colors.lime + s.bold
    bold_green = s.project.colors.green_01 + s.bold
    
    # Styles avec alignement
    green_title = bold_green + s.huge + s.center_txt
    
    # Styles avec bordures
    border = s.container.borders.color(s.text.colors.black) + \
             s.container.borders.solid_border + \
             s.container.borders.size("2px")
    
    # Styles avec padding
    side_padding = ns("padding: 10pt 36pt;")
bs = BlockStyles
```

## 📝 Éléments de Base

### Blocs et Texte

```python
# Bloc simple avec style
html += st_block(s.center_txt, [
    st_write(bs.green_title, "Mon Titre"),
    st_space(size=3)
])

# Bloc avec liste
html += st_block(s.center_txt, [
    st_list(
        list_type=l.ordered,
        li_style=bs.content,
        block_list=[
            st_write(txt="Premier élément"),
            st_write(txt="Second élément")
        ]
    )
])
```

### Images et Médias

```python
# Image simple
st_image(uri="image.png")

# Image avec dimensions
st_image(uri="image.png", width="1150px", height="735.34px")

# Image avec lien
st_image(uri="image.png", link="https://example.com")

# Image avec style auto-height
st_image(s.container.sizes.height_auto, uri="image.png")
```

### Grilles et Tableaux

```python
# Grille 3x2
html += st_grid(3, 2, 
    cell_styles=bs.border + s.container.paddings.little_padding,
    block_list=[
        st_image(uri="image1.png"),
        st_image(uri="image2.png"),
        st_image(uri="image3.png")
    ]
)

# Tableau avec styles personnalisés
html += st_table(
    cell_styles=sg.create("A1,A3", s.project.colors.orange_02) +
                sg.create("A2", s.project.colors.red_01) +
                sg.create("A1:B3", s.bold + s.LARGE),
    block_list=[
        ["Titre", "Lien"],
        ["Item 1", "lien1"],
        ["Item 2", "lien2"]
    ]
)
```

## 🔗 Liens et Navigation

### Liens

```python
# Lien simple
st_write(txt="Cliquez ici", link="https://example.com")

# Lien stylisé
link_style = s.text.colors.blue + s.text.decors.underline_text
st_write(link_style, txt="Lien stylisé", link="https://example.com", no_link_decor=True)
```

### Table des Matières

```python
# Niveau principal
st_write(style, "Section", toc_lvl=TOC("1"))

# Sous-niveau
st_write(style, "Sous-section", toc_lvl=TOC("+1"))
```

## 🎯 Styles Prédéfinis

### Couleurs

```python
# Couleurs du projet
s.project.colors.blue_01
s.project.colors.green_01
s.project.colors.orange_01
s.project.colors.red_01
s.project.colors.brown_01

# Couleurs de texte
s.text.colors.lime
s.text.colors.black
```

### Tailles de Texte

```python
s.huge          # Très grand
s.LARGE         # Plus grand
s.Large         # Grand
s.large         # Normal
```

### Alignements et Mise en Page

```python
s.center_txt
s.container.flex.center_align_items
s.container.layouts.vertical_center_layout
```

### Décorations

```python
s.bold
s.italic
s.text.decors.underline_text
```

## 🔧 Utilitaires

### Espacement

```python
# Espace vertical
st_space(size=3)
st_space("v", size=2)

# Espace horizontal
st_space("h", size=1)

# Saut de ligne
st_br()
```

### Conteneurs

```python
# Padding
s.container.paddings.little_padding
s.container.paddings.small_padding

# Bordures
s.container.borders.solid_border
s.container.borders.size("2px")
```

## 💡 Exemples Complets

### Page de Documentation

```python
def html_block():
    html = ""
    html += st_block(bs.center_txt, [
        st_write(bs.green_title, "Documentation"),
        st_space(size=3),
        st_list(l.ordered, bs.content, [
            "Premier point",
            "Second point"
        ])
    ])
    return html
```

### Showcase avec Grille

```python
def html_block():
    html = ""
    html += st_grid(3, 2, 
        cell_styles=bs.border,
        block_list=[
            st_image(uri="image1.png"),
            st_image(uri="image2.png"),
            st_write(bs.content, "Description")
        ]
    )
    return html
```

### Exemple de Page Complète

```python
def html_block():
    html = ""

    # En-tête avec titre
    html += st_block(s.center_txt + s.LARGE + s.bold, [
        st_write(s.project.colors.blue_01 + s.huge, "Titre Principal", toc_lvl=TOC("1")),
        st_space(size=2),
        st_write(s.project.colors.orange_01, "Sous-titre", toc_lvl=TOC("+1")),
        st_space(size=3)
    ])

    # Contenu principal
    html += st_block(s.center_txt, [
        st_list(
            list_type=l.ordered,
            li_style=bs.content,
            block_list=[
                st_write(txt="Section 1"),
                st_write(txt="Section 2"),
                st_write(txt="Section 3")
            ]
        )
    ])

    # Grille d'images
    html += st_grid(2, 2,
        cell_styles=bs.border + s.container.paddings.little_padding,
        block_list=[
            st_image(uri="image1.png"),
            st_image(uri="image2.png"),
            st_write(bs.content, "Description 1"),
            st_write(bs.content, "Description 2")
        ]
    )

    # Liens et références
    html += st_block(s.center_txt + s.Large, [
        st_write(bs.link_style, txt="Lien 1", link="https://example1.com"),
        st_space(size=1),
        st_write(bs.link_style, txt="Lien 2", link="https://example2.com")
    ])

    return html
```

## 📌 Notes Importantes

1. Toujours initialiser le HTML avec `html = ""`
2. Utiliser les classes de style pour organiser le code
3. Combiner les styles avec l'opérateur `+`
4. Utiliser `st_space()` pour gérer les espacements
5. Penser à la hiérarchie des titres pour la table des matières

## 🔍 Astuces et Bonnes Pratiques

1. Regrouper les styles communs dans une classe `BlockStyles`
2. Utiliser des variables pour les styles réutilisés
3. Commenter les sections complexes
4. Structurer le code en sections logiques
5. Utiliser les espaces verticaux pour améliorer la lisibilité

