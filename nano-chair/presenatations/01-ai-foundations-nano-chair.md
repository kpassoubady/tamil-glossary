---
marp: true
theme: default
paginate: true
style: |
  @import url("https://cdn.jsdelivr.net/gh/kpassoubady/marp-themes@v8/term-chair/term-chair.css");
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
  .vs-grid { display: grid; grid-template-columns: 1fr auto 1fr; gap: 1em; align-items: center; margin-top: 0.8em; }
  .vs-card { border: 2px solid var(--color-primary); border-radius: 10px; padding: 1em; background: #fffdf5; }
  .vs-card h3 { margin-top: 0; }
  .vs-label { font-size: 1.6em; font-weight: 700; color: var(--color-accent); text-align: center; }
  .word-root { display: inline-block; background: var(--color-bg-code); border: 1px dashed var(--color-accent); border-radius: 6px; padding: 0.15em 0.6em; margin: 0.1em; font-weight: 700; color: var(--color-primary-dark); }
  .progress-dot { display: inline-block; width: 0.6em; height: 0.6em; border-radius: 50%; background: var(--color-accent); margin: 0 0.15em; }
  .img-text-grid { display: grid; grid-template-columns: 300px 1fr; gap: 1.8em; align-items: center; margin-top: 0.8em; }
  .img-text-grid img { width: 300px; height: 300px; object-fit: cover; border-radius: 10px; border: 3px solid var(--color-accent); }
  .img-text-grid .quote { font-size: 1.3em; font-weight: 700; color: var(--color-primary); margin: 0 0 0.4em; }
  .img-text-grid.size-350 { grid-template-columns: 350px 1fr; }
  .img-text-grid.size-350 img { width: 350px; height: 350px; }
---

<!-- _class: lead -->
<!-- _paginate: false -->

## செய்மீயறிவு = <span class="word-root">செய்</span> + <span class="word-root">மீ</span> + <span class="word-root">அறிவு</span>

செய்யறிவு அடிப்படைகள்: 15 நிமிட அறிமுகம்

நூல்: AI அலை: நீங்கள் தயாரா? | நுண் பயிலரங்கு

<img class="logo" src="https://cdn.jsdelivr.net/gh/kpassoubady/marp-themes@v8/term-chair/logo.png" />

---

# இன்று நாம் கற்கப் போவது

9 கலைச்சொற்கள் · 15 நிமிடங்கள் · உங்கள் சொந்த வார்த்தையில் விளக்குங்கள்

<div class="term-grid">
<div class="term-card"><span class="tag">நிலைகள்</span><h3>AI · AGI · ASI</h3></div>
<div class="term-card"><span class="tag">நவீன வகைகள்</span><h3>இயற்று · செயலூக்கம் · பன்முகம்</h3></div>
<div class="term-card"><span class="tag">வெளியீடு</span><h3>திறந்த மூலம் · எடை · அடித்தளம் · தோற்றம்</h3></div>
</div>

---

<!-- _class: divider -->

# பகுதி 1
## செய்யறிவின் மூன்று நிலைகள் (Levels of AI)

<img class="logo" src="https://cdn.jsdelivr.net/gh/kpassoubady/marp-themes@v8/term-chair/logo.png" />

---

# 1950: ஆலன் டூரிங்கின் கேள்வி

<div class="img-text-grid">
<div>

<img src="../assets/images/hero-ch01.png" alt="செய்யறிவு அடிப்படைகள்" />

</div>
<div>

<p class="quote">"இயந்திரங்களால் சிந்திக்க முடியுமா?"</p>

இந்தக் கேள்விதான் இன்றைய செய்யறிவுத் துறையின் தொடக்கம். அன்று தொடங்கிய பயணம் இன்று மூன்று நிலைகளாகப் பிரிக்கப்படுகிறது.

</div>
</div>

---

# செய்யறிவு நிலைகள் வரைபடம்

<img src="../assets/diagrams/01-ai-levels.svg" alt="செய்யறிவு நிலைகள்" style="display:block; margin:0 auto; max-height:420px;" />

---

<!-- _class: term -->

# Artificial Intelligence: <span class="tamil">செய்யறிவு</span>

<span class="word-root">செய்</span> + <span class="word-root">அறிவு</span>

மனித அறிவைப் போலச் செயல்படும் திறன் கொண்ட கணினி அமைப்புகள். இன்று நடைமுறையில் இருப்பது இந்த "குறுகிய செய்யறிவு" மட்டுமே.

> 📌 மாற்றுச் சொல்: செயற்கை நுண்ணறிவு

---

<!-- _class: term -->

# Artificial General Intelligence: <span class="tamil">பொதுச் செய்யறிவு</span>

<span class="word-root">பொது</span> + <span class="word-root">செய்யறிவு</span>

மனிதனைப் போல எந்தத் துறையிலும் பொதுவாகச் சிந்திக்கவும், கற்கவும், சிக்கல் தீர்க்கவும் வல்ல AI நிலை.

> 📌 இன்னும்: ஆராய்ச்சி நிலையில் மட்டுமே உள்ளது, நடைமுறையில் இல்லை.

---

<!-- _class: term -->

# Artificial Super Intelligence: <span class="tamil">செய்மீயறிவு</span>

<span class="word-root">செய்</span> + <span class="word-root">மீ</span> + <span class="word-root">அறிவு</span>

"மீ" முன்னொட்டு "மீக்கணிப்பொறி" (super computer) போல் பயன்படுத்தப்படுகிறது. ஒட்டுமொத்த மனித அறிவையும் தாண்டிய திறமைகளைக் கொண்ட கற்பனை AI நிலை.

<p class="progress-dot"></p><span style="font-size:0.8em; color:var(--color-text-light)">குறுகிய AI (இன்று) &rarr; பொதுச் AGI (ஆராய்ச்சி) &rarr; ASI (கற்பனை)</span>

---

<!-- _class: divider -->

# பகுதி 2
## நவீன AI வகைகள் (Modern AI Types, 2023+)

<img class="logo" src="https://cdn.jsdelivr.net/gh/kpassoubady/marp-themes@v8/term-chair/logo.png" />

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

<!-- _class: divider -->

# பகுதி 3
## வெளியீட்டு முறையும் அடித்தளமும் (Openness & Foundation)

<img class="logo" src="https://cdn.jsdelivr.net/gh/kpassoubady/marp-themes@v8/term-chair/logo.png" />

---

# AI மாதிரிகள் எப்படி வெளியிடப்படுகின்றன?

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

<!-- _class: term -->

# Emergent Abilities: <span class="tamil">வெளிப்படும் திறன்கள்</span>

<span class="word-root">தோன்றும்</span> + <span class="word-root">இயல்பு</span>

AI மாதிரியின் அளவு பெருகும்போது, சிறிய மாதிரிகளில் இல்லாத புதிய திறன்கள் தற்செயலாக வெளிப்படும் நிகழ்வு.

> 📌 உதாரணம்: 10 பில்லியன் அளபுருவில் இல்லாத திறன், 100 பில்லியனில் தானாகத் தோன்றுகிறது.

---

<!-- _class: discussion -->

# விவாதம்

பெருமொழி மாதிரிகளில் (LLMs) வெளிப்படும் திறன்கள் (Emergent Abilities) தற்செயலாகத் தோன்றுகின்றன. இத்தகைய திறன்களை முன்கூட்டியே கணிக்க இயலுமா?

---

<!-- _class: discussion-answer -->

# திருப்பிப் பாருங்கள்

செய்யறிவு (AI) &rarr; இயற்றறிவு (Generative) &rarr; செயலூக்கம் (Agentic) &rarr; அடிப்படை மாதிரி (Foundation) &rarr; வெளிப்படும் திறன் (Emergent): ஒவ்வொரு சொல்லும் அடுத்ததற்கு அடித்தளம்.

---

# 📰 AI வரலாற்றில் ஒரு துளி

<div class="img-text-grid size-350">
<div>

<img src="../assets/images/drop-in-history-ch01.png" alt="டார்ட்மவுத் மாநாடு 1956" />

</div>
<div>

1956, டார்ட்மவுத் கல்லூரி. ஜான் மெக்கார்த்தி மற்றும் மார்வின் மின்ஸ்கி "செயற்கை நுண்ணறிவு" என்ற சொல்லை முதன்முதலில் பயன்படுத்தினர்.

அவர்கள் நினைத்தது: "ஒரே கோடைகாலத்தில் முடிந்துவிடும்." உண்மையில் அது இன்னும் தொடரும் பயணம்.

</div>
</div>

---

# இன்று கற்ற 9 சொற்கள்

<div class="term-grid recap">
<div class="term-card"><span class="tag">நிலைகள்</span><h3>செய்யறிவு</h3><p>AI</p></div>
<div class="term-card"><span class="tag">நிலைகள்</span><h3>பொதுச் செய்யறிவு</h3><p>AGI</p></div>
<div class="term-card"><span class="tag">நிலைகள்</span><h3>செய்மீயறிவு</h3><p>ASI</p></div>
<div class="term-card"><span class="tag">வகைகள்</span><h3>இயற்றறிவு</h3><p>Generative AI</p></div>
<div class="term-card"><span class="tag">வகைகள்</span><h3>செயலூக்கச் செய்யறிவு</h3><p>Agentic AI</p></div>
<div class="term-card"><span class="tag">வகைகள்</span><h3>பன்முகச் செய்யறிவு</h3><p>Multimodal AI</p></div>
<div class="term-card"><span class="tag">வெளியீடு</span><h3>திறந்த மூலம் / எடை</h3><p>Open Source / Weight</p></div>
<div class="term-card"><span class="tag">வெளியீடு</span><h3>அடிப்படை மாதிரி</h3><p>Foundation Model</p></div>
<div class="term-card"><span class="tag">வெளியீடு</span><h3>வெளிப்படும் திறன்கள்</h3><p>Emergent Abilities</p></div>
</div>

---

<!-- _class: chat-waterfall -->

# திறந்த கேள்வி

இந்த 9 சொற்களில் நீங்கள் இன்று வீட்டில் யாருக்காவது விளக்கக்கூடிய ஒரு சொல் எது? ஏன் அது?

---

<!-- _class: lead -->
<!-- _paginate: false -->

# நன்றி!

செய்யறிவு அடிப்படைகள்
நூல்: AI அலை: நீங்கள் தயாரா? தமிழில் 300+ செய்யறிவுக் கலைச்சொற்கள்
ஆசிரியர்: காங்கேயன் பசுபதி

கங்கா வளர் தொழில்நுட்பக் கலைச்சொல் ஆய்விருக்கை, யூ.எஸ்.ஏ.
Ganga Emerging Technology Terminology Research Chair, USA

<img class="logo" src="https://cdn.jsdelivr.net/gh/kpassoubady/marp-themes@v8/term-chair/logo.png" />
