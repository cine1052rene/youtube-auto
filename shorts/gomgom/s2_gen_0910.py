# -*- coding: utf-8 -*-
"""시즌2 9·10화 generate.sh 작성기 — 8화 generate.sh의 공통 머리(캐릭터·s2c 기준·크기 규칙)·꼬리(재시도·img/vid)를 그대로 재사용"""
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

EP9 = [
    ("01", "close high angle shot of Gomgom lying in a cozy little felt bed at night, wide awake with its round bead eyes open looking at the ceiling, a patchwork quilt pulled up to its chin, on the bedside table a small wicker basket holding a half-knitted cream scarf with two knitting needles stuck in it, a crescent moon through a round window, a tiny night lamp, a felt alarm clock with no numbers, framed felt pictures",
     "Gomgom turns from one side to the other under the quilt and then opens its eyes again and stares at the ceiling, the moonlight shimmers through the window, the camera slowly arcs around the side of the bed", GO, 4),
    ("02", "medium shot of a cozy living room in the evening, Gomgom in a small wooden rocking chair yawning with its mouth softly open and no teeth, holding knitting needles with a half-finished cream scarf on its lap, tiny Kong standing on both little feet on the flat side table right beside a ball of yarn, Kong is only half as tall as the ball of yarn and one third the width of Gomgom's head, a fireplace with a warm glow, a knitted rug, a bookshelf, a potted plant",
     "Gomgom yawns, slowly puts the needles into the basket and stands up from the rocking chair, tiny Kong stays standing on the side table and tilts its head, Kong never jumps or flies, the fire flickers, the camera glides sideways past the side table", G, 4),
    ("03", "dramatic straight top-down bird's-eye view from the bedroom ceiling looking down at Gomgom lying awake in the middle of a round felt bed, the patchwork quilt spread out like a colorful map, long soft cream and pastel yarn strands curling across the whole bedroom floor in big dreamy spirals around the bed like a frozen whirlpool, balls of yarn, slippers, a rug, the bedside table with the knitting basket and night lamp seen from above, moonlight shapes from the window falling across the floor",
     "Gomgom blinks up at the ceiling and turns its head from side to side on the pillow, the yarn spirals on the floor stay completely still, the camera slowly rotates a little while staying directly above the bed and rises higher" + NOMOVE, GO, 4),
    ("04", "grand high-angle wide shot from an upper corner of a bustling two-floor felt village diner with deep perspective, a wooden balcony level with more tables, a warm chandelier and strings of tiny lights across the ceiling, many checkered tables full of $FRIENDS eating pancakes, Grandpa Owl wearing a small striped apron as the waiter, slightly taller than Gomgom, carrying a tray of plates with no notepad between the tables, Gomgom small at a window table in the corner watching curiously, a big round window with the felt village outside, plants, a cake counter",
     "Grandpa Owl walks carefully between the busy tables carrying the tray and sets plates down in front of customers with a proud nod, the customers chat and eat, Gomgom watches from its window table, the camera glides down from the high corner over the balcony railing toward the floor, everyone's feet stay on the floor", "$GOM; $OWL; Kong is not in this scene", 4),
    ("05", "low angle shot at the diner counter, Grandpa Owl slightly taller than Gomgom standing behind a little wooden cash register with no numbers, having just taken a coin, scratching its head with one wing with a puzzled smile, Gomgom standing at the counter laughing softly with its mouth closed, jars of cookies and a cake stand on the counter",
     "Grandpa Owl drops the coin into the register drawer, then scratches its head as if it forgot something, Gomgom keeps one gentle closed-mouth smile with exactly one small mouth, the mouth shape never changes and never opens, Gomgom's shoulders bob softly as if chuckling, the camera circles slowly at counter height", GOW, 4),
    ("06", "close shot of Gomgom's paws holding the half-knitted cream scarf tightly against its chest, the knitting needles still in it, warm lamp light in the cozy bedroom, Gomgom's face above looking down at the scarf with a slightly worried look",
     "Gomgom hugs the scarf tighter and then slowly loosens its grip with a small sigh, the camera rises from the paws holding the scarf up to Gomgom's face", GO, 4),
    ("07", "medium shot at a small bedside desk under a warm lamp, Gomgom holding a pencil and drawing on a small paper note a simple picture of a scarf and five small circles, no letters or numbers anywhere, tiny Kong standing on both little feet on the flat desk right beside an eraser, Kong is only as tall as the eraser and one third the width of Gomgom's head, a cup of warm milk, a little alarm clock with no numbers, a jar of pencils",
     "Gomgom finishes drawing and puts the pencil down, tiny Kong leans over to peek at the note and nods, Kong stays standing on the desk with its wings folded, the camera slides sideways along the desk", G, 4),
    ("08", "medium shot of Gomgom kneeling on the bedroom rug beside a wicker knitting basket that is much smaller than Gomgom and sits on the floor, Gomgom pinning a small paper note onto the half-knitted cream scarf draped over the basket edge, the note shows a simple drawing of a scarf and five small circles with no letters, balls of colorful yarn inside the basket, warm bedside lamp light, the bed behind",
     "Gomgom presses the pin into the scarf and gently pats the note flat with its paw, then nods to itself, the camera arcs slowly around the basket from the side without zooming in", GO, 4),
    ("09", "low angle shot on the wooden bedroom floor at night, tiny Kong pushing a round cream ball of yarn with both little wings toward the wicker basket, Kong is only half as tall as the ball of yarn, a loose trail of yarn behind, the basket a short distance ahead, the rug edge and slippers nearby, moonlight on the floor",
     "tiny Kong waddles forward pushing the ball of yarn with its wings until the ball rolls up against the basket and stops, Kong keeps both feet on the floor and never jumps or flies, the yarn only moves because Kong pushes it, the camera follows along at floor height" + NOMOVE, "$KONG; Gomgom is not in this scene", 4),
    ("10", "high angle shot of Gomgom fast asleep in the cozy felt bed with a peaceful smile and closed eyes, tiny Kong curled up asleep in the very center of the pillow beside Gomgom's head, Kong only one third the width of Gomgom's head, patchwork quilt, the wicker basket with the scarf and pinned note on the bedside table, stars through the round window",
     "Gomgom stays lying perfectly still fast asleep with eyes closed the whole time, its head stays on the pillow and its body never sits up or moves, only the quilt rises and falls very gently with slow breathing, tiny Kong stays curled up asleep on the pillow and does not move, the stars twinkle in the window, the camera drifts very slowly sideways at the same height", G, 4),
    ("11", "wide shot from behind of Gomgom sitting by a sunny morning window in a little armchair, knitting the cream scarf again on its lap, tiny Kong sitting at the very top center of Gomgom's head between its two round ears, the window shows a bright felt village and blue sky, potted flowers on the sill, the wicker basket beside the chair" + BACK,
     "seen from behind the whole time, Gomgom's paws move the knitting needles calmly, its head does not turn, tiny Kong sits still at the very top center of Gomgom's head looking out the window, sunlight glows, the camera stays directly behind Gomgom and only rises slowly straight up, it never circles around, no face is visible on the back of the head, Kong stays tiny", G, 8),
]

EP10 = [
    ("01", "close eye level shot of Gomgom standing in front of a tall wooden shelf packed with many rows of little glass honey jars of many different golden colors, each jar with a cloth lid tied with string and no labels or letters, Gomgom's mouth softly open in amazement with no teeth and eyes wide, warm shop lights",
     "Gomgom's eyes move up and down the rows of honey jars and its head tilts from side to side, the camera slides sideways along the long shelf toward Gomgom", GO, 4),
    ("02", "dramatic low worm's-eye angle from the honey shop floor looking up at a towering wall of honey jar shelves rising all the way to a high vaulted wooden ceiling with a round skylight, warm golden light glowing through hundreds of amber and gold jars with no labels, a rolling library ladder, hanging dried flowers and a felt bee mobile, Gomgom standing small at the bottom with its head tilted far back gazing up in awe, tiny Kong sitting at the very top center of Gomgom's head between its ears",
     "Gomgom stands still in the same spot in the center of the frame and slowly lifts its head to gaze up at the towering shelves in awe with its mouth closed, exactly one small mouth, tiny Kong on its head looks up too, light glints across the jars, the camera stays low near the floor at the same height and slowly arcs halfway around Gomgom, it never rises and never tilts up, Gomgom stays fully visible in the center of the frame from start to end, Kong stays tiny", G, 4),
    ("03", "medium three-quarter shot of Gomgom in the honey shop holding one small honey jar in each paw, looking back and forth between them with a thoughtful frown, shelves of honey jars behind, a wicker shopping basket on the floor, warm light",
     "Gomgom lifts the left jar, then the right jar, looks back and forth and tilts its head unable to decide, the camera circles slowly around Gomgom", GO, 4),
    ("04", "medium shot of an outdoor felt village market stall, Grandpa Owl slightly taller than Gomgom standing behind a tasting table setting out small tasting spoons in front of little jam jars with no labels, a striped awning and bunting overhead, a few small felt animal friends such as a squirrel and a hedgehog, each about as tall as Gomgom, walking up to the table, baskets of fruit",
     "Grandpa Owl places tiny tasting spoons one by one in front of the jam jars with its wing, the animal friends walk up to the table, the bunting flutters, the camera glides sideways at table height", "$OWL; Gomgom and Kong are not in this scene", 4),
    ("05", "spectacular high aerial view over a festive felt village market square, colorful striped awnings, strings of bunting flags and paper lanterns crisscrossing above, a fountain in the middle, and one very long tasting table crowded with twenty-four little jam jars in rainbow colors with no labels, many small felt animal friends such as squirrels, hedgehogs, foxes and sheep, each about as tall as Gomgom, crowding around it with empty shopping baskets, cobblestone paths and flower carts all around",
     "the animal friends taste from tiny spoons, look at each other, shrug and wander off without picking up any jar, their baskets stay empty, the bunting sways in the breeze, the camera glides slowly along above the long table from high in the air", "$FRIENDS; Gomgom and Kong are not in this scene", 4),
    ("06", "medium shot of a short tasting table with only six little jam jars, a felt squirrel and a felt hedgehog, each about as tall as Gomgom, each happily putting one jam jar into their shopping basket, Grandpa Owl slightly taller than them smiling behind the table, bunting and baskets of fruit",
     "the squirrel and the hedgehog each pick up one jam jar and put it into their basket with a happy nod, Grandpa Owl nods back, the camera arcs slowly around the short table", "$OWL; Gomgom and Kong are not in this scene", 4),
    ("07", "wide shot of Gomgom sitting on a little stool in front of the huge wall of honey jars in the honey shop, holding its head with both paws, looking small and overwhelmed, the shelves stretching high above, warm light",
     "Gomgom holds its head with both paws, then lowers them and lets out a small sigh with its mouth closed, the camera slowly pulls back to reveal how big the wall of jars is", GO, 4),
    ("08", "medium shot inside the honey shop, Gomgom and Grandpa Owl both standing side by side on the wooden shop floor, Grandpa Owl only slightly taller than Gomgom, about a quarter head taller, Grandpa Owl resting one wing gently on Gomgom's shoulder and pointing with the other wing toward one friendly honey jar on a low shelf beside them, Gomgom looking up at Grandpa Owl, warm lamp light, shelves of honey jars behind",
     "Grandpa Owl pats Gomgom's shoulder and nods kindly, Gomgom's face brightens into a soft closed-mouth smile, both keep their feet on the floor, the camera moves slowly around the two of them, Grandpa Owl stays only slightly taller than Gomgom", GOW, 4),
    ("09", "close side shot along a wooden shelf of little honey jars with cloth lids, tiny Kong standing on both little feet on the flat shelf between the jars, Kong only half as tall as one honey jar and one third the width of Gomgom's head, tapping one cloth lid with the tip of its small wing, soft shop light, Gomgom's blurred paw at the edge of the frame",
     "tiny Kong walks along the shelf between the jars and gently taps three cloth lids one after another with the tip of its folded wing, Kong never jumps, never flies and never spreads its wings wide, the jars stay still, the camera follows along the shelf at Kong's height" + NOMOVE, G, 4),
    ("10", "low angle shot of Gomgom hugging one small golden honey jar with both paws and smiling happily with its mouth closed, tiny Kong sitting at the very top center of Gomgom's head between its two round ears, the honey shop shelves softly blurred behind, warm light",
     "Gomgom hugs the honey jar and sways happily from side to side, tiny Kong on top of its head flutters its small wings a little while staying seated, the camera circles slowly at a low angle, Kong stays tiny", G, 4),
    ("11", "wide shot from behind of Gomgom sitting at a small wooden kitchen table at sunset, spreading golden honey on a slice of bread, the small golden honey jar open on the table, tiny Kong standing on both little feet on the flat table beside a teacup, Kong only half as tall as the teacup, a window with a glowing felt village and pink sky beyond, gingham curtains, a teapot" + BACK,
     "seen from behind the whole time, Gomgom slowly spreads honey on the bread, its head does not turn, tiny Kong beside the teacup turns its head to stare at the honey bread and happily hops up and down in place and flutters its small wings excitedly, Kong stays in the same spot right beside the teacup, Kong stays tiny and only half as tall as the teacup even while hopping, its wings stay small, the sunset glows, the camera stays directly behind Gomgom and only rises slowly straight up, it never circles around, no face is visible on the back of the head, Kong stays tiny", G, 8),
]


def esc(s):
    return s.replace('"', '\\"')


for ep, items in (("ep09", EP9), ("ep10", EP10)):
    (H / ep / "prod").mkdir(parents=True, exist_ok=True)
    b = "declare -A IMG MOV CH DUR\n"
    for k, img, mov, ch, dur in items:
        b += f'IMG[{k}]="{esc(img)}"\nMOV[{k}]="{esc(mov)}"\nCH[{k}]="{ch}"; DUR[{k}]={dur}\n'
    keys = " ".join(k for k, *_ in items)
    t = tail.replace(f'KEYS="{old_keys}"', f'KEYS="{keys}"')
    (H / ep / "prod" / "generate.sh").write_text(head + b + "\nmkdir -p img clips" + t, encoding="utf-8")
    print(ep, len(items))
