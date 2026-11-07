/* CT-Dent · site.js — theme, nav, motion, consent, forms */
(function(){
  'use strict';
  var doc = document.documentElement;

  /* ---------- theme ---------- */
  function applyTheme(t){
    doc.setAttribute('data-theme', t);
    var btn = document.getElementById('themeToggle');
    if(btn){ btn.setAttribute('aria-pressed', String(t === 'dark')); }
    try{ localStorage.setItem('ctdent-theme', t); }catch(e){}
  }
  var tt = document.getElementById('themeToggle');
  if(tt) tt.addEventListener('click', function(){
    applyTheme(doc.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
  });

  /* ---------- mobile nav ---------- */
  var burger = document.getElementById('burger'), nav = document.getElementById('mainNav');
  if(burger && nav){
    burger.addEventListener('click', function(){
      var open = nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', String(open));
    });
  }

  /* ---------- reveals + counters ---------- */
  if('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('on'); io.unobserve(e.target); } });
    }, {threshold:.12});
    document.querySelectorAll('.rv').forEach(function(el){ io.observe(el); });

    var cio = new IntersectionObserver(function(es){
      es.forEach(function(e){
        if(!e.isIntersecting) return; cio.unobserve(e.target);
        var el = e.target, target = +el.getAttribute('data-count'), suf = el.getAttribute('data-suffix') || '';
        var dur = 1200, t0 = performance.now();
        (function tick(t){
          var p = Math.min(1, (t - t0) / dur), v = Math.round(target * (0.2 + 0.8 * p * p));
          el.textContent = String(v).replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + suf;
          if(p < 1) requestAnimationFrame(tick);
        })(t0);
      });
    }, {threshold:.4});
    document.querySelectorAll('[data-count]').forEach(function(el){ cio.observe(el); });
  } else {
    document.querySelectorAll('.rv').forEach(function(el){ el.classList.add('on'); });
  }

  /* ---------- cookie consent (GDPR: reject = as easy as accept) ---------- */
  var CKEY = 'ctdent-consent';
  function getConsent(){ try{ return JSON.parse(localStorage.getItem(CKEY)); }catch(e){ return null; } }
  function setConsent(o){ o.ts = Date.now(); try{ localStorage.setItem(CKEY, JSON.stringify(o)); }catch(e){} }
  var banner = document.getElementById('cookieBanner');
  if(banner && !getConsent()){ banner.classList.remove('hidden'); }
  function updateCkOffset(){
    if(!banner) return;
    var open = !banner.classList.contains('hidden');
    document.body.classList.toggle('ck-open', open);
    if(open){ document.body.style.setProperty('--ckh', banner.offsetHeight + 'px'); }
  }
  banner && banner.addEventListener('transitionend', updateCkOffset);
  window.addEventListener('resize', updateCkOffset);
  updateCkOffset();
  function closeBanner(){ if(banner){ banner.classList.add('hidden'); updateCkOffset(); } }
  function bind(id, fn){ var el = document.getElementById(id); if(el) el.addEventListener('click', fn); }
  bind('ckAccept', function(){ setConsent({necessary:true, analytics:true, marketing:true}); closeBanner(); });
  bind('ckReject', function(){ setConsent({necessary:true, analytics:false, marketing:false}); closeBanner(); });
  bind('ckPrefs', function(){
    var p = document.getElementById('cookiePrefs');
    if(p){ p.classList.toggle('open'); updateCkOffset(); setTimeout(updateCkOffset, 400); }
  });
  bind('ckSave', function(){
    var a = document.getElementById('ckAnalytics'), m = document.getElementById('ckMarketing');
    setConsent({necessary:true, analytics:!!(a && a.checked), marketing:!!(m && m.checked)});
    closeBanner();
  });
  bind('ckReopen', function(ev){
    ev.preventDefault();
    if(banner){ banner.classList.remove('hidden');
      var p = document.getElementById('cookiePrefs'); if(p) p.classList.add('open'); updateCkOffset(); setTimeout(updateCkOffset, 400); }
  });

  /* ---------- corner capsule: info card ---------- */
  var cdInfo = document.getElementById('cdInfo'), cdCard = document.getElementById('cdCard');
  if(cdInfo && cdCard){
    cdInfo.addEventListener('click', function(ev){
      ev.stopPropagation();
      var o = cdCard.classList.toggle('open');
      cdInfo.setAttribute('aria-expanded', String(o));
    });
    document.addEventListener('click', function(ev){
      if(!cdCard.contains(ev.target) && cdCard.classList.contains('open')){
        cdCard.classList.remove('open'); cdInfo.setAttribute('aria-expanded', 'false');
      }
    });
    document.addEventListener('keydown', function(ev){
      if(ev.key === 'Escape' && cdCard.classList.contains('open')){
        cdCard.classList.remove('open'); cdInfo.setAttribute('aria-expanded', 'false'); cdInfo.focus();
      }
    });
  }
  (function(){
    var d = new Date().getDay();
    if(d >= 1 && d <= 5){
      var hr = document.getElementById('cdHours'), tg = document.getElementById('cdToday');
      if(hr) hr.classList.add('today');
      if(tg) tg.hidden = false;
    }
  })();

  /* ---------- forms → mailto fallback ---------- */
  var CONTACT_EMAIL = 'info@ct-dent.lv'; /* info@ tiek izveidots; rezerves pastkastīte: ctdentriga@gmail.com */
  function fieldWrap(input){ return input.closest('.field'); }
  document.querySelectorAll('form[data-mailto]').forEach(function(form){
    form.addEventListener('submit', function(ev){
      ev.preventDefault();
      var ok = true, lines = [];
      var subject = form.getAttribute('data-subject') || 'CT-Dent';
      form.querySelectorAll('input,textarea,select').forEach(function(inp){
        var w = fieldWrap(inp);
        if(w) w.classList.remove('invalid');
        if(inp.type === 'checkbox'){
          if(inp.required && !inp.checked){ ok = false; if(w) w.classList.add('invalid'); }
          else if(inp.checked){
            var lbl = form.querySelector('label[for="' + inp.id + '"]');
            lines.push((lbl ? lbl.textContent.trim() : inp.name) + ': ' + (inp.value || 'on'));
          }
          return;
        }
        if(inp.type === 'radio'){
          if(inp.checked) lines.push(inp.name + ': ' + (inp.value || ''));
          return;
        }
        var val = (inp.value || '').trim();
        if(inp.required && !val){ ok = false; if(w) w.classList.add('invalid'); return; }
        if(inp.type === 'email' && val && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)){ ok = false; if(w) w.classList.add('invalid'); return; }
        if(val){
          var lab = form.querySelector('label[for="' + inp.id + '"]');
          lines.push((lab ? lab.textContent.trim() : inp.name) + ': ' + val);
        }
      });
      var status = form.querySelector('[data-formstatus]');
      if(!ok){
        if(status){ status.textContent = status.getAttribute('data-err-text') || 'ERROR'; status.hidden = false; }
        var firstBad = form.querySelector('.field.invalid input,.field.invalid textarea');
        if(firstBad) firstBad.focus();
        return;
      }
      var body = lines.join('\n');
      window.location.href = 'mailto:' + CONTACT_EMAIL +
        '?subject=' + encodeURIComponent(subject) +
        '&body=' + encodeURIComponent(body);
      if(status){ status.textContent = status.getAttribute('data-ok-text') || 'OK'; status.hidden = false; }
    });
  });
})();
