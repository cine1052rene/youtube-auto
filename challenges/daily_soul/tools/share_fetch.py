# 공유 링크(higgsfield.ai/s/ID) → 프롬프트·모델·원본 이미지 URL, 이미지 축소본 저장
# 사용: python tools/share_fetch.py   (data/hof_raw.jsonl 의 link 전부; 이미 받은 건 건너뜀)
# 결과: data/winners_share.jsonl, data/archive/winners/<ID>.jpg
import os, re, json, html, subprocess, urllib.request, io, concurrent.futures as cf
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
OUT = os.path.join(ROOT, 'data', 'winners_share.jsonl')
IMG = os.path.join(ROOT, 'data', 'archive', 'winners'); os.makedirs(IMG, exist_ok=True)
def parse(s):
    m = re.search(r'<p id="_r_\w+_" class="whitespace-pre-wrap[^"]*">(.*?)</p>', s, re.S)
    prompt = html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip() if m else ''
    mm = re.search(r'<span class="truncate">([^<]+)</span></span>로 생성됨', s) or re.search(r'<span class="truncate">([^<]+)</span></span>\s*(?:Generated|generated)', s)
    og = re.search(r'og:image" content="([^"]+)"', s)
    return prompt, (mm.group(1) if mm else ''), (og.group(1) if og else '')
def one(link):
    sid = link.rstrip('/').split('/')[-1]
    try:
        s = subprocess.run([CH, '--headless=new', '--disable-gpu', '--virtual-time-budget=12000', '--dump-dom', link], capture_output=True, timeout=90).stdout.decode('utf-8', 'ignore')
    except Exception as e:
        return {'link': link, 'id': sid, 'error': str(e)}
    prompt, model, img = parse(s)
    thumb = ''
    if img:
        p = os.path.join(IMG, sid + '.jpg')
        try:
            if not os.path.exists(p):
                data = urllib.request.urlopen(img, timeout=60).read()
                im = Image.open(io.BytesIO(data)).convert('RGB'); im.thumbnail((1200, 1200)); im.save(p, quality=85)
            thumb = os.path.relpath(p, ROOT).replace('\\', '/')
        except Exception as e:
            thumb = ''
    return {'link': link, 'id': sid, 'model': model, 'prompt': prompt, 'image_url': img, 'thumb': thumb, 'html_len': len(s)}
if __name__ == '__main__':
    links = []
    for f in ['hof_raw.jsonl', 'hof_scan.jsonl', 'hof_manual.jsonl']:
        fp = os.path.join(ROOT, 'data', f)
        if os.path.exists(fp):
            for l in open(fp, encoding='utf-8'):
                r = json.loads(l)
                if r.get('link') and r['link'] not in links: links.append(r['link'])
    done = set()
    if os.path.exists(OUT):
        for l in open(OUT, encoding='utf-8'):
            r = json.loads(l)
            if r.get('prompt') or r.get('image_url'): done.add(r['link'])
    todo = [l for l in links if l not in done]
    print(len(links), 'links,', len(todo), 'to fetch', flush=True)
    with open(OUT, 'a', encoding='utf-8', newline='\n') as out, cf.ThreadPoolExecutor(4) as ex:
        for r in ex.map(one, todo):
            out.write(json.dumps(r, ensure_ascii=False) + '\n'); out.flush()
            print('OK' if r.get('prompt') else 'NOPROMPT', r['id'], r.get('model', ''), len(r.get('prompt', '')), flush=True)
