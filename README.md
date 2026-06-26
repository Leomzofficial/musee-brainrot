# 🧠 Le Musée du Brainrot de Leomz

La collec de Brainrots de Leomz, réunie au même endroit — même quand ils sont éparpillés sur ses 5 comptes Roblox.

Pour juste **regarder** le musée : ouvre le fichier `index.html` (double-clic), ou va sur le lien du site une fois qu'il est en ligne.

---

## ➕ Ajouter un Brainrot (la vraie méthode, qui reste pour toujours)

Il y a 3 petites étapes.

### 1. La photo
- Va voir ton Brainrot dans le jeu (sur un **serveur privé**, comme ça personne te le vole) et prends une **capture d'écran**.
- Renomme le fichier simplement : **que des minuscules, pas d'espaces, pas d'accents**.
  Exemples : `boumboum.png`, `grenouille_roi.png` ✅ — ❌ pas `Mon Brainrot.png`
- Glisse la photo dans le dossier **`photos/`**.

### 2. La petite ligne
Ouvre `index.html` et cherche la grande liste qui commence par `let COLLECTION = [`.
Copie-colle ce modèle et change les infos :

```js
  {name:"Le nom du Brainrot", tier:"rare", coll:1, img:"photos/boumboum.png", emoji:"🖼️",
   desc:"Ce que tu veux raconter dessus.",
   power:"50", value:"500 §"},
```

À remplir :
- **name** → son nom
- **tier** → sa rareté : `commun`, `rare`, `epique`, `legendaire` ou `mythique`
- **coll** → sur quel compte il est : `1` à `5` (voir la liste plus bas)
- **img** → le nom de ta photo : `"photos/tonfichier.png"`
- **desc** → un petit texte (mets ce que tu veux, c'est plus marrant !)

Pas de photo encore ? Laisse `img:""` et mets un emoji à la place dans `emoji:"🐸"`.

### 3. C'est en ligne
Demande à ton oncle de **mettre à jour le site** (lui s'occupe du `git push`). Et voilà, ta nouvelle carte apparaît ! 🎉

---

## 🎮 Tes 5 comptes

| coll | Compte |
|------|--------------|
| 1 | Kakou19 |
| 2 | Superkakou20 |
| 3 | Superkakou21 |
| 4 | Superkakou22 |
| 5 | Superkakou23 |

Pour changer un pseudo ou une couleur : en haut du `<script>` dans `index.html`, modifie le bloc `COLLECTIONS`. Les boutons de filtre se mettent à jour tout seuls.

---

## ⚡ La méthode rapide (mais ça ne se garde pas)

Dans le musée, le bouton **« + Ajouter »** te laisse poser un Brainrot tout de suite, juste pour t'amuser pendant ta visite. ⚠️ Ça **disparaît dès que tu recharges la page** — pour le garder pour de vrai, utilise les 3 étapes plus haut.

---

## 🛠️ Pour l'oncle — mise en ligne (GitHub Pages)

1. Crée un dépôt **public**, pousse ce dossier tel quel (le fichier s'appelle déjà `index.html`).
2. `Settings → Pages → Source : branche main`.
3. L'URL `https://<pseudo>.github.io/<depot>/` est en ligne en ~1 min.

Aucun build : c'est du HTML/CSS/JS pur. Alternatives glisser-déposer si tu préfères du non-public : **Netlify Drop** ou **Cloudflare Pages**.
