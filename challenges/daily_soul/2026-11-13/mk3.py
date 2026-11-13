import os, sys
SIZE = ("SCALE IS THE MOST IMPORTANT THING: the person is only five centimeters tall, the size of an adult's thumb. "
        "Every everyday object next to them is shown at its real normal size and towers over them. ")
TAIL = ("Look: real film still from a big-budget adventure comedy, shot on 65mm film, the tiny person is a real living human photographed like a real actor with real skin and fabric texture, inside a real full-size ordinary home. "
        "Any visible text must be real words exactly as printed in a dictionary or a published newspaper.")
P = [
# 1 instant coffee into the mug
SIZE + "Morning in a real kitchen. A man in his 30s, five centimeters tall, wearing striped pajamas, has leaned a tiny wooden ladder against the side of a normal white ceramic coffee mug full of hot water; the ladder only reaches the rim, and the mug is three times taller than he is. Standing at the top of the ladder, he holds a normal-size instant coffee stick packet in both arms like a heavy log, the paper packet longer than his whole body, and tips it over the rim, a stream of brown coffee powder pouring into the steaming water. Steam curls around him. Beside the mug, a normal teaspoon lies on the counter, longer than he is tall, and a single sugar cube sits next to him like a large white box. "
"Camera: close macro shot at the height of the mug rim, 100mm macro lens, shallow depth of field, the man and the mug filling the frame, the kitchen window softly blurred behind. "
"Lighting: warm golden morning light from the window, glowing steam, rim light on him and the falling coffee powder. Color palette: white mug, brown coffee, blue-white stripes, warm gold, fine film grain. " + TAIL,
# 2 stomping on the phone keyboard
SIZE + "A woman in her late 20s, five centimeters tall, in a hoodie and socks, is standing on top of her own smartphone lying on the bed, trying to send a text message by stomping on the on-screen keyboard: each glowing key is as big as her foot, and she is mid-jump, one foot slamming down on a letter key, arms out for balance, her face concentrated. The phone is far bigger than she is, the glowing screen lighting her from below; a typed message bubble is visible above the keyboard. Next to the phone, the pillow rises like a hill and the charger cable lies like a thick rope. "
"Camera: close macro shot from just above the phone screen, slightly in front of her, 100mm macro lens, shallow depth of field, she and the keyboard fill the frame. "
"Lighting: cool blue-white light from the phone screen on her face, warm bedside lamp glow in the soft background. Color palette: screen blue-white, grey hoodie, warm amber, soft white bedding, fine film grain. " + TAIL,
# 3 riding a hamster to work
SIZE + "A man in his 30s, five centimeters tall, dressed for the office in a tiny navy suit and tie with a little briefcase, is riding his pet golden hamster across the living room floor toward the front door, like a cowboy on a horse, sitting on the hamster's back and holding a thin ribbon as reins, his tie flying. The hamster is real, round and fluffy, a little bigger than him, running eagerly with its cheeks full. Ahead of them, the door threshold is like a wall, and a normal shoe stands next to them like a huge leather building. "
"Camera: low macro tracking shot at floor level just in front of them, 100mm macro lens, shallow depth of field, the man and the hamster sharp in the center, the hallway and front door softly blurred far behind. "
"Lighting: soft morning sunlight across the wooden floor, warm rim light on the hamster's fur and the man's hair, long soft shadows. Color palette: golden hamster fur, navy suit, warm wood, soft white light, fine film grain. " + TAIL,
# 4 wristwatch as a belt (fixed scale)
SIZE + "In a real bathroom, a man in his 30s, five centimeters tall, in a white undershirt and boxer shorts, stands on the white sink counter getting ready for work: he has stepped into his own normal steel wristwatch and pulled it up around his body, and the round watch face is as big as his whole torso, covering him from chest to knees like a giant shield. He holds it up with both hands and looks at himself in the mirror with a dead-serious, satisfied expression. Next to him a normal toothbrush lying on the counter is three times longer than he is tall. "
"Camera: close macro shot at counter level, 100mm macro lens, shallow depth of field, he fills the right half of the frame, his tiny reflection in the mirror on the left. "
"Lighting: bright clean bathroom light, crisp highlights on the polished steel watch and porcelain. Color palette: white porcelain, silver steel, white undershirt, soft mint, fine film grain. " + TAIL,
# 5 cracking an egg (fixed scale)
SIZE + "In a real kitchen at breakfast time, a man in his 30s, five centimeters tall, in striped pajamas and bare feet, stands on the rim of a black frying pan pushing with his whole body against a normal-size chicken egg that is twice his height, trying to tip it over the edge so it cracks into the pan; a thin crack already runs across the white shell and a drop of egg white is leaking out. Melted butter sizzles in the pan below him. "
"Camera: close macro shot at the height of the pan rim, 100mm macro lens, shallow depth of field, the man and the giant egg filling the frame, the kitchen softly blurred behind. "
"Lighting: warm golden morning sunlight from the side, steam rising from the pan, glossy butter reflections. Color palette: white egg, golden butter, blue-white stripes, black pan, fine film grain. " + TAIL,
]
m = sys.argv[1] if len(sys.argv) > 1 else 'text2image_soul_v2'
d = 'v3'
os.makedirs(d, exist_ok=True)
open(f'{d}/prompts.txt', 'w', encoding='utf-8', newline='\n').write('\n'.join(P) + '\n')
open(f'{d}/model.txt', 'w').write(m + '\n')
open(f'{d}/aspect.txt', 'w').write('3:2\n')
print(m, [len(p.split()) for p in P])
