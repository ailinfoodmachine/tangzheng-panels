import fs from 'node:fs';
import vm from 'node:vm';
const origin='https://zhengtang-metal-panels.jinantongwei481950.chatgpt.site';
const template=fs.readFileSync('src/template.html','utf8');
const renderer=fs.readFileSync('src/render.js','utf8');
const translation=fs.readFileSync('dist/translations.js','utf8');
const catalog=vm.runInNewContext(translation+';({languages,translations})');
const escape=s=>s.replaceAll('&','&amp;').replaceAll('"','&quot;').replaceAll('<','&lt;');
for(const lang of Object.keys(catalog.languages)){
 const nodes={};const node=k=>nodes[k]??={innerHTML:'',textContent:'',setAttribute(){},addEventListener(){}};
 const document={documentElement:{},querySelector:node,querySelectorAll:()=>[]};
 vm.runInNewContext(translation+'\n'+renderer,{document,location:{search:'?lang='+lang},URLSearchParams,URL,localStorage:{getItem(){return null}}});
 let html=template.replace(/<html lang="en">/,`<html lang="${lang}" dir="${lang==='ar'?'rtl':'ltr'}">`)
 .replace(/<title>.*?<\/title>/,`<title>${escape(document.title)}</title>`)
 .replace(/<meta name="description" content="[^"]*">/,`<meta name="description" content="${escape(nodes['meta[name=description]'].content)}">`)
 .replace(/<header>.*?<\/header>/s,`<header>${nodes.header.innerHTML}</header>`)
 .replace(/<div class="hero-copy">.*?<div class="material-art"/s,`<div class="hero-copy">${nodes['.hero-copy'].innerHTML}</div><div class="material-art"`)
 .replace(/<div class="spec-strip">.*?<div id="details"><\/div>/s,`<div class="spec-strip">${nodes['.spec-strip'].innerHTML}</div><div id="details">${nodes['#details'].innerHTML}</div>`)
 .replace(/<footer>.*?<\/footer>/s,`<footer>${nodes.footer.innerHTML}</footer>`)
 .replace(/<script src="translations.js"><\/script>/,'')
 .replace(/(src|href)="(assets\/|style.css|script.js)/g,'$1="/$2');
 const t=catalog.translations[lang];
 html=html.replace('TEXTURE. DEPTH. CHARACTER.',t.texture).replace('Wood, stone and brick metal panel finishes',escape(t.eyebrow));
 ['Rich wood grain metal panel','Grey embossed stone metal panel','Charcoal brick pattern metal panel'].forEach((s,i)=>html=html.replace(s,escape(t.types[[0,4,2][i]])));
 const alternates=Object.keys(catalog.languages).map(l=>`<link rel="alternate" hreflang="${l==='zh'?'zh-Hans':l}" href="${origin}/${l}/">`).join('');
 html=html.replace('</head>',`<link rel="canonical" href="${origin}/${lang}/">${alternates}<link rel="alternate" hreflang="x-default" href="${origin}/en/"></head>`);
 const links=Object.entries(catalog.languages).map(([l,label])=>`<a href="/${l}/" lang="${l}" hreflang="${l}">${label}</a>`).join(' · ');
 html=html.replace('</footer>',`</footer><nav class="language-links" aria-label="${escape(t.lang)}">${links}</nav>`);
 fs.mkdirSync('dist/'+lang,{recursive:true});fs.writeFileSync('dist/'+lang+'/index.html',html);
 if(lang==='en')fs.writeFileSync('dist/index.html',html);
}
fs.writeFileSync('dist/sitemap.xml','<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+Object.keys(catalog.languages).map(l=>`<url><loc>${origin}/${l}/</loc></url>`).join('')+'</urlset>\n');
fs.writeFileSync('dist/robots.txt',`User-agent: *\nAllow: /\nSitemap: ${origin}/sitemap.xml\n`);
console.log('Built 12 fully rendered language pages, root, sitemap and robots.txt');
