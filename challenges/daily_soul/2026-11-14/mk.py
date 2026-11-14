import os, sys
SHADOW = ("KEY POINT: one hard, low light source casts the person's sharp, crisp black shadow large on the plain wall right behind them, and the shadow's pose and action are COMPLETELY DIFFERENT from the real person's pose; the shadow is clearly attached at the person's feet but is doing its own thing. ")
LOOK = ("Look: real film still from a big-budget modern comedy, shot on 65mm film, real people with real skin and fabric texture, real locations. "
        "Any visible text must be real words exactly as printed in a dictionary or a published newspaper.")
P = [
# 1 treadmill vs pizza shadow
SHADOW + "A sweaty man in his 40s in a grey workout shirt runs hard on a treadmill in a quiet home gym at night, red-faced, gritting his teeth, arms pumping, completely focused on his diet. On the bare white wall right behind him, a single desk lamp throws his big black shadow, and the shadow is NOT running at all: the shadow sits relaxed on a shadow sofa, legs crossed, happily eating a big slice of pizza, cheese stretching, a shadow soda can in the other hand. The man has no idea. "
"Camera: eye-level medium-wide shot from the side, 35mm lens, deep focus, the running man in the left half and his much larger relaxed shadow filling the wall on the right. "
"Lighting: one hard warm lamp low on the floor, deep crisp black shadow on the white wall, the rest of the room dark blue. Color palette: grey shirt, black treadmill, white wall, warm lamp amber, cool blue night, fine film grain. " + LOOK,
# 2 proposal, shadow escaping
SHADOW + "In a romantic candlelit restaurant, a nervous young man in a suit kneels on one knee holding up an open ring box to his girlfriend, who covers her mouth with both hands, eyes shining with tears of joy. On the cream-colored wall behind them, the candlelight casts the young man's huge black shadow, and his shadow has panicked: it is sprinting away along the wall toward the exit door, arms flailing, the shadow ring box flying out of its hand. Other diners at nearby tables have started to notice the fleeing shadow, one waiter frozen with a tray. "
"Camera: eye-level medium-wide shot, 35mm lens, deep focus, the kneeling man and the girlfriend in the lower left, the long fleeing shadow stretched across the wall toward the exit on the right. "
"Lighting: warm low candlelight from the table casting one huge crisp shadow on the wall, soft golden glow, deep warm shadows. Color palette: cream wall, dark suit, red dress, gold candlelight, white tablecloth, fine film grain. " + LOOK,
# 3 selfie photobomb shadow
SHADOW + "A young woman in a yellow sundress takes a smiling selfie with her phone held up in front of a sunlit white stucco wall on a summer vacation street. Her own hard black shadow on the wall right behind her is photobombing her picture: the shadow is making rabbit ears with two fingers behind her shadow head, sticking out its tongue, one leg kicked up in a silly pose, fully in frame of her selfie. On her phone screen, the selfie preview shows the shadow's silly pose behind her. She has not noticed. "
"Camera: eye-level medium shot from slightly to the side, 50mm lens, both the woman and the whole silly shadow on the bright wall clearly visible, her phone screen readable. "
"Lighting: harsh bright midday Mediterranean sun from the side, one sharp crisp black shadow on the white wall, saturated colors. Color palette: white wall, yellow dress, blue sky edge, terracotta pot, deep black shadow, fine film grain. " + LOOK,
# 4 meeting, shadow clocking out
SHADOW + "A long, boring corporate meeting in a glass-walled conference room in the late afternoon. Ten employees in business clothes sit around the table facing a presenter and a slide of bar charts, all upright and attentive. Low golden sun from the window throws their shadows across the back white wall. Every shadow sits obediently like its owner, except one: the shadow of a young man in a blue shirt has quietly stood up, put on a shadow coat and a shadow backpack, and is tiptoeing toward the shadow of the door, waving a small goodbye, while the real young man still sits perfectly still, pretending to take notes. "
"Camera: eye-level wide shot from the end of the table, 35mm lens, deep focus, the whole row of seated people and the long wall of shadows behind them, the escaping shadow clearly different from all the others. "
"Lighting: warm low late-afternoon sun from the side window, long crisp shadows on the white wall, the room glowing gold. Color palette: white wall, navy and grey suits, blue shirt, warm gold light, black shadows, fine film grain. " + LOOK,
# 5 stage fright singer, rockstar shadow
SHADOW + "A shy young woman in a plain cardigan stands frozen in front of a microphone on the small stage of a karaoke bar, gripping the mic stand with both hands, eyes squeezed shut, stiff with stage fright, the small audience at tables looking at her. A single bright spotlight from the front throws her shadow huge onto the red velvet curtain behind her, and her shadow is a full rock star: it is jumping in the air with one leg kicked high, hair flying, holding the mic stand above its head like a guitar hero, mouth wide open in a scream of joy. The audience is staring at the shadow, mouths open. "
"Camera: low-angle medium-wide shot from the audience, 35mm lens, deep focus, the frozen woman small in the center and her giant rocking shadow filling the red curtain behind her. "
"Lighting: one hard white spotlight, crisp black shadow on the deep red curtain, colorful bar lights in the dark audience area. Color palette: deep red curtain, beige cardigan, white spotlight, neon pink and blue accents, fine film grain. " + LOOK,
]
m = sys.argv[1] if len(sys.argv) > 1 else 'soul_cinematic'
d = 'v1'
os.makedirs(d, exist_ok=True)
open(f'{d}/prompts.txt', 'w', encoding='utf-8', newline='\n').write('\n'.join(P) + '\n')
open(f'{d}/model.txt', 'w').write(m + '\n')
open(f'{d}/aspect.txt', 'w').write('3:2\n')
print(m, [len(p.split()) for p in P])
