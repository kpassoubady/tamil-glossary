---
marp: true
theme: default
paginate: true
header: "திறந்தநிலையும் அடித்தளமும்"
footer: "AI அலை: நீங்கள் தயாரா? தமிழில் 300+ செய்யறிவுக் கலைச்சொற்கள்"
style: |
  @import url("https://cdn.jsdelivr.net/gh/kpassoubady/marp-themes@v10/term-chair/term-chair.css");
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
  .vs-grid { display: grid; grid-template-columns: 1fr auto 1fr; gap: 1em; align-items: center; margin-top: 0.8em; }
  .vs-card { border: 2px solid var(--color-primary); border-radius: 10px; padding: 1em; background: #fffdf5; }
  .vs-card h3 { margin-top: 0; }
  .vs-label { font-size: 1.6em; font-weight: 700; color: var(--color-accent); text-align: center; }
  section.lead h1 { font-size: 1.4em; white-space: nowrap; }
---

<!-- _class: lead -->
<!-- _paginate: false -->

<div class="badge-row"><span class="badge tnc">TNC55</span><span class="badge chapter">அத்தியாயம் 1</span><span class="badge part">பகுதி 4</span></div>

# திறந்தநிலையும் அடித்தளமும் = <span class="word-root">திறந்த</span> + <span class="word-root">அடித்தளம்</span>

## Openness & Foundation: 15 நிமிட நுண் பயிலரங்கு

நூல்: AI அலை: நீங்கள் தயாரா? | நுண் பயிலரங்கு

<img class="logo" src="https://cdn.jsdelivr.net/gh/kpassoubady/marp-themes@v10/term-chair/logo.png" />

---

# AI மாதிரிகள் எப்படி வெளியிடப்படுகின்றன?

AI மாதிரிகளின் வெளியீட்டு முறை தொழில்துறையின் போக்கை நிர்ணயிக்கிறது. சில மாதிரிகள் முழுமையாகத் திறந்த மூலமாக வெளியிடப்படுகின்றன, சில எடைகளை மட்டும் பகிர்கின்றன. இவை அனைத்தும் ஒரு பொதுவான அடித்தள மாதிரியிலிருந்து கட்டமைக்கப்படுகின்றன.

---

# வெளியீட்டு முறை வரைபடம்

<img src="../assets/diagrams/01-ai-openness.svg" alt="வெளியீட்டு முறை" style="display:block; margin:0 auto; max-height:420px;" />

---

<!-- _class: term -->

# திறந்த மூலம் vs திறந்த எடை

<div class="vs-grid">
<div class="vs-card">
<h3>Open Source AI<br><span class="tamil">திறந்த மூலச் செய்யறிவு</span></h3>
<p style="font-size:0.8em">மூலக் குறிமுறை, எடைகள், பயிற்சித் தரவு ஆகியவை அனைத்தும் பொதுவில்.</p>
</div>
<div class="vs-label">VS</div>
<div class="vs-card">
<h3>Open Weight<br><span class="tamil">திறந்த எடை</span></h3>
<p style="font-size:0.8em">பயிற்சி பெற்ற எடைகள் மட்டுமே பொதுவில் (உ-ம்: Llama, Gemma).</p>
</div>
</div>

---

<!-- _class: term -->

# Foundation Model: <span class="tamil">அடிப்படை மாதிரி</span>

பல்வேறு வேலைகளுக்கு அடித்தளமாக அமையும் பெரும் முன்பயிற்சி பெற்ற AI மாதிரி.

<div class="industry-badge">உதாரணம்</div>
GPT, Claude, Gemini. இவற்றின் மேல் பல பயன்பாடுகள் கட்டப்படுகின்றன.

---

<!-- _class: chat-check -->

# வினா: எது எது?

"பயிற்சி பெற்ற எடைகள் மட்டும் பொதுவில் வெளியிடப்படும், ஆனால் பயிற்சிக் குறிமுறை பொதுவில் இல்லாமல் இருக்கலாம்"

<div class="gfm-alert gfm-note">
<div class="gfm-alert-title">Discuss</div>
<p>அறையில் உள்ளவர்களே பதில் சொல்லுங்கள்! 10 வினாடிகள்.</p>
</div>

---

<!-- _class: chat-check-answer -->

# விடை: திறந்த எடை (Open Weight)

திறந்த மூலச் செய்யறிவு (Open Source AI) மூலக் குறிமுறை, எடைகள், பயிற்சித் தரவு அனைத்தையும் பொதுவில் தரும். திறந்த எடை (Open Weight) எடைகளை மட்டும் தரும்.

---

# இன்று கற்ற 3 சொற்கள்

<div class="term-grid recap">
<div class="term-card"><span class="tag">வெளியீடு</span><h3>திறந்த மூலம்</h3><p>Open Source AI</p></div>
<div class="term-card"><span class="tag">வெளியீடு</span><h3>திறந்த எடை</h3><p>Open Weight</p></div>
<div class="term-card"><span class="tag">அடித்தளம்</span><h3>அடிப்படை மாதிரி</h3><p>Foundation Model</p></div>
</div>

---

<!-- _class: lead -->
<!-- _paginate: false -->

<div class="badge-row"><span class="badge tnc">TNC55</span><span class="badge chapter">அத்தியாயம் 1</span><span class="badge part">பகுதி 5</span></div>

# அடுத்து: அடிப்படைக் கருத்துகள்

திறந்தநிலையும் அடித்தளமும்: முடிந்தது

<span style="font-size:0.55em; color:rgba(253,249,240,0.75)">கங்கா வளர் தொழில்நுட்பக் கலைச்சொல் ஆய்விருக்கை, யூ.எஸ்.ஏ.<br>Ganga Emerging Technology Terminology Research Chair, USA</span>

<img class="logo" src="https://cdn.jsdelivr.net/gh/kpassoubady/marp-themes@v10/term-chair/logo.png" />
