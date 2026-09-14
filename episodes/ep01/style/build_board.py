# -*- coding: utf-8 -*-
"""기법 탐색 보드"""
import base64, pathlib, subprocess

HERE = pathlib.Path(__file__).parent
OUT = HERE / "style_board.html"

SRC = {
    "presets/contact": ("sheet", 1100),
    "tx_papercraft": ("t_paper", 980), "tx_diorama": ("t_dio", 980),
    "tx_collage": ("t_col", 980), "tx_clay": ("t_clay", 980),
    "v2_a": ("t_real", 980), "tech_claymotion": ("t_fail", 760),
}
for src, (dst, w) in SRC.items():
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(HERE / f"{src}.png"),
                    "-vf", f"scale={w}:-1", "-q:v", "4", str(HERE / f"{dst}.jpg")], check=True)

def b64(n):
    return base64.b64encode((HERE / f"{n}.jpg").read_bytes()).decode()

TESTED = [
    dict(k="t_paper", n="종이 레이어 터널", en="Layered Papercraft", rank="1위", kind="pick",
         v="<b>압도적입니다.</b> 종이 층이 겹겹이 안으로 파고들고 그 끝에 장면이 들어앉아 있습니다. "
           "지적하셨던 &lsquo;배경이 붙어있다&rsquo;는 문제가 구조적으로 사라집니다 &mdash; 깊이가 기법 자체에 내장돼 있으니까요.",
         w="매 컷이 &lsquo;종이 층을 통해 한 장면을 들여다본다&rsquo;는 하나의 문법이 됩니다. 시그니처가 되기 좋습니다."),
    dict(k="t_dio", n="미니어처 상자", en="Cardboard Diorama", rank="2위", kind="good",
         v="골판지 상자 안에 작은 인물이 서 있습니다. <b>은유가 그림에 이미 들어있습니다</b> &mdash; "
           "거대한 시스템 속의 한 사람. 심리학 소재와 정확히 맞물립니다.",
         w="요즘 미니어처 룩이 특히 잘 먹힙니다. 다만 상자 프레임이 매번 같아서 단조로워질 수 있습니다."),
    dict(k="t_col", n="혼합매체 콜라주", en="Mixed Media", rank="3위", kind="warn",
         v="찢은 종이와 잉크 드로잉이 겹친 아트북 감성입니다. 지적인 느낌이 강합니다.",
         w="<b>깨진 손글씨가 사방에 있습니다.</b> 갤러리 작품처럼 보여서 설명 영상으로는 산만합니다."),
    dict(k="t_clay", n="클레이", en="Claymotion", rank="탈락", kind="bad",
         v=None,
         w="<b>인물만 점토고 배경은 실사</b>로 또 섞였습니다. 앞서 애니메·플랫에서 겪은 문제와 같습니다. "
           "Soul 2.0은 화면 전체를 하나의 재질로 통일하는 걸 어려워합니다."),
]

cards = "\n".join(f'''
      <article class="card {t['kind']}">
        <div class="frame">
          <img src="data:image/jpeg;base64,{b64(t['k'])}" alt="{t['n']}" />
          <span class="rank">{t['rank']}</span>
        </div>
        <div class="body">
          <header><div><h3>{t['n']}</h3><p class="en">{t['en']}</p></div></header>
          {f'<p class="plus">{t["v"]}</p>' if t['v'] else ''}
          <p class="minus">{t['w']}</p>
        </div>
      </article>''' for t in TESTED)

HTML = f'''<title>종이 층을 통해 들여다보기</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Noto+Sans+KR:wght@400;500;700&display=swap">
<style>
  :root {{
    --paper:#F6F3EC; --card:#FFFFFF; --edge:#E0D9CC;
    --ink:#242019; --soft:#6E665C; --gold:#B07817; --teal:#1F6E6A; --red:#B44A32;
    --serif:"Gowun Batang",Georgia,serif; --sans:"Noto Sans KR",system-ui,sans-serif;
  }}
  :root:not([data-theme="light"]) {{ color-scheme:light; }}
  @media (prefers-color-scheme:dark) {{
    :root:not([data-theme="light"]) {{
      --paper:#16140F; --card:#201D17; --edge:#353026;
      --ink:#EEE8DC; --soft:#A29889; --gold:--gold; --gold:#D9A340; --teal:#4FAEA8; --red:#D77A5E;
    }}
  }}
  :root[data-theme="dark"] {{
    --paper:#16140F; --card:#201D17; --edge:#353026;
    --ink:#EEE8DC; --soft:#A29889; --gold:#D9A340; --teal:#4FAEA8; --red:#D77A5E;
  }}
  * {{ box-sizing:border-box; }}
  body {{ background:var(--paper); color:var(--ink); font-family:var(--sans);
          line-height:1.76; padding:0 20px; padding-block:44px 72px; }}
  .wrap {{ max-width:740px; margin:0 auto; display:flex; flex-direction:column; gap:50px; }}

  .eyebrow {{ font-size:12px; letter-spacing:.2em; color:var(--teal); font-weight:700;
              text-transform:uppercase; margin:0 0 12px; }}
  h1 {{ font-family:var(--serif); font-size:clamp(28px,7vw,40px); margin:0 0 18px;
        line-height:1.3; font-weight:700; text-wrap:balance; }}
  h2 {{ font-family:var(--serif); font-size:24px; margin:0 0 8px; font-weight:700; }}
  .sectnote {{ margin:0 0 22px; color:var(--soft); font-size:14.5px; }}
  .lede {{ margin:0 0 14px; font-size:15.5px; color:var(--soft); }}
  .lede b {{ color:var(--ink); font-weight:500; }}

  .agree {{ background:var(--card); border-left:3px solid var(--teal); padding:17px 19px;
            display:flex; flex-direction:column; gap:11px; }}
  .agree p {{ margin:0; font-size:15px; }}
  .agree .head {{ font-family:var(--serif); font-size:17px; font-weight:700; }}
  .cond {{ list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:9px; }}
  .cond li {{ display:flex; gap:11px; font-size:14.5px; }}
  .cond b {{ font-family:var(--serif); color:var(--teal); flex-shrink:0; }}
  .cond span {{ color:var(--soft); }}
  .cond i {{ font-style:normal; color:var(--ink); font-weight:500; }}

  .sheet img {{ width:100%; max-width:100%; height:auto; display:block;
                border:1px solid var(--edge); }}

  .cards {{ display:flex; flex-direction:column; gap:28px; }}
  .card {{ background:var(--card); border:1px solid var(--edge); overflow:hidden; }}
  .card.pick {{ border:2px solid var(--gold); }}
  .card.bad img {{ opacity:.6; }}
  .frame {{ position:relative; line-height:0; }}
  .frame img {{ width:100%; max-width:100%; height:auto; display:block; }}
  .rank {{ position:absolute; top:0; left:0; padding:6px 12px; font-size:12px;
           font-weight:700; background:var(--ink); color:var(--paper); }}
  .pick .rank {{ background:var(--gold); color:#201D17; }}
  .bad .rank {{ background:var(--red); color:#fff; }}
  .body {{ padding:18px 19px 21px; display:flex; flex-direction:column; gap:10px; }}
  .body h3 {{ font-family:var(--serif); font-size:20px; margin:0; font-weight:700; }}
  .en {{ margin:1px 0 0; font-size:11px; letter-spacing:.13em;
         text-transform:uppercase; color:var(--soft); }}
  .plus, .minus {{ margin:0; font-size:14.5px; padding-left:16px; position:relative; }}
  .plus::before {{ content:"+"; position:absolute; left:0; color:var(--teal); font-weight:700; }}
  .minus::before {{ content:"−"; position:absolute; left:0; color:var(--red); font-weight:700; }}
  .minus {{ color:var(--soft); }}

  .ba {{ display:grid; grid-template-columns:1fr; gap:14px; }}
  .ba figure {{ margin:0; }}
  .ba img {{ width:100%; max-width:100%; height:auto; display:block; border:1px solid var(--edge); }}
  .ba figcaption {{ font-size:13px; margin-top:7px; color:var(--soft); }}
  .ba b {{ color:var(--ink); }}
  @media (min-width:640px) {{ .ba {{ grid-template-columns:1fr 1fr; }} }}

  .note {{ background:var(--card); border:1px solid var(--edge); padding:18px 19px;
           display:flex; flex-direction:column; gap:10px; }}
  .note h3 {{ font-family:var(--serif); font-size:17px; margin:0; font-weight:700; }}
  .note p {{ margin:0; font-size:14.5px; color:var(--soft); }}
  .note img {{ width:100%; max-width:340px; height:auto; border:1px solid var(--edge); }}

  .ask {{ border-top:2px solid var(--edge); padding-top:30px;
          display:flex; flex-direction:column; gap:15px; }}
  .ask .q {{ background:var(--card); border-left:3px solid var(--gold); padding:15px 17px; }}
  .ask h3 {{ font-family:var(--serif); font-size:18px; margin:0 0 6px; font-weight:700; }}
  .ask p {{ margin:0; font-size:14.5px; color:var(--soft); }}
  .bal {{ font-size:13.5px; color:var(--soft); font-variant-numeric:tabular-nums; margin:0; }}
</style>

<div class="wrap">
  <section>
    <p class="eyebrow">기법 탐색</p>
    <h1>실사를 버리고 기법으로 갑니다</h1>
    <div class="agree">
      <p class="head">방향에 동의합니다.</p>
      <p>AI 실사는 이미 흔합니다. &lsquo;예쁜 사람 + 좋은 빛&rsquo;은 배경화면이지 무기가 아닙니다.
         유튜브의 진짜 병목은 화질이 아니라 <b>피드에서 스크롤을 멈추게 하는가</b>이고, 거기엔 기법이 훨씬 강합니다.</p>
      <p>다만 조건 셋을 붙이고 싶습니다.</p>
      <ul class="cond">
        <li><b>1</b><span><i>350번 반복 가능한가.</i> 한 컷 쇼케이스용 기법은 열 번 하면 지칩니다.</span></li>
        <li><b>2</b><span><i>유행이 꺾여도 버티는가.</i> 지금 뜨는 것에 묶으면 3개월 뒤 늙어 보입니다.</span></li>
        <li><b>3</b><span><i>이야기를 돕는가.</i> 멋만 부리고 내용과 무관하면 금방 질립니다.</span></li>
      </ul>
    </div>
  </section>

  <section>
    <h2>Higgsfield가 가진 기법 22종</h2>
    <p class="sectnote">
      추측하지 않고 실제 라이브러리를 뒤졌습니다. <b>조회는 무료</b>라 크레딧이 들지 않았습니다.
      점토, 종이공예, 펠트인형, 픽셀아트, 화이트보드까지 있습니다.
    </p>
    <div class="sheet"><img src="data:image/jpeg;base64,{b64('sheet')}" alt="기법 22종 목록" /></div>
  </section>

  <section>
    <h2>이 중 넷을 실제로 뽑아봤습니다</h2>
    <p class="sectnote">
      비교가 되도록 <b>아까 그 마트 장면</b> 그대로 썼습니다. 실사판과 직접 견주실 수 있습니다.
    </p>
    <div class="ba">
      <figure><img src="data:image/jpeg;base64,{b64('t_real')}" alt="실사판" />
        <figcaption><b>실사판</b> &mdash; 잘 뽑혔지만 어디서 본 듯합니다</figcaption></figure>
      <figure><img src="data:image/jpeg;base64,{b64('t_paper')}" alt="종이 레이어판" />
        <figcaption><b>종이 레이어판</b> &mdash; 같은 장면, 전혀 다른 물건</figcaption></figure>
    </div>
  </section>

  <section>
    <div class="cards">{cards}
    </div>
  </section>

  <section class="note">
    <h3>한 가지 배운 것</h3>
    <p>프리셋을 레퍼런스 이미지로 물려봤더니 <b>프롬프트를 통째로 덮어버렸습니다.</b>
       마트를 요청했는데 프리셋 원본인 화산 단면이 그대로 나왔습니다.
       스타일만이 아니라 내용까지 복사합니다.</p>
    <img src="data:image/jpeg;base64,{b64('t_fail')}" alt="레퍼런스 실패 사례" />
    <p>그래서 <b>기법을 말로 서술하는 방식</b>으로 바꿨고, 그게 위의 결과입니다. 구도는 제가 잡고 질감만 가져옵니다.</p>
  </section>

  <section class="ask">
    <div class="q">
      <h3>1. 종이 레이어입니까, 미니어처 상자입니까?</h3>
      <p>둘 다 강합니다. 종이 레이어는 <b>화면이 더 아름답고</b>, 미니어처 상자는 <b>은유가 더 셉니다</b>.
         고르시면 그 기법으로 서로 다른 장면 4개를 뽑아 &mdash; 350컷을 버틸 수 있는지 확인하겠습니다.</p>
    </div>
    <div class="q">
      <h3>2. 스토리는 아직 2번입니까, 3번입니까?</h3>
      <p><b>2번 일상 심리학</b>(마트·지하철) / <b>3번 행복 철학</b>(지중해·올리브).
         기법이 정해지면 어느 쪽이 더 어울리는지도 같이 봐야 합니다.</p>
    </div>
    <p class="bal">지금까지 쓴 크레딧 2.52 &middot; 남은 잔액 297.48 &middot; 전체의 0.8%</p>
  </section>
</div>
'''

OUT.write_text(HTML, encoding="utf-8")
print(f"생성 완료 ({len(HTML)/1024:.0f}KB)")
