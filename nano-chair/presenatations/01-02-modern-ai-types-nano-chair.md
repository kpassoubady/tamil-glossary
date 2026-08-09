---
marp: true
theme: default
paginate: true
header: "நவீன AI வகைகள்"
footer: "AI அலை: நீங்கள் தயாரா? தமிழில் 300+ செய்யறிவுக் கலைச்சொற்கள்"
style: |
  @import url("https://cdn.jsdelivr.net/gh/kpassoubady/marp-themes@v9/term-chair/term-chair.css");
  section { animation: fadeIn 0.6s ease-in; }
  @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
  .term-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1em; margin-top: 0.6em; }
  .term-card { border: 2px solid var(--color-accent); border-radius: 10px; padding: 0.8em; background: #fffdf5; text-align: center; }
  .term-card .tag { display: block; font-size: 0.7em; color: var(--color-text-light); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.3em; }
  .term-card h3 { margin: 0.2em 0; font-size: 1.15em; }
  .term-card p { font-size: 0.75em; margin: 0.2em 0 0; color: var(--color-text); }
  .term-grid.recap { gap: 0.5em; margin-top: 0.3em; }
  .term-grid.recap .term-card { padding: 0.35em 0.5em; }
  .term-grid.recap .term-card .tag { font-size: 0.55em; margin-bottom: 0.1em; }
  .term-grid.recap .term-card h3 { font-size: 0.85em; margin: 0.05em 0; line-height: 1.15; }
  .term-grid.recap .term-card p { font-size: 0.6em; margin: 0.1em 0 0; }
  .word-root { display: inline-block; background: var(--color-bg-code); border: 1px dashed var(--color-accent); border-radius: 6px; padding: 0.15em 0.6em; margin: 0.1em; font-weight: 700; color: var(--color-primary-dark); }
---

<!-- _class: lead -->
<!-- _paginate: false -->

<div class="badge-row"><span class="badge chapter">அத்தியாயம் 1</span><span class="badge part">பகுதி 2</span></div>

# நவீன AI வகைகள் = <span class="word-root">இயற்று</span> + <span class="word-root">செயலூக்கம்</span> + <span class="word-root">பன்முகம்</span>

## Generative · Agentic · Multimodal AI: 15 நிமிட நுண் பயிலரங்கு

நூல்: AI அலை: நீங்கள் தயாரா? | நுண் பயிலரங்கு

<img class="logo" src="https://cdn.jsdelivr.net/gh/kpassoubady/marp-themes@v9/term-chair/logo.png" />

---

# 2023-க்குப் பிறகு ஏன் இவ்வளவு வேகம்?

செய்யறிவுத் துறை 2023-க்குப் பிறகு வேகமாக விரிவடைந்துள்ளது. உரை, படம், ஒலி உருவாக்கும் மாதிரிகள், தானே முடிவெடுத்துச் செயல்படும் மாதிரிகள், பல வகை உள்ளீடுகளைக் கையாளும் மாதிரிகள்: இவை மூன்றும் இன்றைய முதன்மை AI வகைகள்.

---

# செய்யறிவுப் பரிணாம வரைபடம்

<img src="../assets/diagrams/01-ai-evolution.svg" alt="செய்யறிவுப் பரிணாமம்" style="display:block; margin:0 auto; max-height:420px;" />

---

<!-- _class: term -->

# Generative AI: <span class="tamil">இயற்றறிவு</span>

<span class="word-root">இயற்று</span> (உருவாக்கு) + <span class="word-root">அறிவு</span>

புதிய உரை, படம், ஒலி அல்லது நிரல் குறிமுறைகளைத் தாமாகவே உருவாக்கும் திறன் கொண்ட AI மாதிரி.

<div class="industry-badge">உதாரணம்</div>
ChatGPT ஒரு கட்டுரையை எழுதித் தருவது, Midjourney ஒரு படத்தை உருவாக்குவது.

---

<!-- _class: term -->

# Agentic AI: <span class="tamil">செயலூக்கச் செய்யறிவு</span>

<span class="word-root">செயல்</span> + <span class="word-root">ஊக்கம்</span> + <span class="word-root">செய்யறிவு</span>

தானே முடிவெடுத்துக் கருவிகளைப் பயன்படுத்தி இலக்கு நோக்கித் தொடர்ச்சியாகச் செயல்படும் AI மாதிரி.

<div class="industry-badge">உதாரணம்</div>
கணினி பொறியாளர் Claude CLI போன்ற கருவிகளைப் பயன்படுத்துவது.

---

<!-- _class: term -->

# Multimodal AI: <span class="tamil">பன்முகச் செய்யறிவு</span>

<span class="word-root">பன்</span> (பல) + <span class="word-root">முகம்</span> + <span class="word-root">செய்யறிவு</span>

உரை, படம், ஒலி, காணொளி போன்ற பல வகை உள்ளீடுகளை ஒரே நேரத்தில் கையாளும் திறன் கொண்ட AI மாதிரி.

<div class="industry-badge">உதாரணம்</div>
ஒரு படத்தைக் காட்டி, "இதில் என்ன இருக்கிறது?" எனக் குரலில் கேட்பது.

---

<!-- _class: chat-check -->

# வினா: இந்தச் சொல் எது?

"தானே முடிவெடுத்துக் கருவிகளைப் பயன்படுத்தி இலக்கு நோக்கித் தொடர்ச்சியாகச் செயல்படும் AI மாதிரி"

<div class="gfm-alert gfm-note">
<div class="gfm-alert-title">Discuss</div>
<p>அறையில் உள்ளவர்களே பதில் சொல்லுங்கள்! 10 வினாடிகள்.</p>
</div>

---

<!-- _class: chat-check-answer -->

# விடை: செயலூக்கச் செய்யறிவு (Agentic AI)

செயல் + ஊக்கம் + செய்யறிவு. இயற்றறிவிலிருந்து (Generative AI) வேறுபாடு: இயற்றறிவு உருவாக்குகிறது, செயலூக்கச் செய்யறிவு செயல்படுகிறது.

---

# இன்று கற்ற 3 சொற்கள்

<div class="term-grid recap">
<div class="term-card"><span class="tag">வகை 1</span><h3>இயற்றறிவு</h3><p>Generative AI</p></div>
<div class="term-card"><span class="tag">வகை 2</span><h3>செயலூக்கச் செய்யறிவு</h3><p>Agentic AI</p></div>
<div class="term-card"><span class="tag">வகை 3</span><h3>பன்முகச் செய்யறிவு</h3><p>Multimodal AI</p></div>
</div>

---

<!-- _class: lead -->
<!-- _paginate: false -->

<div class="badge-row"><span class="badge chapter">அத்தியாயம் 1</span><span class="badge part">பகுதி 3</span></div>

# அடுத்து: உணர்வும் பண்பாடும்

நவீன AI வகைகள்: முடிந்தது

<span style="font-size:0.55em; color:rgba(253,249,240,0.75)">கங்கா வளர் தொழில்நுட்பக் கலைச்சொல் ஆய்விருக்கை, யூ.எஸ்.ஏ.<br>Ganga Emerging Technology Terminology Research Chair, USA</span>

<img class="logo" src="https://cdn.jsdelivr.net/gh/kpassoubady/marp-themes@v9/term-chair/logo.png" />
