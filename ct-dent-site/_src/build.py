# -*- coding: utf-8 -*-
"""CT-Dent static site generator. Run: python3 build.py  (output: ../public)"""
import os, re, json, shutil, html
from content import (LANGS, PREFIX, SITE, PHONE, PHONE_HREF, ADDR, HOURS, TIMES, EMAIL, COMMON, P)

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, '..', 'public')
ASSETS = '/assets'

def e(s): return html.escape(s, quote=True)

def url_for(lang, slug):
    return '/' + PREFIX[lang] + (slug + '/' if slug else '')

def abs_url(lang, slug):
    return SITE + PREFIX[lang] + (slug + '/' if slug else '')

def asset(p): return ASSETS + '/' + p

# ------------------------------------------------------------------ shared bits
def logo_svg(lang):
    tag = {'lv': 'ZOBU SKENĒŠANAS CENTRS', 'en': 'DENTAL SCANNING CENTRE', 'ru': 'ЦЕНТР ЗУБНОГО СКАНИРОВАНИЯ'}[lang]
    return ('<svg viewBox="0 0 250 66" role="img" aria-label="CT-Dent" class="logo-svg">'
            '<text x="2" y="42" font-family="Manrope,system-ui,sans-serif" font-size="36" font-weight="700" fill="currentColor" letter-spacing="-1">CT</text>'
            '<circle cx="76" cy="30" r="6.5" fill="#9dc300"/>'
            '<text x="90" y="42" font-family="Manrope,system-ui,sans-serif" font-size="36" font-weight="300" fill="#9dc300">dent</text>'
            '<text x="3" y="60" font-family="Manrope,system-ui,sans-serif" font-size="9.5" letter-spacing="3.2" fill="currentColor" opacity=".72">%s</text></svg>' % tag)

LOGO_TAG = {'lv': 'zobu skenēšanas centrs', 'en': 'dental scanning centre', 'ru': 'центр зубного сканирования'}
def logo_img(lang):
    return '<img class="logo-img" src="%s" alt="CT-Dent — %s" width="562" height="222">' % (asset('img/logo.png'), LOGO_TAG[lang])

ICON = {
 'pin': '<path d="M12 2a8 8 0 0 0-8 8c0 5.4 7 11.5 7.3 11.8a1 1 0 0 0 1.4 0C13 21.5 20 15.4 20 10a8 8 0 0 0-8-8Zm0 11a3 3 0 1 1 0-6 3 3 0 0 1 0 6Z"/>',
 'clock': '<path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm1 10.6 4.2 2.5-.8 1.3L11 13V7h2v5.6Z"/>',
 'phone': '<path d="M6.6 10.8a15.5 15.5 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.2.4 2.4.6 3.7.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.7.1.3 0 .7-.2 1l-2.3 2.1Z"/>',
 'mail': '<path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2Zm0 4-8 5-8-5V6l8 5 8-5v2Z"/>',
 'user': '<path d="M12 12a5 5 0 1 0-5-5 5 5 0 0 0 5 5Zm0 2c-4.4 0-8 2.2-8 5v1h16v-1c0-2.8-3.6-5-8-5Z"/>',
 'arr': '<path d="M13 5l7 7-7 7-1.4-1.4L16.2 13H4v-2h12.2l-4.6-4.6L13 5Z"/>',
 'check': '<path d="M9 16.2 4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2Z"/>',
}
def ic(name, cls=''):
    return '<svg viewBox="0 0 24 24"%s aria-hidden="true">%s</svg>' % ((' class="%s"' % cls if cls else ''), ICON[name])

def head(pg, lang):
    d = pg['data'][lang]
    c = COMMON[lang]
    alts = ''.join('<link rel="alternate" hreflang="%s" href="%s">' % (hl, abs_url(L, pg['slugs'][L]))
                   for L, hl in (('lv', 'lv'), ('en', 'en'), ('ru', 'ru')))
    xd = '<link rel="alternate" hreflang="x-default" href="%s">' % abs_url('lv', pg['slugs']['lv'])
    og_locale = {'lv': 'lv_LV', 'en': 'en_GB', 'ru': 'ru_RU'}[lang]
    jsonld = ''
    if pg['id'] == 'home':
        jsonld = ('<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@type": "MedicalClinic",
            "name": "CT-Dent", "legalName": "SIA \"CT-Dent\",", "telephone": PHONE,
            "address": {"@type": "PostalAddress", "streetAddress": "Cēsu iela 31 k-2", "addressLocality": "Riga", "postalCode": "LV-1012", "addressCountry": "LV"},
            "openingHours": "Mo-Fr 09:30-18:00",
            "url": SITE, "logo": SITE + "assets/img/logo.png",
            "medicalSpecialty": "Dentistry"}, ensure_ascii=False) + '</script>')
    return f'''<!DOCTYPE html>
<html lang="{lang}" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(d['title'])}</title>
<meta name="description" content="{e(d['meta'])}">
<link rel="canonical" href="{abs_url(lang, pg['slugs'][lang])}">
{alts}{xd}
<meta property="og:type" content="website">
<meta property="og:site_name" content="CT-Dent">
<meta property="og:title" content="{e(d['title'])}">
<meta property="og:description" content="{e(d['meta'])}">
<meta property="og:url" content="{abs_url(lang, pg['slugs'][lang])}">
<meta property="og:image" content="{SITE}assets/img/scan.jpg">
<meta property="og:locale" content="{og_locale}">
<meta name="theme-color" content="#081a20">
<link rel="icon" type="image/svg+xml" href="{asset('img/favicon.svg')}">
<link rel="stylesheet" href="{asset('css/main.css')}">
<script>(function(){{try{{var t=localStorage.getItem('ctdent-theme');if(!t)t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();</script>
{jsonld}</head>'''

def topbar(lang, pg):
    c = COMMON[lang]
    langs = ''.join('<a class="langbtn" href="%s" hreflang="%s" lang="%s"%s>%s</a>' %
                    (url_for(L, pg['slugs'][L]), hl, L, ' aria-current="true"' if L == lang else '', L.upper())
                    for L, hl in (('lv', 'lv'), ('en', 'en'), ('ru', 'ru')))
    return f'''<div class="topbar">
  <div class="wrap">
    <div class="topbar-info">
      <a class="tb-item tb-phone" href="{PHONE_HREF}">{ic('phone')}<span>{PHONE}</span></a>
      <span class="tb-item tb-addr">{ic('pin')}<span>{e(ADDR[lang])}</span></span>
      <span class="tb-item tb-hours">{ic('clock')}<span>{e(HOURS[lang])}</span></span>
    </div>
    <div class="topbar-controls">
      <div class="lang-seg" role="group" aria-label="Language">{langs}</div>
      <button class="theme-switch" id="themeToggle" aria-label="{e(c['theme_label'])}" aria-pressed="false">
        <svg class="sun" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 17a5 5 0 1 0 0-10 5 5 0 0 0 0 10Zm0-15v3m0 14v3M2 12h3m14 0h3M4.9 4.9l2.1 2.1m10 10 2.1 2.1m0-14.2-2.1 2.1m-10 10-2.1 2.1"/></svg>
        <svg class="moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 14.4A9 9 0 1 1 9.6 3 7 7 0 0 0 21 14.4Z"/></svg>
        <span class="knob" aria-hidden="true"></span>
      </button>
    </div>
  </div>
</div>'''

NAV = [('services', 'nav_svc'), ('cbct', 'nav_about'), ('irys', 'nav_dent'), ('contact', 'nav_contact')]
def capsule(lang, pg):
    c = COMMON[lang]
    byid = {p['id']: p for p in P}
    contact = url_for(lang, byid['contact']['slugs'][lang])
    langs = ''.join('<a class="langbtn" href="%s" hreflang="%s" lang="%s"%s>%s</a>' %
                    (url_for(L, pg['slugs'][L]), hl, L, ' aria-current="true"' if L == lang else '', L.upper())
                    for L, hl in (('lv', 'lv'), ('en', 'en'), ('ru', 'ru')))
    return f'''<div class="corner-dock" id="cornerDock">
  <button class="cd-info" id="cdInfo" aria-expanded="false" aria-controls="cdCard" aria-label="{e(c['cd_info'])}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm1 15h-2v-6h2v6Zm0-8h-2V7h2v2Z"/></svg></button>
  <a class="cd-phone" href="{PHONE_HREF}">{ic('phone')}<span>{PHONE}</span></a>
  <span class="cd-div" aria-hidden="true"></span>
  <div class="lang-seg" role="group" aria-label="Language">{langs}</div>
  <button class="theme-switch" id="themeToggle" aria-label="{e(c['theme_label'])}" aria-pressed="false">
    <svg class="sun" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 17a5 5 0 1 0 0-10 5 5 0 0 0 0 10Zm0-15v3m0 14v3M2 12h3m14 0h3M4.9 4.9l2.1 2.1m10 10 2.1 2.1m0-14.2-2.1 2.1m-10 10-2.1 2.1"/></svg>
    <svg class="moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 14.4A9 9 0 1 1 9.6 3 7 7 0 0 0 21 14.4Z"/></svg>
    <span class="knob" aria-hidden="true"></span>
  </button>
  <div class="corner-card" id="cdCard">
    <h4>{e(c['ct_addr_t'])}</h4>
    <p class="ip-strong">{e(c['ct_addr'])}</p>
    <h4 style="margin-top:18px">{e(c['ct_hours_t'])}</h4>
    <div class="hours-row" id="cdHours"><span>{e(c['cd_days'])}</span><span>{TIMES}<em class="today-tag" id="cdToday" hidden>{e(c['cd_today'])}</em></span></div>
    <p class="cd-mail"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <a class="cd-get" href="{contact}">{e(c['cd_get'])} <span aria-hidden="true">&rarr;</span></a>
  </div>
</div>'''

def header(lang, pg):
    c = COMMON[lang]
    byid = {p['id']: p for p in P}
    links = ''.join('<a href="%s"%s>%s</a>' % (url_for(lang, byid[i]['slugs'][lang]),
                    ' aria-current="page"' if i == pg['id'] else '', e(c[k])) for i, k in NAV)
    return f'''<header class="site">
  <div class="wrap navrow">
    <a class="logo" href="{url_for(lang, '')}" aria-label="CT-Dent — {e(c['nav_home'])}">{logo_img(lang)}</a>
    <button class="nav-burger" id="burger" aria-label="{e(c['menu_label'])}" aria-expanded="false" aria-controls="mainNav"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18v2H3V6Zm0 5h18v2H3v-2Zm0 5h18v2H3v-2Z"/></svg></button>
    <nav class="main" id="mainNav" aria-label="Main">{links}</nav>
    <a class="login-chip" href="{url_for(lang, byid['portal-login']['slugs'][lang])}">{ic('user')}<span>{e(c['login'])}</span></a>
    <a class="btn btn-solid" href="{url_for(lang, byid['referral']['slugs'][lang])}"><span>{e(c['cta_book'])}</span><span class="ar" aria-hidden="true">→</span></a>
  </div>
</header>'''

def footer(lang):
    c = COMMON[lang]
    byid = {p['id']: p for p in P}
    u = lambda i: url_for(lang, byid[i]['slugs'][lang])
    return f'''<footer class="site">
  <div class="wrap">
    <div class="f-grid">
      <div>
        <span class="f-logo">{logo_img(lang)}</span>
        <p style="margin-top:18px">{e(c['f_about'])}</p>
      </div>
      <div>
        <h4>{e(c['f_nav'])}</h4>
        <a href="{u('services')}">{e(c['nav_svc'])}</a>
        <a href="{u('cbct')}">{e(c['nav_about'])}</a>
        <a href="{u('irys')}">{e(c['nav_dent'])}</a>
        <a href="{u('contact')}">{e(c['nav_contact'])}</a>
        <a href="{u('downloads')}">{e(c['d_downloads'])}</a>
      </div>
      <div>
        <h4>{e(c['f_legal'])}</h4>
        <a href="{u('privacy')}">{e(c['f_privacy'])}</a>
        <a href="{u('cookies')}">{e(c['f_cookies'])}</a>
        <a href="{u('terms')}">{e(c['f_terms'])}</a>
        <a href="#" id="ckReopen">{e(c['ck_prefs'])}</a>
      </div>
    </div>
    <div class="f-bottom">
      <span>{e(c['f_copy'])}</span>
      <span>{e(c['f_addr'])}</span>
    </div>
  </div>
</footer>'''

def cookie(lang):
    c = COMMON[lang]
    return f'''<div class="cookie hidden" id="cookieBanner" role="dialog" aria-modal="false" aria-labelledby="ckT">
  <div class="wrap">
    <p id="ckT"><span>{e(c['ck_text'])}</span><a href="{url_for(lang, [p for p in P if p['id']=='cookies'][0]['slugs'][lang])}">{e(c['f_cookies'])}</a>.</p>
    <div class="btns">
      <button class="btn btn-solid btn-sm" id="ckAccept">{e(c['ck_accept'])}</button>
      <button class="btn btn-reject btn-sm" id="ckReject">{e(c['ck_reject'])}</button>
      <button class="btn btn-line btn-sm" id="ckPrefs" aria-expanded="false" aria-controls="cookiePrefs">{e(c['ck_prefs'])}</button>
    </div>
  </div>
  <div class="wrap cookie-prefs" id="cookiePrefs">
    <div style="flex:1 1 340px">
      <label class="check"><input type="checkbox" checked disabled> {e(c['ck_nec'])}</label>
      <label class="check"><input type="checkbox" id="ckAnalytics" checked> {e(c['ck_an'])}</label>
      <label class="check"><input type="checkbox" id="ckMarketing"> {e(c['ck_mk'])}</label>
    </div>
    <div class="btns"><button class="btn btn-solid btn-sm" id="ckSave">{e(c['ck_save'])}</button></div>
  </div>
</div>'''

# ------------------------------------------------------------------ blocks
def b_trust(c):
    return '<div class="trust" aria-hidden="false"><div class="wrap">%s</div></div>' % ''.join('<span>%s</span>' % e(t) for t in c['trust'])

def b_stats(c):
    cells = ''
    for txt, lab, cnt, suf in c['stats']:
        inner = txt
        if cnt is None:
            inner = '<i>%s</i>' % txt.split()[0] + ' ' + ' '.join(txt.split()[1:])
        attr = ' data-count="%d" data-suffix="%s"' % (cnt, suf) if cnt is not None else ''
        cells += '<div class="stat rv" role="listitem"><b%s>%s</b><span>%s</span></div>' % (attr, inner if cnt is not None else txt, e(lab))
    return '<div class="stats" role="list"><div class="wrap">%s</div></div>' % cells

def b_rows(c, lang):
    byid = {p['id']: p for p in P}
    ids = ['cbct', 'opg', 'ceph', 'tmj']
    rows = ''
    for n, (tag, t, d) in zip(ids, c['svc']):
        rows += ('<article class="svc-row rv"><span class="idx">0%d</span>'
                 '<h3><span class="tagm">%s</span>%s</h3><p>%s</p>'
                 '<a class="go" href="%s" aria-label="%s"><span aria-hidden="true">→</span></a></article>') % (
                 len(rows) // 0 if False else int(n and ['cbct','opg','ceph','tmj'].index(n) + 1), e(tag), e(t), e(d),
                 url_for(lang, byid[n]['slugs'][lang]), e(t))
    rows = ''
    for i, (nid, (tag, t, d)) in enumerate(zip(ids, c['svc']), 1):
        rows += ('<article class="svc-row rv"><span class="idx">0%d</span>'
                 '<h3><span class="tagm">%s</span>%s</h3><p>%s</p>'
                 '<a class="go" href="%s" aria-label="%s"><span aria-hidden="true">→</span></a></article>') % (
                 i, e(tag), e(t), e(d), url_for(lang, byid[nid]['slugs'][lang]), e(t))
    return '<div class="svc-list">%s</div>' % rows

def b_steps(c):
    nums = ['I.', 'II.', 'III.', 'IV.']
    items = ''.join('<div class="step rv"><span class="n">%s</span><h3>%s</h3><p>%s</p></div>' % (n, e(t), e(d))
                    for n, (t, d) in zip(nums, c['steps']))
    return '<div class="steps">%s</div>' % items

def b_checks(c):
    return '<ul class="checks">%s</ul>' % ''.join('<li><span>%s</span></li>' % e(x) for x in c['checks'])

def b_split(c, lang):
    return f'''<div class="wrap split">
  <div class="rv">
    <span class="kicker">{e(c['cbct_tag'])}</span>
    <h2>{e(c['cbct_h2'])}</h2>
    <p class="lede">{e(c['cbct_p'])}</p>
    {b_checks(c)}
  </div>
  <figure class="imgframe rv">
    <img src="{asset('img/scan.jpg')}" alt="3D CBCT" loading="lazy" width="980" height="653">
    <span class="scanline" aria-hidden="true"></span>
    <figcaption>MyRay Hyperion X9 · Cone Beam CT · 0.2 mm</figcaption>
  </figure>
</div>'''

def b_why(c):
    nums = ['I.', 'II.', 'III.', 'IV.']
    items = ''.join('<div class="why-item rv"><span class="n">%s</span><h3>%s</h3><p>%s</p></div>' % (n, e(t), e(d))
                    for n, (t, d) in zip(nums, c['why']))
    return f'''<section class="why" id="why">
  <div class="wrap">
    <div class="sec-head rv"><span class="sec-idx">04</span><div><span class="kicker" style="color:var(--amber)">{e(c['why_tag'])}</span><h2>{e(c['why_h2'])}</h2></div></div>
    <div class="why-grid">{items}</div>
    {b_quote(c)}
  </div>
</section>'''

def b_quote(c):
    return f'''<blockquote class="quote rv">
  <img src="{asset('img/patient.jpg')}" alt="" width="92" height="118">
  <div><p>{e(c['q_text'])}</p><cite>{e(c['q_author'])}</cite></div>
</blockquote>'''

def b_band(c, lang):
    byid = {p['id']: p for p in P}
    return f'''<section class="band" id="dentists"><div class="wrap"><div class="inner">
  <div class="rv"><span class="kicker">{e(c['d_tag'])}</span><h2>{e(c['d_h2'])}</h2><p>{e(c['d_p'])}</p></div>
  <div class="actions rv">
    <a class="btn btn-solid" href="{url_for(lang, byid['portal-login']['slugs'][lang])}"><span>{e(c['d_login'])}</span><span class="ar" aria-hidden="true">→</span></a>
    <a class="btn btn-line" href="{url_for(lang, byid['downloads']['slugs'][lang])}"><span>{e(c['d_downloads'])}</span></a>
    <a class="btn btn-line" href="{url_for(lang, byid['portal-register']['slugs'][lang])}"><span>{e(c['d_register'])}</span></a>
  </div>
</div></div></section>'''

def b_faq(c):
    items = ''.join('<details><summary><span>%s</span><span class="pm" aria-hidden="true">+</span></summary><div class="a">%s</div></details>' % (e(q), e(a)) for q, a in c['faq'])
    return f'''<div class="wrap"><div class="sec-head rv"><span class="sec-idx">05</span><div><span class="kicker">{e(c['faq_tag'])}</span><h2>{e(c['faq_h2'])}</h2></div></div><div class="faq rv">{items}</div></div>'''

def b_contact_info(c):
    rows = [('pin', c['ct_addr_t'], c['ct_addr'], None), ('phone', c['ct_tel_t'], PHONE, PHONE_HREF),
            ('mail', c['ct_mail_t'], EMAIL, 'mailto:' + EMAIL),
            ('clock', c['ct_hours_t'], c['ct_hours'], None)]
    out = ''
    for i, t, v, href in rows:
        val = '<a href="%s">%s</a>' % (href, v) if href else v
        out += '<div class="c-row"><span class="ico">%s</span><div><b>%s</b><span>%s</span></div></div>' % (ic(i), e(t), val)
    return out

def b_contact(c, lang):
    return f'''<div class="wrap">
  <div class="sec-head rv"><span class="sec-idx">06</span><div><span class="kicker">{e(c['ct_tag'])}</span><h2>{e(c['ct_h2'])}</h2><p>{e(c['ct_p'])}</p></div></div>
  <div class="contact-grid">
    <div class="rv">{b_contact_info(c)}</div>
    <div class="map-ph rv">{e(c['ct_map'])}</div>
  </div>
</div>'''

def sec_head(idx, kicker, h2, p=None):
    return '<div class="sec-head rv"><span class="sec-idx">%s</span><div><span class="kicker">%s</span><h2>%s</h2>%s</div></div>' % (
        idx, e(kicker), e(h2), ('<p>%s</p>' % e(p)) if p else '')

def page_hero(c, d, lang, crumbs=None):
    cr = '<nav class="crumbs" aria-label="Breadcrumb"><a href="%s">%s</a>' % (url_for(lang, ''), e(c['nav_home']))
    for label, href in (crumbs or []):
        cr += ' <span aria-hidden="true">/</span> <a href="%s">%s</a>' % (href, e(label))
    cr += ' <span aria-hidden="true">/</span> <span>%s</span></nav>' % e(d['h1'])
    return '<section class="page-hero"><div class="wrap">%s<h1>%s</h1><p class="lede-sm">%s</p></div></section>' % (cr, e(d['h1']), e(d['lead']))

def prose_block(sections):
    out = '<div class="prose rv">'
    for h, paras in sections:
        if h: out += '<h2>%s</h2>' % e(h) if '<span' not in h else '<h2>%s</h2>' % h
        for p in paras:
            out += '<p>%s</p>' % p if ('<span' in p or '<strong' in p) else '<p>%s</p>' % e(p)
        if isinstance(paras, list) and h and all(len(x) < 120 for x in paras):
            pass
    out += '</div>'
    return out

def prose_lists(sections):
    """sections: list of (heading|None, list-of-paragraphs); if heading present and items short -> ul"""
    out = '<div class="prose rv">'
    for h, paras in sections:
        if h: out += '<h2>%s</h2>' % h
        if h and len(paras) > 1 and all(len(x) < 90 for x in paras):
            out += '<ul>%s</ul>' % ''.join('<li>%s</li>' % e(x) for x in paras)
        else:
            for p in paras:
                out += '<p>%s</p>' % p
    out += '</div>'
    return out

# ------------------------------------------------------------------ templates
def tpl_home(pg, lang):
    c = COMMON[lang]
    byid = {p['id']: p for p in P}
    h1 = c['hero_h1']
    return f'''<main id="main">
<section class="hero" aria-labelledby="heroH1">
  <div class="wrap">
    <div class="rv on">
      <span class="kicker">{e(c['hero_badge'])}</span>
      <h1 id="heroH1">{e(h1[0])} <span class="acc">{e(h1[1])}</span> {e(h1[2])}</h1>
      <p class="hero-sub">{e(c['hero_sub'])}</p>
      <div class="hero-ctas">
        <a class="btn btn-solid" href="{url_for(lang, byid['referral']['slugs'][lang])}"><span>{e(c['cta_book'])}</span><span class="ar" aria-hidden="true">→</span></a>
        <a class="btn btn-line" href="{asset('docs/nosutijuma-veidlapa.pdf')}"><span>{e(c['cta_pdf'])}</span></a>
        <a class="link-u" href="{url_for(lang, byid['irys']['slugs'][lang])}">{e(c['cta_how'])}</a>
      </div>
      <p class="hero-note" role="note"><b>{e(c['note_b'])}</b>&nbsp;<span>{e(c['hero_note'])}</span></p>
    </div>
    <div class="hero-visual rv on">
      <div class="arch"><img src="{asset('img/patient.jpg')}" alt="" width="860" height="573"></div>
      <div class="chip chip-1"><img src="{asset('img/scan.jpg')}" alt=""><span class="t">{e(c['fc1'])}</span></div>
      <div class="chip chip-2"><span class="n">−40%</span><span class="t">{e(c['fc2'])}</span></div>
    </div>
  </div>
</section>
{b_trust(c)}
{b_stats(c)}
<section id="services"><div class="wrap">
  {sec_head('01', c['svc_tag'], c['svc_h2'], c['svc_p'])}
  {b_rows(c, lang)}
</div></section>
<section class="alt" id="how"><div class="wrap">
  {sec_head('02', c['hw_tag'], c['hw_h2'], c['hw_p'])}
  {b_steps(c)}
</div></section>
<section id="cbct">{b_split(c, lang)}</section>
{b_why(c)}
{b_band(c, lang)}
<section id="faq">{b_faq(c)}</section>
<section class="alt" id="contact">{b_contact(c, lang)}</section>
</main>'''

def tpl_page(pg, lang):
    c = COMMON[lang]; d = pg['data'][lang]
    body = ''
    for kind, _ in d['blocks']:
        if kind == 'rows':
            body += '<section id="services"><div class="wrap">%s%s</div></section>' % (sec_head('01', c['svc_tag'], c['svc_h2'], c['svc_p']), b_rows(c, lang))
        elif kind == 'steps':
            body += '<section class="alt" id="how"><div class="wrap">%s%s</div></section>' % (sec_head('02', c['hw_tag'], c['hw_h2'], c['hw_p']), b_steps(c))
        elif kind == 'band':
            body += b_band(c, lang)
        elif kind == 'prose':
            body += '<section class="tight"><div class="wrap">%s</div></section>' % prose_lists(d['prose'])
        elif kind == 'why':
            body += b_why(c)
        elif kind == 'quote':
            body += '<section class="tight"><div class="wrap">%s</div></section>' % b_quote(c)
    return '<main id="main">%s%s</main>' % (page_hero(c, d, lang), body)

def tpl_service(pg, lang):
    c = COMMON[lang]; d = pg['data'][lang]
    intro = ''.join('<p>%s</p>' % e(p) for p in d['intro'])
    how = ''
    if d.get('how'):
        how = '<h2>%s</h2>%s' % ({'lv': 'Kā norit izmeklējums', 'en': 'How the examination works', 'ru': 'Как проходит обследование'}[lang],
                                 ''.join('<p>%s</p>' % e(p) for p in d['how']))
    uses_h = {'lv': 'Kam izmanto', 'en': 'What it is used for', 'ru': 'Для чего применяется'}[lang]
    return f'''<main id="main">
{page_hero(c, d, lang, [(c['nav_svc'], url_for(lang, [p for p in P if p['id']=='services'][0]['slugs'][lang]))])}
<section class="tight"><div class="wrap"><div class="prose rv">{intro}<h2>{uses_h}</h2><ul>{''.join('<li>%s</li>' % e(u) for u in d['uses'])}</ul>{how}</div>
<figure class="imgframe rv" style="margin-top:44px"><img src="{asset('img/scan.jpg')}" alt="" loading="lazy" width="980" height="653"><span class="scanline" aria-hidden="true"></span><figcaption>MyRay Hyperion X9 · Cone Beam CT</figcaption></figure>
</div></section>
{b_band(c, lang)}
</main>'''

SHOT = {'lv': 'ekrānuzņēmums', 'en': 'screenshot', 'ru': 'скриншот'}

def g_img_fig(d):
    if not d.get('img'): return ''
    src, alt, cap = d['img']
    return '<figure class="imgframe rv" style="margin-top:40px"><img src="%s" alt="%s" loading="lazy"><span class="scanline" aria-hidden="true"></span><figcaption>%s</figcaption></figure>' % (asset(src), e(alt), e(cap))

def g_steps(d, lang):
    hd = {'lv': ('INSTRUKCIJA', '10 soļi ar ekrānuzņēmumiem'), 'en': ('MANUAL', '10 steps with screenshots'), 'ru': ('ИНСТРУКЦИЯ', '10 шагов со скриншотами')}[lang]
    rows = ''
    for i, st in enumerate(d['steps_img'], 1):
        title, text = st[0], st[1]
        imgs = st[2] if len(st) > 2 else None
        figs = ''
        if imgs:
            if isinstance(imgs, str): imgs = [imgs]
            for im in imgs:
                figs += '<figure class="gfig"><img src="%s" alt="%s — %s" loading="lazy"></figure>' % (asset(im), e(title), e(SHOT[lang]))
        rows += '<article class="gstep rv"><span class="gnum">%02d</span><div class="gtext"><h3>%s</h3><p>%s</p>%s</div></article>' % (i, e(title), e(text), figs)
    return '<section class="alt"><div class="wrap">%s<div class="gsteps">%s</div></div></section>' % (sec_head('01', hd[0], hd[1]), rows)

def g_gallery(d, lang, idx):
    hd = {'lv': ('PIEMĒRI', 'Reāli CBCT piemēri'), 'en': ('EXAMPLES', 'Real CBCT examples'), 'ru': ('ПРИМЕРЫ', 'Реальные примеры КЛКТ')}[lang]
    items = ''
    for src, cap in d['gallery']:
        items += '<a class="gal-item rv" href="%s" target="_blank" rel="noopener"><img src="%s" alt="%s" loading="lazy"><span>%s</span></a>' % (asset(src), asset(src), e(cap), e(cap))
    return '<section class="tight"><div class="wrap">%s<div class="gal">%s</div></div></section>' % (sec_head(idx, hd[0], hd[1]), items)

def g_cards(d, lang, byid, idx):
    hd = {'lv': ('SADAĻAS', 'Šīs sadaļas lapas'), 'en': ('SECTIONS', 'Pages of this section'), 'ru': ('РАЗДЕЛЫ', 'Страницы этого раздела')}[lang]
    cards = ''
    for pid, title, sub in d['cards']:
        cards += '<a class="kid-card rv" href="%s"><span class="kid-t">%s</span><span class="kid-s">%s</span><span class="kid-ar" aria-hidden="true">&rarr;</span></a>' % (url_for(lang, byid[pid]['slugs'][lang]), e(title), e(sub))
    return '<section class="tight"><div class="wrap">%s<div class="kid-cards">%s</div></div></section>' % (sec_head(idx, hd[0], hd[1]), cards)

def tpl_guide(pg, lang):
    c = COMMON[lang]; d = pg['data'][lang]
    byid = {p['id']: p for p in P}
    if pg['id'] == 'irys':
        crumbs = None
    else:
        crumbs = [(c['nav_dent'], url_for(lang, byid['irys']['slugs'][lang]))]
    intro = ''.join('<p>%s</p>' % e(p) for p in d['intro'])
    body = '<section class="tight"><div class="wrap"><div class="prose rv">%s<ul>%s</ul></div>%s</div></section>' % (
        intro, ''.join('<li>%s</li>' % e(u) for u in d['uses']), g_img_fig(d))
    idx = 1
    if d.get('steps_img'):
        body += g_steps(d, lang); idx += 1
    if d.get('gallery'):
        body += g_gallery(d, lang, '%02d' % idx); idx += 1
    if d.get('cards'):
        body += g_cards(d, lang, byid, '%02d' % idx)
    return '<main id="main">\n%s\n%s\n%s\n</main>' % (page_hero(c, d, lang, crumbs), body, b_band(c, lang))

def tpl_downloads(pg, lang):
    c = COMMON[lang]; d = pg['data'][lang]
    byid = {p['id']: p for p in P}
    open_t = {'lv': 'Atvērt', 'en': 'Open', 'ru': 'Открыть'}[lang]
    view_t = {'lv': 'Skatīt', 'en': 'View', 'ru': 'Смотреть'}[lang]
    out = ''
    for gi, (gtitle, items) in enumerate(d['groups'], 1):
        rows = ''
        for name, meta, href, badge in items:
            if href.startswith('docs/') or href.startswith('img/'):
                h = asset(href); t = open_t; extra = ' target="_blank" rel="noopener"'
            elif href.startswith('http'):
                h = href; t = open_t; extra = ' target="_blank" rel="noopener"'
            else:
                h = url_for(lang, href); t = view_t; extra = ''
            rows += ('<div class="dl-row rv"><span class="fico %s">%s</span><div class="meta"><b>%s</b><span>%s</span></div>'
                     '<a class="btn btn-line btn-sm"%s href="%s"><span>%s</span><span class="ar" aria-hidden="true">&rarr;</span></a></div>') % (
                     badge.lower(), badge, e(name), e(meta), extra, h, t)
        out += '<div class="dl-group"><h2 class="dl-h"><span class="ix">%02d</span>%s</h2><div class="dl-list">%s</div></div>' % (gi, e(gtitle), rows)
    crumbs = [(c['nav_dent'], url_for(lang, byid['irys']['slugs'][lang]))]
    return f'''<main id="main">
{page_hero(c, d, lang, crumbs)}
<section class="tight"><div class="wrap">{out}<p class="form-note">{e(d['note'])}</p></div></section>
</main>'''

def field(fid, label, req=False, ftype='text', hint=None, full=False, errtxt='!'):
    if ftype == 'textarea':
        return ('<div class="field%s"><label for="%s">%s%s</label><textarea id="%s" name="%s"%s></textarea>%s<span class="err">%s</span></div>') % (
            ' full' if full else '', fid, e(label), ' <span class="req" aria-hidden="true">*</span>' if req else '',
            fid, fid, ' required' if req else '', ('<span class="hint">%s</span>' % e(hint)) if hint else '', e(errtxt))
    return ('<div class="field%s"><label for="%s">%s%s</label><input type="%s" id="%s" name="%s"%s>%s<span class="err">%s</span></div>') % (
        ' full' if full else '', fid, e(label), ' <span class="req" aria-hidden="true">*</span>' if req else '',
        ftype, fid, fid, ' required' if req else '', ('<span class="hint">%s</span>' % e(hint)) if hint else '', e(errtxt))

def tpl_referral(pg, lang):
    c = COMMON[lang]; d = pg['data'][lang]; f = d['f']
    secs = d['sec']
    s = '<form data-mailto data-subject="%s" novalidate>' % e({'lv': 'Nosūtījums — CT-Dent', 'en': 'Referral — CT-Dent', 'ru': 'Направление — CT-Dent'}[lang])
    s += '<div class="form-sec"><span class="no">I.</span><h3>%s</h3></div><div class="form-grid">' % e(secs[0])
    s += field('rf_df', f['doc_first'], True, errtxt=f['req']) + field('rf_dl', f['doc_last'], True, errtxt=f['req'])
    s += field('rf_de', f['doc_email'], True, 'email', errtxt=f['req']) + field('rf_dp', f['doc_phone'], True, 'tel', errtxt=f['req']) + '</div>'
    s += '<div class="form-sec"><span class="no">II.</span><h3>%s</h3></div><div class="form-grid">' % e(secs[1])
    s += field('rf_cn', f['cl_name'], True, errtxt=f['req']) + field('rf_ce', f['cl_email'], False, 'email')
    s += field('rf_ca', f['cl_addr'], False, 'text', None, True) + '</div>'
    s += '<div class="form-sec"><span class="no">III.</span><h3>%s</h3></div><div class="form-grid">' % e(secs[2])
    s += field('rf_pf', f['pt_first'], True, errtxt=f['req']) + field('rf_pl', f['pt_last'], True, errtxt=f['req'])
    s += field('rf_pb', f['pt_birth'], True, 'date', errtxt=f['req']) + field('rf_pp', f['pt_phone'], False, 'tel') + '</div>'
    s += '<div class="form-sec"><span class="no">IV.</span><h3>%s</h3></div><div class="checks-form">' % e(secs[3])
    s += ''.join('<label class="check"><input type="checkbox" name="2D" value="%s"> %s</label>' % (e(x), e(x)) for x in f['d2']) + '</div>'
    s += '<div class="form-sec"><span class="no">V.</span><h3>%s</h3></div><div class="checks-form">' % e(secs[4])
    s += ''.join('<label class="check"><input type="checkbox" name="3D" value="%s"> %s</label>' % (e(x), e(x)) for x in f['d3']) + '</div>'
    s += '<div class="form-sec"><span class="no">VI.</span><h3>%s</h3></div>' % e(secs[5])
    s += '<div class="field full" style="margin-bottom:20px"><label>%s</label><div class="checks-form"><label class="check"><input type="radio" name="analysis" value="%s" checked> %s</label><label class="check"><input type="radio" name="analysis" value="%s"> %s</label></div></div>' % (e(f['an']), e(f['an_y']), e(f['an_y']), e(f['an_n']), e(f['an_n']))
    s += '<div class="form-grid">' + field('rf_sign', f['sign'], True, 'text', f['hint_sign'], True, errtxt=f['req']) + '</div>'
    s += '<label class="consent"><input type="checkbox" required id="rf_consent"> <span>%s</span></label>' % e(f['consent'])
    s += '<div class="field full"><div class="err" data-formstatus hidden></div></div>'
    s += '<div class="hero-ctas" style="margin-top:8px"><button class="btn btn-solid" type="submit"><span>%s</span><span class="ar" aria-hidden="true">→</span></button>' % e(f['submit'])
    s += '<a class="btn btn-line" href="%s"><span>%s</span></a></div>' % (asset('docs/nosutijuma-veidlapa.pdf'), e(f['pdf']))
    s += '<p class="form-note" data-formstatus2 hidden></p>'
    s += '</form>'
    # wire status texts
    s = s.replace('<div class="err" data-formstatus hidden></div>',
                  '<p class="form-note" data-formstatus hidden data-ok-text="%s" data-err-text="%s"></p>' % (e(f['ok']), e(f['err'])))
    return '<main id="main">%s<section class="tight"><div class="wrap">%s</div></section></main>' % (page_hero(c, d, lang), s)

def tpl_contact(pg, lang):
    c = COMMON[lang]; d = pg['data'][lang]; f = d['f']
    s = '<form data-mailto data-subject="%s" novalidate><div class="form-grid">' % e({'lv': 'Ziņojums — CT-Dent', 'en': 'Message — CT-Dent', 'ru': 'Сообщение — CT-Dent'}[lang])
    s += field('ct_n', f['name'], True, errtxt=f['err']) + field('ct_e', f['email'], True, 'email', errtxt=f['err'])
    s += field('ct_p', f['phone'], False, 'tel') + field('ct_m', f['msg'], True, 'textarea', None, True, errtxt=f['err']) + '</div>'
    s = s.replace('id="ct_m" name="ct_m"', 'id="ct_m" name="ct_m"')
    s += '<label class="consent"><input type="checkbox" required id="ct_consent"> <span>%s</span></label>' % e(f['consent'])
    s += '<p class="form-note" data-formstatus hidden data-ok-text="%s" data-err-text="%s"></p>' % (e(f['ok']), e(f['err']))
    s += '<div class="hero-ctas"><button class="btn btn-solid" type="submit"><span>%s</span><span class="ar" aria-hidden="true">→</span></button></div></form>' % e(f['submit'])
    return f'''<main id="main">
{page_hero(c, d, lang)}
<section class="tight"><div class="wrap"><div class="contact-grid" style="margin-bottom:56px">
  <div class="rv">{b_contact_info(c)}</div>
  <div class="map-ph rv">{e(c['ct_map'])}</div>
</div>{s}</div></section>
</main>'''

def tpl_portal(pg, lang):
    c = COMMON[lang]; d = dict(pg['data'][lang]); d.setdefault('lead', d['sub'])
    fields = ''
    if pg['id'] == 'portal-login':
        fields = ('<div class="field"><label for="pl_e">%s</label><input type="text" id="pl_e" autocomplete="username"></div>'
                  '<div class="field"><label for="pl_p">%s</label><input type="password" id="pl_p" autocomplete="current-password"></div>') % (
                  e(d['f']['email']), e(d['f']['pw']))
    card = f'''<div class="portal-card rv">
  <h2>{e(d['h1'])}</h2><p class="sub">{e(d['sub'])}</p>
  {fields}
  <div class="hero-ctas"><a class="btn btn-solid" href="{d['link']}"><span>{e(d['link_t'])}</span><span class="ar" aria-hidden="true">→</span></a></div>
  <p class="portal-note">{e(d['note'])}</p>
</div>'''
    return '<main id="main">%s<section class="tight"><div class="wrap">%s</div></section></main>' % (page_hero(c, d, lang), card)

def tpl_legal(pg, lang):
    c = COMMON[lang]; d = pg['data'][lang]
    return '<main id="main">%s<section class="tight"><div class="wrap">%s</div></section></main>' % (
        page_hero(c, d, lang), prose_lists(d['body']))

TPL = {'home': tpl_home, 'page': tpl_page, 'service': tpl_service, 'guide': tpl_guide,
       'downloads': tpl_downloads, 'referral': tpl_referral, 'contact': tpl_contact,
       'portal': tpl_portal, 'legal': tpl_legal}

# ------------------------------------------------------------------ build
def build():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(ROOT, '..', 'assets'), os.path.join(OUT, 'assets'))
    # font-face + css
    css = open(os.path.join(ROOT, '..', 'assets', 'css', 'main.css')).read()
    ff = open(os.path.join(ROOT, 'fontface.css')).read()
    css = css.replace('__FONTFACE__', ff)
    os.makedirs(os.path.join(OUT, 'assets', 'css'), exist_ok=True)
    open(os.path.join(OUT, 'assets', 'css', 'main.css'), 'w').write(css)
    # favicon
    open(os.path.join(OUT, 'assets', 'img', 'favicon.svg'), 'w').write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0e5f5c"/><circle cx="32" cy="32" r="11" fill="#9dc300"/></svg>')
    sitemap = []
    for pg in P:
        for lang in LANGS:
            slug = pg['slugs'][lang]
            rel = PREFIX[lang] + slug
            dpath = os.path.join(OUT, rel) if rel else OUT
            os.makedirs(dpath, exist_ok=True)
            body = TPL[pg['tpl']](pg, lang)
            htmlout = head(pg, lang) + '\n<body>\n<a class="skip" href="#main">%s</a>\n%s\n%s\n%s\n%s\n%s\n<script src="%s" defer></script>\n</body>\n</html>' % (
                e(COMMON[lang]['skip']), header(lang, pg), body, footer(lang), capsule(lang, pg), cookie(lang), asset('js/site.js'))
            with open(os.path.join(dpath, 'index.html'), 'w', encoding='utf-8') as fh:
                fh.write(htmlout)
            sitemap.append(abs_url(lang, slug))
    # robots + sitemap
    open(os.path.join(OUT, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nSitemap: %ssitemap.xml\n' % SITE)
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        ''.join('<url><loc>%s</loc></url>\n' % u for u in sitemap) + '</urlset>')
    # security headers configs
    open(os.path.join(OUT, '_headers'), 'w').write('''/*
  Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()
  Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; font-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self' mailto:; frame-ancestors 'self'
''')
    open(os.path.join(OUT, '.htaccess'), 'w').write('''<IfModule mod_headers.c>
Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"
Header always set X-Content-Type-Options "nosniff"
Header always set X-Frame-Options "SAMEORIGIN"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=()"
Header always set Content-Security-Policy "default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; font-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self' mailto:; frame-ancestors 'self'"
</IfModule>
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
RewriteRule ^lejupielades/$ /arstiem/lejupielades/ [R=301,L]
RewriteRule ^en/downloads/$ /en/for-dentists/downloads/ [R=301,L]
RewriteRule ^ru/zagruzki/$ /ru/vracham/zagruzki/ [R=301,L]
</IfModule>
''')
    open(os.path.join(OUT, '_redirects'), 'w').write(
        '/lejupielades/ /arstiem/lejupielades/ 301\n'
        '/en/downloads/ /en/for-dentists/downloads/ 301\n'
        '/ru/zagruzki/ /ru/vracham/zagruzki/ 301\n')
    print('pages built:', len(sitemap))

if __name__ == '__main__':
    build()
