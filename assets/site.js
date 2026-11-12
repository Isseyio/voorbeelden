(() => {
  // Profielfoto van Issey: vervangt het monogram zodra assets/issey.jpg bestaat.
  const monos = document.querySelectorAll('.me-mono');
  if (!monos.length) return;
  const im = new Image();
  im.onload = () => monos.forEach(el => {
    const i = document.createElement('img');
    i.className = 'me-photo'; i.src = im.src; i.alt = 'Issey Kooijmans'; i.width = 112; i.height = 112;
    el.replaceWith(i);
  });
  // Eerst de eigen kopie in de repo, anders de foto uit Issey's handtekening (Framer).
  const fallback = 'https://framerusercontent.com/images/XVQUjl2gQ9UFJzeQzPjpBYq510.jpg?scale-down-to=256';
  im.onerror = () => { if (im.src !== fallback) im.src = fallback; };
  im.src = new URL('../assets/issey.jpg', document.baseURI).href;
})();
(() => {
  document.querySelectorAll('.mail-more').forEach(b => b.addEventListener('click', () => b.closest('.mail-frame').classList.add('open')));
  const dlg = document.querySelector('.lb');
  if (!dlg) return;
  const track = dlg.querySelector('.lb-track');
  const slides = [...dlg.querySelectorAll('.lb-slide')];
  const count = dlg.querySelector('.lb-count');
  const cur = () => Math.round(track.scrollLeft / track.clientWidth);
  const label = () => { count.textContent = `${cur() + 1} / ${slides.length}`; };
  const go = (i, smooth = true) => {
    i = Math.max(0, Math.min(slides.length - 1, i));
    track.scrollTo({ left: i * track.clientWidth, behavior: smooth ? 'smooth' : 'auto' });
  };
  document.querySelectorAll('.ad-btn').forEach(b => b.addEventListener('click', () => {
    dlg.showModal();
    document.documentElement.style.overflow = 'hidden';
    requestAnimationFrame(() => { go(+b.dataset.i, false); label(); });
  }));
  const close = () => dlg.close();
  dlg.addEventListener('close', () => { document.documentElement.style.overflow = ''; });
  dlg.querySelector('.lb-close').addEventListener('click', close);
  dlg.querySelector('.lb-prev').addEventListener('click', () => go(cur() - 1));
  dlg.querySelector('.lb-next').addEventListener('click', () => go(cur() + 1));
  track.addEventListener('scroll', () => requestAnimationFrame(label), { passive: true });
  track.addEventListener('click', e => { if (e.target === track || e.target.classList.contains('lb-slide')) close(); });
  dlg.addEventListener('keydown', e => {
    if (e.key === 'ArrowRight') go(cur() + 1);
    if (e.key === 'ArrowLeft') go(cur() - 1);
  });
})();

(() => {
  // Rekenblok "Wat kan dit opleveren?": voor de week-sectie op elke voorbeeldpagina.
  const week = document.querySelector('.week');
  const anchor = week && week.closest('section');
  if (!anchor || document.querySelector('.calc-sec')) return;
  const m = document.title.match(/Voorbeelden voor (.+?) ·/);
  const merk = m ? m[1] : '';
  const eur = new Intl.NumberFormat('nl-NL', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 });
  const num = new Intl.NumberFormat('nl-NL');
  const nice = v => { const step = v < 2000 ? 10 : v < 20000 ? 50 : 100; return Math.round(v / step) * step; };
  // Branchegemiddelden: omzet per ontvanger van een nieuwsbrief (Klaviyo) en omzet per euro advertentiebudget (Meta, e-commerce).
  const RPR = [0.05, 0.10, 0.15], ROAS = [2, 2.5, 3], MAILS = 4, DAGEN = 30;
  const sec = document.createElement('section');
  sec.className = 'sec calc-sec';
  sec.id = 'rekenvoorbeeld';
  sec.innerHTML = `
    <div class="wrap">
      <p class="eyebrow">Rekenvoorbeeld</p>
      <h2>Wat kan dit opleveren${merk ? ' voor ' + merk.replace(/</g, '&lt;') : ''}?</h2>
      <p class="lead">Schuif met de balken en zie wat een nieuwsbrief of een vast advertentiebudget vaak oplevert.</p>
      <div class="calc-grid">
        <div class="calc">
          <span class="calc-tag"><i></i>Nieuwsbrief</span>
          <label for="calc-lijst">Mensen op jullie e-maillijst <output id="calc-lijst-v"></output></label>
          <input type="range" id="calc-lijst" min="1000" max="50000" step="500" value="10000">
          <div class="scale"><span>1.000</span><span>50.000</span></div>
          <div class="calc-out"><strong id="calc-mail"></strong><span>omzet per nieuwsbrief</span><em id="calc-mail-sub"></em></div>
        </div>
        <div class="calc">
          <span class="calc-tag adv"><i></i>Advertenties</span>
          <label for="calc-budget">Advertentiebudget per dag <output id="calc-budget-v"></output></label>
          <input type="range" id="calc-budget" min="10" max="300" step="5" value="50">
          <div class="scale"><span>€&nbsp;10</span><span>€&nbsp;300</span></div>
          <div class="calc-out"><strong id="calc-ads"></strong><span>omzet per maand</span><em id="calc-ads-sub"></em></div>
        </div>
      </div>
      <p class="small">Rekenvoorbeeld op basis van gemiddelden uit de branche: een nieuwsbrief levert vaak zo'n €&nbsp;0,05 tot €&nbsp;0,15 omzet per ontvanger op (Klaviyo), advertenties op Instagram en Facebook vaak zo'n 2 tot 3 keer het budget (e-commerce). Geen garantie: jullie eigen cijfers kunnen hoger of lager uitvallen.</p>
    </div>`;
  anchor.before(sec);
  const $ = id => sec.querySelector('#' + id);
  const fill = el => el.style.setProperty('--p', ((el.value - el.min) / (el.max - el.min) * 100) + '%');
  const update = () => {
    const lijst = +$('calc-lijst').value, budget = +$('calc-budget').value;
    $('calc-lijst-v').textContent = num.format(lijst);
    $('calc-mail').textContent = '±\u00a0' + eur.format(nice(lijst * RPR[1]));
    $('calc-mail-sub').textContent = `Vaak tussen ${eur.format(nice(lijst * RPR[0]))} en ${eur.format(nice(lijst * RPR[2]))}. Met ${MAILS} nieuwsbrieven per maand: ±\u00a0${eur.format(nice(lijst * RPR[1] * MAILS))}.`;
    const maand = budget * DAGEN;
    $('calc-budget-v').textContent = eur.format(budget);
    $('calc-ads').textContent = '±\u00a0' + eur.format(nice(maand * ROAS[1]));
    $('calc-ads-sub').textContent = `Vaak tussen ${eur.format(nice(maand * ROAS[0]))} en ${eur.format(nice(maand * ROAS[2]))}, bij ${eur.format(maand)} budget per maand.`;
    sec.querySelectorAll('input[type=range]').forEach(fill);
  };
  sec.querySelectorAll('input[type=range]').forEach(el => el.addEventListener('input', update));
  update();
})();
