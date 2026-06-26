#!/usr/bin/env python3
"""
2e passe : images + desc manquantes depuis steal-a-brainrot.org
Ne télécharge/patche que ce qui est encore vide dans index.html.
"""

import re, io, sys, unicodedata, urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image

PHOTOS_DIR = Path("/Users/michaelmougin/Documents/Brainrots/photos")
HTML_PATH  = Path("/Users/michaelmougin/Documents/Brainrots/index.html")
BASE  = "https://steal-a-brainrot.org"
UA    = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
MAX_W, QUAL = 700, 82

SITE_SLUGS = set("""
1x1x1x1 25 67 abyssaloco agarrini-la-palini alessio anpali-babel antonio aquarino
arcadopus arcadragon bacuru-and-egguru ballerina-peppermintina bambu-bambu-sahur
bananita-dolphinita bananito bananito-bandito bandito-axolito baskito bearito-cabinito
bee-loco belula-beluga berryno bisonte-giuppitere blackhole-goat blueberrinni-octopusini
boatito-auratito boba-panda bombardiro-vaccariro boppin-bunny brunito-marsito brutto-gialutto
buho-de-fuego buho-de-noelo buho-de-volto bulbito-bandito-traktorito bunito-bunito-spinito
bunny-and-eggy bunny-bunny-bunny-sahur bunny-tralala bunnyman buntteo burguro-and-fryuro
burrito-bandito camera-ramena capitano-gullini capitano-moby cappuccino-clownino
caramello-filtrello carloo carrotini-brainini cash-or-card caylusaurus celestial-pegasus
celularcini-viciosini centrucci-nuclucci cerberus chachechi chicleteira-bicicleteira
chicleteira-cupideira chicleteira-noelteira chicleteira-surfeiteira chicleteirina-bicicleteirina
chill-puppy chillin-chili chihuanini-taconini chimnino chimpanzini-spiderini chipso-and-queso
chocco-bunny chrismasmamat churrito-bunnito cigno-fulgoro clickerino-crabo cloverat-clapat
clovkur-kurkur cocoa-assassino coco-and-mango cocosini-mama coffin-tung-tung-tung-sahur
cooki-and-milki corn-corn-corn-sahur craburger crabbo-limonetta cuadramat-and-pakrahmatmamat
cupcake-koala cupid-cupid-sahur cupid-hotspot digi-narwhal dj-panda doi-doi-do
dolphini-jetskini donkeyturbo-express dragon-aquanini dragon-cannelloni dragon-gingerini
dug-dug-dug duggy-bros dul-dul-dul easter-easter-easter-sahur eggdin-egg-egg-dun
eid-eid-eid-sahur electro-quacko elefanto-frigo esok-sekolah eviledon extinct-matteo
extinct-tralalero festive-67 fishboard fishino-clownino fizzy-soda flancito flipa-sandala
fortunu-and-cashuru foxini-lanternini fragola-la-la-la fragrama-and-chocrama frankentteo
frio-ninja frogo-elfo frogato-pirato futbolini-skatini garama-and-madundung gattito-tacoto
gelato-lumacho giftini-spyderini ginger-cisterna ginger-gerat ginger-globo girafini-raftini
glaciator globa-steppa goat gobblino-uniciclino gold-gold-gold gorillo-subwoofero
graipuss-medussi granny griffin guerriro-digitale guest-666 gym-bros headless-horseman
ho-ho-ho-sahur hopilikalika-hopilikalako horegini-boom hydra-bunny hydra-dragon-cannelloni
ice-dragon jacko-jack-jack jacko-spaventosa jackorilla jelly-moby jingle-jingle-sahur
job-job-job-sahur john-doe john-pork jolly-jolly-sahur kalika-bros karkerheart-luvkur
karker-sahur karkerkar-kurkur ketchuru-and-musturu ketupat-bros ketupat-kepat kraken
krupuk-pagi-pagi la-anniversary-grande la-casa-boo la-cucaracha la-easter-grande
la-extinct-grande la-food-combinasion la-ginger-sekolah la-grande-combinasion la-jolly-grande
la-karkerkar-combinasion la-lucky-grande la-romantic-grande la-sahur-combinasion
la-secret-combinasion la-spooky-grande la-summer-grande la-supreme-combinasion
la-taco-combinasion la-vacca-jacko-linterino la-vacca-lepre-lepreino la-vacca-prese-presente
la-vacca-saturno-saturnita las-capuchinas las-sis las-tralaleritas las-vaquitas-saturnitas
lavadorito-spinito list-list-list-sahur los-25 los-67 los-amigos los-bombinitos los-bros
los-bunitos los-burritos los-candies los-chicleteiras los-chihuaninis los-chillis
los-combinasionas los-crocodillitos los-cucarachas los-cupids los-gattitos los-hackers
los-hotspotsitos los-jobcitos los-jolly-combinasionas los-karkeritos los-matteos
los-mi-gatitos los-mobilis los-noobinis los-nooo-my-hotspotsitos los-orcalitos los-planitos
los-primos los-puggies los-quesadillas los-sekolahs los-spaghettis los-spooky-combinasionas
los-spyderinis los-sweethearts los-tacoritas los-tipi-tacos los-tortus los-tralaleritos
los-trios love-love-bear love-love-love-sahur lovin-rose luck-luck-luck-sahur lumaca-malefica
luv-luv-luv magi-ribbitini malame-amarele mangolini-parrocini mariachi-corazoni
mastodontico-telepiedone meowl mi-gatito mieteteira-chicleteira money-money-bros money-money-man
money-money-puggy money-money-reindeer mummy-ambalabu mummio-rappitto nacho-spyder
naughty-naughty noobini-santanini noo-la-polizia noo-my-candy noo-my-eggs noo-my-examine
noo-my-gold noo-my-heart noo-my-present nooo-my-hotspot nuclearo-dinossauro octoball
ombrello-topolino orbi-mochi orcaledon orcalero-orcala orcalita-orcala pakrahmatmatina
pancake-and-syrup pandanini-frostini paradiso-axolottino patteo penguino-cocosino
penguin-tree perrito-burrito piccionetta-macchina pi-pi-watermelon pinealotto-fruttarino
pipi-avocado pipi-corni pirulitoita-bicicleteira please-my-present pop-pop-sahur
popcuru-and-fizzuru pot-hotspot pot-pumpkin pretzo-robo pumpkini-spyderini quackini-snackini
quackula quesadilla-crocodila quesadillo-vampiro rang-ring-bus reindeer-tralala
reinito-sleighito rhino-helicopterino rico-dinero rocco-disco robo-grafito rossetti-tualetti
rosey-and-teddy rubrikiko sammyni-cakini sammyni-fattini sammyni-spyderini sand-sand-sand
santa-hotspot santteo sealo-regalo serafinna-medusella signore-carapace sigma-girl
skibidi-toilet skull-skull-skull snailenzo snailo-clovero spaghetti-tualetti
spioniro-golubiro spinny-hammy spongini-quackini spooky-and-pumpky spyder-elephant
squalanana steakini-fattini stoppo-luminino strawberrita strawberry-elephant sushi-inu
swag-soda swaggy-bros tacorillo-crocodillo tacorita-bicicleta tang-tang-keletang
tartaragno telemorte tentacolo-tecnico ti-ti-ti-sahur tictac-sahur tigrilini-watermelini
tigroligre-frutonni tirilikalika-tirilikalako to-to-to-sahur tootini-shrimpini
torrtuginni-dragonfrutini tortuginni-sandcastlini tralaledon tralalero-tralala
tralalita-tralala tree-tree-tree-sahur trenostruzzo-turbo-4000 trenoturbo-axolotrico-9000
trickolino triplito-tralaleritos trippi-troppi trippi-troppi-troppa-trippa trulimero-trulicina
tuff-toucan tung-tung-tung-sahur ventoliero-pavonero vulturino-skeletono w-or-l
wheelchair-granny yess-my-examine yeti-claus zibra-zubra-zibralini zombie-tralala
""".split())

MANUAL = {
    # Corrections orthographiques
    "Blueberrenni Octopusini":        "blueberrinni-octopusini",
    "Maggi Ribbiniti":                "magi-ribbitini",
    "Celularcini Visiosini":          "celularcini-viciosini",
    "Tigrillini Watermelini":         "tigrilini-watermelini",
    "Tigroline Frutonni":             "tigroligre-frutonni",
    "Noo My Hotspot":                 "nooo-my-hotspot",
    "Nooo My Examen":                 "noo-my-examine",
    "Yes My Examen":                  "yess-my-examine",
    "Krupuk Pagi Pagi Pagi":          "krupuk-pagi-pagi",
    "Los Crocodilitos":               "los-crocodillitos",
    "Cocosino Mama":                  "cocosini-mama",
    "Centrucci Neclucci":             "centrucci-nuclucci",
    "Jackorila":                      "jackorilla",
    "Vulturino Esqueletono":          "vulturino-skeletono",
    "Tang Tang Kelatang":             "tang-tang-keletang",
    "Fragama And Chocrama":           "fragrama-and-chocrama",
    "Los Combinacionas":              "los-combinasionas",
    "Spooky and Pompky":              "spooky-and-pumpky",
    "Los Spooky Combinacionas":       "los-spooky-combinasionas",
    "Chillin Chillin":                "chillin-chili",
    "Pipi Watermelon":                "pi-pi-watermelon",
    "Ti Ti Ti Ti Sahur":              "ti-ti-ti-sahur",
    "To To To To Sahur":              "to-to-to-sahur",
    "Pirolitoita Bicicleteira":       "pirulitoita-bicicleteira",
    "Pakrahmatmamatina":              "pakrahmatmatina",
    "Rosetti Tualetti":               "rossetti-tualetti",
    "Clovker Kurkur":                 "clovkur-kurkur",
    "Trenotubo Axolotrico 9000":      "trenoturbo-axolotrico-9000",
    "Trenozztruzzo Turbo 4000":       "trenostruzzo-turbo-4000",
    "Triplito Tralaleritos (Secret)": "triplito-tralaleritos",
    "Los Jolly Combinasionas":        "los-jolly-combinasionas",
    # Nouvelles corrections (2e passe)
    "Cupkake Koala":                  "cupcake-koala",
    "Trullimero Trulicina":           "trulimero-trulicina",
    "Buho de Nuelo":                  "buho-de-noelo",
    "Los Gatitos":                    "los-gattitos",
    "Ketupak Kepat":                  "ketupat-kepat",
    "Las Tacoritas":                  "los-tacoritas",
    "Noobini Santanini":              "noobini-santanini",
}

def slugify(n):
    n = re.sub(r'\(.*?\)', '', n)
    n = unicodedata.normalize('NFKD', n).lower()
    n = re.sub(r'[^a-z0-9]+', '-', n)
    return re.sub(r'-+', '-', n).strip('-')

def site_slug(name):
    if name in MANUAL:
        return MANUAL[name]
    s = slugify(name)
    return s if s in SITE_SLUGS else None

def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read()
    except Exception:
        return None

def to_jpg(data, dest):
    try:
        img = Image.open(io.BytesIO(data))
        if img.mode in ('RGBA','LA','P'):
            bg = Image.new('RGB', img.size, (255,255,255))
            bg.paste(img.convert('RGBA'), mask=img.convert('RGBA').split()[3])
            img = bg
        else:
            img = img.convert('RGB')
        if img.width > MAX_W or img.height > MAX_W:
            img.thumbnail((MAX_W, MAX_W), Image.LANCZOS)
        img.save(dest, 'JPEG', quality=QUAL, optimize=True)
        return True
    except Exception as e:
        print(f"  [err] {e}", file=sys.stderr)
        return False

def parse(raw):
    h = re.sub(r'<!--.*?-->', '', raw.decode('utf-8', errors='replace'))
    desc = prix = revenu = ""
    m = re.search(r'<p class="text-base text-gray-500 mb-2">(.+?)</p>', h)
    if m: desc = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    m = re.search(r'Base Cost</div><div[^>]*>\$([^<]+)', h)
    if m: prix = "$" + m.group(1).strip()
    m = re.search(r'Income per Second</div><div[^>]*>\$([^<]+)', h)
    if m: revenu = "$" + m.group(1).strip() + "/s"
    return desc, prix, revenu

# ── Lire l'état actuel de index.html ──
html = HTML_PATH.read_text(encoding='utf-8')

accounts = {'Kakou19','Superkakou20','Superkakou21','Superkakou22','Superkakou23'}
entries_raw = re.findall(r'\{name:"[^"]+",.*?(?=,?\s*\{name:|,?\s*\];)', html, re.DOTALL)

need_desc = set()
all_names = []
for e in entries_raw:
    nm = re.search(r'name:"([^"]+)"', e)
    if not nm or nm.group(1) in accounts: continue
    name = nm.group(1)
    all_names.append(name)
    if re.search(r'desc:""', e): need_desc.add(name)

# Construire la liste : toutes les entrées qui ont un slug sur le site
to_fetch = {}
unmapped = []
for name in all_names:
    s = site_slug(name)
    if s:
        to_fetch[name] = s
    else:
        unmapped.append(name)

print(f"Sur le site : {len(to_fetch)}   Hors site : {len(unmapped)}   Sans desc : {len(need_desc)}")
print(f"\n→ Téléchargement de toutes les images + descriptions manquantes\n")

def process(name, slug):
    r = {"name": name, "slug": slug, "img_path": None, "img_new": False,
         "desc": "", "prix": "", "revenu": ""}
    # Image : toujours re-télécharger depuis le site pour rester à jour
    dest = PHOTOS_DIR / f"{slug}.jpg"
    data = fetch(f"{BASE}/images/brainrots/{slug}.webp")
    if data and to_jpg(data, dest):
        r["img_path"] = f"photos/{slug}.jpg"
        r["img_new"] = True
    elif dest.exists():
        r["img_path"] = f"photos/{slug}.jpg"   # garder l'existante si download échoue
    # Page pour desc/prix/revenu (seulement si desc encore vide)
    if name in need_desc:
        raw = fetch(f"{BASE}/brainrots/{slug}")
        if raw:
            r["desc"], r["prix"], r["revenu"] = parse(raw)
    return r

results = {}
with ThreadPoolExecutor(max_workers=20) as ex:
    futs = {ex.submit(process, n, s): n for n, s in to_fetch.items()}
    for fut in as_completed(futs):
        r = fut.result()
        results[r["name"]] = r

# ── Patch index.html entrée par entrée ──
imgs_ok = imgs_updated = descs_ok = 0
for name, r in results.items():
    pat = rf'\{{[^{{}}]*name:"{re.escape(name)}"[^{{}}]*\}}'
    m = re.search(pat, html)
    if not m:
        print(f"  [warn] entrée non trouvée pour {name}", file=sys.stderr)
        continue
    old = m.group(0)
    new = old
    if r["img_path"]:
        cur = re.search(r'img:"([^"]*)"', old)
        cur_val = cur.group(1) if cur else ''
        if cur_val != r["img_path"]:
            new = re.sub(r'img:"[^"]*"', f'img:"{r["img_path"]}"', new)
            if r["img_new"]: imgs_updated += 1
        if r["img_new"]: imgs_ok += 1
    if r["desc"] and re.search(r'desc:""', old):
        safe = r["desc"].replace('\\', '\\\\').replace('"', '\\"')
        new = re.sub(r'desc:""', f'desc:"{safe}"', new)
        descs_ok += 1
    if r["prix"] and re.search(r'prix:"\?"', old):
        new = re.sub(r'prix:"\?"', f'prix:"{r["prix"]}"', new)
    if r["revenu"] and re.search(r'revenu:"\?"', old):
        new = re.sub(r'revenu:"\?"', f'revenu:"{r["revenu"]}"', new)
    if new != old:
        html = html.replace(old, new, 1)

HTML_PATH.write_text(html, encoding='utf-8')

# ── Résumé ──
print(f"\n✅ Images téléchargées : {imgs_ok}  (dont chemins mis à jour : {imgs_updated})")
print(f"✅ Nouvelles descriptions : {descs_ok}")
