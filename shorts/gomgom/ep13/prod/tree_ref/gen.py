import subprocess, json, sys, urllib.request, time
HF = "C:/Users/cine1/AppData/Roaming/npm/higgsfield.cmd"
STYLE = open("C:/tmp/newstyle.txt", encoding="utf-8").read().strip()
TREE = ("one single distinctive felt tree: its thick trunk bends in one big graceful S-curve, leaning to the left near the ground "
        "and curving back to the right halfway up, with one round knot bump on the bend, a few twisty curly crooked branches, "
        "soft rough felt bark in warm light brown, fluffy rounded clumps of mint and fresh green felt leaves")
def run(args):
    out = subprocess.run([HF, "generate", "create"] + args + ["--json"], capture_output=True, text=True, encoding="utf-8", stdin=subprocess.DEVNULL).stdout
    jid = json.loads(out)[0]
    w = subprocess.run([HF, "generate", "wait", jid, "--json"], capture_output=True, text=True, encoding="utf-8", stdin=subprocess.DEVNULL).stdout
    return jid, json.loads(w).get("result_url")
def img(name, prompt, ref=None):
    a = ["seedream_v5_lite", "--prompt", prompt + ", " + STYLE, "--aspect_ratio", "9:16", "--quality", "high"]
    if ref: a += ["--image-references", ref]
    jid, url = run(a)
    urllib.request.urlretrieve(url, name + ".png"); print(name, jid, url, flush=True)
mode = sys.argv[1]
if mode == "now":
    p = ("full view of " + TREE + ", now a HUGE old tree that has grown for a hundred years, the S-curved trunk very thick, "
         "a very wide round canopy spreading far to both sides and casting a broad cool pastel shade circle on a bright sunny felt meadow, "
         "a tiny wooden bench and little mushrooms at the foot of the trunk look very small, wildflowers, rolling pastel felt hills, "
         "no animals, no characters")
    img("now_A", p); img("now_B", p)
elif mode == "past":
    ref = sys.argv[2]
    p = ("the exact same tree as in the reference image, with exactly the same S-curved trunk shape, the same knot bump and the same twisty branches, "
         "but long ago when it was much younger and smaller, only a modest young tree with a thinner S-curved trunk and a small round canopy, "
         "standing in a bright felt forest clearing among other tall perfectly straight young trees, ferns, small mushrooms, a forest path, "
         "the crooked S-shape is clearly visible and stands out against the straight trees, no animals, no characters")
    img("past_A", p, ref)
