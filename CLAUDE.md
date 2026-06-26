# CLAUDE.md — Le Grand Musée des Brainrots de Leomz

Contexte pour Claude Code. Lis ce fichier avant toute modification.

## C'est quoi ce projet
Un site web d'une seule page (`index.html`) : un "musée virtuel" qui présente la
collection de Brainrots (créatures du jeu Roblox *Steal a Brainrot*) du neveu, **Leomz**.
La collection est répartie sur 5 comptes Roblox et réunie ici en un seul endroit.

Hébergé sur **GitHub Pages** : dépôt `Leomzofficial/musee-brainrot`,
en ligne sur `https://leomzofficial.github.io/musee-brainrot/`.

## Comment ça marche pour l'utilisateur
1. **Écran d'accueil** : la façade dorée (`titre.jpg`) en plein écran + un bouton **ENTRER**.
2. Au clic sur ENTRER, l'accueil s'efface en fondu et on découvre la **collection** :
   décor = l'intérieur du musée (`fond.jpg`), avec les Brainrots affichés en cartes.

## Fichiers
- `index.html` — TOUT est dedans (HTML + CSS + JS, aucune dépendance, aucun build).
- `titre.jpg` — la façade dorée, utilisée en fond plein écran de l'accueil.
- `fond.jpg` — l'intérieur de la galerie, utilisé en fond de la page collection.
- `banniere.jpg` — ancienne bannière, **non utilisée** (peut être ignorée ou supprimée).
- `photos/` — les captures d'écran des Brainrots (une image par créature).
- `photos/exemple.png` — image d'exemple ; à supprimer quand de vraies photos existent.
- `README.md` — mode d'emploi pour Leomz.

## Ajouter / modifier des Brainrots
Tout se passe dans `index.html`, dans le tableau `COLLECTION` (commenté dans le code).
Chaque Brainrot est un objet :
```js
{name:"Nom", tier:"rare", coll:1, img:"photos/nomfichier.png", emoji:"🐸",
 desc:"petit texte", power:"50", value:"500 §"},
```
- `tier` (rareté) : `commun` | `rare` | `epique` | `legendaire` | `mythique`
- `coll` (compte d'origine) : entier de `1` à `5` (voir plus bas)
- `img` : chemin vers la capture, ex. `"photos/boumboum.png"` ; mettre `""` si pas de photo
- `emoji` : affiché à la place de l'image si `img` est vide ou introuvable

## Les 5 comptes (bloc `COLLECTIONS` en haut du `<script>`)
| coll | pseudo |
|------|--------------|
| 1 | Kakou19 |
| 2 | Superkakou20 |
| 3 | Superkakou21 |
| 4 | Superkakou22 |
| 5 | Superkakou23 |
Les boutons de filtre "comptes" et le menu du formulaire sont générés
automatiquement depuis ce bloc : pour renommer un compte ou changer sa couleur,
modifier UNIQUEMENT `COLLECTIONS`, ne pas toucher au HTML des filtres.

## Architecture interne (JS)

Tout le code est dans le `<script>` en bas de `index.html`. Pas de framework, pas de modules.

- **`COLLECTION`** → tableau de données, source unique de vérité pour les cartes.
- **`COLLECTIONS`** → objet de config des comptes (nom + couleur). Ne jamais dupliquer cette info dans le HTML.
- **`TIERS` / `RC`** → mappent les clés de rareté vers les classes CSS (`r-commun`, etc.) et les valeurs de couleur CSS (`--rc`).
- **`visible()`** → filtre `COLLECTION` selon `activeFilter`, `activeColl` et `searchTerm`. Appelée par `render()`.
- **`render()`** → reconstruit intégralement `#gallery` en innerHTML à partir de `visible()`. Appelée à chaque changement de filtre ou de recherche.
- **`openPiece(idx)`** → remplit et ouvre `#modal` avec le détail d'une carte (index dans `COLLECTION`).
- **`buildAccounts()`** → génère les boutons de filtre `#chipsColl` et les `<option>` du formulaire depuis `COLLECTIONS`. Appelée une seule fois au chargement.
- **`savePiece()`** → pousse un objet dans `COLLECTION` puis appelle `render()`. Mémoire uniquement, reset au rechargement.
- **Deux modals** : `#modal` (détail lecture seule) et `#addModal` (formulaire ajout). Ouverture/fermeture par `.classList.add/remove('open')`.
- **Intro** : `#intro` est `position:fixed` z-index 200 ; le clic sur ENTRER ajoute `.hide` (opacity 0) puis `display:none` après 650 ms. Le scroll est bloqué (`overflow:hidden`) jusqu'à ce clic.

## Règles importantes
- **Noms de fichiers images** : minuscules, sans espaces ni accents (ex. `boumboum.png`,
  pas `Mon Brainrot.png`). C'est la cause n°1 d'images qui ne s'affichent pas.
- **Optimiser les images** avant de les committer (cible ~500 Ko max) : l'utilisateur
  est sur un MacBook Intel et les gros fichiers font ramer le navigateur. Compresser
  en JPEG qualité ~82-85, largeur max ~1400 px. (Pillow dispo en Python.)
- **Performance** : pas de `filter: blur()` lourds ni de `background-attachment: fixed`
  (ça a déjà fait laguer). Les fonds plein écran se font via un élément `position:fixed`.
  Les cartes utilisent `content-visibility:auto` pour rester fluides en grand nombre.
- **Garder le fichier unique** : pas de framework, pas de build, pas de CDN superflu.
- Toujours respecter `prefers-reduced-motion` (déjà géré dans le CSS).

## Publier (mise en ligne)
GitHub Pages publie automatiquement la branche `main`. Après une modif :
```bash
git add .
git commit -m "message clair"
git push
```
Le site est à jour ~1 minute après. (Auth déjà faite via `gh auth login`.)

## Style / ton
Public = ado de 12 ans. Design fun et coloré (cartes type jeu, raretés colorées,
police Fredoka). Vocabulaire décontracté dans les textes (pas de jargon de musée
"officiel"). Le titre du site et l'identité visuelle tournent autour de Leomz.
