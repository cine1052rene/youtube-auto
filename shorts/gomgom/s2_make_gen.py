# -*- coding: utf-8 -*-
"""시즌2 7·8화 generate.sh 작성기 (fix1006/fix.sh 머리·꼬리 재사용, 별 배지·S2 기준 이미지)"""
import pathlib

H = pathlib.Path(__file__).parent
src = (H / "fix1006" / "fix.sh").read_text(encoding="utf-8")
head = src.split("declare -A IMG MOV CH DUR")[0]
head = head.replace("REF=../ref/gomgom_master_s1.png", "REF=../../ref/gomgom_master_s2.png")
head = head.replace("wearing a small coral pink felt heart badge on its chest",
                    "wearing a small matte yellow felt star badge on its chest with no glow and no plastic shine")
head = head.replace("# 10/6 사용자 지적 수정", "# 시즌2 에피소드 생성(그림→영상). 사용: bash generate.sh img|vid [키...]\n# (구) 10/6", 1)
head = head.replace("SIZE=", 'FRIENDS="small felt animal friends such as a rabbit, a squirrel and a hedgehog, each about as tall as Gomgom"\nSIZE=', 1)
tail = src.split("mkdir -p img clips")[1]

BACK = (", seen from behind so the star badge on Gomgom's chest is hidden and NOT visible, Gomgom's back is plain cream "
        "fuzzy wool with only the thin brown satchel strap crossing it")
G = "$GOM; $KONG"
GO = "$GOM; Kong is not in this scene"
GOW = "$GOM; $OWL; Kong is not in this scene"
FR = "$FRIENDS; Gomgom and Kong are not in this scene"

EP7 = [
    ("01", "close three-quarter angle across a cluttered felt workbench at dusk, Gomgom sitting with a half-built miniature brick house made of tiny felt bricks in front of it, a tiny trowel in its paw, looking up in surprise at a round window where the orange sun is already setting, tiny Kong perched on Gomgom's shoulder, spools of thread, little jars of felt bricks, a desk lamp, a cork board with felt fabric swatches",
     "Gomgom looks from the half-built house up to the window as the last sunlight fades, its ears droop a little, tiny Kong on its shoulder tilts its head, the lamp flickers on, the camera slowly arcs from the workbench side toward the window", G, 4),
    ("02", "bright high angle shot of a sunny afternoon workshop, Gomgom happily laying out a neat plan on the workbench next to a pile of tiny felt bricks, a small wooden hammer, a ruler and a tiny bucket of glue, tiny Kong perched on top of the brick pile cheerfully, sunlight pouring through a big window with potted plants and hanging tools on a pegboard",
     "Gomgom places the first few felt bricks in a row and nods confidently, tiny Kong hops on top of the brick pile, sunlight sparkles on the dust, the camera glides down from a high angle to table height", G, 4),
    ("03", "low angle shot from the workbench surface, Gomgom carefully stacking tiny felt bricks into a wall that wobbles, a few bricks fallen over beside it, a round wall clock behind, warm late afternoon light, tiny Kong on Gomgom's head watching the wall",
     "the wall of felt bricks wobbles and two bricks tumble down, Gomgom catches one and sighs with its mouth closed, the wall clock hands sweep forward quickly, the camera slides sideways along the bench past the brick wall", G, 4),
    ("04", "wide shot from outside the workshop window at night, looking in through the glowing window at Gomgom still working at the bench by lamp light, the miniature brick house still without a roof, a crescent moon and stars above a tiny felt village, fireflies, a little potted plant on the window sill",
     "seen through the window, Gomgom rubs its eyes and keeps working under the lamp, fireflies drift past the glass, the camera slowly pulls back from the window to reveal the dark sleepy village", GO, 4),
    ("05", "medium shot inside Grandpa Owl's cozy treehouse library, Grandpa Owl standing slightly taller than Gomgom next to a big felt hourglass on a little table, Gomgom listening with its paws together, curved shelves of tiny books, hanging dried flowers, a teapot with a knitted cozy, round window with forest view, warm lamp light",
     "Grandpa Owl gently turns the big felt hourglass over and the sand starts to fall, Gomgom watches it closely and blinks, the camera arcs slowly around the two of them from eye level", GOW, 4),
    ("06", "dreamy medium shot of Gomgom gazing upward with a soft smile, a soft translucent felt thought bubble above its head showing a tiny picture of the brick house finished with a bright sun, sparkles inside the bubble, the cozy treehouse library softly blurred behind with shelves and lanterns",
     "inside the thought bubble the tiny brick house builds itself in a flash, Gomgom smiles dreamily, then the bubble wobbles softly, the camera rises along the bubble and tilts down to Gomgom", GO, 4),
    ("07", "top down shot of a wooden desk covered with Gomgom's old felt projects, a lopsided felt birdhouse, a half-knitted tiny scarf, a little boat model, Gomgom's paws flipping a scrapbook of old felt photos with no letters, tiny Kong walking across the scrapbook",
     "Gomgom's paws slowly flip the pages of the old scrapbook, tiny Kong hops from one page to the next, the camera drifts from top down to a low side angle along the desk", G, 4),
    ("08", "medium shot at a cozy breakfast nook, Gomgom sitting with a tiny notebook and a pencil, tapping the pencil on its chin thoughtfully, a cup of cocoa and a plate of tiny cookies, morning light through checkered curtains, tiny Kong perched on Gomgom's shoulder peeking at the notebook, a little cuckoo clock on the wall",
     "Gomgom taps the pencil on its chin and then raises one finger as if it has an idea, tiny Kong flaps its little wings on the shoulder, steam curls from the cocoa, the camera moves from the cuckoo clock across to Gomgom", G, 4),
    ("09", "close shot of Gomgom looking at a cork board covered with small felt photos of its old finished projects, each photo pinned next to a tiny felt sun or moon sticker, no letters or numbers anywhere, Gomgom pointing at one photo with a curious face, string lights around the board",
     "Gomgom moves its paw from one felt photo to the next and nods slowly as it remembers, the string lights twinkle, the camera slides along the cork board toward Gomgom's face", GO, 4),
    ("10", "low angle shot of a big friendly felt wall clock on the workshop wall, tiny Kong sitting on top of the clock and leaning down to push the long minute hand with its little wing, Gomgom below drawing a big generous circle on a felt calendar with no letters, warm morning light",
     "tiny Kong pushes the clock's minute hand around in a big circle and wobbles happily, Gomgom below draws a wide circle on the calendar, the camera tilts down from the clock to Gomgom", G, 4),
    ("11", "golden hour three-quarter shot of Gomgom proudly placing the last tiny felt roof tile on the finished miniature brick house on the workbench, the house has a little chimney and tiny windows glowing warmly, tiny Kong standing on the roof ridge, the orange sun still above the hills through the window",
     "Gomgom presses the last roof tile into place and steps back with a happy closed-mouth smile, tiny Kong does a little hop on the roof ridge, the windows of the tiny house light up, the camera pulls back and arcs around the finished house", G, 4),
    ("12", "wide shot from behind of Gomgom sitting on the workshop porch step at sunset beside the finished miniature brick house placed on the step, tiny Kong perched on Gomgom's shoulder, a watering can, a little lantern and flower pots on the porch, a handmade felt village and pink sky beyond" + BACK,
     "seen from behind, Gomgom sits on the porch as the sunset deepens, tiny Kong snuggles against its ear, the tiny house windows glow and fireflies rise, the camera rises slowly and pulls back to reveal the glowing village, Kong stays tiny on the shoulder", G, 8),
]
EP8 = [
    ("01", "close shot of Gomgom in front of a round wooden mirror in a cozy bedroom in the morning, one tuft of fur on top of its head sticking straight up, Gomgom patting it with both paws with a worried face, a felt hairbrush and a tiny comb on the dresser, morning sun through curtains, a little potted cactus",
     "Gomgom pats the sticking-up tuft down with both paws but it springs back up again, Gomgom's ears droop in a funny worried way, the camera moves from the mirror reflection around to Gomgom's side", GO, 4),
    ("02", "wide eye level shot of a bustling handmade felt village market street with striped awnings, fruit stalls, flower carts and bunting flags, Gomgom walking in with one paw held over the sticking-up tuft on its head, tiny Kong perched on Gomgom's shoulder, $FRIENDS shopping in the background",
     "Gomgom walks into the market keeping one paw on its head, glancing left and right, tiny Kong on its shoulder looks around curiously, the awnings flutter, the camera tracks backward in front of Gomgom", G, 4),
    ("03", "low angle shot of Gomgom standing in the middle of the market with its shoulders hunched, a soft warm theater spotlight beam shining down on it from above like on a stage, the rest of the market slightly dimmer around it, tiny Kong on its shoulder squinting up at the light",
     "the soft spotlight follows Gomgom as it takes two shy steps, Gomgom hunches lower and holds its tuft, tiny Kong squints at the light, the camera circles slowly around Gomgom at low height", G, 4),
    ("04", "high angle wide shot above the busy felt market, all the small felt animal friends busy with their own things, a rabbit choosing carrots, a squirrel counting acorns, a hedgehog arranging flowers, nobody looking at Gomgom who stands small in the middle, bunting and lanterns between the stalls",
     "the animal friends keep busy with their shopping and nobody turns to Gomgom, the camera rises higher above the market to show everyone busy, small Gomgom in the middle looks around", "$GOM; $FRIENDS; Kong is not visible", 4),
    ("05", "medium shot of Grandpa Owl standing slightly taller than Gomgom at a little outdoor market stall, Grandpa Owl holding up a tiny bright yellow felt T-shirt with a funny cartoon face print and no letters, Gomgom looking at it with a curious face, a clothesline of tiny felt clothes behind them, baskets and lanterns",
     "Grandpa Owl lifts the tiny bright T-shirt and wiggles it, Gomgom tilts its head with interest, the clothesline sways in the breeze, the camera arcs slowly around the stall", GOW, 4),
    ("06", "wide shot of a cozy felt classroom with little wooden desks, a small felt rabbit standing at the doorway wearing the bright yellow T-shirt with a funny face print and no letters, cheeks pink and covering its face shyly, $FRIENDS sitting at the desks, a board with only doodles of flowers and no letters, potted plants",
     "the small rabbit in the bright T-shirt shuffles shyly into the classroom covering its face, the camera pushes in from the back of the room past the desks", FR, 4),
    ("07", "medium wide shot of the same felt classroom, the shy rabbit in the bright yellow T-shirt sitting down, three of the four animal friends busy reading picture books, drawing and chatting, only one hedgehog glancing at the T-shirt briefly, warm window light, plants and a globe",
     "most of the animal friends keep reading and drawing without looking up, only the hedgehog glances once at the T-shirt and goes back to its book, the rabbit relaxes and smiles, the camera slides sideways along the desks", FR, 4),
    ("08", "front view of a tiny cozy felt puppet theater stage with velvet curtains and little footlights, Gomgom standing alone on the stage under a bright spotlight looking shy, rows of little wooden seats where a few felt animals are turned around chatting to each other",
     "the bright spotlight on Gomgom slowly widens and softens into warm general light, Gomgom looks up and its shoulders relax, the curtains sway, the camera pulls back from the stage to the seats", GO, 4),
    ("09", "eye level shot along the busy felt market stalls, a rabbit weighing carrots on a little scale, a squirrel counting acorns into jars, a hedgehog tying a bouquet of felt flowers, everyone happily focused on their own work, warm afternoon light, bunting overhead, Gomgom small in the background",
     "the market friends keep busy with their own tasks, carrots tumble onto the scale and acorns drop into jars, the camera tracks along the stalls past each busy friend", "$GOM; $FRIENDS; Kong is not visible", 4),
    ("10", "close shot of Gomgom sitting on a market bench, tiny Kong standing on top of Gomgom's head pressing down the sticking-up tuft with both little wings, Gomgom giggling with its eyes squeezed shut and mouth closed, a basket of apples beside it, flower stall behind",
     "tiny Kong presses the tuft down with its little wings, the tuft springs back up and Kong presses again, Gomgom giggles with closed mouth, the camera arcs slowly around the bench", G, 4),
    ("11", "wide three-quarter shot of Gomgom walking happily through the market with its head held high and the tuft still sticking up, holding a little paper bag of bread, tiny Kong perched on its head, stall keepers busy with their work, bunting, lanterns and flower carts",
     "Gomgom walks cheerfully past the stalls looking around with a happy face, tiny Kong rides on its head, a squirrel waves casually and goes back to work, the camera tracks alongside Gomgom", G, 4),
    ("12", "wide shot from behind of Gomgom sitting on a little hill at sunset overlooking the felt market village where lanterns are lighting up, tiny Kong perched on Gomgom's head next to the sticking-up tuft, a paper bag of bread beside Gomgom, pink and gold sky" + BACK,
     "seen from behind, Gomgom sits on the hill as the lanterns of the market light up one by one, tiny Kong snuggles beside the tuft, the breeze makes the tuft wiggle, the camera rises slowly and pulls back to reveal the whole glowing village", G, 8),
]


def esc(s):
    return s.replace('"', '\\"')


for ep, items in (("ep07", EP7), ("ep08", EP8)):
    b = "declare -A IMG MOV CH DUR\n"
    for k, img, mov, ch, dur in items:
        b += f'IMG[{k}]="{esc(img)}"\nMOV[{k}]="{esc(mov)}"\nCH[{k}]="{ch}"; DUR[{k}]={dur}\n'
    keys = " ".join(k for k, *_ in items)
    t = tail.replace('KEYS="e04_05 e06_05 e06_06 e06_07 e06_11 e06_12"', f'KEYS="{keys}"')
    (H / ep / "prod" / "generate.sh").write_text(head + b + "\nmkdir -p img clips" + t, encoding="utf-8")
    print(ep, len(items))


# ---- 파생 쇼츠 (시즌1 기간이라 하트 배지·S1 기준 이미지) ----
head1 = src.split("declare -A IMG MOV CH DUR")[0].replace("REF=../ref/gomgom_master_s1.png", "REF=../../ref/gomgom_master_s1.png")
D1 = [  # 댓글 답장: 쉴 때 스트레칭
    ("01", "medium shot of Gomgom in a cozy sunlit living room reading a small handwritten felt postcard with no letters visible, a soft smile, tiny Kong perched on Gomgom's shoulder peeking at the postcard, a knitted rug, a plant, a basket of yarn and a window with curtains",
     "Gomgom reads the little postcard and nods with a warm closed-mouth smile, tiny Kong leans in to look, the curtains sway, the camera moves slowly from the window side to Gomgom", G, 4),
    ("02", "three-quarter shot of Gomgom on a small felt yoga mat stretching both arms high above its head with eyes happily closed, tiny Kong on top of Gomgom's head stretching its little wings upward to copy it while keeping them small, morning sunlight, a potted plant, a tiny water bottle and a towel",
     "Gomgom stretches both arms up and leans gently side to side, tiny Kong on its head copies the stretch with its small wings, then both relax with a happy sigh, the camera arcs slowly around the mat", G, 4),
]
D2 = [  # 콩이 미니 장면: 이슬방울
    ("01", "macro close-up in a morning felt garden, tiny Kong standing on a big green felt leaf next to one round glittering dewdrop, Kong's small wings folded neatly against its round body, soft golden morning light, felt flowers and a ladybug in the blurred background",
     "tiny Kong leans close to the dewdrop and sees its own little reflection, it tilts its head and gives a tiny happy hop on the leaf keeping its wings folded, the dewdrop sparkles, the camera slowly arcs around the leaf", "$KONG; Gomgom is not in this scene", 4),
    ("02", "medium shot of Gomgom crouching in the morning garden beside the big felt leaf, looking at the sparkling dewdrop with a soft surprised smile, tiny Kong on the leaf pointing at the dewdrop with one small wing, flower beds, a watering can and a little fence",
     "Gomgom leans in to look at the dewdrop and smiles warmly, tiny Kong bounces happily on the leaf, morning light sparkles through the dewdrop, the camera rises gently from the leaf to Gomgom", G, 4),
]
for ep, items in (("epd01", D1), ("epd02", D2)):
    (H / ep / "prod").mkdir(parents=True, exist_ok=True)
    b = "declare -A IMG MOV CH DUR\n"
    for k, img, mov, ch, dur in items:
        b += f'IMG[{k}]="{esc(img)}"\nMOV[{k}]="{esc(mov)}"\nCH[{k}]="{ch}"; DUR[{k}]={dur}\n'
    keys = " ".join(k for k, *_ in items)
    t = tail.replace('KEYS="e04_05 e06_05 e06_06 e06_07 e06_11 e06_12"', f'KEYS="{keys}"')
    (H / ep / "prod" / "generate.sh").write_text(head1 + b + "\nmkdir -p img clips" + t, encoding="utf-8")
    print(ep, len(items))
