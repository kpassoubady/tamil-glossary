---
marp: true
theme: default
paginate: true
header: "அடிப்படைக் கருத்துகள்"
footer: "AI அலை: நீங்கள் தயாரா? தமிழில் 300+ செய்யறிவுக் கலைச்சொற்கள்"
style: |
  @import url("https://cdn.jsdelivr.net/gh/kpassoubady/marp-themes@v10/term-chair/term-chair.css");
  section { animation: fadeIn 0.6s ease-in; }
  @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
  .term-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.8em; margin-top: 0.6em; }
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
  .progress-dot { display: inline-block; width: 0.6em; height: 0.6em; border-radius: 50%; background: var(--color-accent); margin: 0 0.15em; }
---

<!-- _class: lead -->
<!-- _paginate: false -->

<div class="badge-row"><span class="badge tnc">TNC55</span><span class="badge chapter">அத்தியாயம் 1</span><span class="badge part">பகுதி 5</span></div>

# அடிப்படைக் கருத்துகள் = <span class="word-root">நெறிமுறை</span> + <span class="word-root">சாரப்படுத்தல்</span> + <span class="word-root">தோன்றுமியல்பு</span>

## Algorithm · Abstraction · Emergence: 15 நிமிட நுண் பயிலரங்கு

நூல்: AI அலை: நீங்கள் தயாரா? | நுண் பயிலரங்கு

<img class="logo" src="https://cdn.jsdelivr.net/gh/kpassoubady/marp-themes@v10/term-chair/logo.png" />

---

# AI-ன் கட்டுமான அடித்தளம்

நெறிமுறை, சாரப்படுத்தல், தோன்றுமியல்பு ஆகிய அடிப்படைக் கருத்துகள் AI-ன் கட்டுமானத்தில் இன்றியமையாதவை. இவை மூன்றும் ஒன்றோடொன்று தொடர்புடையவை.

---

<!-- _class: term -->

# Algorithm: <span class="tamil">நெறிமுறை</span>

<span class="word-root">நெறி</span> (method/rule) + <span class="word-root">முறை</span> (procedure)

ஒரு வேலையைச் செய்ய அல்லது சிக்கலைத் தீர்க்கத் தேவையான துல்லியமான படிநிலை வரிசை.

<div class="industry-badge">உதாரணம்</div>
சரிவிறக்கம் (Gradient Descent), A* தேடல் ஆகியவை நெறிமுறைகளுக்கு எடுத்துக்காட்டுகள்.

---

<!-- _class: term -->

# Abstraction: <span class="tamil">சாரப்படுத்தல்</span>

<span class="word-root">சாரம்</span> (essence) + <span class="word-root">படுத்தல்</span> (to render)

விவரங்களை மறைத்துப் பொதுக் கருத்தை அல்லது இடைமுகத்தை மட்டும் வெளிக்காட்டுதல். கணினியியலின் அடிப்படைக் கருத்துகளில் ஒன்று.

---

<!-- _class: term -->

# Emergence: <span class="tamil">தோன்றுமியல்பு</span>

<span class="word-root">தோன்றும்</span> (arising) + <span class="word-root">இயல்பு</span> (nature)

சிறிய கூறுகளின் சேர்க்கையால், அவை தனித்தனியாகக் கொண்டிராத புதிய பண்புகள் தற்செயலாக வெளிப்படும் நிகழ்வு.

---

<!-- _class: term -->

# Emergent Abilities: <span class="tamil">வெளிப்படும் திறன்கள்</span>

AI மாதிரியின் அளவு பெருகும்போது, சிறிய மாதிரிகளில் இல்லாத புதிய திறன்கள் தற்செயலாக வெளிப்படும் நிகழ்வு.

<p class="progress-dot"></p><span style="font-size:0.8em; color:var(--color-text-light)">நெறிமுறை &rarr; சாரப்படுத்தல் &rarr; தோன்றுமியல்பு &rarr; வெளிப்படும் திறன்கள்</span>

> 📌 உதாரணம்: 10 பில்லியன் அளபுருவில் இல்லாத திறன், 100 பில்லியனில் தானாகத் தோன்றுகிறது.

---

<!-- _class: discussion -->

# விவாதம்

பெருமொழி மாதிரிகளில் (LLMs) வெளிப்படும் திறன்கள் (Emergent Abilities) தற்செயலாகத் தோன்றுகின்றன. இத்தகைய திறன்களை முன்கூட்டியே கணிக்க இயலுமா?

---

<!-- _class: discussion-answer -->

# திருப்பிப் பாருங்கள்

நெறிமுறை (Algorithm) &rarr; சாரப்படுத்தல் (Abstraction) &rarr; தோன்றுமியல்பு (Emergence) &rarr; வெளிப்படும் திறன்கள் (Emergent Abilities). ஒவ்வொரு கருத்தும் அடுத்ததற்கு அடித்தளம்.

---

# இன்று கற்ற 4 சொற்கள்

<div class="term-grid recap">
<div class="term-card"><span class="tag">கருத்து</span><h3>நெறிமுறை</h3><p>Algorithm</p></div>
<div class="term-card"><span class="tag">கருத்து</span><h3>சாரப்படுத்தல்</h3><p>Abstraction</p></div>
<div class="term-card"><span class="tag">கருத்து</span><h3>தோன்றுமியல்பு</h3><p>Emergence</p></div>
<div class="term-card"><span class="tag">கருத்து</span><h3>வெளிப்படும் திறன்கள்</h3><p>Emergent Abilities</p></div>
</div>

---

<!-- _class: lead -->
<!-- _paginate: false -->

<div class="badge-row"><span class="badge tnc">TNC55</span><span class="badge chapter">அத்தியாயம் 1</span><span class="badge part">பகுதி 6</span></div>

# அடுத்து: அணுகுமுறைகள்

அடிப்படைக் கருத்துகள்: முடிந்தது

<span style="font-size:0.55em; color:rgba(253,249,240,0.75)">கங்கா வளர் தொழில்நுட்பக் கலைச்சொல் ஆய்விருக்கை, யூ.எஸ்.ஏ.<br>Ganga Emerging Technology Terminology Research Chair, USA</span>

<img class="logo" src="https://cdn.jsdelivr.net/gh/kpassoubady/marp-themes@v10/term-chair/logo.png" />
