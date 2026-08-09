---
marp: true
theme: default
paginate: true
header: "அணுகுமுறைகள்"
footer: "AI அலை: நீங்கள் தயாரா? தமிழில் 300+ செய்யறிவுக் கலைச்சொற்கள்"
style: |
  @import url("https://cdn.jsdelivr.net/gh/kpassoubady/marp-themes@v9/term-chair/term-chair.css");
  section { animation: fadeIn 0.6s ease-in; }
  @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
  .term-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1em; margin-top: 0.6em; }
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
  .img-text-grid { display: grid; grid-template-columns: 300px 1fr; gap: 1.8em; align-items: center; margin-top: 0.8em; }
  .img-text-grid img { width: 300px; height: 300px; object-fit: cover; border-radius: 10px; border: 3px solid var(--color-accent); }
  .img-text-grid .quote { font-size: 1.3em; font-weight: 700; color: var(--color-primary); margin: 0 0 0.4em; }
  .img-text-grid.size-350 { grid-template-columns: 350px 1fr; }
  .img-text-grid.size-350 img { width: 350px; height: 350px; }
  section.lead h1 { font-size: 1.6em; white-space: nowrap; }
---

<!-- _class: lead -->
<!-- _paginate: false -->

<div class="badge-row"><span class="badge chapter">அத்தியாயம் 1</span><span class="badge part">பகுதி 6</span></div>

# அணுகுமுறைகள் = <span class="word-root">குறி</span> + <span class="word-root">இயக்கியம்</span>

## Connectionism · Symbolism: 15 நிமிட நுண் பயிலரங்கு

நூல்: AI அலை: நீங்கள் தயாரா? | நுண் பயிலரங்கு

<img class="logo" src="https://cdn.jsdelivr.net/gh/kpassoubady/marp-themes@v9/term-chair/logo.png" />

---

# இருவெவ்வேறு சிந்தனைப் பள்ளிகள்

செய்யறிவின் அடிப்படையில் இரு முதன்மை அணுகுமுறைகள் இருக்கின்றன. ஒன்று விதிகளையும் ஏரணத்தையும் நம்பியது. மற்றொன்று நரம்பணு வலைப்பின்னலை ஒத்திருக்க முயன்றது. இன்றைய பெருமொழி மாதிரிகள் இவ்விரண்டின் கலவையிலிருந்து பிறந்தவை.

---

# AI அணுகுமுறைகள் வரைபடம்

<img src="../assets/diagrams/01-ai-approaches.svg" alt="AI அணுகுமுறைகள்" style="display:block; margin:0 auto; max-height:420px;" />

---

<!-- _class: term -->

# Symbolism: <span class="tamil">குறியியக்கியம்</span>

<span class="word-root">குறி</span> (sign/symbol) + <span class="word-root">இயக்கியம்</span> (-ism / theory)

விதிகளையும் ஏரணத்தையும் பயன்படுத்தித் தரவுகளைக் குறியீடுகள் மூலம் மனித அறிவாகக் கணினிக்குப் புகட்டும் முற்காலச் செய்யறிவு அணுகுமுறை.

> 📌 மாற்றுச் சொல்: குறியீட்டு அணுகுமுறை

---

<!-- _class: term -->

# Connectionism: <span class="tamil">இணைப்புக்கொள்கை</span>

<span class="word-root">இணைப்பு</span> (connection) + <span class="word-root">கொள்கை</span> (theory)

மூளையின் நரம்பணு வலைப்பின்னலைப் போலக் கணினி அமைப்புகளையும் ஒன்றோடொன்று இணைத்துச் செயல்பட வைக்கும் அணுகுமுறை.

> 📌 மாற்றுச் சொல்: இணைப்பியக்கம்

---

<!-- _class: chat-check -->

# வினா: இது எந்த அணுகுமுறை?

"மூளையின் நரம்பணு வலைப்பின்னலைப் போலக் கணினி அமைப்புகளை இணைத்துச் செயல்பட வைக்கும் அணுகுமுறை"

<div class="gfm-alert gfm-note">
<div class="gfm-alert-title">Discuss</div>
<p>அறையில் உள்ளவர்களே பதில் சொல்லுங்கள்! 10 வினாடிகள்.</p>
</div>

---

<!-- _class: chat-check-answer -->

# விடை: இணைப்புக்கொள்கை (Connectionism)

குறியியக்கியம் (Symbolism) விதிகளையும் ஏரணத்தையும் நம்பியது. இணைப்புக்கொள்கை (Connectionism) நரம்பணு வலைப்பின்னலை ஒத்தது. இன்றைய நரவலைகள் (Neural Networks) இணைப்புக்கொள்கையிலிருந்து வந்தவை.

---

# 📰 AI வரலாற்றில் ஒரு துளி

<div class="img-text-grid size-350">
<div>

<img src="../assets/images/drop-in-history-ch01.png" alt="டார்ட்மவுத் மாநாடு 1956" />

</div>
<div>

1956, டார்ட்மவுத் கல்லூரி. ஜான் மெக்கார்த்தி மற்றும் மார்வின் மின்ஸ்கி "செயற்கை நுண்ணறிவு" என்ற சொல்லை முதன்முதலில் பயன்படுத்தினர். அந்த முதல் தலைமுறை AI முழுக்க குறியியக்கியத்தை (Symbolism) நம்பியிருந்தது.

அவர்கள் நினைத்தது: "ஒரே கோடைகாலத்தில் முடிந்துவிடும்." உண்மையில் அது இன்னும் தொடரும் பயணம்.

</div>
</div>

---

# இன்று கற்ற 2 சொற்கள்

<div class="term-grid recap">
<div class="term-card"><span class="tag">அணுகுமுறை</span><h3>குறியியக்கியம்</h3><p>Symbolism: விதிசார்</p></div>
<div class="term-card"><span class="tag">அணுகுமுறை</span><h3>இணைப்புக்கொள்கை</h3><p>Connectionism: நரம்பணு சார்</p></div>
</div>

---

<!-- _class: lead -->
<!-- _paginate: false -->

<div class="badge-row"><span class="badge chapter">அத்தியாயம் 1</span><span class="badge part">பகுதி 6</span></div>

# நன்றி!

அணுகுமுறைகள்: அத்தியாயம் 1 நிறைவு
ஆசிரியர்: காங்கேயன் பசுபதி

<span style="font-size:0.55em; color:rgba(253,249,240,0.75)">கங்கா வளர் தொழில்நுட்பக் கலைச்சொல் ஆய்விருக்கை, யூ.எஸ்.ஏ.<br>Ganga Emerging Technology Terminology Research Chair, USA</span>

<img class="logo" src="https://cdn.jsdelivr.net/gh/kpassoubady/marp-themes@v9/term-chair/logo.png" />
