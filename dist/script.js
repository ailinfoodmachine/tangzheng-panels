const menu=document.querySelector('.language');
const legacy=new URLSearchParams(location.search).get('lang');
const supported=Array.from(menu.options,option=>option.value);
if(legacy&&supported.includes(legacy))location.replace('/'+legacy+'/'+location.hash);
menu.addEventListener('change',event=>{
 try{localStorage.setItem('zhengtang-language',event.target.value)}catch{}
 location.assign('/'+event.target.value+'/'+location.hash);
});
const products=Array.from(document.querySelectorAll('.product-choice'));
const swatches=Array.from(document.querySelectorAll('.swatch'));
const selectionValue=document.querySelector('.selection-value');
const enquiry=document.querySelector('.selection-enquiry');
const enquiryWhatsApp=document.querySelector('.selection-whatsapp');
let selectedStyle=products[0]?.dataset.style||'';
let selectedCode=products[0]?.dataset.code||'';
let selectedColour=swatches[0]?.dataset.colour||'';
function updateSelection(){
 if(!selectionValue||!enquiry)return;
 selectionValue.textContent=[selectedStyle,selectedCode,selectedColour].filter(Boolean).join(' · ');
 const subject=[enquiry.dataset.prefix,selectedCode,selectedColour,selectedStyle].filter(Boolean).join(' — ');
 enquiry.href=`mailto:${enquiry.dataset.email}?subject=${encodeURIComponent(subject)}`;
}
products.forEach(button=>button.addEventListener('click',()=>{
 products.forEach(item=>{item.setAttribute('aria-pressed','false');item.closest('.product')?.classList.remove('is-selected')});
 button.setAttribute('aria-pressed','true');button.closest('.product')?.classList.add('is-selected');
 selectedStyle=button.dataset.style;selectedCode=button.dataset.code;updateSelection();
}));
swatches.forEach(button=>button.addEventListener('click',()=>{
 swatches.forEach(item=>{item.setAttribute('aria-pressed','false');item.classList.remove('is-selected')});
 button.setAttribute('aria-pressed','true');button.classList.add('is-selected');selectedColour=button.dataset.colour;updateSelection();
}));

const catalogFilters=Array.from(document.querySelectorAll('.catalog-filter'));
const sampleChoices=Array.from(document.querySelectorAll('.sample-choice'));
const selectedSamples=new Map();
const selectionLabels={zh:['已选','款'],en:['Selected','items'],ar:['تم الاختيار','منتجات'],ru:['Выбрано','поз.']};
catalogFilters.forEach(button=>button.addEventListener('click',()=>{
 catalogFilters.forEach(item=>item.classList.remove('is-active'));button.classList.add('is-active');
 const group=button.dataset.group;
 document.querySelectorAll('.sample-card').forEach(card=>{card.hidden=group!=='all'&&card.dataset.group!==group});
}));
sampleChoices.forEach(button=>button.addEventListener('click',()=>{
 const key=`${button.dataset.style}|${button.dataset.code}`;
 const card=button.closest('.sample-card');
 if(selectedSamples.has(key)){selectedSamples.delete(key);card?.classList.remove('is-selected');button.setAttribute('aria-pressed','false')}
 else{selectedSamples.set(key,{style:button.dataset.style,code:button.dataset.code});card?.classList.add('is-selected');button.setAttribute('aria-pressed','true')}
 if(!selectionValue||!enquiry)return;
 const items=Array.from(selectedSamples.values());
 const label=selectionLabels[document.documentElement.lang]||selectionLabels.en;
 selectionValue.textContent=items.length?`${label[0]} ${items.length} ${label[1]} · ${items.map(item=>item.code).join(' · ')}`:enquiry.dataset.empty||'Choose one or more models';
 const subject=items.length?`${enquiry.dataset.prefix} — ${items.map(item=>`${item.code} ${item.style}`).join(' | ')}`:`${enquiry.dataset.prefix} catalogue enquiry`;
 enquiry.href=`mailto:${enquiry.dataset.email}?subject=${encodeURIComponent(subject)}`;
 if(enquiryWhatsApp){const message=items.length?`TANGZHENG enquiry: ${items.map(item=>`${item.code} ${item.style}`).join(' | ')}`:'TANGZHENG catalogue enquiry';enquiryWhatsApp.href=`https://wa.me/${enquiryWhatsApp.dataset.wa}?text=${encodeURIComponent(message)}`}
}));
