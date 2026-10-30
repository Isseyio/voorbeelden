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
