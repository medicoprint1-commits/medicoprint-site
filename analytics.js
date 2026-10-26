/* Google Analytics : chargement uniquement après accord du visiteur. */
(() => {
  'use strict';
  const id = window.MEDICOPRINT_ANALYTICS_ID;
  if (!/^G-[A-Z0-9]+$/.test(id || '') || location.protocol === 'file:') return;
  const key = 'medicoprint-analytics-consent-v1';
  let choice;
  let started = false;
  try { choice = localStorage.getItem(key); } catch (_) { /* Choix limité à la page. */ }
  window.dataLayer = window.dataLayer || [];
  const gtag = function () { window.dataLayer.push(arguments); };
  const consent = (analytics) => ({
    analytics_storage: analytics,
    ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'
  });
  gtag('consent', 'default', consent('denied'));
  function start() {
    if (started) return;
    started = true;
    window['ga-disable-' + id] = false;
    gtag('consent', 'update', consent('granted'));
    gtag('js', new Date());
    // Ne pas transmettre les paramètres d'URL, les ancres ou les titres de page.
    const cleanURL = (url) => {
      const parsed = new URL(url);
      return parsed.origin + parsed.pathname;
    };
    gtag('config', id, {
      page_location: cleanURL(location.href), page_title: 'MEDICOPRINT',
      page_referrer: document.referrer ? cleanURL(document.referrer) : '',
      allow_google_signals: false, allow_ad_personalization_signals: false,
      send_page_view: true
    });
    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + id;
    document.head.appendChild(script);
  }
  function save(value) {
    choice = value;
    try { localStorage.setItem(key, value); } catch (_) { /* Aucun stockage disponible. */ }
    banner.hidden = true;
    if (value === 'accepted') start();
    else if (started) {
      window['ga-disable-' + id] = true;
      gtag('consent', 'update', consent('denied'));
      location.reload();
    }
  }
  const style = document.createElement('style');
  style.textContent = '.mp-consent{position:fixed;bottom:18px;left:18px;right:18px;z-index:9999;max-width:620px;padding:20px;background:#fff;color:#172c32;border:1px solid #007b70;border-radius:12px;box-shadow:0 4px 24px #0003;font:15px/1.5 Arial,sans-serif}.mp-consent[hidden]{display:none}.mp-consent p{margin:0 0 12px}.mp-consent button,.mp-consent-settings{padding:10px 14px;margin:4px;border:1px solid #007b70;border-radius:6px;background:#fff;color:#005f56;cursor:pointer;font:14px Arial,sans-serif}.mp-consent-settings{display:block;margin:18px auto}';
  document.head.appendChild(style);
  const banner = document.createElement('section');
  banner.className = 'mp-consent';
  banner.setAttribute('aria-label', 'Mesure d’audience');
  const message = document.createElement('p');
  message.textContent = 'Acceptez-vous les cookies Google Analytics pour mesurer les visites de ce site ? Les données de navigation sont transmises à Google. Vous pouvez refuser et modifier votre choix à tout moment.';
  banner.appendChild(message);
  for (const [label, value] of [['Accepter', 'accepted'], ['Refuser', 'denied']]) {
    const button = document.createElement('button');
    button.type = 'button'; button.textContent = label;
    button.addEventListener('click', () => save(value));
    banner.appendChild(button);
  }
  banner.hidden = choice === 'accepted' || choice === 'denied';
  document.body.appendChild(banner);
  const settings = document.createElement('button');
  settings.type = 'button'; settings.className = 'mp-consent-settings';
  settings.textContent = 'Mes préférences de mesure d’audience';
  settings.addEventListener('click', () => {
    banner.hidden = false; banner.querySelector('button').focus();
  });
  document.body.appendChild(settings);
  if (choice === 'accepted') start();
})();
