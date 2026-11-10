import os
T = (" Shot with a normal or short telephoto lens (50mm to 85mm), natural perspective, no wide-angle distortion."
     " Real full-scale world with real people for scale, not a miniature diorama, not a tabletop model."
     " Any visible text must be real words exactly as printed in a dictionary or a published newspaper.")
P = [
# 6 gingerbread village kids preparing Christmas
"Cinematic photorealistic family Christmas movie scene, a world where everything is made of food. A whole village square at blue hour on Christmas Eve, where every house is built of thick real gingerbread with white royal icing trim dripping like icicles, roofs of chocolate wafers, windows of clear melted sugar glowing warm from inside, street lamps of giant red-and-white candy canes, the ground covered in powdered sugar snow still falling softly. In the middle stands a tall Christmas tree made of a giant green broccoli, decorated with gumdrops and marshmallows. The whole village is busy with happy children in groups of two and three, all wearing homemade costumes: puffy gingerbread cookie suits with icing buttons, and little knight armor made of cookies and wafer biscuits with candy shields. In the foreground two gingerbread-suit kids carry a long garland of popcorn together, laughing; on a ladder a cookie-armored boy hangs a glowing gumdrop on the broccoli tree while his friend holds the ladder; to the side three kids roll a huge snowball of powdered sugar; one small girl secretly licks an icing icicle from a roof. Warm golden window light against deep blue dusk, gingerbread brown, icing white, candy cane red, broccoli green, rainbow gumdrops. Eye-level medium-wide shot, 50mm lens, ARRI Alexa, Kodak Vision3 500T, subtle grain, falling sugar snow frozen in the air. Important visual details: the gingerbread houses, the broccoli Christmas tree, the children's cookie costumes and cookie armor, and each small group's activity are all clearly readable; the children's faces are joyful and natural. Cozy, magical, delicious.",
]
P = [p + T for p in P]
d, m = ('v3', 'text2image_soul_v2')
os.makedirs(d, exist_ok=True)
open(f'{d}/prompts.txt', 'w', encoding='utf-8', newline='\n').write('\n'.join(P) + '\n')
open(f'{d}/model.txt', 'w').write(m + '\n')
open(f'{d}/aspect.txt', 'w').write('3:2\n')
print([len(p.split()) for p in P])
