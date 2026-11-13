import os, sys
# 11/12 당선작 구조: 주인공 → 핵심 소품 → 세계 → Camera → Lighting → Look → 금지 목록
LOOK = ("Look: real film still from a big-budget modern adventure comedy, shot on 65mm motion picture film, a real living human only about five centimeters tall photographed like a real actor, real skin and fabric texture, a real full-size ordinary home with real materials. "
        "Photoreal only, one tiny person, full-size real home not a miniature set, not a toy, not a figurine, no CGI look, no cartoon style, no text, no logos, no watermark, no extra limbs, no distorted hands.")
P = [
# 1 frying an egg
"A man in his 30s who went to bed six feet tall woke up this morning only the size of a thumb in his own apartment, and he still has to make breakfast. He wears wrinkled blue-and-white striped cotton pajamas and is barefoot, standing on the rim of a black frying pan on the stove, lifting a whole normal-size white chicken egg high above his head with both arms, back arched, about to smash it on the pan's edge with his entire body, his face determined and straining. "
"The egg is bigger than his torso, its shell matte with fine pores, a thin crack already running across it and one clear drop of egg white falling into the sizzling melted butter below, tiny bubbles popping. "
"Around him the ordinary kitchen rises like a giant landscape: the steel stovetop, a salt shaker as tall as a lighthouse, a coffee mug like a tower, crumbs like boulders on the counter. "
"Camera: low-angle full-body hero shot at his eye level from the stovetop, 35mm lens, deep focus so the kitchen behind him stays readable, he stands in the left third of the frame with the egg raised against the bright window. "
"Lighting: warm golden morning sunlight from the kitchen window behind him, soft steam rising from the pan catching the light, warm rim light on his hair and the egg, glossy reflections on the butter. Color palette: golden butter, egg white, blue stripes, black steel, fine film grain. "
+ LOOK,
# 2 riding the dog to work
"A woman in her late 20s who went to bed normal size woke up only the size of a thumb in her own home, and she still has to go to work. She is dressed for the office in a neat navy blazer, white blouse and trousers, a tiny leather handbag over her shoulder, riding on top of the head of the family's golden retriever like a rider on a horse, one hand gripping its fur, her hair blown back, laughing with excitement. "
"The golden retriever trots happily down the hallway toward the front door, tongue out, ears bouncing, every strand of its golden fur visible. "
"Ahead in the hallway, her own normal-size shoes stand by the door like two huge leather boats, and her keys hang on a hook high above like a mountain ledge. "
"Camera: low dynamic tracking shot at the dog's eye level, slightly in front of them, 35mm lens, the woman and the dog's head sharp in the center of the frame, the hallway and front door ahead, gentle motion blur on the floor and walls for speed. "
"Lighting: soft bright morning light through the frosted glass of the front door, warm rim light on her hair and the dog's fur, warm wooden floor reflections. Color palette: golden fur, navy blazer, warm wood, soft white light, fine film grain. "
+ LOOK,
# 3 video meeting on the keyboard
"A man in his 30s who went to bed six feet tall woke up only the size of a thumb, and he still has a work video call at nine. He wears a white dress shirt, a red tie and blue pajama shorts, and he is jumping high in the air above his own laptop keyboard, both arms flung up, tie flying, about to land with both feet on a single key to unmute himself, his face focused like an athlete. "
"The silver laptop keyboard spreads under him like a huge field of square tiles; above him the bright laptop screen shows a normal video meeting with four colleagues in small windows, waiting politely. "
"Around the laptop his ordinary home desk rises like a giant landscape: a coffee mug as tall as a building, a pen lying like a fallen log, a sticky note like a yellow wall. "
"Camera: low-angle full-body shot from the keyboard level, 35mm lens, deep focus, he is caught at the top of his jump in the lower center of the frame with the glowing screen and the colleagues behind and above him. "
"Lighting: cool blue-white light from the laptop screen on his face mixed with warm desk lamp light from the side, soft reflections on the silver keys. Color palette: white shirt, red tie, silver keyboard, screen blue, warm lamp amber, fine film grain. "
+ LOOK,
# 4 wristwatch as a belt
"A man in his 30s who went to bed normal size woke up only the size of a thumb in his own bathroom, and he is getting ready for work as usual. He stands on the white porcelain edge of the bathroom sink in his white undershirt, boxer shorts and socks, wearing his own normal steel wristwatch around his waist like a giant belt: he has stepped into the open metal band, and the big round watch face covers his belly like a shield, slightly too big and slipping, while he adjusts his hair and looks at himself in the mirror with a completely serious, satisfied expression. "
"The watch is real polished stainless steel with a white dial and black hands, reflecting the light. "
"Around him the ordinary bathroom rises like a giant landscape: a toothpaste tube as long as a bus, a razor like a crane, a single drop of water from the faucet the size of his head, his reflection in the huge mirror. "
"Camera: eye-level full-body shot on the sink counter, 35mm lens, deep focus, he stands in the right third of the frame facing the mirror, his reflection visible on the left. "
"Lighting: bright clean bathroom light from above, crisp highlights on the porcelain and the steel watch, soft shadows. Color palette: white porcelain, silver steel, mint blue toothpaste, skin tones, fine film grain. "
+ LOOK,
# 5 sock from the washing machine
"A woman in her 30s who went to bed normal size woke up only the size of a thumb in her own home, and Saturday is still laundry day. She wears grey leggings and an oversized lilac hoodie, standing on the rim of the round door opening of a front-loading washing machine, leaning far back with her whole body, heels dug in, pulling one long wet striped sock out of the drum like a fisherman hauling in a heavy net, her face scrunched with effort. "
"The wet sock is ten times longer than she is, heavy and dripping, its colorful stripes dark with water, water drops falling and splashing on the floor. "
"Around her the ordinary laundry room rises like a giant landscape: an open box of laundry detergent like a skyscraper, a clothespin lying like a fallen tree, the dark drum of the machine like a cave. "
"Camera: low-angle full-body shot from the machine door rim, 35mm lens, deep focus, she is in the left third of the frame pulling toward the camera, the long sock stretching back into the dark drum. "
"Lighting: soft daylight from a small window, glistening highlights on the wet sock and water drops, cool shadows inside the drum. Color palette: white machine, lilac hoodie, colorful striped sock, cool grey, fine film grain. "
+ LOOK,
]
m = sys.argv[1] if len(sys.argv) > 1 else 'text2image_soul_v2'
d = 'v2'
os.makedirs(d, exist_ok=True)
open(f'{d}/prompts.txt', 'w', encoding='utf-8', newline='\n').write('\n'.join(P) + '\n')
open(f'{d}/model.txt', 'w').write(m + '\n')
open(f'{d}/aspect.txt', 'w').write('3:2\n')
print(m, [len(p.split()) for p in P])
