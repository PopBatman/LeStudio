(() => {
  const exchange = document.getElementById("exchange");
  function openInvitation() {
    if (!exchange || !location.hash || location.hash === "#contenu") return;
    const code = location.hash.slice(1);
    history.replaceState(null, "", location.pathname);
    const field = document.getElementById("invite-code");
    field.value = code;
    exchange.requestSubmit();
  }
  openInvitation();
  window.addEventListener("hashchange", openInvitation);
  const target = document.querySelector('[aria-invalid="true"], [data-feedback]');
  if (target) target.focus();
})();
