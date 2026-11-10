(() => {
  const page = document.querySelector('.reader-page');
  if (!page) return;
  let raised = false;
  const liftOnce = () => {
    if (!raised && window.scrollY > 24) {
      raised = true;
      page.classList.add('is-raised');
      window.removeEventListener('scroll', liftOnce);
    }
  };
  window.addEventListener('scroll', liftOnce, { passive: true });
})();
