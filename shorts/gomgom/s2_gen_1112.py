# -*- coding: utf-8 -*-
"""시즌2 11·12화 generate.sh 작성기 — 8화 generate.sh 공통 머리(캐릭터·s2c 기준·크기 규칙)·꼬리(img/vid)를 재사용"""
import pathlib

H = pathlib.Path(__file__).parent
src = (H / "ep08" / "prod" / "generate.sh").read_text(encoding="utf-8")
head = src.split("declare -A IMG MOV CH DUR")[0]
tail = src.split("mkdir -p img clips", 1)[1]
old_keys = tail.split('KEYS="', 1)[1].split('"', 1)[0]

BACK = (", seen from behind so the star badge on Gomgom's chest is hidden and NOT visible, Gomgom's back is plain cream "
        "fuzzy wool with only the thin brown satchel strap crossing it")
G = "$GOM; $KONG"
GO = "$GOM; Kong is not in this scene"
GOW = "$GOM; $OWL; Kong is not in this scene"
NOMOVE = ", no object moves by itself, everything that moves is moved by a character's paw or wing"
TWO = "a felt squirrel and a felt hedgehog, each about as tall as Gomgom"
BEHIND_MOV = (", seen from behind the whole time, its head does not turn, the camera stays directly behind and only rises slowly straight up, "
              "it never circles around, no face is visible on the back of the head, Kong stays tiny")
UMB = "a brand-new bright yellow umbrella with a curved wooden handle"

EP11 = [
    ("01", f"close eye level shot of Gomgom standing in a cozy felt entryway holding {UMB}, closed, with both paws and gazing at it with its mouth softly open in delight and no teeth, tiny Kong sitting at the very top center of Gomgom's head between its two round ears, a wooden shoe rack with little boots, coat hooks, a round window with rain outside, a doormat",
     "Gomgom gently turns the closed umbrella in its paws to admire it and tilts its head, tiny Kong on its head tilts its head too, the camera slowly rises from low in front of Gomgom, Kong stays tiny", G, 4),
    ("02", "spectacular view through a big arched window speckled with raindrops, Gomgom inside hugging a closed bright yellow umbrella and pressing its nose to the glass, outside a rainy miniature felt village with glowing lanterns, puddles, cobblestone streets, flower boxes and tiny rooftops, warm light inside, cool blue rain outside",
     "Gomgom presses its nose to the window and bounces happily on its feet while hugging the umbrella, the rain keeps falling outside the window, the camera moves slowly from outside the glass toward Gomgom", GO, 4),
    ("03", f"medium shot of a rainy felt village alley, Gomgom standing proudly under an open bright yellow umbrella, {TWO} standing under a shop awning watching and smiling, cobblestones, puddles, flower pots, lanterns",
     "Gomgom twirls the open umbrella once by its handle with a proud smile, the squirrel and the hedgehog clap their paws, raindrops spin off the umbrella edge, the camera arcs slowly from beside the friends toward Gomgom, everyone's feet stay on the ground", "$GOM; " + TWO + "; Kong is not in this scene", 4),
    ("04", "medium side shot of a felt entryway corner, a closed bright yellow umbrella leaning quietly against the wall beside a shoe rack, Gomgom walking past it in the background eating a cookie and not looking at the umbrella, warm lamp light, coat hooks",
     "Gomgom walks past munching its cookie without looking at the umbrella, the umbrella stays leaning completely still in the corner, the camera slides sideways at umbrella height following Gomgom" + NOMOVE, GO, 4),
    ("05", "medium shot of a cozy felt living room, a felt raccoon friend about as tall as Gomgom sitting on a plump sofa hugging a small sparkling pouch of gold coins with no letters or numbers anywhere, knitted cushions, a lamp, a window, a rug",
     "the raccoon hugs the pouch of coins happily, then slowly sets it down on the sofa beside it and lets out a small yawn with its mouth softly open and no teeth, the camera slowly arcs around the sofa", "a felt raccoon friend about as tall as Gomgom; Gomgom and Kong are not in this scene", 4),
    ("06", "medium shot of a cozy study full of bookshelves, Grandpa Owl slightly taller than Gomgom sitting in a little armchair talking kindly, Gomgom sitting across from it on a small stool listening, a small round table between them with two teacups, a warm reading lamp, a globe",
     "Grandpa Owl lifts one wing slightly as it explains, Gomgom nods slowly with a closed-mouth smile, the camera glides slowly between the two of them, Grandpa Owl stays only slightly taller than Gomgom", GOW, 4),
    ("07", f"low angle shot in the felt entryway, Gomgom picking up {UMB} again from the corner and smiling, tiny Kong standing on both little feet on the flat top of the wooden shoe rack right beside a pair of small rain boots, Kong only half as tall as one rain boot and one third the width of Gomgom's head, coat hooks, round window with rain",
     "Gomgom opens the umbrella with a happy closed-mouth smile, tiny Kong on the shoe rack tilts its head and watches, Kong never jumps or flies, the camera looks up from low and rises a little", G, 4),
    ("08", "spectacular wide shot from behind of Gomgom walking slowly down a rainy flower-lined lane under an open bright yellow umbrella, tiny Kong sitting at the very top center of Gomgom's head under the umbrella, felt cottages with glowing windows, hydrangea bushes, lanterns, puddles reflecting the yellow umbrella, gentle rain" + BACK,
     "Gomgom walks slowly forward down the lane with its feet on the ground, raindrops bounce off the umbrella" + BEHIND_MOV.replace("only rises slowly straight up", "follows at the same distance and rises a little"), G, 4),
    ("09", "close side shot under the yellow umbrella, Gomgom with its eyes softly closed listening to the rain with a peaceful closed-mouth smile, tiny Kong sitting at the very top center of Gomgom's head also looking out, raindrops dripping from the umbrella edge, soft rainy light, blurred flowers behind",
     "Gomgom keeps its eyes closed and its gentle closed-mouth smile the whole time, exactly one small mouth that never opens, raindrops drip from the umbrella edge, tiny Kong sways a little, the camera slowly arcs beside Gomgom's face, Kong stays tiny", G, 4),
    ("10", "low angle shot by a puddle on a cobblestone path as the rain stops, sunlight breaking through the clouds lighting up the bright yellow umbrella, Gomgom tilting the umbrella back to look up at the sky, tiny Kong standing on both little feet on a flat round stepping stone beside the puddle, Kong only as tall as a small daisy growing beside the stone and one third the width of Gomgom's head, sparkling raindrops on flowers",
     "sunlight spreads across the path, Gomgom gently twirls the umbrella and smiles with its mouth closed, tiny Kong flutters its small wings a little while staying standing on the stone, Kong never jumps or flies, the camera rises slowly from puddle level, Kong stays tiny", G, 4),
    ("11", "wide shot from behind of Gomgom standing in an open felt cottage doorway in the evening after the rain, the bright yellow umbrella resting in an umbrella stand beside the door, tiny Kong sitting at the very top center of Gomgom's head, a soft rainbow over the wet village and pink sky beyond, a welcome mat, potted flowers" + BACK,
     "Gomgom stands still gazing at the rainbow" + BEHIND_MOV, G, 8),
]

EP12 = [
    ("01", "medium three-quarter front shot of Gomgom standing on a grassy hilltop at sunset wearing a small damp backpack, gazing at a glowing orange and pink sunset over rolling felt hills with a gentle smile and no teeth, tiny Kong sitting at the very top center of Gomgom's head between its two round ears, wildflowers, a winding path below",
     "Gomgom takes a slow deep breath and its shoulders relax, tiny Kong on its head looks at the sunset too, the sunset glows, the camera slides slowly sideways in front of Gomgom, Kong stays tiny", G, 4),
    ("02", "spectacular wide shot of a sunny morning meadow with a winding flower path, a felt windmill, rolling hills and fluffy clouds, Gomgom walking along the path carrying a wicker picnic basket, tiny Kong standing on both little feet on the flat wicker lid of the basket, Kong only one third the width of Gomgom's head, butterflies, daisies",
     "Gomgom walks happily along the flower path with its feet on the ground swinging the basket gently, tiny Kong stays standing on the basket lid and looks around, Kong never jumps or flies, the camera tracks alongside at the same distance, Kong stays tiny", G, 4),
    ("03", "high angle shot of Gomgom in the middle of an open meadow under sudden dark rain clouds, heavy rain pouring down, Gomgom holding the wicker picnic basket over its head to block the rain, tiny Kong peeking out of the small front pocket of Gomgom's brown satchel, the flower path turning into puddles, a misty forest edge",
     "Gomgom lifts the basket above its head in surprise, the rain pours down hard, tiny Kong ducks into the satchel pocket, the camera slowly descends from above toward Gomgom, Kong stays tiny", G, 4),
    ("04", f"medium shot of a cozy felt cabin like a little laboratory, Grandpa Owl slightly taller than Gomgom standing beside two round wooden basins of water on a table, a felt squirrel about as tall as Gomgom dipping one paw into the left basin and flinching from the cold, a small wooden sand hourglass on the table, shelves of jars, a window",
     "the squirrel dips its paw into the water and hunches its shoulders shivering, Grandpa Owl watches the sand hourglass closely, the camera glides sideways at basin height", "$OWL; a felt squirrel about as tall as Gomgom; Gomgom and Kong are not in this scene", 4),
    ("05", "medium shot in the same cozy felt cabin, a felt squirrel about as tall as Gomgom pointing with one paw at the right one of two round wooden basins of water and nodding, Grandpa Owl slightly taller than Gomgom smiling beside it, a small sand hourglass on the table, shelves of jars",
     "the squirrel points at the right basin and nods firmly, Grandpa Owl nods back with a smile, the camera arcs slowly around the table from the other side", "$OWL; a felt squirrel about as tall as Gomgom; Gomgom and Kong are not in this scene", 4),
    ("06", "medium shot by a warm crackling fireplace, Grandpa Owl slightly taller than Gomgom and Gomgom sitting side by side in two little armchairs talking, two teacups on a small table, a knitted rug, a bookshelf, warm firelight",
     "Grandpa Owl lifts one wing slightly as it explains, Gomgom listens and nods slowly with a closed-mouth smile, the firelight flickers, the camera moves slowly in from the fireplace side, Grandpa Owl stays only slightly taller than Gomgom", GOW, 4),
    ("07", "medium side shot of Gomgom sitting by a cabin window in the evening, warm sunset light glowing on its face, a thoughtful gentle smile with its mouth closed, the damp picnic basket on the floor beside it, potted plants on the sill",
     "Gomgom looks out the window and slowly nods to itself with a soft closed-mouth smile, the sunset light shifts, the camera slides slowly along the window toward Gomgom's face", GO, 4),
    ("08", "spectacular low angle wide shot of a rain-washed meadow with a huge bright rainbow arching across the clearing sky, sunbeams through parting clouds, sparkling wet grass and wildflowers, Gomgom standing with the picnic basket set down beside it, looking up at the rainbow, tiny Kong sitting at the very top center of Gomgom's head",
     "Gomgom slowly opens its arms wide toward the rainbow with a closed-mouth smile, exactly one small mouth, the clouds drift apart, tiny Kong looks up too, the camera rises slowly from low, Kong stays tiny", G, 4),
    ("09", "medium shot on a checkered picnic blanket under the rainbow, Gomgom holding a warm mug of cocoa with both paws, tiny Kong standing on both little feet on the blanket right beside a small cup, Kong only half as tall as the small cup and one third the width of Gomgom's head, cookies on a plate, the wicker basket, wet flowers glistening",
     "Gomgom blows gently on the cocoa and takes a small sip, tiny Kong beside the small cup nods happily, Kong never jumps or flies, steam rises from the mug, the camera circles slowly at blanket height, Kong stays tiny", G, 4),
    ("10", "wide shot from behind of Gomgom walking home along a sunset path carrying the wicker basket, tiny Kong sitting at the very top center of Gomgom's head, the sky glowing red and gold, felt cottages with lit windows in the distance, fireflies, wildflowers along the path" + BACK,
     "Gomgom walks slowly away along the path with its feet on the ground, the sky glows warmer" + BEHIND_MOV.replace("only rises slowly straight up", "follows slowly and rises a little"), G, 4),
    ("11", "wide shot from behind of Gomgom standing at a cabin window at night, a warm mug of cocoa on the windowsill and a small crayon drawing of a rainbow with no letters propped beside it, tiny Kong standing on both little feet on the flat windowsill right beside the mug, Kong only half as tall as the mug, stars and a crescent moon over the felt village outside, gingham curtains" + BACK,
     "Gomgom stands still gazing at the stars, tiny Kong on the windowsill looks out too" + BEHIND_MOV, G, 8),
]


def esc(s):
    return s.replace('"', '\\"')


for ep, items in (("ep11", EP11), ("ep12", EP12)):
    (H / ep / "prod").mkdir(parents=True, exist_ok=True)
    b = "declare -A IMG MOV CH DUR\n"
    for k, img, mov, ch, dur in items:
        b += f'IMG[{k}]="{esc(img)}"\nMOV[{k}]="{esc(mov)}"\nCH[{k}]="{ch}"; DUR[{k}]={dur}\n'
    keys = " ".join(k for k, *_ in items)
    t = tail.replace(f'KEYS="{old_keys}"', f'KEYS="{keys}"')
    (H / ep / "prod" / "generate.sh").write_text(head + b + "\nmkdir -p img clips" + t, encoding="utf-8")
    print(ep, len(items))
