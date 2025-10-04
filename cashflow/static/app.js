async function fillSelect(url, selectEl, selectedValue) {
  if (!selectEl) return;
  selectEl.innerHTML = '<option value="">— любой —</option>';
  const res = await fetch(url);
  const data = await res.json();
  const items = Array.isArray(data) ? data : (data.results || data);
  for (const item of items) {
    const opt = document.createElement('option');
    opt.value = item.id; opt.textContent = item.name || item.title || (`#${item.id}`);
    if (selectedValue && String(selectedValue) === String(item.id)) opt.selected = true;
    selectEl.appendChild(opt);
  }
}
