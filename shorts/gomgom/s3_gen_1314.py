# -*- coding: utf-8 -*-
"""시즌3 13·14화 generate.sh 작성기 — 12화 generate.sh 공통 머리(캐릭터·s2c 기준·크기 규칙)·꼬리(img/vid) 재사용
11/17 사용자: 콩이 동작 제한(날기·날개 펴기)·캐릭터 복제 제한 해제 → 화면 보고 다시 규칙 추가. 콩이 크기(머리 폭 1/3)는 유지."""
import pathlib

H = pathlib.Path(__file__).parent
src = (H / "ep12" / "prod" / "generate.sh").read_text(encoding="utf-8")
head = src.split("declare -A IMG MOV CH DUR")[0]
tail = src.split("mkdir -p img clips", 1)[1]
old_keys = tail.split('KEYS="', 1)[1].split('"', 1)[0]

BACK = (", seen from behind so the star badge on Gomgom's chest is hidden and NOT visible, Gomgom's back is plain cream "
        "fuzzy wool with only the thin brown satchel strap crossing it")
G = "$GOM; $KONG"
GO = "$GOM; Kong is not in this scene"
NOMOVE = ", no object moves by itself, everything that moves is moved by a character's paw or wing"
TURTLE = ("Grandpa Turtle, a kind old felt turtle with olive green felt skin on its face, arms and legs (not cream, not a bear), a dark green felt shell on its back, a long soft white beard and a small woven straw conical hat, "
          "standing upright, Grandpa Turtle is slightly taller than Gomgom, about a quarter head taller, never shorter than Gomgom and never twice as big")
BUFFALO = ("Grandpa Buffalo, a kind old felt water buffalo with soft grey wool, long white droopy eyebrows, small curved horns and a tiny cloth bundle "
           "tied on its back, Grandpa Buffalo is slightly taller than Gomgom, about a quarter head taller, never shorter than Gomgom and never twice as big")
RACCOON = "a felt raccoon friend about as tall as Gomgom"
TREE = ("a huge ancient gnarled oak tree with a thick twisted crooked trunk and wide spreading crooked branches, covered in soft felt leaves, "
        "clearly bent and knotted so it could never be cut into straight lumber")
BOAT = "a small bright yellow folded paper boat"

EP13 = [
    ("01", "medium shot from a low angle of Gomgom sitting alone in the corner of a cozy felt workshop with empty paws, looking down at the floor, head drooping and shoulders slumped, a sad gloomy expression with droopy eyes and a small downturned closed mouth, not smiling at all, tiny Kong sitting at the very top center of Gomgom's head between its two round ears, wooden shelves with tools, spools of yarn, wood shavings on the floor, warm window light",
     "Gomgom lets out a small sigh and its shoulders sink a little more, tiny Kong on its head peeks down at Gomgom's face, the camera slowly moves in from low in front, Kong stays tiny", G, 4),
    ("02", "high angle shot looking down at a wooden worktable covered with messy unfinished felt crafts, half-sewn pieces, tangled yarn and scattered buttons, Gomgom resting its chin on one paw staring blankly at them, tiny Kong standing on both little feet on the flat tabletop right beside a spool of thread, Kong only as tall as the spool and one third the width of Gomgom's head",
     "Gomgom picks up an unfinished piece, looks at it, and sets it down again with a small sigh, tiny Kong looks at the pile, the camera moves slowly sideways above the table, Kong stays tiny", G, 4),
    ("03", "spectacular wide view through a round workshop window onto a busy miniature felt village on a sunny day, a felt squirrel pushing a little cart full of acorns, a felt hedgehog fixing a cottage roof on a short ladder, a felt rabbit hanging laundry, flower boxes, cobblestone lanes, tiny rooftops, the window frame and a bit of Gomgom's shoulder in the near foreground",
     "the friends keep busy, the squirrel pushes its cart along, the hedgehog taps the roof with a little hammer, the laundry sways in the breeze, the camera pushes slowly out through the window toward the village", "a felt squirrel, a felt hedgehog and a felt rabbit, each about as tall as Gomgom; $GOM seen only as a small part of its shoulder; Kong is not in this scene", 4),
    ("04", f"spectacular extreme low angle shot looking up from the forest floor at {TREE} towering over a mossy forest clearing, Gomgom standing small at the base of the trunk looking up at it, tiny Kong sitting at the very top center of Gomgom's head, sunbeams through the leaves, ferns, mushrooms, fallen leaves",
     "Gomgom slowly tilts its head back to look up at the huge crooked tree, leaves sway gently in the breeze, the camera starts at the roots and rises up along the twisted trunk toward the wide branches, Kong stays tiny", G, 4),
    ("05", f"storybook-like warm scene in the same forest clearing, three felt beaver carpenters (real beavers, not bears: dark brown felt beavers with a wide flat scaly paddle-shaped tail clearly visible, small round ears, a blunt rounded snout and two small orange front teeth) wearing little work aprons and carrying small wooden tool boxes and saws on their shoulders walking past {TREE}, the beavers glancing at the crooked trunk and shaking their heads, soft golden light, ferns, a forest path",
     "the three beavers glance at the crooked tree, shake their heads and wave a paw dismissively, then keep walking along the path with their feet on the ground, the camera tracks alongside them at their height", "three felt beaver carpenters each about as tall as Gomgom; Gomgom and Kong are not in this scene", 4),
    ("06", f"wide shot of {TREE} alone in a felt meadow, shown in four seasons at once as a seamless panorama from left to right: pink spring blossoms, bright green summer leaves, red and gold autumn leaves, and white winter snow, the tree itself stays exactly the same crooked shape, rolling felt hills behind",
     "time passes gently, falling blossoms, fluttering leaves and soft snowflakes drift down through the air, the tree stays exactly the same, the camera slowly circles around the tree", "no characters in this scene; Gomgom and Kong are not in this scene", 4),
    ("07", f"medium shot under the shade of {TREE}, {TURTLE} standing beside Gomgom and talking kindly, Gomgom listening with a gentle closed-mouth smile, tiny Kong sitting at the very top center of Gomgom's head, dappled sunlight, moss, roots, a small stone bench",
     "Grandpa Turtle raises one hand and points up at the crooked tree as it explains, Gomgom nods slowly, the camera glides slowly between the two of them, Grandpa Turtle stays only slightly taller than Gomgom, Kong stays tiny", f"$GOM; {TURTLE}; $KONG", 4),
    ("08", f"spectacular high angle wide shot of the cool shade under {TREE} on a bright sunny day, many felt animal friends resting in the shade, a squirrel napping on a root, a hedgehog and a rabbit sharing a picnic on a checkered blanket, a little fox reading a book, sunbeams flickering through the leaves, wildflowers",
     "a breeze stirs the leaves and the dappled sunlight dances, the friends stretch lazily and smile, the camera descends slowly from high in the branches down into the shade", "a felt squirrel, a felt hedgehog, a felt rabbit and a small felt fox, each about as tall as Gomgom; Gomgom and Kong are not in this scene", 4),
    ("09", f"close shot of {TURTLE} gently resting one hand on the thick twisted trunk of {TREE} and smiling up at it, rough bark texture, moss, small mushrooms, sunlight on the leaves",
     "Grandpa Turtle pats the trunk softly and looks up with a warm smile, the camera rises slowly along the trunk toward the branches", f"{TURTLE}; Gomgom and Kong are not in this scene", 4),
    ("10", f"medium shot of Gomgom sitting in the shade under {TREE} with a peaceful closed-mouth smile, tiny Kong sitting on Gomgom's lap, Kong one third the width of Gomgom's head, a felt squirrel and a felt hedgehog leaning comfortably against Gomgom on each side, dappled sunlight, roots, wildflowers",
     "Gomgom looks around at its resting friends with a warm smile, tiny Kong tilts its head, the friends snuggle closer, the camera moves slowly in from the front, Kong stays tiny", "$GOM; $KONG; a felt squirrel and a felt hedgehog, each about as tall as Gomgom", 4),
    ("11", f"wide shot from behind of Gomgom sitting at the foot of {TREE} at sunset, tiny Kong sitting at the very top center of Gomgom's head, a golden orange sky, long soft shadows, rolling felt hills, the huge crooked tree silhouetted against the glowing sky" + BACK,
     "Gomgom sits still gazing at the sunset, the sunset light deepens, the camera stays directly behind and slowly pulls back and rises to show the whole crooked tree, no face is visible on the back of the head, Kong stays tiny", G, 8),
]

EP14 = [
    ("01", "medium shot from behind of Gomgom stomping out of a felt cottage door with its fists balled and cheeks flushed pink, tiny Kong sitting at the very top center of Gomgom's head, a garden path, flower pots, a picket fence" + BACK,
     "Gomgom stomps a few steps away from the door with its feet on the ground, the door stays as it is, the camera follows from behind, no face is visible on the back of the head, Kong stays tiny", G, 4),
    ("02", f"medium shot through a cottage window of {RACCOON} inside with its arms crossed and turned away with a pouty face, gingham curtains, a teapot on the table, potted plants on the sill",
     f"the raccoon turns its head away with a huff and keeps its arms crossed, the camera moves slowly from outside the window toward the glass", f"{RACCOON}; Gomgom and Kong are not in this scene", 4),
    ("03", "low angle shot at water level of Gomgom sitting on a mossy rock by a clear forest stream, tossing a small pebble into the water with a pouty closed-mouth face, tiny Kong sitting at the very top center of Gomgom's head, ripples spreading, ferns, smooth river stones, dappled sunlight",
     "Gomgom tosses a small pebble with its paw, it plops into the water and ripples spread, Gomgom pouts, the camera stays low near the water surface and slides slowly toward Gomgom, Kong stays tiny", G, 4),
    ("04", "spectacular close shot at water level of a clear stream flowing around a large smooth round rock, the water gently parting and curling around both sides of the rock, sparkling sunlight on the ripples, pebbles visible under the clear water, felt moss on the rock",
     "the water flows smoothly around the rock and joins again behind it, sparkles dance on the surface, the camera glides low over the water toward the rock and past it", "no characters in this scene; Gomgom and Kong are not in this scene", 4),
    ("05", "spectacular bird's-eye view looking straight down at a winding sparkling forest stream curving around many smooth rocks, green moss, ferns and wildflowers along both banks, sunlight glittering on the water",
     "the water keeps flowing and sparkling around the rocks, the camera moves slowly downstream following the water from high above", "no characters in this scene; Gomgom and Kong are not in this scene", 4),
    ("06", f"medium shot across a forest stream, {BUFFALO} sitting peacefully on a flat rock on the far bank, Gomgom on the near bank looking up at it, tiny Kong sitting at the very top center of Gomgom's head, ferns, river stones, dappled sunlight",
     "Grandpa Buffalo gestures gently with one hoof toward the flowing water as it speaks, Gomgom lifts its head and listens, the camera glides slowly over the stream between them, Grandpa Buffalo stays only slightly taller than Gomgom, Kong stays tiny", f"$GOM; {BUFFALO}; $KONG", 4),
    ("07", "spectacular wide shot along a forest stream, little felt birds drinking at the water's edge, wildflowers and lush green grass growing thick wherever the water touches, a small felt deer drinking, butterflies, sunlight",
     "the birds dip their beaks to drink, the flowers sway, butterflies flutter, the camera moves slowly sideways along the stream", "small felt birds and a small felt deer; Gomgom and Kong are not in this scene", 4),
    ("08", f"close shot of Gomgom's paws gently placing {BOAT} onto the surface of the clear stream, Gomgom's soft closed-mouth smile visible above, river stones and moss",
     "Gomgom slowly lets go of the paper boat and it begins to float, the camera stays close to Gomgom's paws at water level", GO, 4),
    ("09", f"medium shot at water level of {BOAT} floating down the stream with tiny Kong standing at the front of the boat with its little wings spread, Kong one third the width of Gomgom's head, Gomgom walking along the bank beside it, ferns, rocks, sparkling water",
     "the paper boat floats along and turns gently around a rock, tiny Kong flaps its little wings happily at the bow, Gomgom walks beside it on the bank with its feet on the ground, the camera tracks alongside the boat at water level, Kong stays tiny", G, 4),
    ("10", f"low angle shot from under a small wooden footbridge over the stream, {RACCOON} on the bridge leaning down and holding {BOAT} it just scooped out of the water, smiling at Gomgom, Gomgom on the bank waving shyly, tiny Kong sitting at the very top center of Gomgom's head, flowers, sunlight",
     "the raccoon holds up the paper boat and smiles, Gomgom waves shyly with a closed-mouth smile, the camera looks up from under the bridge and rises slowly", f"$GOM; $KONG; {RACCOON}", 4),
    ("11", f"wide shot from behind of Gomgom and {RACCOON} sitting side by side on the stream bank at sunset, tiny Kong sitting at the very top center of Gomgom's head, {BOAT} floating away downstream, the water glowing gold and pink, ferns and reeds silhouetted" + BACK,
     "they sit still side by side watching the boat drift away, the sunset light glitters on the water, the camera stays directly behind and slowly pulls back, no faces are visible on the backs of their heads, Kong stays tiny", f"$GOM; $KONG; {RACCOON}", 8),
]


def esc(s):
    return s.replace('"', '\\"')


for ep, items in (("ep13", EP13), ("ep14", EP14)):
    (H / ep / "prod").mkdir(parents=True, exist_ok=True)
    b = "declare -A IMG MOV CH DUR\n"
    for k, img, mov, ch, dur in items:
        b += f'IMG[{k}]="{esc(img)}"\nMOV[{k}]="{esc(mov)}"\nCH[{k}]="{ch}"; DUR[{k}]={dur}\n'
    keys = " ".join(k for k, *_ in items)
    t = tail.replace(f'KEYS="{old_keys}"', f'KEYS="{keys}"')
    (H / ep / "prod" / "generate.sh").write_text(head + b + "\nmkdir -p img clips" + t, encoding="utf-8")
    print(ep, len(items))
