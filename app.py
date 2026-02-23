"""
DCDS 8991 — College Admission  Part 1
Scrollable simulation with Apple-style section transitions.
"""

import math
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="College Admission | DCDS 8991", page_icon="🎓", layout="wide")
st.title("College Admission — DCDS 8991")

NAVY   = "#1e3a5f"
ORANGE = "#ea580c"
PURPLE = "#7c3aed"
PINK   = "#db2777"
COFFEE = "#78350f"
GREEN  = "#059669"
RED    = "#dc2626"

# Data is generated fresh in JS on every replay (probabilistic)

# ── Rim icons for circle ──────────────────────────────────────────────────────
rim_svg = ""
for i in range(100):
    grp = "A" if i < 50 else "D"
    col = NAVY if grp == "A" else ORANGE
    angle = 2 * math.pi * i / 100 - math.pi / 2
    cx = 350 + 282 * math.cos(angle)
    cy = 350 + 282 * math.sin(angle)
    rim_svg += (
        f'<g class="picon" data-group="{grp}" transform="translate({cx:.1f},{cy:.1f})">'
        f'<circle r="13" fill="{col}" stroke="white" stroke-width="1.5"/>'
        f'<circle cx="0" cy="-4" r="4" fill="white" opacity="0.9"/>'
        f'<path d="M-5.5,0.5 Q-5.5,8 0,8 Q5.5,8 5.5,0.5 Q5.5,-2 0,-2 Q-5.5,-2 -5.5,0.5 Z" fill="white" opacity="0.9"/>'
        f'</g>'
    )

# ── Center hover panels (SVG groups) ─────────────────────────────────────────
def big_icon(tx, ty, fill, clip_id):
    ol = "#dde3ee"
    return (
        f'<g transform="translate({tx},{ty})">'
        f'<circle cx="0" cy="-13" r="10" fill="{ol}" stroke="#c9d3e0" stroke-width="1"/>'
        f'<path d="M-13,-4 Q-13,18 0,18 Q13,18 13,-4 Q13,-10 0,-10 Q-13,-10 -13,-4 Z" fill="{ol}" stroke="#c9d3e0" stroke-width="1"/>'
        f'<circle cx="0" cy="-13" r="10" fill="{fill}" clip-path="url(#{clip_id})"/>'
        f'<path d="M-13,-4 Q-13,18 0,18 Q13,18 13,-4 Q13,-10 0,-10 Q-13,-10 -13,-4 Z" fill="{fill}" clip-path="url(#{clip_id})"/>'
        f'</g>'
    )

def center_panel(group):
    is_adv   = group == "A"
    title    = "Advantaged Group (A)" if is_adv else "Disadvantaged Group (D)"
    tcol     = NAVY if is_adv else ORANGE
    frac     = "⅔" if is_adv else "⅓"
    clip     = "clip23" if is_adv else "clip13"
    pf       = "4/9 ≈ 44%" if is_adv else "1/9 ≈ 11%"
    fc       = GREEN if is_adv else RED
    sub      = "Higher resources → higher probabilities" if is_adv else "Fewer resources → lower probabilities"
    ix1 = big_icon(268, 328, PURPLE, clip)
    ix2 = big_icon(268, 418, PINK,   clip)
    return (
        f'<g id="center-{group}" visibility="hidden">'
        f'<text x="350" y="236" text-anchor="middle" font-size="17" font-weight="700" fill="{tcol}">{title}</text>'
        f'<text x="350" y="257" text-anchor="middle" font-size="12" fill="#64748b">{sub}</text>'
        f'<line x1="155" y1="268" x2="545" y2="268" stroke="#e2e8f0" stroke-width="1.5"/>'
        f'{ix1}'
        f'<text x="302" y="314" font-size="15" font-weight="700" fill="{PURPLE}">P(x\u2081 = 1) = {frac}</text>'
        f'<text x="302" y="332" font-size="12" fill="#94a3b8">probability of having feature x\u2081</text>'
        f'{ix2}'
        f'<text x="302" y="404" font-size="15" font-weight="700" fill="{PINK}">P(x\u2082 = 1) = {frac}</text>'
        f'<text x="302" y="422" font-size="12" fill="#94a3b8">probability of having feature x\u2082</text>'
        f'<line x1="155" y1="440" x2="545" y2="440" stroke="#e2e8f0" stroke-width="1.5"/>'
        f'<text x="350" y="459" text-anchor="middle" font-size="12" fill="#475569">'
        f'f = x\u2081 \u2227 x\u2082   \u2192   <tspan font-weight="700" fill="{fc}">P(f=1) = {pf}</tspan>'
        f'</text></g>'
    )

# ── Full HTML ─────────────────────────────────────────────────────────────────
HTML = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: -apple-system, 'Segoe UI', sans-serif;
  background: #ffffff;
  overflow-x: hidden;
}}

/* ── Sections ── */
.section {{
  width: 100%;
  min-height: 740px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2.5rem 1.5rem 2rem;
}}
.fade-section {{
  opacity: 0;
  transform: translateY(28px);
  transition: opacity 0.85s cubic-bezier(.4,0,.2,1),
              transform 0.85s cubic-bezier(.4,0,.2,1);
}}
.fade-section.visible {{
  opacity: 1;
  transform: translateY(0);
}}

/* ── Scroll hint ── */
.scroll-hint {{
  margin-top: 1.2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  color: #94a3b8;
  font-size: 0.8rem;
  animation: bounce 2s ease-in-out infinite;
}}
@keyframes bounce {{
  0%,100% {{ transform: translateY(0); }}
  50%      {{ transform: translateY(6px); }}
}}

/* ── Section title ── */
.sec-eyebrow {{
  width: 48px; height: 4px; border-radius: 99px;
  margin: 0 auto 1rem;
}}
.sec-title {{
  font-size: 1.65rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.35rem;
  text-align: center;
}}
.sec-sub {{
  font-size: 0.9rem;
  color: #64748b;
  margin-bottom: 1.4rem;
  text-align: center;
}}

/* ── Legend pills ── */
.pills {{
  display: flex; gap: 0.75rem; flex-wrap: wrap;
  justify-content: center; margin-bottom: 1.2rem;
}}
.pill {{
  display: flex; align-items: center; gap: 6px;
  padding: 5px 14px; border-radius: 999px;
  font-size: 0.82rem; font-weight: 600; border: 2px solid;
}}
.pill-hat  {{ color:{PURPLE}; border-color:{PURPLE}; background:#f5f3ff; }}
.pill-shoe {{ color:{COFFEE}; border-color:{COFFEE}; background:#fef3c7; }}

/* ── Speed control ── */
.speed-row {{
  display: flex; align-items: center; gap: 0.75rem;
  margin-bottom: 1.4rem;
  font-size: 0.82rem; color: #475569;
}}
.speed-row input[type="range"] {{
  accent-color: {PURPLE}; width: 130px; cursor: pointer;
}}
.speed-lbl {{
  font-variant-numeric: tabular-nums;
  min-width: 44px; color: {PURPLE}; font-weight: 600;
}}
.replay-btn {{
  padding: 5px 15px; border-radius: 7px; border: none;
  background: #1e293b; color: white;
  font-size: 0.82rem; font-weight: 600; cursor: pointer;
  transition: background 0.15s, transform 0.1s;
}}
.replay-btn:hover {{ background: #0f172a; transform: translateY(-1px); }}
.replay-btn:active {{ transform: translateY(0); }}

/* ── Person grid ── */
.pgrid {{
  display: grid;
  grid-template-columns: repeat(10, 1fr);
  gap: 4px;
  width: min(640px, 94vw);
  margin-bottom: 1rem;
}}
.pslot {{
  display: flex; justify-content: center; align-items: flex-end;
  height: 80px;
  opacity: 0;
  transform: translateX(18px) scale(0.88);
  transition: opacity 0.28s ease, transform 0.28s ease;
}}
.pslot.shown {{
  opacity: 1;
  transform: translateX(0) scale(1);
}}

/* ── Smaller slot for 10×10 grid ── */
.pslot-sm {{
  height: 66px;
}}

/* ── Admitted highlight ── */
.pslot.admitted {{
  outline: 3px solid #f59e0b;
  outline-offset: -2px;
  border-radius: 8px;
  background: rgba(245,158,11,0.12);
  transition: outline 0.3s, background 0.3s;
}}
.pslot.not-admitted {{
  opacity: 0.25;
  transition: opacity 0.5s;
}}

/* ── Counter bar ── */
.counter-bar {{
  display: flex; gap: 1.5rem; flex-wrap: wrap;
  justify-content: center;
  padding: 0.7rem 1.5rem;
  background: #f8fafc;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  font-size: 0.875rem; color: #334155;
  min-height: 44px; min-width: 300px;
  transition: opacity 0.4s;
}}
.cstat {{ font-weight: 700; }}
.cx1 {{ color: {PURPLE}; }}
.cx2 {{ color: {COFFEE}; }}
.cf  {{ color: {GREEN}; }}

/* ── Circle section ── */
.picon {{ cursor: pointer; }}
.picon:hover circle, .picon:hover path {{ opacity: 0.7; transition: opacity 0.12s; }}

/* ── Gen section grid overrides ── */
#gen-adv-g2 .pslot,
#gen-dis-g2 .pslot {{
  height: 88px;
  align-items: flex-end;
}}
#gen-adv-g1 .pslot,
#gen-adv-g2 .pslot,
#gen-dis-g1 .pslot,
#gen-dis-g2 .pslot {{
  overflow: visible;
}}

/* ── Gen section admitted / rejected ── */
.pslot.gen-admitted {{
  outline: 3px solid #f59e0b;
  outline-offset: -2px;
  border-radius: 8px;
  background: rgba(253,224,71,0.35);
}}
.pslot.gen-rejected {{
  outline: 2px solid #fca5a5;
  outline-offset: -2px;
  border-radius: 8px;
  background: #f9fafb;
}}
.pslot.gen-rejected svg {{
  filter: grayscale(100%) opacity(0.35);
}}
/* Baby tooltip */
#baby-tooltip {{
  position: fixed;
  z-index: 9999;
  pointer-events: none;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  padding: 8px 10px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
  text-align: center;
  font-size: 0.75rem;
  color: #334155;
  min-width: 80px;
  transform: translate(-50%, -108%);
  transition: opacity 0.12s;
}}

/* ── Scenario tabs ── */
.stab {{
  padding: 0.55rem 1.1rem;
  border-radius: 10px;
  border: 2px solid #e2e8f0;
  background: #f8fafc;
  color: #64748b;
  font-family: inherit;
  font-size: 0.8rem;
  text-align: center;
  line-height: 1.4;
  cursor: pointer;
  transition: all 0.15s;
  min-width: 110px;
}}
.stab:hover {{ border-color: #6366f1; color: #4338ca; }}
.stab.active {{
  border-color: #6366f1;
  background: #eef2ff;
  color: #4338ca;
}}
.stab strong {{ font-size: 1rem; display: block; }}

/* ── Transition preset buttons ── */
.tp-preset {{
  padding: 4px 10px;
  border-radius: 999px;
  border: 1.5px solid #6ee7b7;
  background: white;
  color: #065f46;
  font-size: 0.75rem;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.12s;
}}
.tp-preset:hover {{ background: #d1fae5; border-color: #059669; }}
.tp-preset.active {{ background: #059669; color: white; border-color: #059669; }}

/* ── Evo chart legend buttons ── */
.evo-leg-btn {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
  border-radius: 999px;
  border: 2px solid #e2e8f0;
  background: white;
  font-family: inherit;
  font-size: 0.8rem;
  color: #334155;
  cursor: pointer;
  transition: all 0.15s;
  user-select: none;
}}
.evo-leg-btn:hover {{
  border-color: var(--c, #6366f1);
  background: #f8fafc;
}}
.evo-leg-btn.hidden {{
  opacity: 0.4;
  text-decoration: line-through;
  background: #f1f5f9;
}}

/* ── Scale-up section ── */
.n-slider-row {{
  display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;
  justify-content: center; margin-bottom: 1.4rem;
  font-size: 0.88rem; color: #475569;
}}
.n-slider-row input[type="range"] {{
  accent-color: #334155; width: 200px; cursor: pointer;
}}
.n-val {{
  font-size: 1.4rem; font-weight: 800; color: #1e293b;
  min-width: 60px; text-align: center;
}}
.mini-grid {{
  display: grid;
  gap: 2px;
  width: min(680px, 94vw);
  margin-bottom: 1rem;
}}
.mcell {{
  border-radius: 4px;
  overflow: hidden;
  opacity: 0;
  transform: scale(0.7);
  transition: opacity 0.18s ease, transform 0.18s ease;
}}
.mcell.shown {{
  opacity: 1;
  transform: scale(1);
}}
.mcell.admitted {{
  outline: 2px solid #f59e0b;
  outline-offset: -1px;
  background: rgba(245,158,11,0.15) !important;
}}
.mcell.not-admitted {{
  opacity: 0.2;
  transition: opacity 0.4s;
}}
/* ── Averaged runs progress bar ── */
.avg-progress-wrap {{
  width: min(660px,94vw);
  height: 6px;
  background: #e2e8f0;
  border-radius: 999px;
  overflow: hidden;
  margin-bottom: 0.75rem;
}}
.avg-progress-bar-inner {{
  height: 100%;
  width: 0%;
  background: linear-gradient(90deg, #059669, #0f766e);
  border-radius: 999px;
  transition: width 0.12s ease;
}}
.insight-box {{
  padding: 1rem 1.5rem;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  font-size: 0.875rem;
  color: #334155;
  max-width: 640px;
  text-align: center;
  line-height: 1.6;
  margin-top: 0.5rem;
}}
</style>
</head>
<body>

<!-- ═══════════ SECTION 1 — Circle ═══════════ -->
<div class="section" id="sec-circle">
<svg width="680" height="680" viewBox="0 0 700 700">
<defs>
  <clipPath id="clip23"><rect x="-18" y="-10" width="36" height="28"/></clipPath>
  <clipPath id="clip13"><rect x="-18" y="4"  width="36" height="14"/></clipPath>
</defs>
<circle cx="350" cy="350" r="266" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2.5"/>
<g id="center-default">
  <text x="350" y="332" text-anchor="middle" font-size="22" font-weight="700" fill="#334155">100 Students</text>
  <text x="350" y="357" text-anchor="middle" font-size="13" fill="#94a3b8">50 Advantaged · 50 Disadvantaged</text>
  <text x="350" y="382" text-anchor="middle" font-size="12" fill="#cbd5e1">hover a student</text>
</g>
{center_panel("A")}
{center_panel("D")}
{rim_svg}
</svg>

<div style="display:flex;gap:2rem;margin-top:0.4rem;font-size:13px;color:#475569;">
  <span><svg width="10" height="10" style="vertical-align:middle;margin-right:4px"><circle cx="5" cy="5" r="5" fill="{NAVY}"/></svg><strong>Advantaged (A)</strong> 50</span>
  <span><svg width="10" height="10" style="vertical-align:middle;margin-right:4px"><circle cx="5" cy="5" r="5" fill="{ORANGE}"/></svg><strong>Disadvantaged (D)</strong> 50</span>
  <span><svg width="10" height="10" style="vertical-align:middle;margin-right:4px"><circle cx="5" cy="5" r="5" fill="{PURPLE}"/></svg>x₁</span>
  <span><svg width="10" height="10" style="vertical-align:middle;margin-right:4px"><circle cx="5" cy="5" r="5" fill="{PINK}"/></svg>x₂</span>
</div>

<div class="scroll-hint">
  <span>scroll to simulate</span>
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <polyline points="6 9 12 15 18 9"/>
  </svg>
</div>
</div>


<!-- ═══════════ SECTION 2 — Advantaged ═══════════ -->
<div class="section fade-section" id="sec-adv">
  <div class="sec-eyebrow" style="background:{NAVY}"></div>
  <h2 class="sec-title">Advantaged Group <span style="color:{NAVY}">(A)</span></h2>
  <p class="sec-sub">Drawing x₁ and x₂ independently — each with <strong>P = 2/3</strong></p>

  <div class="pills">
    <div class="pill pill-hat">🎩 &nbsp;Hat = x₁ = 1 &nbsp;·&nbsp; P = 2/3</div>
    <div class="pill pill-shoe">👟 &nbsp;Sneakers = x₂ = 1 &nbsp;·&nbsp; P = 2/3</div>
  </div>

  <div class="speed-row">
    <span>Animation speed:</span>
    <input type="range" id="spd-adv" min="20" max="500" value="110"
           oninput="document.getElementById('lbl-adv').textContent=this.value+'ms'">
    <span class="speed-lbl" id="lbl-adv">110ms</span>
    <button class="replay-btn" onclick="replayAdv()">▶ Run</button>
  </div>

  <div class="pgrid" id="grid-adv"></div>
  <div class="counter-bar" id="cnt-adv">⏳ initializing…</div>
</div>


<!-- ═══════════ SECTION 3 — Disadvantaged ═══════════ -->
<div class="section fade-section" id="sec-dis">
  <div class="sec-eyebrow" style="background:{ORANGE}"></div>
  <h2 class="sec-title">Disadvantaged Group <span style="color:{ORANGE}">(D)</span></h2>
  <p class="sec-sub">Drawing x₁ and x₂ independently — each with <strong>P = 1/3</strong></p>

  <div class="pills">
    <div class="pill pill-hat">🎩 &nbsp;Hat = x₁ = 1 &nbsp;·&nbsp; P = 1/3</div>
    <div class="pill pill-shoe">👟 &nbsp;Sneakers = x₂ = 1 &nbsp;·&nbsp; P = 1/3</div>
  </div>

  <div class="speed-row">
    <span>Animation speed:</span>
    <input type="range" id="spd-dis" min="20" max="500" value="110"
           oninput="document.getElementById('lbl-dis').textContent=this.value+'ms'">
    <span class="speed-lbl" id="lbl-dis">110ms</span>
    <button class="replay-btn" onclick="replayDis()">▶ Run</button>
  </div>

  <div class="pgrid" id="grid-dis"></div>
  <div class="counter-bar" id="cnt-dis">⏳ initializing…</div>
</div>


<!-- ═══════════ SECTION 4 — All 100, rank by f, admit top 5/18 ═══════════ -->
<div class="section fade-section" id="sec-all" style="min-height:920px;">
  <div class="sec-eyebrow" style="background:#334155"></div>
  <h2 class="sec-title">Scenario 0 — Rank by f, Admit Top 5/18</h2>
  <p class="sec-sub">All 100 students · rank by f = x₁ ∧ x₂ · admit top <strong>⌈100 × 5/18⌉ = 28</strong></p>

  <div class="pills">
    <div class="pill pill-hat">🎩 &nbsp;Hat = x₁</div>
    <div class="pill pill-shoe">👟 &nbsp;Sneakers = x₂</div>
    <div class="pill" style="color:#059669;border-color:#059669;background:#f0fdf4;">🟩 &nbsp;f = 1 (both)</div>
    <div class="pill" style="color:#b45309;border-color:#f59e0b;background:#fffbeb;">⭐ &nbsp;Admitted</div>
  </div>

  <div class="speed-row">
    <span>Animation speed:</span>
    <input type="range" id="spd-all" min="10" max="300" value="60"
           oninput="document.getElementById('lbl-all').textContent=this.value+'ms'">
    <span class="speed-lbl" id="lbl-all">60ms</span>
    <button class="replay-btn" onclick="replayAll()">▶ Run</button>
  </div>

  <div class="pgrid" id="grid-all" style="width:min(680px,94vw);"></div>
  <div class="counter-bar" id="cnt-all" style="margin-top:0.75rem;">Press Run to start</div>
</div>


<!-- ═══════════ SECTION 5 — All Scenarios + Scale ═══════════ -->
<div class="section fade-section" id="sec-scale" style="min-height:1000px;">
  <div class="sec-eyebrow" style="background:#6366f1"></div>
  <h2 class="sec-title">Admission Scenarios — Scale Up</h2>
  <p class="sec-sub">Choose a decision rule · adjust N · press Run</p>

  <!-- Scenario selector -->
  <div id="scenario-tabs" style="display:flex;gap:0.5rem;flex-wrap:wrap;justify-content:center;margin-bottom:1.2rem;">
    <button class="stab active" data-s="0" onclick="selectScenario(0)">
      <strong>Scenario 1</strong><br><span>Rank by f = x₁∧x₂</span>
    </button>
    <button class="stab" data-s="1" onclick="selectScenario(1)">
      <strong>Scenario 2</strong><br><span>Only x₁, no group</span>
    </button>
    <button class="stab" data-s="2" onclick="selectScenario(2)">
      <strong>Scenario 3</strong><br><span>x₁ + group as proxy</span>
    </button>
    <button class="stab" data-s="3" onclick="selectScenario(3)">
      <strong>Scenario 4</strong><br><span>x₂ for D only</span>
    </button>
  </div>

  <!-- Scenario description -->
  <div id="scenario-desc" style="
    max-width:620px;text-align:center;margin-bottom:1.2rem;
    padding:0.75rem 1.2rem;border-radius:10px;
    background:#f8fafc;border:1px solid #e2e8f0;
    font-size:0.85rem;color:#475569;line-height:1.6;">
  </div>

  <div class="n-slider-row">
    <span>N =</span>
    <span class="n-val" id="n-val-lbl">100</span>
    <input type="range" id="n-slider" min="100" max="2000" step="50" value="100"
           oninput="onNSlider(this.value)">
    <span style="color:#94a3b8;font-size:0.8rem">100 ↔ 2 000</span>
  </div>

  <div class="speed-row">
    <span>Animation speed:</span>
    <input type="range" id="spd-scale" min="1" max="100" value="15"
           oninput="document.getElementById('lbl-scale').textContent=this.value+'ms'">
    <span class="speed-lbl" id="lbl-scale">15ms</span>
    <button class="replay-btn" onclick="replayScale()">▶ Run</button>
  </div>

  <div class="mini-grid" id="mgrid"></div>
  <div class="counter-bar" id="cnt-scale" style="margin-top:0.5rem;">Select a scenario and press Run</div>
  <div class="insight-box" id="insight-scale" style="display:none;margin-top:0.75rem;"></div>
</div>


<!-- ═══════════ SECTION 6 — Evolutionary Model (Scenario 1) ═══════════ -->
<div class="section fade-section" id="sec-gen" style="min-height:1600px;">
  <div class="sec-eyebrow" style="background:#0f766e"></div>
  <h2 class="sec-title">Part 2 — Evolutionary Model</h2>
  <p class="sec-sub">Choose admission rule · Gen 1 → Gen 2 · watch group membership evolve</p>

  <!-- Shared scenario selector (also drives the long-run chart) -->
  <div style="display:flex;gap:0.5rem;flex-wrap:wrap;justify-content:center;margin-bottom:1.2rem;">
    <button class="stab active" id="evo-stab-0" onclick="selectEvoScenario(0)">
      <strong>Scenario 1</strong><br><span>Rank by f = x₁∧x₂</span>
    </button>
    <button class="stab" id="evo-stab-1" onclick="selectEvoScenario(1)">
      <strong>Scenario 2</strong><br><span>Only x₁, no group</span>
    </button>
    <button class="stab" id="evo-stab-2" onclick="selectEvoScenario(2)">
      <strong>Scenario 3</strong><br><span>x₁ + group as proxy</span>
    </button>
    <button class="stab" id="evo-stab-3" onclick="selectEvoScenario(3)">
      <strong>Scenario 4</strong><br><span>x₂ for D only</span>
    </button>
  </div>

  <!-- Transition probability sliders -->
  <div style="
    max-width:620px;width:100%;padding:1rem 1.4rem;border-radius:12px;
    background:#f0fdf4;border:1px solid #6ee7b7;margin-bottom:1.4rem;">
    <div style="font-size:0.82rem;font-weight:700;color:#065f46;margin-bottom:0.6rem;">
      Transition probabilities &nbsp;<span style="font-weight:400;color:#6b7280">(P that child is <strong>Advantaged</strong>)</span>
    </div>
    <!-- Preset buttons -->
    <div style="display:flex;gap:0.4rem;flex-wrap:wrap;margin-bottom:0.9rem;">
      <button class="tp-preset active" onclick="applyPreset(0)">🏠 Ours</button>
      <button class="tp-preset" onclick="applyPreset(1)">📋 From PDF</button>
      <button class="tp-preset" onclick="applyPreset(2)">🚧 Locked in</button>
      <button class="tp-preset" onclick="applyPreset(3)">🚀 Strong mobility</button>
      <button class="tp-preset" onclick="applyPreset(4)">🪟 Glass ceiling</button>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.75rem 2rem;">

      <div>
        <label style="font-size:0.78rem;color:#065f46;">
          ⭐ Admitted <strong style="color:{NAVY}">A</strong> → child A:
          <strong id="lbl-pAA">90%</strong>
        </label><br>
        <input type="range" min="0" max="1" step="0.01" value="0.90" id="sl-pAA"
               style="width:100%;accent-color:#1e3a5f;"
               oninput="document.getElementById('lbl-pAA').textContent=Math.round(this.value*100)+'%';updateTP()">
      </div>

      <div>
        <label style="font-size:0.78rem;color:#065f46;">
          ⭐ Admitted <strong style="color:{ORANGE}">D</strong> → child A:
          <strong id="lbl-pDA">60%</strong>
        </label><br>
        <input type="range" min="0" max="1" step="0.01" value="0.60" id="sl-pDA"
               style="width:100%;accent-color:{ORANGE};"
               oninput="document.getElementById('lbl-pDA').textContent=Math.round(this.value*100)+'%';updateTP()">
      </div>

      <div>
        <label style="font-size:0.78rem;color:#065f46;">
          ❌ Not admitted <strong style="color:{NAVY}">A</strong> → child A:
          <strong id="lbl-pAN">30%</strong>
        </label><br>
        <input type="range" min="0" max="1" step="0.01" value="0.30" id="sl-pAN"
               style="width:100%;accent-color:#1e3a5f;"
               oninput="document.getElementById('lbl-pAN').textContent=Math.round(this.value*100)+'%';updateTP()">
      </div>

      <div>
        <label style="font-size:0.78rem;color:#065f46;">
          ❌ Not admitted <strong style="color:{ORANGE}">D</strong> → child A:
          <strong id="lbl-pDN">10%</strong>
        </label><br>
        <input type="range" min="0" max="1" step="0.01" value="0.10" id="sl-pDN"
               style="width:100%;accent-color:{ORANGE};"
               oninput="document.getElementById('lbl-pDN').textContent=Math.round(this.value*100)+'%';updateTP()">
      </div>

    </div>
    <!-- Preset description -->
    <div id="tp-preset-desc" style="
      display:none;margin-top:0.6rem;padding:0.5rem 0.75rem;
      background:white;border-radius:7px;border:1px solid #a7f3d0;
      font-size:0.75rem;color:#047857;line-height:1.5;">
    </div>
  </div>

  <!-- Controls -->
  <div class="speed-row" style="margin-bottom:1.2rem;">
    <span>Animation speed:</span>
    <input type="range" id="spd-gen" min="20" max="400" value="80"
           oninput="document.getElementById('lbl-gen').textContent=this.value+'ms'">
    <span class="speed-lbl" id="lbl-gen">80ms</span>
    <button class="replay-btn" onclick="runGen()">▶ Run</button>
  </div>

  <!-- Advantaged block -->
  <div style="width:min(680px,94vw);">
    <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.5rem;">
      <span style="font-size:0.85rem;font-weight:700;color:{NAVY};">Advantaged (A) — Generation 1</span>
      <span id="gen-adv-stat" style="font-size:0.8rem;color:#64748b;"></span>
    </div>
    <div class="pgrid" id="gen-adv-g1" style="width:100%;margin-bottom:0.3rem;"></div>

    <div id="gen-adv-arrow" style="display:none;text-align:center;font-size:1.5rem;
         color:#94a3b8;margin:0.4rem 0;animation:bounce 1.5s infinite;">↓</div>

    <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.5rem;">
      <span id="gen-adv-g2-lbl" style="font-size:0.85rem;font-weight:700;color:#475569;display:none;">
        Their children — Generation 2
      </span>
      <span id="gen-adv-g2-stat" style="font-size:0.8rem;color:#64748b;"></span>
    </div>
    <div class="pgrid" id="gen-adv-g2" style="width:100%;margin-bottom:1.2rem;"></div>
  </div>

  <!-- Disadvantaged block -->
  <div style="width:min(680px,94vw);">
    <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.5rem;">
      <span style="font-size:0.85rem;font-weight:700;color:{ORANGE};">Disadvantaged (D) — Generation 1</span>
      <span id="gen-dis-stat" style="font-size:0.8rem;color:#64748b;"></span>
    </div>
    <div class="pgrid" id="gen-dis-g1" style="width:100%;margin-bottom:0.3rem;"></div>

    <div id="gen-dis-arrow" style="display:none;text-align:center;font-size:1.5rem;
         color:#94a3b8;margin:0.4rem 0;animation:bounce 1.5s infinite;">↓</div>

    <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.5rem;">
      <span id="gen-dis-g2-lbl" style="font-size:0.85rem;font-weight:700;color:#475569;display:none;">
        Their children — Generation 2
      </span>
      <span id="gen-dis-g2-stat" style="font-size:0.8rem;color:#64748b;"></span>
    </div>
    <div class="pgrid" id="gen-dis-g2" style="width:100%;"></div>
  </div>

</div>


<!-- ═══════════ SECTION 7 — Long-run Evolution ═══════════ -->
<div class="section fade-section" id="sec-evo" style="min-height:820px;">
  <div class="sec-eyebrow" style="background:#0f766e"></div>
  <h2 class="sec-title">Long-run Evolution — <span id="evo-scenario-title">Scenario 1</span></h2>
  <p class="sec-sub">Run up to 1 000 generations at full speed · watch social mobility unfold</p>
  <div id="evo-tp-summary" style="
    font-size:0.75rem;color:#059669;font-weight:600;
    padding:4px 12px;border-radius:999px;background:#f0fdf4;
    border:1px solid #6ee7b7;margin-bottom:0.8rem;">
    Using: A→A=90% · D→A=60% · ¬A→A=30% · ¬D→A=10%
  </div>

  <div style="display:flex;gap:2rem;flex-wrap:wrap;justify-content:center;align-items:center;margin-bottom:1.2rem;">
    <div class="n-slider-row" style="margin-bottom:0;">
      <span>Generations:</span>
      <span class="n-val" id="evo-gen-lbl" style="font-size:1.2rem;">200</span>
      <input type="range" id="evo-gen-slider" min="10" max="1000" step="10" value="200"
             oninput="document.getElementById('evo-gen-lbl').textContent=this.value">
    </div>
    <div class="speed-row" style="margin-bottom:0;">
      <span>Speed:</span>
      <input type="range" id="evo-spd" min="1" max="100" value="8"
             oninput="document.getElementById('evo-spd-lbl').textContent=this.value+'ms'">
      <span class="speed-lbl" id="evo-spd-lbl">8ms</span>
    </div>
    <button class="replay-btn" onclick="runEvo()">▶ Run</button>
  </div>

  <!-- Live counters -->
  <div id="evo-status" style="
    font-size:0.85rem;color:#475569;margin-bottom:0.8rem;
    display:flex;gap:1.5rem;flex-wrap:wrap;justify-content:center;min-height:22px;">
  </div>

  <!-- Canvas chart -->
  <canvas id="evo-canvas" width="660" height="260"
    style="border-radius:12px;border:1px solid #e2e8f0;background:#f8fafc;
           max-width:min(660px,94vw);"></canvas>

  <!-- Clickable legend (Plotly-style) -->
  <div style="display:flex;gap:0.6rem;flex-wrap:wrap;justify-content:center;margin-top:0.75rem;">
    <button id="evo-leg-fracD"  class="evo-leg-btn" onclick="toggleEvoLine('fracD')"
            style="--c:{ORANGE};">
      <svg width="22" height="8"><line x1="0" y1="4" x2="22" y2="4" stroke="{ORANGE}" stroke-width="2.5"/></svg>
      Frac D in population
    </button>
    <button id="evo-leg-equity" class="evo-leg-btn" onclick="toggleEvoLine('equity')"
            style="--c:#059669;">
      <svg width="22" height="8"><line x1="0" y1="4" x2="22" y2="4" stroke="#059669" stroke-width="2.5"/></svg>
      Equity (frac D admitted)
    </button>
    <button id="evo-leg-eff"    class="evo-leg-btn" onclick="toggleEvoLine('eff')"
            style="--c:{PURPLE};">
      <svg width="22" height="8"><line x1="0" y1="4" x2="22" y2="4" stroke="{PURPLE}" stroke-width="2.5"/></svg>
      Efficiency (avg f)
    </button>
  </div>
</div>


<!-- ═══════════ SECTION 8 — Averaged Long-run ═══════════ -->
<div class="section fade-section" id="sec-avg" style="min-height:860px;">
  <div class="sec-eyebrow" style="background:#0f766e"></div>
  <h2 class="sec-title">Averaged Long-run — <span id="avg-scenario-title">Scenario 1</span></h2>
  <p class="sec-sub">Run <em>R</em> independent simulations · average the results · watch noise collapse</p>

  <div style="max-width:620px;padding:0.75rem 1.2rem;border-radius:10px;
              background:#f0fdf4;border:1px solid #6ee7b7;
              font-size:0.82rem;color:#065f46;line-height:1.6;
              margin-bottom:1.2rem;text-align:center;">
    Each run is a fully independent simulation. Averaging over <em>R</em> runs cancels
    out random noise and reveals the <strong>expected long-run behavior</strong> —
    the law of large numbers at work.
  </div>

  <!-- Scenario selector -->
  <div style="display:flex;gap:0.5rem;flex-wrap:wrap;justify-content:center;margin-bottom:1.2rem;">
    <button class="stab active" id="avg-stab-0" onclick="selectAvgScenario(0)">
      <strong>Scenario 1</strong><br><span>Rank by f = x₁∧x₂</span>
    </button>
    <button class="stab" id="avg-stab-1" onclick="selectAvgScenario(1)">
      <strong>Scenario 2</strong><br><span>Only x₁, no group</span>
    </button>
    <button class="stab" id="avg-stab-2" onclick="selectAvgScenario(2)">
      <strong>Scenario 3</strong><br><span>x₁ + group as proxy</span>
    </button>
    <button class="stab" id="avg-stab-3" onclick="selectAvgScenario(3)">
      <strong>Scenario 4</strong><br><span>x₂ for D only</span>
    </button>
  </div>

  <!-- Sliders: runs + generations -->
  <div style="display:flex;gap:2rem;flex-wrap:wrap;justify-content:center;align-items:center;margin-bottom:1.2rem;">
    <div class="n-slider-row" style="margin-bottom:0;">
      <span>Runs (R):</span>
      <span class="n-val" id="avg-runs-lbl" style="font-size:1.2rem;">50</span>
      <input type="range" id="avg-runs-slider" min="1" max="200" step="1" value="50"
             oninput="document.getElementById('avg-runs-lbl').textContent=this.value">
    </div>
    <div class="n-slider-row" style="margin-bottom:0;">
      <span>Generations:</span>
      <span class="n-val" id="avg-gen-lbl" style="font-size:1.2rem;">200</span>
      <input type="range" id="avg-gen-slider" min="10" max="1000" step="10" value="200"
             oninput="document.getElementById('avg-gen-lbl').textContent=this.value">
    </div>
    <button class="replay-btn" onclick="runAvgEvo()">▶ Run</button>
  </div>

  <!-- Progress bar -->
  <div class="avg-progress-wrap">
    <div class="avg-progress-bar-inner" id="avg-progress-bar"></div>
  </div>

  <!-- Status line -->
  <div id="avg-status" style="font-size:0.82rem;color:#475569;margin-bottom:0.8rem;
       display:flex;gap:1.5rem;flex-wrap:wrap;justify-content:center;min-height:20px;"></div>

  <!-- Canvas chart -->
  <canvas id="avg-canvas" width="660" height="260"
    style="border-radius:12px;border:1px solid #e2e8f0;background:#f8fafc;
           max-width:min(660px,94vw);"></canvas>

  <!-- Clickable legend -->
  <div style="display:flex;gap:0.6rem;flex-wrap:wrap;justify-content:center;margin-top:0.75rem;">
    <button id="avg-leg-fracD"  class="evo-leg-btn" onclick="toggleAvgLine('fracD')"
            style="--c:{ORANGE};">
      <svg width="22" height="8"><line x1="0" y1="4" x2="22" y2="4" stroke="{ORANGE}" stroke-width="2.5"/></svg>
      Frac D in population
    </button>
    <button id="avg-leg-equity" class="evo-leg-btn" onclick="toggleAvgLine('equity')"
            style="--c:#059669;">
      <svg width="22" height="8"><line x1="0" y1="4" x2="22" y2="4" stroke="#059669" stroke-width="2.5"/></svg>
      Equity (frac D admitted)
    </button>
    <button id="avg-leg-eff"    class="evo-leg-btn" onclick="toggleAvgLine('eff')"
            style="--c:{PURPLE};">
      <svg width="22" height="8"><line x1="0" y1="4" x2="22" y2="4" stroke="{PURPLE}" stroke-width="2.5"/></svg>
      Efficiency (avg f)
    </button>
  </div>
</div>


<script>
/* ── Data — generated fresh on every replay ──── */
function genPop(n, pX1, pX2) {{
  var out = [];
  for (var i = 0; i < n; i++) {{
    out.push({{ x1: Math.random() < pX1 ? 1 : 0,
               x2: Math.random() < pX2 ? 1 : 0 }});
  }}
  return out;
}}

/* ── Person SVG builder ───────────────────────── */
function makePerson(group, x1, x2, small) {{
  var bc = group === 'A' ? '{NAVY}' : '{ORANGE}';
  var w = small ? 42 : 52;
  var h = small ? 60 : 72;
  var hat = '';
  if (x1) {{
    hat = '<rect x="-6.5" y="-40" width="13" height="16" rx="2.5" fill="{PURPLE}"/>'
        + '<rect x="-9.5" y="-26" width="19" height="4" rx="1.5" fill="{PURPLE}"/>'
        + '<rect x="-6.5" y="-28" width="13" height="2.5" fill="#5b21b6"/>';
  }}
  var shoes = '';
  if (x2) {{
    shoes = '<ellipse cx="-5" cy="18" rx="6" ry="2.5" fill="{COFFEE}"/>'
          + '<ellipse cx="5"  cy="18" rx="6" ry="2.5" fill="{COFFEE}"/>';
  }}
  return '<svg viewBox="-16 -46 32 68" width="' + w + '" height="' + h + '">'
       + hat
       + '<circle cx="0" cy="-12" r="9.5" fill="' + bc + '"/>'
       + '<path d="M-10.5,-3.5 Q-10.5,14.5 0,14.5 Q10.5,14.5 10.5,-3.5 Q10.5,-9.5 0,-9.5 Q-10.5,-9.5 -10.5,-3.5 Z" fill="' + bc + '"/>'
       + shoes
       + '</svg>';
}}

/* ── Animation engine ─────────────────────────── */
var timers = [];

function runGrid(gridId, cntId, data, group, speed) {{
  timers.forEach(function(t) {{ clearTimeout(t); }});
  timers = [];
  var grid = document.getElementById(gridId);
  grid.innerHTML = '';
  /* reset counter */
  document.getElementById(cntId).innerHTML = '&#8987; initializing\u2026';

  /* Build all slots invisible */
  var slots = data.map(function(p) {{
    var d = document.createElement('div');
    d.className = 'pslot';
    d.innerHTML = makePerson(group, p.x1, p.x2);
    grid.appendChild(d);
    return d;
  }});

  /* Stagger reveal */
  var shown = 0;
  data.forEach(function(p, i) {{
    var t = setTimeout(function() {{
      slots[i].classList.add('shown');
      shown++;
      /* Update running counter */
      var nx1 = 0, nx2 = 0, nf = 0;
      for (var k = 0; k <= i; k++) {{
        if (data[k].x1) nx1++;
        if (data[k].x2) nx2++;
        if (data[k].x1 && data[k].x2) nf++;
      }}
      var el = document.getElementById(cntId);
      if (shown === data.length) {{
        el.innerHTML =
          '<span class="cstat cx1">🎩 x\u2081=1: ' + nx1 + '/50 (' + Math.round(nx1/50*100) + '%)</span>'
        + '<span class="cstat cx2">👟 x\u2082=1: ' + nx2 + '/50 (' + Math.round(nx2/50*100) + '%)</span>'
        + '<span class="cstat cf">\u2713 f=1 (both): ' + nf + '/50 (' + Math.round(nf/50*100) + '%)</span>';
        /* Highlight f=1 slots with green border */
        slots.forEach(function(sl, k) {{
          if (data[k].x1 && data[k].x2) {{
            sl.style.outline = '3px solid {GREEN}';
            sl.style.outlineOffset = '-2px';
            sl.style.borderRadius = '8px';
            sl.style.backgroundColor = 'rgba(5,150,105,0.08)';
          }}
        }});
      }} else {{
        el.innerHTML =
          '<span class="cstat cx1">🎩 x\u2081=1: ' + nx1 + '&hellip;</span>'
        + '<span class="cstat cx2">👟 x\u2082=1: ' + nx2 + '&hellip;</span>';
      }}
    }}, i * speed);
    timers.push(t);
  }});
}}

function replayAdv() {{
  var spd = parseInt(document.getElementById('spd-adv').value);
  runGrid('grid-adv', 'cnt-adv', genPop(50, 2/3, 2/3), 'A', spd);
}}
function replayDis() {{
  var spd = parseInt(document.getElementById('spd-dis').value);
  runGrid('grid-dis', 'cnt-dis', genPop(50, 1/3, 1/3), 'D', spd);
}}

/* ── Combined section (Scenario 0) ───────────── */
var allTimers = [];

function runAll(speed) {{
  allTimers.forEach(function(t) {{ clearTimeout(t); }});
  allTimers = [];

  var grid = document.getElementById('grid-all');
  grid.innerHTML = '';
  document.getElementById('cnt-all').innerHTML = '&#8987; initializing\u2026';

  /* Generate 100 people: 50 A + 50 D */
  var raw = [];
  var ap = genPop(50, 2/3, 2/3);
  var dp = genPop(50, 1/3, 1/3);
  ap.forEach(function(p) {{ raw.push({{x1:p.x1, x2:p.x2, group:'A', f: p.x1&&p.x2?1:0}}); }});
  dp.forEach(function(p) {{ raw.push({{x1:p.x1, x2:p.x2, group:'D', f: p.x1&&p.x2?1:0}}); }});

  /* Build slots */
  var slots = raw.map(function(p) {{
    var d = document.createElement('div');
    d.className = 'pslot pslot-sm';
    d.innerHTML = makePerson(p.group, p.x1, p.x2, true);
    grid.appendChild(d);
    return d;
  }});

  var shown = 0;
  raw.forEach(function(p, i) {{
    var t = setTimeout(function() {{
      slots[i].classList.add('shown');
      shown++;

      /* Live counter while appearing */
      if (shown < raw.length) {{
        var nx1=0, nx2=0;
        for (var k=0; k<=i; k++) {{ if(raw[k].x1) nx1++; if(raw[k].x2) nx2++; }}
        document.getElementById('cnt-all').innerHTML =
          '<span class="cstat cx1">🎩 x\u2081=1: '+nx1+'</span>'
         +'<span class="cstat cx2">👟 x\u2082=1: '+nx2+'</span>';
        return;
      }}

      /* All shown — Phase 1: highlight f=1 in green */
      var nf = raw.filter(function(d){{return d.f;}}).length;
      document.getElementById('cnt-all').innerHTML =
        '<span class="cstat cf">\u2713 Students with f=1: '+nf+'/100 \u2014 ranking\u2026</span>';

      slots.forEach(function(sl, k) {{
        if (raw[k].f) {{
          sl.style.outline = '3px solid {GREEN}';
          sl.style.outlineOffset = '-2px';
          sl.style.borderRadius = '8px';
          sl.style.background = 'rgba(5,150,105,0.08)';
        }}
      }});

      /* Phase 2 after 1.4s: apply admission (gold = in, dim = out) */
      var t2 = setTimeout(function() {{
        var K = Math.round(100 * 5/18);  /* 28 */

        /* Shuffle then sort by f desc for random tie-breaking */
        var indexed = raw.map(function(d,i){{ return {{d:d, idx:i}}; }});
        indexed.sort(function(){{ return Math.random()-0.5; }});
        indexed.sort(function(a,b){{ return b.d.f - a.d.f; }});
        var admSet = {{}};
        indexed.slice(0, K).forEach(function(e){{ admSet[e.idx] = true; }});

        /* Reset green highlights, apply admitted / not-admitted */
        slots.forEach(function(sl, k) {{
          sl.style.outline = '';
          sl.style.background = '';
          sl.style.borderRadius = '';
          sl.classList.remove('shown');   /* re-trigger for smooth transition */
          sl.classList.add('shown');
          if (admSet[k]) {{
            sl.classList.add('admitted');
          }} else {{
            sl.classList.add('not-admitted');
          }}
        }});

        var nA = 0, nD = 0, nAdmF = 0;
        for (var k=0; k<raw.length; k++) {{
          if (!admSet[k]) continue;
          if (raw[k].group==='A') nA++;
          else nD++;
          if (raw[k].f) nAdmF++;
        }}
        var eq = Math.round(nD/K*100);
        var eff = Math.round(nAdmF/K*100);

        document.getElementById('cnt-all').innerHTML =
          '<span>Admitted: <strong>'+K+'</strong>/100</span>'
         +'<span style="color:{NAVY};font-weight:700">\u25a0 A: '+nA+'</span>'
         +'<span style="color:{ORANGE};font-weight:700">\u25a0 D: '+nD+'</span>'
         +'<span class="cstat cf">Efficiency (avg f): '+eff+'%</span>'
         +'<span class="cstat cx1">Equity (frac D): '+eq+'%</span>';
      }}, 1400);
      allTimers.push(t2);
    }}, i * speed);
    allTimers.push(t);
  }});
}}

function replayAll() {{
  var spd = parseInt(document.getElementById('spd-all').value);
  runAll(spd);
}}

/* ── Evolutionary section ────────────────────── */
var genTimers = [];

/* ── Person SVG with pacifier shape ── */
function makePersonGen(group, x1, x2, isBaby) {{
  var bc = group === 'A' ? '{NAVY}' : '{ORANGE}';
  /* baby uses taller viewBox to fit pacifier below body */
  var vb = isBaby ? '-16 -46 32 76' : '-16 -46 32 68';
  var w = 52, h = isBaby ? 80 : 72;

  var hat = '';
  if (!isBaby && x1) {{
    hat = '<rect x="-6.5" y="-40" width="13" height="16" rx="2.5" fill="{PURPLE}"/>'
        + '<rect x="-9.5" y="-26" width="19" height="4" rx="1.5" fill="{PURPLE}"/>'
        + '<rect x="-6.5" y="-28" width="13" height="2.5" fill="#5b21b6"/>';
  }}
  var shoes = '';
  if (!isBaby && x2) {{
    shoes = '<ellipse cx="-5" cy="18" rx="6" ry="2.5" fill="{COFFEE}"/>'
          + '<ellipse cx="5"  cy="18" rx="6" ry="2.5" fill="{COFFEE}"/>';
  }}

  /* Mamila (baby bottle) */
  var pacifier = '';
  if (isBaby) {{
    pacifier =
      /* nipple */
      '<ellipse cx="0" cy="14" rx="2.2" ry="3" fill="#f59e0b"/>'
      /* collar ring */
    + '<rect x="-4" y="16.5" width="8" height="2.5" rx="1.2" fill="#e2a800"/>'
      /* bottle body outline */
    + '<rect x="-5.5" y="19" width="11" height="11" rx="2.5" fill="#fde68a" stroke="#f59e0b" stroke-width="1.2"/>'
      /* milk fill inside */
    + '<rect x="-4.2" y="20" width="8.4" height="9" rx="1.8" fill="white" opacity="0.85"/>'
      /* measurement lines */
    + '<line x1="-2.5" y1="23" x2="2.5" y2="23" stroke="#f59e0b" stroke-width="0.8" opacity="0.6"/>'
    + '<line x1="-2.5" y1="26" x2="2.5" y2="26" stroke="#f59e0b" stroke-width="0.8" opacity="0.6"/>';
  }}

  return '<svg viewBox="' + vb + '" width="' + w + '" height="' + h + '">'
       + hat
       + '<circle cx="0" cy="-12" r="9.5" fill="' + bc + '"/>'
       + '<path d="M-10.5,-3.5 Q-10.5,14.5 0,14.5 Q10.5,14.5 10.5,-3.5 Q10.5,-9.5 0,-9.5 Q-10.5,-9.5 -10.5,-3.5 Z" fill="' + bc + '"/>'
       + shoes + pacifier
       + '</svg>';
}}

/* ── Transition probabilities (updated by sliders) ── */
var TP = {{ pAA: 0.90, pDA: 0.60, pAN: 0.30, pDN: 0.10 }};

var TP_PRESETS = [
  {{
    name: 'Ours',
    desc: 'Our model (Group D notebook): admitted A→90% A, admitted D→60% A, rejected A→30% A, rejected D→10% A.',
    pAA: 0.90, pDA: 0.60, pAN: 0.30, pDN: 0.10
  }},
  {{
    name: 'From PDF',
    desc: 'Assignment example (p₁=½, p₂=⅓): admitted A always stays A, admitted D has 50% chance, rejected D stays D, rejected A has 1/3 chance.',
    pAA: 1.0, pDA: 0.50, pAN: 0.333, pDN: 0.0
  }},
  {{
    name: 'Locked in',
    desc: 'Groups are completely rigid. Admitted A stays A, rejected A stays A too. D always stays D. Zero social mobility.',
    pAA: 1.0, pDA: 0.0, pAN: 1.0, pDN: 0.0
  }},
  {{
    name: 'Strong mobility',
    desc: 'Admission = guaranteed A for everyone regardless of group. Rejection still gives 50/50 chance. Fastest convergence.',
    pAA: 1.0, pDA: 1.0, pAN: 0.5, pDN: 0.5
  }},
  {{
    name: 'Glass ceiling',
    desc: 'Admitted D has only 10% chance of becoming A. The structural gap barely closes even after 1000 generations.',
    pAA: 1.0, pDA: 0.1, pAN: 0.333, pDN: 0.0
  }}
];

function applyPreset(idx) {{
  var p = TP_PRESETS[idx];
  document.querySelectorAll('.tp-preset').forEach(function(b,i) {{
    b.classList.toggle('active', i === idx);
  }});
  var map = [['pAA','sl-pAA','lbl-pAA'], ['pDA','sl-pDA','lbl-pDA'],
             ['pAN','sl-pAN','lbl-pAN'], ['pDN','sl-pDN','lbl-pDN']];
  map.forEach(function(m) {{
    document.getElementById(m[1]).value = p[m[0]];
    document.getElementById(m[2]).textContent = Math.round(p[m[0]]*100) + '%';
  }});
  updateTP();
  /* show preset description */
  var desc = document.getElementById('tp-preset-desc');
  if (desc) {{ desc.textContent = p.desc; desc.style.display = 'block'; }}
}}

function updateTP() {{
  TP.pAA = parseFloat(document.getElementById('sl-pAA').value);
  TP.pDA = parseFloat(document.getElementById('sl-pDA').value);
  TP.pAN = parseFloat(document.getElementById('sl-pAN').value);
  TP.pDN = parseFloat(document.getElementById('sl-pDN').value);
  /* clear active preset on manual change */
  var map = [['pAA','sl-pAA'],['pDA','sl-pDA'],['pAN','sl-pAN'],['pDN','sl-pDN']];
  /* update long-run subtitle */
  var sub = document.getElementById('evo-tp-summary');
  if (sub) {{
    sub.textContent = 'Using: A\u2192A='+(TP.pAA*100).toFixed(0)+'%'
      +' · D\u2192A='+(TP.pDA*100).toFixed(0)+'%'
      +' · \u00acA\u2192A='+(TP.pAN*100).toFixed(0)+'%'
      +' · \u00acD\u2192A='+(TP.pDN*100).toFixed(0)+'%';
  }}
}}

function childGroup(parentGroup, admitted) {{
  if (admitted) {{
    return Math.random() < (parentGroup === 'A' ? TP.pAA : TP.pDA) ? 'A' : 'D';
  }} else {{
    return Math.random() < (parentGroup === 'A' ? TP.pAN : TP.pDN) ? 'A' : 'D';
  }}
}}

/* ── Tooltip ── */
var tooltip = null;
function ensureTooltip() {{
  if (!tooltip) {{
    tooltip = document.createElement('div');
    tooltip.id = 'baby-tooltip';
    tooltip.style.display = 'none';
    document.body.appendChild(tooltip);
  }}
}}

function showBabyTooltip(slot, child) {{
  ensureTooltip();
  var rect = slot.getBoundingClientRect();
  var gc = child.group === 'A' ? '{NAVY}' : '{ORANGE}';
  tooltip.innerHTML =
    makePersonGen(child.group, child.x1, child.x2, true)
    + '<div style="font-weight:700;color:'+gc+';margin-top:2px;">Group '+child.group+'</div>';
  tooltip.style.display = 'block';
  tooltip.style.left = (rect.left + rect.width/2) + 'px';
  tooltip.style.top  = (rect.top + window.scrollY) + 'px';
}}

function hideTooltip() {{
  if (tooltip) tooltip.style.display = 'none';
}}

/* ── Main gen runner ── */
function runGen() {{
  genTimers.forEach(function(t) {{ clearTimeout(t); }});
  genTimers = [];

  var spd = parseInt(document.getElementById('spd-gen').value);

  /* Generate 50 A + 50 D */
  var advPop = genPop(50, 2/3, 2/3).map(function(p) {{
    return {{ group:'A', x1:p.x1, x2:p.x2, f:p.x1&&p.x2?1:0, admitted:0 }};
  }});
  var disPop = genPop(50, 1/3, 1/3).map(function(p) {{
    return {{ group:'D', x1:p.x1, x2:p.x2, f:p.x1&&p.x2?1:0, admitted:0 }};
  }});

  /* Admission: Scenario 1 (rank by f) on all 100 */
  var all100 = advPop.concat(disPop);
  admitEvo(all100);

  /* Pre-generate ALL children up front so hover can show them */
  function makeChildren(parents) {{
    return parents.map(function(p) {{
      var cg = childGroup(p.group, p.admitted);
      var cp = cg === 'A' ? 2/3 : 1/3;
      var cx1 = Math.random() < cp ? 1 : 0;
      var cx2 = Math.random() < cp ? 1 : 0;
      return {{ group:cg, x1:cx1, x2:cx2, f:cx1&&cx2?1:0, admitted:0 }};
    }});
  }}
  var advKids = makeChildren(advPop);
  var disKids = makeChildren(disPop);

  /* --- Animate Gen1 grid with hover → show baby tooltip --- */
  function animateGroup(pop, kids, gridId, statId, delay) {{
    var grid = document.getElementById(gridId);
    grid.innerHTML = '';
    document.getElementById(statId).textContent = '';

    var slots = pop.map(function(p, i) {{
      var d = document.createElement('div');
      d.className = 'pslot';
      d.style.cursor = 'pointer';
      d.innerHTML = makePersonGen(p.group, p.x1, p.x2, false);
      /* hover shows the baby tooltip */
      d.addEventListener('mouseenter', function() {{ showBabyTooltip(d, kids[i]); }});
      d.addEventListener('mouseleave', hideTooltip);
      grid.appendChild(d);
      return d;
    }});

    var shown = 0;
    pop.forEach(function(p, i) {{
      var t = setTimeout(function() {{
        slots[i].classList.add('shown');
        shown++;
        if (shown === pop.length) {{
          pop.forEach(function(pp, k) {{
            slots[k].classList.add(pp.admitted ? 'gen-admitted' : 'gen-rejected');
          }});
          var nAdm = pop.filter(function(pp) {{ return pp.admitted; }}).length;
          document.getElementById(statId).innerHTML =
            '<span style="color:#f59e0b;font-weight:700">\u2b50 '+nAdm+' admitted</span>'
           +'&nbsp;&nbsp;<span style="color:#ef4444;font-weight:700">\u274c '+(pop.length-nAdm)+' rejected</span>'
           +'&nbsp;&nbsp;<span style="color:#94a3b8;font-size:0.75rem">(hover a person to see their child)</span>';
        }}
      }}, delay + i * spd);
      genTimers.push(t);
    }});
    return delay + pop.length * spd;
  }}

  /* --- Animate Gen2 (children) grid --- */
  function animateChildren(kids, gridId, statId, lblId, arrowId, delay) {{
    var t0 = setTimeout(function() {{
      document.getElementById(arrowId).style.display = 'block';
      document.getElementById(lblId).style.display   = 'flex';
    }}, delay - 200);
    genTimers.push(t0);

    var grid = document.getElementById(gridId);
    grid.innerHTML = '';
    document.getElementById(statId).textContent = '';

    var slots = kids.map(function(c) {{
      var d = document.createElement('div');
      d.className = 'pslot';
      d.innerHTML = makePersonGen(c.group, c.x1, c.x2, true);
      grid.appendChild(d);
      return d;
    }});

    kids.forEach(function(c, i) {{
      var t = setTimeout(function() {{
        slots[i].classList.add('shown');
        if (i === kids.length - 1) {{
          var nA = kids.filter(function(cc) {{ return cc.group==='A'; }}).length;
          var nD = kids.length - nA;
          document.getElementById(statId).innerHTML =
            '<span style="color:{NAVY};font-weight:700">\u25a0 A: '+nA+'</span>'
           +'&nbsp;&nbsp;<span style="color:{ORANGE};font-weight:700">\u25a0 D: '+nD+'</span>';
        }}
      }}, delay + i * spd);
      genTimers.push(t);
    }});
  }}

  /* Reset UI */
  ['gen-adv-arrow','gen-dis-arrow'].forEach(function(id) {{
    document.getElementById(id).style.display = 'none';
  }});
  ['gen-adv-g2-lbl','gen-dis-g2-lbl'].forEach(function(id) {{
    document.getElementById(id).style.display = 'none';
  }});
  ['gen-adv-g2','gen-dis-g2','gen-adv-g1','gen-dis-g1'].forEach(function(id) {{
    document.getElementById(id).innerHTML = '';
  }});

  /* Run: A gen1 → A gen2 → D gen1 → D gen2 */
  var t1end = animateGroup(advPop, advKids, 'gen-adv-g1', 'gen-adv-stat', 0);
  animateChildren(advKids, 'gen-adv-g2', 'gen-adv-g2-stat', 'gen-adv-g2-lbl', 'gen-adv-arrow', t1end + 700);

  var t2start = t1end + 50*spd + 1400;
  var t2end   = animateGroup(disPop, disKids, 'gen-dis-g1', 'gen-dis-stat', t2start);
  animateChildren(disKids, 'gen-dis-g2', 'gen-dis-g2-stat', 'gen-dis-g2-lbl', 'gen-dis-arrow', t2end + 700);
}}

/* ── Scale-up section ────────────────────────── */
var scaleTimers  = [];
var currentN     = 100;
var currentScen  = 0;

/* ── Scenario metadata ──────────────────────────────────────────────────── */
var SCEN_META = [
  {{
    label: 'Scenario 1 — Full info: rank by f = x₁ ∧ x₂',
    desc:  'The algorithm observes <strong>both x₁ (hat) and x₂ (sneakers)</strong>. '
          +'It scores each student by their true potential f = x₁ ∧ x₂ and admits the top 5/18. '
          +'Highest efficiency, but equity is low because A students are much more likely to have f=1.',
    score: function(p) {{ return p.f; }}
  }},
  {{
    label: 'Scenario 2 — Only x₁, no group info',
    desc:  'The algorithm can only see <strong>x₁ (hat)</strong> and ignores group membership. '
          +'Score = x₁. Since A has P(x₁=1)=2/3 and D has P(x₁=1)=1/3, A students still dominate '
          +'but D students with hats compete equally. Equity improves; efficiency drops because x₁ alone is a weaker predictor of f.',
    score: function(p) {{ return p.x1; }}
  }},
  {{
    label: 'Scenario 3 — x₁ + group as proxy for x₂',
    desc:  'The algorithm uses <strong>x₁ and group</strong> to estimate the full f. '
          +'Score = x₁ × P(x₂=1 | group): A scores 2/3 if x₁=1, D scores 1/3 if x₁=1. '
          +'Better efficiency than Scenario 2 (group predicts x₂), but equity drops — group is used as a penalty against D.',
    score: function(p) {{ return p.x1 * (p.group === 'A' ? 2/3 : 1/3); }}
  }},
  {{
    label: 'Scenario 4 — x₂ measured only for D',
    desc:  'For <strong>D students</strong>, both x₁ and x₂ are observed (D with f=1 jump to the top). '
          +'For <strong>A students</strong>, only x₁ is used (score = x₁). '
          +'This targeted measurement boosts equity for D without penalising anyone by group label.',
    score: function(p) {{
      if (p.group === 'D' && p.x1 === 1 && p.x2 === 1) return 2;
      return p.x1;
    }}
  }}
];

function selectScenario(s) {{
  currentScen = s;
  document.querySelectorAll('.stab').forEach(function(b) {{
    b.classList.toggle('active', parseInt(b.dataset.s) === s);
  }});
  document.getElementById('scenario-desc').innerHTML = SCEN_META[s].desc;
}}

function onNSlider(v) {{
  currentN = parseInt(v);
  document.getElementById('n-val-lbl').textContent = v;
}}

function makeMini(group, x1, x2, sz) {{
  var bc = group === 'A' ? '{NAVY}' : '{ORANGE}';
  var s = sz; var h = Math.round(sz * 1.35);
  var svg = '<svg width="'+s+'" height="'+h+'" viewBox="0 0 20 27" preserveAspectRatio="xMidYMid meet">';
  if (x1) svg += '<rect x="4" y="0" width="12" height="4" rx="2" fill="{PURPLE}"/>';
  svg += '<circle cx="10" cy="9.5" r="5.5" fill="'+bc+'"/>';
  svg += '<path d="M3.5,13.5 Q3.5,22 10,22 Q16.5,22 16.5,13.5 Q16.5,10.5 10,10.5 Q3.5,10.5 3.5,13.5 Z" fill="'+bc+'"/>';
  if (x2) svg += '<rect x="4" y="22.5" width="12" height="3.5" rx="1.5" fill="{COFFEE}"/>';
  svg += '</svg>';
  return svg;
}}

function runScale(N, scenario, speed) {{
  scaleTimers.forEach(function(t) {{ clearTimeout(t); }});
  scaleTimers = [];

  var K    = Math.round(N * 5/18);
  var meta = SCEN_META[scenario];
  var cols = Math.max(10, Math.ceil(Math.sqrt(N)));
  var cw   = Math.max(8, Math.floor(674 / cols));
  var grid = document.getElementById('mgrid');
  grid.style.gridTemplateColumns = 'repeat('+cols+', '+cw+'px)';
  grid.innerHTML = '';
  document.getElementById('cnt-scale').innerHTML = '&#8987; generating '+N+' students\u2026';
  document.getElementById('insight-scale').style.display = 'none';

  /* Generate */
  var half = Math.floor(N/2);
  var raw  = [];
  genPop(half,   2/3, 2/3).forEach(function(p) {{ raw.push({{x1:p.x1,x2:p.x2,group:'A',f:p.x1&&p.x2?1:0}}); }});
  genPop(N-half, 1/3, 1/3).forEach(function(p) {{ raw.push({{x1:p.x1,x2:p.x2,group:'D',f:p.x1&&p.x2?1:0}}); }});

  /* Assign scores */
  raw.forEach(function(p) {{ p.score = meta.score(p); }});

  /* Build cells */
  var cells = raw.map(function(p) {{
    var d = document.createElement('div');
    d.className = 'mcell';
    d.style.width  = cw+'px';
    d.style.height = Math.round(cw*1.35)+'px';
    d.innerHTML = makeMini(p.group, p.x1, p.x2, cw);
    grid.appendChild(d);
    return d;
  }});

  /* Staggered appear */
  var shown = 0;
  raw.forEach(function(p, i) {{
    var t = setTimeout(function() {{
      cells[i].classList.add('shown');
      shown++;
      if (shown < raw.length) return;

      document.getElementById('cnt-scale').innerHTML =
        '<span>\u23f3 Ranking by <strong>'+meta.label+'</strong>\u2026</span>';

      /* Phase 2: admit after short pause */
      var t2 = setTimeout(function() {{
        var indexed = raw.map(function(d,idx) {{ return {{d:d,idx:idx}}; }});
        indexed.sort(function() {{ return Math.random()-0.5; }});        /* shuffle for ties */
        indexed.sort(function(a,b) {{ return b.d.score - a.d.score; }}); /* stable sort by score */
        var admSet = {{}};
        indexed.slice(0,K).forEach(function(e) {{ admSet[e.idx] = true; }});

        cells.forEach(function(c,k) {{
          if (admSet[k]) {{ c.classList.add('admitted'); }}
          else           {{ c.classList.add('not-admitted'); }}
        }});

        var nA=0, nD=0, nAdmF=0;
        for (var k=0; k<raw.length; k++) {{
          if (!admSet[k]) continue;
          if (raw[k].group==='A') nA++; else nD++;
          if (raw[k].f) nAdmF++;
        }}
        var eq  = (nD/K*100).toFixed(1);
        var eff = (nAdmF/K*100).toFixed(1);

        document.getElementById('cnt-scale').innerHTML =
          '<span>Admitted: <b>'+K+'</b>/'+N+'</span>'
         +'<span style="color:{NAVY};font-weight:700">\u25a0 A: '+nA+' ('+Math.round(nA/K*100)+'%)</span>'
         +'<span style="color:{ORANGE};font-weight:700">\u25a0 D: '+nD+' ('+Math.round(nD/K*100)+'%)</span>'
         +'<span class="cstat cf">Efficiency (avg f): '+eff+'%</span>'
         +'<span class="cstat cx1">Equity (frac D): '+eq+'%</span>';

        /* Insight */
        var ins = document.getElementById('insight-scale');
        ins.style.display = 'block';
        /* Theoretical values scale with N:
           S0: equity=20%, eff=100%  (stable)
           S1: equity≈34%, eff≈55%  (stable, converges to 1/3 / (1/3+2/3) × ... )
           S2: equity→0%  with large N (E[tier1]=N/3 > K=5N/18, tier1 always fills K)
           S3: equity≈57%, eff≈55%  (stable) */
        /* Exact theoretical values from the class lecture (Algorithmic Fairness.pdf):
           S1: avg f = 1,   frac D = 1/5
           S2: avg f = 5/9, frac D = 1/3
           S3: avg f = 2/3, frac D = 0   (E[A-hat]=N/3 > K=5N/18 with large N)
           S4: avg f = 3/5, frac D = 2/5                                          */
        var theoryNote = [
          'Theory (class lecture): Efficiency = <b>1 = 100%</b> · Equity = <b>1/5 = 20%</b>',
          'Theory (class lecture): Efficiency = <b>5/9 \u2248 56%</b> · Equity = <b>1/3 \u2248 33%</b>',
          'Theory (class lecture): Efficiency = <b>2/3 \u2248 67%</b> · Equity = <b>0%</b><br>'
            +'<span style="color:#dc2626">\u26a0\ufe0f Using group as proxy always pushes all D below '
            +'all A-with-hat. With large N, no D student ever gets admitted.</span>',
          'Theory (class lecture): Efficiency = <b>3/5 = 60%</b> · Equity = <b>2/5 = 40%</b>'
        ];
        ins.innerHTML =
          '<strong>'+meta.label+'</strong><br>'
         +'Simulated — Efficiency: <b>'+eff+'%</b> · Equity (frac D): <b>'+eq+'%</b><br>'
         +'<span style="color:#64748b">'+theoryNote[scenario]+'</span>';
        ins.style.borderColor = '#6366f1';
      }}, 900);
      scaleTimers.push(t2);
    }}, i * speed);
    scaleTimers.push(t);
  }});
}}

function replayScale() {{
  var spd = parseInt(document.getElementById('spd-scale').value);
  runScale(currentN, currentScen, spd);
}}

/* Init scenario description on load */
selectScenario(0);

/* ── Shared evo scenario selector ───────────── */
var currentEvoScen = 0;

function selectEvoScenario(s) {{
  currentEvoScen = s;
  for (var i = 0; i < 4; i++) {{
    var b = document.getElementById('evo-stab-'+i);
    if (b) b.classList.toggle('active', i === s);
  }}
  /* update long-run title */
  var titles = ['Scenario 1','Scenario 2','Scenario 3','Scenario 4'];
  var el = document.getElementById('evo-scenario-title');
  if (el) el.textContent = titles[s];
}}

/* ── Long-run Evolution ──────────────────────── */
var evoTimer    = null;
var evoRAF      = null;
var evoHistory  = [];
var evoT        = 200;
var evoVisible  = {{fracD: true, equity: true, eff: true}};

function toggleEvoLine(key) {{
  evoVisible[key] = !evoVisible[key];
  var btn = document.getElementById('evo-leg-' + key);
  btn.classList.toggle('hidden', !evoVisible[key]);
  if (evoHistory.length) drawEvoChart(evoHistory, evoT);
}}

/* Simulation state: array of {{group, x1, x2, f, admitted}} */
function makeInitialPop() {{
  var pop = [];
  genPop(50, 2/3, 2/3).forEach(function(p) {{
    pop.push({{group:'A', x1:p.x1, x2:p.x2, f:p.x1&&p.x2?1:0, admitted:0}});
  }});
  genPop(50, 1/3, 1/3).forEach(function(p) {{
    pop.push({{group:'D', x1:p.x1, x2:p.x2, f:p.x1&&p.x2?1:0, admitted:0}});
  }});
  return pop;
}}

function admitEvo(pop) {{
  var K       = Math.round(pop.length * 5/18);
  var scoreFn = SCEN_META[currentEvoScen].score;
  pop.forEach(function(p) {{ p.admitted = 0; }});
  var idx = pop.map(function(p,i) {{ return {{s: scoreFn(p), i:i}}; }});
  idx.sort(function() {{ return Math.random()-0.5; }});
  idx.sort(function(a,b) {{ return b.s - a.s; }});
  idx.slice(0,K).forEach(function(e) {{ pop[e.i].admitted = 1; }});
}}

function nextGenEvo(pop) {{
  return pop.map(function(p) {{
    var cg = childGroup(p.group, p.admitted);
    var cp = cg==='A' ? 2/3 : 1/3;
    var cx1 = Math.random()<cp?1:0, cx2 = Math.random()<cp?1:0;
    return {{group:cg, x1:cx1, x2:cx2, f:cx1&&cx2?1:0, admitted:0}};
  }});
}}

function calcMetrics(pop) {{
  var N = pop.length;
  var K = Math.round(N*5/18);
  var adm = pop.filter(function(p) {{ return p.admitted; }});
  var fracD = pop.filter(function(p) {{ return p.group==='D'; }}).length / N;
  var equity = adm.filter(function(p) {{ return p.group==='D'; }}).length / K;
  var eff    = adm.reduce(function(s,p) {{ return s+p.f; }},0) / K;
  return {{fracD:fracD, equity:equity, eff:eff}};
}}

function drawEvoChart(hist, T) {{
  var canvas = document.getElementById('evo-canvas');
  var ctx    = canvas.getContext('2d');
  var W = canvas.width, H = canvas.height;
  var PAD = {{l:38, r:18, t:16, b:28}};
  var cw = W - PAD.l - PAD.r;
  var ch = H - PAD.t - PAD.b;

  ctx.clearRect(0,0,W,H);

  /* background */
  ctx.fillStyle = '#f8fafc';
  ctx.fillRect(0,0,W,H);

  /* grid lines */
  ctx.strokeStyle = '#e2e8f0';
  ctx.lineWidth = 1;
  for (var g=0; g<=4; g++) {{
    var yg = PAD.t + ch - g/4*ch;
    ctx.beginPath(); ctx.moveTo(PAD.l,yg); ctx.lineTo(PAD.l+cw,yg); ctx.stroke();
    ctx.fillStyle='#94a3b8'; ctx.font='10px sans-serif'; ctx.textAlign='right';
    ctx.fillText((g*25)+'%', PAD.l-4, yg+3.5);
  }}

  /* x axis label */
  ctx.fillStyle='#94a3b8'; ctx.font='10px sans-serif'; ctx.textAlign='center';
  ctx.fillText('Generation', PAD.l+cw/2, H-4);

  if (!hist.length) return;

  /* draw each metric (respects evoVisible toggle) */
  var metrics = [
    {{key:'fracD',  color:'{ORANGE}'}},
    {{key:'equity', color:'#059669'}},
    {{key:'eff',    color:'{PURPLE}'}}
  ];

  metrics.forEach(function(m) {{
    if (!evoVisible[m.key]) return;   /* skip hidden lines */
    ctx.beginPath();
    ctx.strokeStyle = m.color;
    ctx.lineWidth = 2.2;
    ctx.lineJoin = 'round';
    hist.forEach(function(h, i) {{
      var x = PAD.l + (i/(Math.max(T-1,1)))*cw;
      var y = PAD.t + ch - h[m.key]*ch;
      if (i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
    }});
    ctx.stroke();

    /* dot at current end */
    var last = hist[hist.length-1];
    var lx = PAD.l + ((hist.length-1)/Math.max(T-1,1))*cw;
    var ly = PAD.t + ch - last[m.key]*ch;
    ctx.beginPath();
    ctx.arc(lx,ly,3.5,0,2*Math.PI);
    ctx.fillStyle = m.color;
    ctx.fill();
  }});
}}

function runEvo() {{
  if (evoTimer) clearTimeout(evoTimer);
  if (evoRAF)   cancelAnimationFrame(evoRAF);

  var T   = parseInt(document.getElementById('evo-gen-slider').value);
  var spd = parseInt(document.getElementById('evo-spd').value);

  evoT       = T;
  evoHistory = [];
  var pop    = makeInitialPop();
  var hist   = evoHistory;
  var gen    = 0;

  /* how many gens to compute per tick */
  var batch = Math.max(1, Math.round(20 / spd));

  function tick() {{
    for (var b=0; b<batch && gen<T; b++) {{
      admitEvo(pop);
      hist.push(calcMetrics(pop));
      pop = nextGenEvo(pop);
      gen++;
    }}

    drawEvoChart(hist, T);

    var last = hist[hist.length-1];
    var nD   = Math.round(last.fracD * pop.length);
    var nA   = pop.length - nD;
    document.getElementById('evo-status').innerHTML =
      '<span>Gen <strong>'+gen+'</strong>/'+T+'</span>'
     +'<span style="color:{NAVY};font-weight:600">\u25a0 A: '+nA+'</span>'
     +'<span style="color:{ORANGE};font-weight:600">\u25a0 D: '+nD+'</span>'
     +'<span style="color:#059669">Equity: '+(last.equity*100).toFixed(1)+'%</span>'
     +'<span style="color:{PURPLE}">Efficiency: '+(last.eff*100).toFixed(1)+'%</span>';

    if (gen < T) {{
      evoTimer = setTimeout(tick, spd);
    }}
  }}

  tick();
}}

/* ── Averaged Evolution ──────────────────────────────────────────────────── */
var avgTimer2     = null;
var currentAvgScen = 0;
var avgHistoryData = [];
var avgVisible2   = {{fracD: true, equity: true, eff: true}};

function selectAvgScenario(s) {{
  currentAvgScen = s;
  for (var i = 0; i < 4; i++) {{
    var b = document.getElementById('avg-stab-'+i);
    if (b) b.classList.toggle('active', i === s);
  }}
  var titles = ['Scenario 1','Scenario 2','Scenario 3','Scenario 4'];
  var el = document.getElementById('avg-scenario-title');
  if (el) el.textContent = titles[s];
}}

/* Admit using an explicit scenario index (doesn't touch currentEvoScen) */
function admitScen(pop, scen) {{
  var K = Math.round(pop.length * 5/18);
  var scoreFn = SCEN_META[scen].score;
  pop.forEach(function(p) {{ p.admitted = 0; }});
  var idx = pop.map(function(p,i) {{ return {{s: scoreFn(p), i:i}}; }});
  idx.sort(function() {{ return Math.random()-0.5; }});
  idx.sort(function(a,b) {{ return b.s - a.s; }});
  idx.slice(0,K).forEach(function(e) {{ pop[e.i].admitted = 1; }});
}}

function drawAvgChart(hist, T) {{
  var canvas = document.getElementById('avg-canvas');
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  var W = canvas.width, H = canvas.height;
  var PAD = {{l:38, r:18, t:16, b:28}};
  var cw = W - PAD.l - PAD.r, ch = H - PAD.t - PAD.b;
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle = '#f8fafc'; ctx.fillRect(0,0,W,H);
  ctx.strokeStyle = '#e2e8f0'; ctx.lineWidth = 1;
  for (var g=0; g<=4; g++) {{
    var yg = PAD.t + ch - g/4*ch;
    ctx.beginPath(); ctx.moveTo(PAD.l,yg); ctx.lineTo(PAD.l+cw,yg); ctx.stroke();
    ctx.fillStyle='#94a3b8'; ctx.font='10px sans-serif'; ctx.textAlign='right';
    ctx.fillText((g*25)+'%', PAD.l-4, yg+3.5);
  }}
  ctx.fillStyle='#94a3b8'; ctx.font='10px sans-serif'; ctx.textAlign='center';
  ctx.fillText('Generation', PAD.l+cw/2, H-4);
  if (!hist.length) return;
  var metrics = [
    {{key:'fracD',  color:'{ORANGE}'}},
    {{key:'equity', color:'#059669'}},
    {{key:'eff',    color:'{PURPLE}'}}
  ];
  metrics.forEach(function(m) {{
    if (!avgVisible2[m.key]) return;
    ctx.beginPath(); ctx.strokeStyle=m.color; ctx.lineWidth=2.2; ctx.lineJoin='round';
    hist.forEach(function(h, i) {{
      var x = PAD.l + (i/(Math.max(T-1,1)))*cw;
      var y = PAD.t + ch - h[m.key]*ch;
      if (i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
    }});
    ctx.stroke();
    var last = hist[hist.length-1];
    var lx = PAD.l + ((hist.length-1)/Math.max(T-1,1))*cw;
    var ly = PAD.t + ch - last[m.key]*ch;
    ctx.beginPath(); ctx.arc(lx,ly,3.5,0,2*Math.PI); ctx.fillStyle=m.color; ctx.fill();
  }});
}}

function toggleAvgLine(key) {{
  avgVisible2[key] = !avgVisible2[key];
  var btn = document.getElementById('avg-leg-'+key);
  if (btn) btn.classList.toggle('hidden', !avgVisible2[key]);
  if (avgHistoryData.length) {{
    drawAvgChart(avgHistoryData, parseInt(document.getElementById('avg-gen-slider').value));
  }}
}}

function runAvgEvo() {{
  if (avgTimer2) clearTimeout(avgTimer2);
  var T    = parseInt(document.getElementById('avg-gen-slider').value);
  var R    = parseInt(document.getElementById('avg-runs-slider').value);
  var scen = currentAvgScen;

  var sumFracD = [], sumEquity = [], sumEff = [];
  for (var ti = 0; ti < T; ti++) {{ sumFracD.push(0); sumEquity.push(0); sumEff.push(0); }}

  var completed = 0;
  var BATCH = Math.max(1, Math.ceil(R/40));

  document.getElementById('avg-progress-bar').style.width = '0%';
  document.getElementById('avg-status').innerHTML = 'Initializing\u2026';
  avgHistoryData = [];

  function tick() {{
    var end = Math.min(completed + BATCH, R);
    for (var r = completed; r < end; r++) {{
      var pop = makeInitialPop();
      for (var gt = 0; gt < T; gt++) {{
        admitScen(pop, scen);
        var m = calcMetrics(pop);
        sumFracD[gt]  += m.fracD;
        sumEquity[gt] += m.equity;
        sumEff[gt]    += m.eff;
        pop = nextGenEvo(pop);
      }}
    }}
    completed = end;
    document.getElementById('avg-progress-bar').style.width = Math.round(completed/R*100)+'%';

    var hist = [];
    for (var ti2 = 0; ti2 < T; ti2++) {{
      hist.push({{
        fracD:  sumFracD[ti2]  / completed,
        equity: sumEquity[ti2] / completed,
        eff:    sumEff[ti2]    / completed
      }});
    }}
    avgHistoryData = hist;
    drawAvgChart(hist, T);

    var last = hist[T-1];
    document.getElementById('avg-status').innerHTML =
      (completed < R
        ? '<span style="color:#64748b">Running '+completed+'/'+R+' simulations\u2026</span>'
        : '<strong style="color:#059669">\u2713 '+R+' runs averaged</strong>')
      +' &nbsp;\u00b7&nbsp; Gen '+T+': '
      +'<span style="color:#059669">Equity '+(last.equity*100).toFixed(1)+'%</span>'
      +' &nbsp; <span style="color:{PURPLE}">Efficiency '+(last.eff*100).toFixed(1)+'%</span>';

    if (completed < R) {{ avgTimer2 = setTimeout(tick, 0); }}
  }}
  tick();
}}

/* ── Circle hover ─────────────────────────────── */
var icons    = document.querySelectorAll('.picon');
var cDef = document.getElementById('center-default');
var cA   = document.getElementById('center-A');
var cD   = document.getElementById('center-D');

icons.forEach(function(icon) {{
  icon.addEventListener('mouseenter', function() {{
    cDef.setAttribute('visibility','hidden');
    cA.setAttribute('visibility', icon.dataset.group==='A' ? 'visible' : 'hidden');
    cD.setAttribute('visibility', icon.dataset.group==='D' ? 'visible' : 'hidden');
  }});
  icon.addEventListener('mouseleave', function() {{
    cDef.setAttribute('visibility','visible');
    cA.setAttribute('visibility','hidden');
    cD.setAttribute('visibility','hidden');
  }});
}});

/* ── Scroll-triggered fade-in ──────────────────────────────────────────── */
/* Streamlit's scroll container isn't always window — we poll multiple       */
/* sources every 250ms and show sections as they enter the viewport.         */

var iframeTopAbs = null;
var triggered = {{}};

function getIframeTop() {{
  if (iframeTopAbs !== null) return iframeTopAbs;
  try {{
    var frames = window.parent.document.querySelectorAll('iframe');
    for (var i = 0; i < frames.length; i++) {{
      try {{
        if (frames[i].contentWindow === window) {{
          var r = frames[i].getBoundingClientRect();
          var parentScroll = window.parent.scrollY || window.parent.pageYOffset ||
                             window.parent.document.documentElement.scrollTop || 0;
          iframeTopAbs = r.top + parentScroll;
          return iframeTopAbs;
        }}
      }} catch(ex) {{}}
    }}
  }} catch(ex) {{}}
  return 0;
}}

function getScrollState() {{
  var y = 0, vh = 900;
  /* Try every possible Streamlit scroll container */
  var selectors = [
    '[data-testid="stAppViewContainer"]',
    '[data-testid="block-container"]',
    '.main', 'section.main', 'section'
  ];
  try {{ y = Math.max(y, window.parent.scrollY || window.parent.pageYOffset || 0); }} catch(e) {{}}
  try {{ y = Math.max(y, window.parent.document.documentElement.scrollTop || 0); }} catch(e) {{}}
  try {{ y = Math.max(y, window.parent.document.body.scrollTop || 0); }} catch(e) {{}}
  try {{
    selectors.forEach(function(sel) {{
      try {{
        var el = window.parent.document.querySelector(sel);
        if (el) y = Math.max(y, el.scrollTop || 0);
      }} catch(e) {{}}
    }});
  }} catch(e) {{}}
  try {{ vh = window.parent.innerHeight || 900; }} catch(e) {{}}
  return {{ y: y, vh: vh }};
}}

function triggerSection(id) {{
  if (triggered[id]) return;
  triggered[id] = true;
  var sec = document.getElementById(id);
  if (!sec) return;
  sec.classList.add('visible');
  if (id === 'sec-adv')   setTimeout(replayAdv,   350);
  if (id === 'sec-dis')   setTimeout(replayDis,   350);
  if (id === 'sec-all')   setTimeout(replayAll,   350);
    if (id === 'sec-scale') setTimeout(replayScale, 350);
    if (id === 'sec-gen')   setTimeout(runGen, 350);
    if (id === 'sec-evo')   setTimeout(runEvo, 350);
}}

function checkSections() {{
  var sv   = getScrollState();
  var iTop = getIframeTop();
  document.querySelectorAll('.fade-section').forEach(function(s) {{
    if (iTop + s.offsetTop < sv.y + sv.vh * 0.92) triggerSection(s.id);
  }});
}}

/* Poll every 250ms — works regardless of which element Streamlit scrolls */
setInterval(checkSections, 250);

/* Hard fallback: show everything after 10s in case nothing fired */
setTimeout(function() {{
    ['sec-adv','sec-dis','sec-all','sec-scale','sec-gen','sec-evo','sec-avg'].forEach(function(id) {{
    var sec = document.getElementById(id);
    if (sec) sec.classList.add('visible');
  }});
}}, 10000);
</script>
</body>
</html>"""

components.html(HTML, height=11000, scrolling=False)
