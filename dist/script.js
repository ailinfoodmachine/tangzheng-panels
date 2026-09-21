const menu=document.querySelector('.language');
const legacy=new URLSearchParams(location.search).get('lang');
const supported=Array.from(menu.options,option=>option.value);
if(legacy&&supported.includes(legacy))location.replace('/'+legacy+'/'+location.hash);
menu.addEventListener('change',event=>{
 try{localStorage.setItem('zhengtang-language',event.target.value)}catch{}
 location.assign('/'+event.target.value+'/'+location.hash);
});
