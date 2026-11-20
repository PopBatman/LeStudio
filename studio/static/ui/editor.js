const editor = document.querySelector('.ed-workshop');
const statusMessage = document.getElementById('ed-status');
const errorSummary = document.getElementById('ed-error');
if (errorSummary) {
  errorSummary.focus();
} else if (document.getElementById('ed-observation')) {
  document.getElementById('ed-observation').focus();
} else if (statusMessage.textContent.trim()) {
  // Focus a surviving landmark after a redirect, including after a removal.
  const inspector = document.getElementById('inspecteur');
  inspector?.setAttribute('aria-describedby', 'ed-status');
  inspector?.focus();
}
editor.addEventListener('submit', (event) => {
  const form = event.target;
  if (form.method !== 'post') return;
  if (form.getAttribute('aria-busy') === 'true') {
    event.preventDefault();
    return;
  }
  form.setAttribute('aria-busy', 'true');
  if (event.submitter?.value === 'verify') {
    statusMessage.textContent = 'Vérification de la source Wagtail en cours…';
  } else {
    statusMessage.textContent = event.submitter?.name === 'relire' ? 'Relecture en cours…' : 'Enregistrement en cours…';
  }
});
window.addEventListener('pageshow', (event) => {
  if (event.persisted) {
    editor.querySelectorAll('[aria-busy]').forEach(form => form.removeAttribute('aria-busy'));
    statusMessage.textContent = '';
  }
});

const positionData = document.getElementById('ed-sibling-parents');
if (positionData) {
  const parents = JSON.parse(positionData.textContent);
  const destination = document.getElementById('id_parent');
  const position = document.getElementById('id_before');
  const siblings = Array.from(position.options);
  function showPositions() {
    const selection = position.value;
    const available = siblings.filter(option => !option.value || parents[option.value] === destination.value);
    position.replaceChildren(...available);
    position.value = available.some(option => option.value === selection) ? selection : '';
  }
  if (parents && typeof parents === 'object') {
    destination.addEventListener('change', showPositions);
    showPositions();
  }
}
