/**
 * Progressive enhancement for lead forms.
 * Without JS the form posts to the PHP endpoint, which redirects to the thank-you page.
 * With JS: inline validation, async submit, refined inline confirmation, conversion event.
 */
type Messages = {
  required: string;
  email: string;
  phone: string;
  date: string;
  consent: string;
  invalid: string;
  sending: string;
  error: string;
};

const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const PHONE = /^\+?[0-9 ()./-]{6,20}$/;

function setError(el: HTMLElement, msg: string) {
  const field = el.closest('.field, .choice, .consent-wrap');
  const err = field?.querySelector<HTMLElement>('.field__err, .choice__err');
  if (msg) el.setAttribute('aria-invalid', 'true');
  else el.removeAttribute('aria-invalid');
  if (err) err.textContent = msg;
}

function validate(form: HTMLFormElement, m: Messages): HTMLElement | null {
  let first: HTMLElement | null = null;
  const controls = form.querySelectorAll<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>('input, select, textarea');
  const seenRadio = new Set<string>();
  controls.forEach((el) => {
    if (el.closest('.hp') || el.type === 'hidden') return;
    let msg = '';
    const v = el.value.trim();
    if (el instanceof HTMLInputElement && el.type === 'radio') {
      if (seenRadio.has(el.name)) return;
      seenRadio.add(el.name);
      const group = form.querySelectorAll<HTMLInputElement>(`input[name="${el.name}"]`);
      const checked = Array.from(group).some((r) => r.checked);
      if (el.required && !checked) msg = m.required;
      const fs = el.closest('fieldset') as HTMLElement | null;
      if (fs) setError(fs, msg);
      if (msg && !first) first = el;
      return;
    }
    if (el instanceof HTMLInputElement && el.type === 'checkbox') {
      if (el.required && !el.checked) msg = m.consent;
    } else if (el.required && !v) msg = m.required;
    else if (v && el.type === 'email' && !EMAIL.test(v)) msg = m.email;
    else if (v && el.type === 'tel' && !PHONE.test(v)) msg = m.phone;
    else if (v && el.type === 'date') {
      const d = new Date(v + 'T23:59:59');
      if (Number.isNaN(d.getTime()) || d.getTime() < Date.now()) msg = m.date;
    }
    setError(el, msg);
    if (msg && !first) first = el;
  });
  return first;
}

export function initForm(form: HTMLFormElement) {
  if (form.dataset.ready) return;
  form.dataset.ready = '1';
  const m = JSON.parse(form.dataset.messages || '{}') as Messages;
  const status = form.querySelector<HTMLElement>('[data-form-status]');
  const submit = form.querySelector<HTMLButtonElement>('[type="submit"]');
  const done = document.getElementById(form.dataset.done || '');
  const started = form.querySelector<HTMLInputElement>('input[name="_t"]');
  if (started) started.value = String(Date.now());
  form.noValidate = true;

  const today = new Date();
  today.setMinutes(today.getMinutes() - today.getTimezoneOffset());
  form.querySelectorAll<HTMLInputElement>('input[type="date"]').forEach((d) => (d.min = today.toISOString().slice(0, 10)));

  form.addEventListener('input', (e) => {
    const el = e.target as HTMLElement;
    if (el.getAttribute('aria-invalid') === 'true') setError(el, '');
    if (el instanceof HTMLInputElement && el.type === 'radio') {
      const fs = el.closest('fieldset');
      if (fs) setError(fs as HTMLElement, '');
    }
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const first = validate(form, m);
    if (first) {
      if (status) {
        status.dataset.state = 'error';
        status.textContent = m.invalid;
      }
      first.focus();
      return;
    }
    submit?.setAttribute('aria-busy', 'true');
    const label = submit?.innerHTML;
    if (submit) submit.textContent = m.sending;
    if (status) {
      status.dataset.state = '';
      status.textContent = '';
    }
    try {
      const res = await fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' },
      });
      const data = (await res.json().catch(() => ({}))) as { ok?: boolean; errors?: Record<string, string> };
      if (!res.ok || !data.ok) {
        if (data.errors) {
          for (const [name, msg] of Object.entries(data.errors)) {
            const el = form.querySelector<HTMLElement>(`[name="${name}"]`);
            if (el) setError(el, msg);
          }
        }
        throw new Error('send_failed');
      }
      const event = form.dataset.event || 'quote_request';
      const type = (form.querySelector<HTMLInputElement | HTMLSelectElement>('[name="event_type"], [name="partner_type"]:checked')?.value) || undefined;
      window.meteoraTrack?.(event, { form: form.dataset.form, type, page_path: location.pathname });
      form.hidden = true;
      if (done) {
        done.hidden = false;
        done.focus();
        done.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    } catch {
      if (status) {
        status.dataset.state = 'error';
        status.innerHTML = `${m.error} <a href="mailto:info@meteoraevents.com">info@meteoraevents.com</a>.`;
      }
    } finally {
      submit?.removeAttribute('aria-busy');
      if (submit && label) submit.innerHTML = label;
    }
  });
}

export function initForms() {
  document.querySelectorAll<HTMLFormElement>('form[data-lead-form]').forEach(initForm);
}
