import os
T = (" Shot with a normal or short telephoto lens (50mm to 85mm), natural perspective, no wide-angle distortion."
     " Any visible text must be real words exactly as printed in a dictionary or a published newspaper.")
P = [
# 1 dragon: asleep, living creature
"Cinematic photorealistic fantasy scene, epic and funny: deep inside a vast dark cave, a living enormous dragon lies fast asleep on a mountain of gold coins, goblets and jewels. Its huge head rests on the treasure, both eyes fully closed, heavy eyelids shut, its wet nostrils flaring with each breath, smoke curling out, real weathered scales with scars, dust and moisture, a breathing animal and not a statue. Standing on tiptoe right in front of its giant nostrils is a housekeeper in a plain black dress, white apron and rubber gloves, holding her breath, calmly dusting a golden crown with a feather duster, her face focused and professional. The dragon's warm breath blows her hair and a cloud of dust sideways. Warm gold light reflecting up from the treasure, deep shadowy cave, dark emerald scales, the white apron as the brightest accent. Eye-level medium shot, 85mm lens, ARRI Alexa, Kodak Vision3 500T, subtle grain, shallow depth of field, the precise moment frozen. Important visual details: the dragon's eyes are closed and it is clearly asleep and alive; its nostril is right beside the housekeeper; the feather duster, the crown and the blown dust are clearly visible. The chore is boring, the stakes are not. Heroic, epic, funny.",
# 5 bed on the wing with passengers
"Cinematic photorealistic action scene, epic and funny: a passenger jet flies above a sea of white clouds at sunset, seen from beside the fuselage looking out along the long silver wing. Strapped to the top surface of the WING, not the fuselage, is a neatly made hotel bed with a headboard, held by cargo straps. A hotel housekeeper in a grey uniform, clipped to a safety harness, kneels on the wing and tucks in the corner of the white sheet with perfect hospital corners while the wind tears at everything: the bedsheet billows up like a huge sail, her hair whips sideways, one pillow flies away behind her. In the foreground, a row of oval cabin windows along the fuselage shows passengers pressing their shocked faces against the glass, one filming with a phone. Warm golden sunset light, white sheets, silver wing, pink and orange clouds. Medium shot, 50mm lens, ARRI Alexa, Kodak Vision3 250D, subtle grain, the precise moment frozen. Important visual details: the bed is clearly on the wing, the housekeeper is tucking the sheet, the sheet billows, and the shocked passengers' faces are visible in the windows; no airline name or logo on the plane. The chore is boring, the stakes are not. Heroic, epic, funny.",
]
P = [p + T for p in P]
d, m = ('v2', 'soul_cinematic')
os.makedirs(d, exist_ok=True)
open(f'{d}/prompts.txt', 'w', encoding='utf-8', newline='\n').write('\n'.join(P) + '\n')
open(f'{d}/model.txt', 'w').write(m + '\n')
open(f'{d}/aspect.txt', 'w').write('3:2\n')
print([len(p.split()) for p in P])
