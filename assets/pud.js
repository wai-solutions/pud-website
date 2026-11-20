(function(){
'use strict';
const $=(s,c=document)=>c.querySelector(s), $$=(s,c=document)=>[...c.querySelectorAll(s)];
let LITE=false;try{LITE=localStorage.getItem('pudlite')==='1'}catch(e){}
const RM=matchMedia('(prefers-reduced-motion: reduce)').matches||LITE;
if(LITE)document.body.classList.add('lite-on');
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
function rng(seed){let s=seed*9301+49297;return()=>{s=(s*9301+49297)%233280;return s/233280}}
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

/* =============== ART: architectural plan drawings =============== */
function art(kind,seed,W=400,H=300){
  const r=rng(seed);const g=[];
  const grid=(n,col,sw)=>{let s='';for(let i=0;i<=n;i++)s+=`<line x1="${i*W/n}" y1="0" x2="${i*W/n}" y2="${H}" stroke="${col}" stroke-width="${sw}"/>`;const m=Math.round(n*H/W);for(let i=0;i<=m;i++)s+=`<line x1="0" y1="${i*H/m}" x2="${W}" y2="${i*H/m}" stroke="${col}" stroke-width="${sw}"/>`;return s};
  g.push(`<rect width="${W}" height="${H}" fill="#F6F3EF"/>`,grid(20,'#ECE7E0',.6));
  const k=Math.max(W/400,H/300);g.push(`<g transform="translate(${(W-400*k)/2} ${(H-300*k)/2}) scale(${k})">`);
  if(kind==='coast'||kind==='bay'){
    const y0=kind==='bay'?140:105+r()*30;let d=`M0 ${y0}`;
    for(let x=0;x<=400;x+=40)d+=` Q ${x+20} ${y0+(r()-.5)*40+(kind==='bay'?Math.sin(x/70)*35:0)} ${x+40} ${y0+(r()-.5)*20+(kind==='bay'?Math.sin((x+40)/70)*35:0)}`;
    g.push(`<path d="${d} L400 0 L0 0Z" fill="#E4EBEF"/>`);
    for(let i=1;i<6;i++)g.push(`<path d="${d}" transform="translate(0 ${-i*9})" fill="none" stroke="#D0DBE1" stroke-width=".7"/>`);
    g.push(`<path d="${d}" fill="none" stroke="#9fb1ba" stroke-width="1"/>`);
    for(let i=0;i<34;i++){const x=10+r()*380,y=y0+28+r()*150,w=8+r()*30,h=8+r()*22;g.push(`<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${r()>.86?'#EE4223':'#fff'}" stroke="#bdb5aa" stroke-width=".7"/>`)}
    g.push(`<path d="M20 ${y0+40} C 140 ${y0+120} 260 ${y0+20} 390 ${y0+90}" fill="none" stroke="#111" stroke-width="1.1" stroke-dasharray="5 4"/>`);
    if(kind==='bay')g.push(`<circle cx="${150+r()*120}" cy="${y0-40}" r="24" fill="none" stroke="#EE4223" stroke-width="1.2"/>`);
  }else if(kind==='grid'||kind==='capital'){
    const rot=(r()-.5)*26;g.push(`<g transform="rotate(${rot} 200 150)">`);
    for(let i=-3;i<15;i++)for(let j=-3;j<12;j++){if(r()>.18){const f=r();g.push(`<rect x="${i*34+4}" y="${j*34+4}" width="28" height="28" fill="${f>.92?'#EE4223':f>.62?'#E7E2DB':'#fff'}" stroke="#c8c0b5" stroke-width=".6"/>`)}}
    g.push(`</g><path d="M-10 ${150+(r()-.5)*60} L410 ${150+(r()-.5)*60}" stroke="#fff" stroke-width="14"/><path d="M${200+(r()-.5)*80} -10 L${200+(r()-.5)*80} 310" stroke="#fff" stroke-width="10"/>`);
    if(kind==='capital')g.push(`<rect x="0" y="${120+r()*40}" width="400" height="22" fill="#DCE6D7"/>`);
  }else if(kind==='sacred'){
    const cx=140+r()*120,cy=120+r()*60;
    for(let i=8;i>0;i--)g.push(`<circle cx="${cx}" cy="${cy}" r="${i*22}" fill="none" stroke="#d6cec3" stroke-width=".7"/>`);
    for(let a=0;a<360;a+=15)g.push(`<line x1="${cx}" y1="${cy}" x2="${cx+Math.cos(a*Math.PI/180)*190}" y2="${cy+Math.sin(a*Math.PI/180)*190}" stroke="#e3dcd2" stroke-width=".6"/>`);
    const pts=[[40+r()*30,230+r()*30],[140,170+r()*20],[250,120+r()*20],[350,70+r()*30]];
    g.push(`<path d="M${pts.map(p=>p.join(' ')).join(' L')}" fill="none" stroke="#111" stroke-width="1.2" stroke-dasharray="6 4"/>`);
    pts.forEach((p,i)=>g.push(`<circle cx="${p[0]}" cy="${p[1]}" r="${i===3?9:6}" fill="${i===3?'#EE4223':'#fff'}" stroke="#111" stroke-width="1"/>`));
    for(let i=0;i<40;i++)g.push(`<circle cx="${r()*400}" cy="${r()*300}" r="${1+r()*2}" fill="#cfc6ba"/>`);
  }else if(kind==='heritage'){
    g.push(`<path d="M0 230 L400 230" stroke="#bdb5aa"/>`);
    [[60+r()*60,230,60+r()*30],[180+r()*40,230,48+r()*22],[280+r()*30,230,28+r()*18]].forEach(([x,y,s],i)=>{g.push(`<path d="M${x-s} ${y} L${x} ${y-s*1.25} L${x+s} ${y}Z" fill="${i===0?'#EE4223':'#fff'}" stroke="#9c9285" stroke-width=".8"/><path d="M${x} ${y-s*1.25} L${x+s*.25} ${y}" stroke="#9c9285" stroke-width=".6"/>`)});
    for(let i=0;i<9;i++)g.push(`<path d="M0 ${240+i*7} Q 200 ${232+i*7} 400 ${244+i*7}" fill="none" stroke="#ddd5ca" stroke-width=".7"/>`);
    g.push(`<path d="M${320+r()*30} 30 C 300 120 360 180 320 300" fill="none" stroke="#9fb1ba" stroke-width="5" opacity=".6"/>`);
  }else if(kind==='aswan'){
    g.push(`<path d="M0 0 L400 0 L400 120 Q 300 160 220 120 T 0 150Z" fill="#E4EBEF"/>`);
    for(let i=0;i<5;i++)g.push(`<path d="M0 ${150-i*10} Q 110 ${120-i*10} 220 ${120-i*10} T 400 ${120-i*10}" fill="none" stroke="#D0DBE1" stroke-width=".7"/>`);
    for(let i=0;i<22;i++){const x=20+r()*360,y=170+r()*110,s=10+r()*16;g.push(`<rect x="${x}" y="${y}" width="${s}" height="${s}" fill="#fff" stroke="#b9ae9f" stroke-width=".7"/><path d="M${x} ${y} Q ${x+s/2} ${y-s*.6} ${x+s} ${y}" fill="${r()>.8?'#EE4223':'#F1ECE5'}" stroke="#b9ae9f" stroke-width=".7"/>`)}
  }else if(kind==='tower'){
    const n=7+Math.floor(r()*4),hi=Math.floor(r()*n);
    for(let i=0;i<n;i++){const x=30+i*(340/n),w=340/n-8,h=60+r()*180;g.push(`<rect x="${x}" y="${270-h}" width="${w}" height="${h}" fill="${i===hi?'#EE4223':'#fff'}" stroke="#b9ae9f" stroke-width=".7"/>`);for(let y=270-h+8;y<268;y+=10)g.push(`<line x1="${x+4}" x2="${x+w-4}" y1="${y}" y2="${y}" stroke="${i===hi?'#f7a291':'#e6e0d8'}" stroke-width=".7"/>`)}
    g.push(`<line x1="0" x2="400" y1="270" y2="270" stroke="#111" stroke-width="1"/>`);
  }else if(kind==='region'){
    for(let i=0;i<15;i++){let d='M';for(let x=0;x<=400;x+=20)d+=`${x} ${10+i*20+Math.sin(x/50+i+seed)*12+(r()-.5)*4} `;g.push(`<path d="${d}" fill="none" stroke="#d6cec3" stroke-width=".7"/>`)}
    for(let i=0;i<10;i++){const x=40+r()*320,y=40+r()*220;g.push(`<circle cx="${x}" cy="${y}" r="${3+r()*5}" fill="${i<2?'#EE4223':'#fff'}" stroke="#111" stroke-width=".8"/>`)}
    g.push(`<path d="M30 270 C 120 ${150+r()*60} 200 ${190+r()*60} 370 40" fill="none" stroke="#111" stroke-width="1.1" stroke-dasharray="5 4"/>`);
  }else if(kind==='park'){
    for(let i=0;i<64;i++){const x=r()*400,y=r()*300,s=4+r()*14;g.push(`<circle cx="${x}" cy="${y}" r="${s}" fill="${r()>.93?'#EE4223':'#E1E7DA'}" stroke="#c6cdbd" stroke-width=".6"/>`)}
    g.push(`<path d="M-10 ${170+r()*50} C 100 140 220 260 410 ${100+r()*50}" fill="none" stroke="#fff" stroke-width="12"/>`);
  }else if(kind==='cube'){
    for(let i=0;i<6;i++)for(let j=0;j<4;j++){const x=30+i*58,y=40+j*62;g.push(`<rect x="${x}" y="${y}" width="46" height="46" fill="${i===2&&j===1?'#EE4223':'#fff'}" stroke="#b9ae9f"/><path d="M${x} ${y} L${x+10} ${y-9} L${x+56} ${y-9} L${x+46} ${y}" fill="#ECE6DE" stroke="#b9ae9f" stroke-width=".7"/>`)}
  }else if(kind==='people'){
    for(let i=0;i<9;i++){const cx=40+i*42+r()*10,cy=150+(r()-.5)*80;g.push(`<circle cx="${cx}" cy="${cy}" r="${10+r()*8}" fill="${i===4?'#EE4223':'#fff'}" stroke="#111" stroke-width=".8"/>`)}
    g.push(`<path d="M20 230 Q 200 120 380 230" fill="none" stroke="#111" stroke-dasharray="4 4"/>`);
  }
  g.push('</g>');
  return `<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid slice" aria-hidden="true">${g.join('')}</svg>`;
}

/* =============== DATA =============== */
const KIND={"Strategic Advisory": "sacred", "Master Planning": "grid", "Urban & Regional Planning": "region", "Coastal & Tourism": "coast", "Architecture": "tower", "Landscape": "park"};
const P=(window.PUD_PROJECTS||[]).map((p,i)=>({...p,k:KIND[p.t]||'grid',e:i+3,sc:p.sc?[p.sc]:null,q:null}));
const TYPES=['Strategic Advisory','Master Planning','Urban & Regional Planning','Coastal & Tourism','Architecture','Landscape'];
const REG={egypt:'Egypt',ksa:'Saudi Arabia',intl:'International'};

const NEWS=[
 {s:'share-cairo-2026',c:'Event',h:'SHARE Architects brings its first African forum to Cairo, at the Grand Egyptian Museum',x:'Dr. Amr Attia joins the local organising committee for the 13–14 December forum.',d:'Dec 2026',img:'pyramids-plateau.jpg',
  f:[['When','13–14 December 2026'],['Where','Grand Egyptian Museum, Giza'],['Format','International architecture forum'],['PUD role','Local organising committee']],
  b:['For the first time, the SHARE Architects forum comes to Africa — and it lands in Cairo, at the Grand Egyptian Museum, within sight of the Pyramids. Over two days, architects, planners and developers from across the region and beyond will meet to discuss how the next generation of cities and buildings should be shaped.',
     'Dr. Amr Attia, CEO of PUD Consultants, sits on the local organising committee alongside Prof. Iman Gawad, Karim El Hayawan and Dr. Tamer Elgabaly. For PUD, the forum is a chance to bring the international design conversation to Egypt, and to put Egyptian practice at the centre of it.',
     'The programme is built around four themes that reflect where the region is heading: public architecture and the design of facades; housing and mixed-use development; capital, design and nation-building; and sustainability and artificial intelligence in design.',
     'The theme of capital and nation-building speaks directly to PUD’s own work — from strategic advisory on the New Administrative Capital to destination planning at the Pyramids. Sixty years after PUD was founded in Cairo, hosting this conversation at home feels like the right way to mark the anniversary.'],
  l:[['Pyramids Plateau Destination','project-pyramids-plateau.html'],['New Administrative Capital','project-new-administrative-capital.html']]},
 {s:'share-georgia-2026',c:'Talk',h:'“Making a New Capital City Work”: Dr. Amr Attia speaks at SHARE Georgia 2026',x:'Among 30 speakers from 10 countries in Tbilisi.',d:'Sep 2026',img:'new-administrative-capital.jpg',
  f:[['When','22 September 2026'],['Where','Pullman Tbilisi Axis Towers, Georgia'],['Speakers','30 speakers from 10 countries'],['Talk','Making a New Capital City Work']],
  b:['At SHARE Georgia 2026 in Tbilisi, Dr. Amr Attia joined 30 speakers from 10 countries to talk about one of the hardest questions in city-making: how do you make a new capital city actually work?',
     'Drawing on PUD’s strategic advisory for Egypt’s New Administrative Capital, the talk looked beyond the master plan, at what it takes for a new capital to grow into a living, working city.',
     'The forum brought together some of the most influential names in global architecture, with keynotes from Herzog & de Meuron, Foster + Partners and Henning Larsen. Among the reflections shared after the forum, Alexander Novikov singled out Dr. Attia’s presentation as one of its highlights.',
     'For PUD, conversations like this are part of how the firm works: sharing what we learn on the ground, and bringing back ideas from peers around the world to the projects we shape at home.'],
  l:[['New Administrative Capital','project-new-administrative-capital.html']]},
 {s:'pyramids-framework',c:'Project',h:'Pyramids Destination: a scenario tool shaped with WATG and PUD’s local expert team',x:'Field work and archival photography reshaped the role of Dahshur.',d:'Sep 2026',p:'pyramids-plateau',
  f:[['Project','Pyramids Destination framework'],['Partners','WATG'],['PUD role','Local expert team, led by Dr. Amr Attia'],['Location','Giza to Dahshur, Egypt']],
  b:['Planning a destination around the world’s most visited ancient site means making choices that will shape it for generations. To make those choices clearer, the team behind the Pyramids Destination framework built a scenario decision tool: a way to test how different strategies for access, visitor flows and development would play out across the wider landscape.',
     'The work was developed with WATG, alongside a local expert team led by Dr. Amr Attia of PUD. Local knowledge proved decisive. A field route through the landscape, together with archival photographs shared by Dr. Fekri Hassan, changed the team’s understanding of Dahshur — and with it, the role Dahshur plays in the framework.',
     'It is a reminder of something PUD has believed since 1966: good plans are not drawn from a distance. They come from walking the land, reading its history and listening to the people who know it best.'],
  l:[['Pyramids Plateau Destination','project-pyramids-plateau.html']]},
 {s:'akhet-master-plan',c:'Project',h:'AKHET: the Tourism Master Plan of Pyramids Destination',x:'Completed with WATG for the Ministry of Housing and the Ministry of Tourism.',d:'Aug 2026',img:'li-pyramids.jpg',
  f:[['Plan','AKHET — Tourism Master Plan'],['Completed','December 2024'],['Clients','Ministry of Housing · Ministry of Tourism'],['Partners','WATG']],
  b:['AKHET is the tourism master plan for Pyramids Destination — a long-term vision for how visitors will experience the Giza plateau and the landscape around it. The name comes from the ancient Egyptian word for the horizon, the place where the sun rises and sets.',
     'Completed in December 2024 for the Ministry of Housing and the Ministry of Tourism, the plan was developed with WATG, with PUD as part of the core team. It sets out how to protect the last surviving wonder of the ancient world while creating a world-class destination around it: new arrival experiences, carefully placed hospitality, and a landscape restored with respect for its history.',
     'For PUD, AKHET brings together six decades of work in heritage, tourism and regional planning — and a commitment to making places that honour the past while serving the people who visit and live there today.'],
  l:[['Pyramids Plateau Destination','project-pyramids-plateau.html']]},
 {s:'sumou-launch',c:'Project',h:'Sumou Boulevard launches: EGP 7 billion booked in 24 hours',x:'6.1× oversubscribed, with 70% of buyers under 40.',d:'Jun 2026',p:'sumou-boulevard',
  f:[['Bookings','EGP 7 billion in 24 hours'],['Demand','6.1× oversubscribed · 3,343 unit requests'],['Buyers','70% under 40'],['PUD role','SMEs for the steering committee']],
  b:['Sumou Boulevard, by Paragon-Adeer, set out to be the region’s first regenerative city. Its launch showed how much appetite there is for that idea: EGP 7 billion in bookings within 24 hours, and demand 6.1 times greater than the units on offer, with 3,343 unit requests.',
     'Perhaps the most telling number is who is buying. Seventy percent of buyers are under 40 — a young generation choosing a place designed around nature, community and long-term value rather than short-term returns.',
     'PUD provides the subject-matter experts for the project’s steering committee, helping to keep the regenerative vision at the heart of every decision as the city moves from plan to reality.'],
  l:[['Sumou Boulevard','project-sumou-boulevard.html']]},
 {s:'pyramids-delivered',c:'Project',h:'A wonderful close to an amazing project: the Pyramids master plan is delivered',x:'A world-class team with WATG and Wimberly Interiors.',d:'Dec 2025',img:'li-pyramids.jpg',
  f:[['Milestone','Master plan delivered'],['Partners','WATG · Wimberly Interiors'],['With','Luxury Partners · Shaker Consultancy Group'],['Location','Giza, Egypt']],
  b:['In December 2025, Dr. Amr Attia marked the close of the Pyramids master plan with a simple message: it had been an honour to work with a world-class team.',
     'The project brought together WATG and Wimberly Interiors with PUD, Luxury Partners and Shaker Consultancy Group, guided by local knowledge keepers and cultural interpreters including Dr. Fekri Hassan, Dr. Michael Jones and Dalila ElKerdany. Team members described the aim as restoring one of the world’s most significant cultural landscapes with reverence and sensitivity, so that it can anchor a new era of tourism.',
     'For PUD, it is the kind of project that defines a practice: global expertise and local understanding working as one, in service of a place that belongs to everyone.'],
  l:[['Pyramids Plateau Destination','project-pyramids-plateau.html']]},
 {s:'60-years',c:'Story',h:'PUD celebrates 60 years of shaping sustainable cities',x:'From a founder’s vision in 1966 to 150+ projects across 11 countries.',d:'2026',img:'cover-60.jpg',
  f:[['Founded','1966, Cairo'],['Projects','150+'],['Countries','11'],['Cities','60+']],
  b:['In 1966, Prof. Abdallah Abdel Aziz Attia founded PUD on a simple belief: that planning should begin with people and with the natural and cultural environments they live in.',
     'Sixty years later, that vision continues through Prof. Dr. Amr A. Attia. PUD has delivered 150+ projects across 11 countries and 60+ cities — from Alex to Aswan, across the Red Sea to Saudi Arabia, and beyond.',
     'The anniversary is a moment to look back, and to ask the question that has always driven the firm: what should we build next?'],
  l:[['Read the 60-year story','60-years.html']]}
].map(n=>Object.assign(n,{u:'article-'+n.s+'.html'}));
const nthumb=n=>n.p&&bySlug(n.p)?pimg(bySlug(n.p)):(n.img?`<img src="img/${n.img}" alt="" loading="lazy">`:art('region',3));
const CH_IMG=['founder.jpg','amr-attia-2.jpg','massoumbou-diwom.jpg','alamein-riviera.jpg','founder-2.jpg','sumou-boulevard.jpg'];
const CHAPTERS=[
 ['01','Every legacy begins with a vision','In 1966, Prof. Abdallah Abdel Aziz Attia founded PUD.','ch1','cube',2],
 ['02','A great leader builds beyond today','The vision continues through Prof. Dr. Amr A. Attia.','ch2','people',4],
 ['03','Global minds. One mission.','100+ clients and 90+ collaborations across six decades.','ch3','region',6],
 ['04','From Alex to Aswan, and beyond','150+ projects across 11 countries and 60+ cities.','journey','coast',8],
 ['05','Developed, tested, carried forward','20+ awards, from Cairo to Paris.','timeline','heritage',10],
 ['06','What should we build next?','The next chapter belongs to the generations who will shape the future.','next','grid',12]
];
const PARTNERS=[
 ['AECOM','WATG','Gensler','HKS','Morphosis','Buro Happold','Khatib & Alami','NAGA Architects','Frantz Slater Design Collective','DMAA','SIE','Metropoli','Typsa','HAK','Cracknell','HM','ECG','100 Architects','MDR Architects','LANDinc','Crystal Lagoons'],
 ['Ministry of Housing, Utilities & Urban Communities','Ministry of Tourism','GOPP','Egyptian Naval Forces','MOMRAH','PIF','Royal Commission for Jubail & Yanbu','YUWDDA','GIZ','GTZ','BMZ','AGEG','Fawaz Alhokair Estate','Al-Aqeelah','Al Mozaini Real Estate','AK RealEstate Investment','Shaker Consultancy Group'],
 ['Bechtel','Webuild','Hassan Allam','Orascom Construction','CCC','El Hazek','RME','ACC Arabian Construction','Indra','McKinsey','BCG','Hill International']];
const STAFF_IMG={'Prof. Dr. Amr Attia':'amr-attia','Dr. Amro Taibah':'amro-taibah','Eng. Mostafa Fawzy':'mostafa-fawzy','Eng. Sherif Saleh':'sherif-saleh','Dr. Essam Saleh':'essam-saleh','Arch. Ehab Kamal':'ehab-kamal','Arch. Ahmed Naguib':'ahmed-naguib'};
const STAFF=[['Prof. Dr. Amr Attia','Principal & Visionary Lead, CEO','30+'],['Dr. Amro Taibah','Landscape planning, conservation & restoration, desert and coastal ecosystems','30+'],['Eng. Mostafa Fawzy','Construction Director, multinational project delivery','37+'],['Eng. Sherif Saleh','Strategic finance, green economy & startup transformation','30+'],['Dr. Essam Saleh','Development Manager, business development','30+'],['Arch. Ehab Kamal','Senior Master Planner, architecture & landscape','37+'],['Arch. Ahmed Naguib','Senior Urban Designer, research-led city planning','10+']];
const NETWORK=[['Anthony Mallows','Former CEO, WATG · Placemaking & real estate strategy'],['Dan Ringelstein','Former Director, SOM · City planning & mixed-use master planning'],['Charles Ledward','Former Global Head, AECOM · Economic planning & delivery'],['Dr. Alfonso Vegara','Founder, Fundación Metropoli · Former ISOCARP President'],['Joanna M. Esty','Former VP, AECOM · Smart cities & infrastructure technology'],['Marc Stringa','Founder, Territorio · City-scale strategic planning'],['Dr. Saleh Al Hathloul','Architectural identity · Arab Muslim city · Urbanism'],['Prof. Fekri Hassan','Emeritus Professor, UCL · Cultural heritage management'],['Dr. Dalila El-Kerdany','Cairo University · Heritage preservation & conservation'],['Keith Still','Crowd management & crowd security'],['Bernardus Djonoputro','Regional development & infrastructure financing'],['Mohamed El Baradei','CEO, VS Capital · Urban branding & PPP'],['Del Hossain','RIBA architect · Leadership & design management'],['Michael Jones','Heritage consultant · Archaeological conservation'],['Dr. Basim Omar Kadi','Hajj & Umrah expert']];
const AWARDS=[['Nasser Memorial Civic Center, Egypt','First Prize'],['Planning of Luxor City and its Region','First Prize'],['El-Ashish Urbanized Communities, Kuwait','First Prize'],['Al-Jahraa Low Income Housing, Kuwait','First Prize'],['Obour Memorial and Museum, Ismailia','First Prize'],['Tut-Amoun Village Hotel, Aswan','First Prize'],['National Development Bank Complex, Cairo','First Prize'],['El-Arish City Master Planning','First Prize'],['Marina El-Alamein Tourist Center, Phase 3','First Prize'],['Marina Matrouh Tourist Complex','First Prize'],['Saudi Import Company HQ, Jeddah','First Prize'],['Hurghada Hotel and Shopping Mall','First Prize'],['Samatour Tourist Resort, Gulf of Suez','First Prize'],['El-Khamayel Residential City, 6th of October','First Prize'],['Strategic planning, North Coast at Ras El Hekma','First Prize'],['Residential compound, 6th of October City','First Prize'],['Aluminum City Residential Quarters, Nagaa Hammady','Second Prize'],['Suez Canal Bank Headquarters, Cairo','Second Prize'],['El-Bustan Hotel, Recreational & Offices Building','Second Prize'],['Hotel & Administrative Complex, Kasr El-Nil','Second Prize'],['Industrial Union Building','Second Prize'],['El-Shark Insurance Complex','Second Prize'],['500-feddan development, International Park, Alexandria','Second Prize']];
const TL=[[1966,'PUD is founded','Prof. Abdallah Abdel Aziz Attia establishes PUD.',1],[1978,'NW Coast Regional Vision','An early regional vision for Egypt’s North West Coast.'],[1981,'Tut Amoun Village','Egypt’s first tourist village, Lake Nasser.',1],[1986,'Marina El-Alamein','First large-scale tourism project on the NW Coast.'],[1991,'Hilton Dahab Village','An early international resort on the Gulf of Aqaba.'],[1992,'Rome Biennale','Tut Amoun recognised internationally.'],[1993,'Marina Latakia','Coastal development in Syria.'],[1994,'Madinah Hotels','Hospitality architecture in Madinah.'],[2001,'Royal Oasis Compound','Residential compound, Sheikh Zayed.'],[2008,'New Najaf City','City-making in Iraq.'],[2010,'International Star, Paris','Leadership in Quality award.',1],[2012,'Jeddah Spatial Framework','City plans for Jeddah.'],[2018,'PUD Saudi','Founded by Dr. Amr A. Attia.',1],[2022,'Alamein Riviera & Azha','North Coast destinations.'],[2024,'Al Mashaaer','Holy Sites master plan advisory.'],[2025,'Pyramids Plateau & NAC','Giza destination; New Capital Phases 2–4.'],[2026,'60 years','Sumou Boulevard and Cairo Media City.',1]];
const PAGES=[['Home','index.html'],['Projects','projects.html'],['60 Years','60-years.html'],['People','people.html'],['Sustainability','sustainability.html'],['News','news.html'],['About','about.html'],['Contact','contact.html']];

const pimg=(p,big)=>p&&p.i?`<img src="img/${p.s}${big?'':'-t'}.jpg" alt="${esc(p.n)}" loading="lazy" decoding="async">`:art(p?p.k:'grid',p?p.e:1,big?1600:400,big?900:300);
const bySlug=s=>P.find(p=>p.s===s);
const arrowR='<svg viewBox="0 0 16 16"><path d="M2 8h12M9 3l5 5-5 5"/></svg>',arrowL='<svg viewBox="0 0 16 16"><path d="M14 8H2M7 3L2 8l5 5"/></svg>';
const pcard=p=>`<a class="pc" href="project-${p.s}.html" data-r="${p.r}" data-t="${esc(p.t)}"><div class="th">${pimg(p)}</div><h3>${esc(p.n)}</h3><div class="meta">${esc(p.l)}</div></a>`;
const ncard=n=>`<a class="card" href="${n.u}"${/^http/.test(n.u)?' target="_blank" rel="noopener"':''}><div class="th">${nthumb(n)}</div><div class="lbl">${n.c}</div><h3>${esc(n.h)}</h3><div class="meta">${n.d}</div></a>`;

/* =============== CHROME =============== */
const body=document.body, hdr=$('.hdr');
/* ---- CTA landing: same-page links glide to their section; new pages open at the top (or at their section) ---- */
try{history.scrollRestoration='manual'}catch(e){}
const HOFF=()=>(hdr?hdr.offsetHeight:64)+12;
const secOf=h=>{if(!h)return null;try{return document.getElementById(decodeURIComponent(h))}catch(e){return null}};
const goSec=(el,smooth)=>{const y=el.getBoundingClientRect().top+scrollY-HOFF();scrollTo({top:Math.max(0,y),behavior:smooth&&!RM?'smooth':'instant'})};
const landing=()=>{const el=secOf(location.hash.slice(1));if(el&&el.id!=='main'){goSec(el,false);setTimeout(()=>goSec(el,false),350)}else scrollTo({top:0,behavior:'instant'})};
scrollTo({top:0,behavior:'instant'});
addEventListener('load',()=>requestAnimationFrame(()=>requestAnimationFrame(landing)));
addEventListener('pageshow',e=>{if(e.persisted)landing()});
document.addEventListener('click',e=>{
  const a=e.target.closest('a[href]');if(!a||a.target==='_blank'||e.metaKey||e.ctrlKey||e.shiftKey)return;
  const href=a.getAttribute('href');if(/^(https?:|mailto:|tel:)/.test(href))return;
  const here=location.pathname.split('/').pop()||'index.html';const [file,hash]=href.split('#');
  if((file===''||file===here)&&hash!==undefined){const el=secOf(hash);
    if(el){e.preventDefault();e.stopImmediatePropagation();body.classList.remove('menu-open','search-open','lock');const mb=$('#menuBtn');if(mb)mb.setAttribute('aria-expanded','false');history.pushState(null,'','#'+hash);goSec(el,true)}
    else if(hash===''||file===here){/* hash-routed views (project pages, filters) start from the top */setTimeout(()=>scrollTo({top:0,behavior:'instant'}),0)}}
},true);
const fade=$('.fade');
if(fade)requestAnimationFrame(()=>fade.classList.add('gone'));
addEventListener('pageshow',e=>{if(e.persisted&&fade){fade.classList.remove('go');fade.classList.add('gone')}});
document.addEventListener('click',e=>{
  const a=e.target.closest('a');if(!a||!fade||RM)return;
  const href=a.getAttribute('href')||'';
  if(a.target==='_blank'||href.startsWith('#')||/^(https?:|mailto:|tel:)/.test(href)||!/\.html/.test(href)||e.metaKey||e.ctrlKey||e.shiftKey)return;
  const here=location.pathname.split('/').pop()||'index.html';const [file,hash]=href.split('#');
  if(file===here){body.classList.remove('menu-open','search-open','lock');if(hash&&file==='project.html'){}return}
  e.preventDefault();fade.classList.remove('gone');fade.classList.add('go');setTimeout(()=>{location.href=href},300);
});
const menuBtn=$('#menuBtn'),searchBtn=$('#searchBtn');
function closeAll(){body.classList.remove('menu-open','search-open','lock');menuBtn&&menuBtn.setAttribute('aria-expanded','false')}
menuBtn&&menuBtn.addEventListener('click',()=>{const open=!body.classList.contains('menu-open')&&!body.classList.contains('search-open');closeAll();if(open){body.classList.add('menu-open','lock');menuBtn.setAttribute('aria-expanded','true')}});
$$('.mi-x').forEach(b=>b.addEventListener('click',()=>{const mi=b.closest('.mi');mi.classList.toggle('open');b.setAttribute('aria-expanded',mi.classList.contains('open'))}));
searchBtn&&searchBtn.addEventListener('click',()=>{const open=!body.classList.contains('search-open');closeAll();if(open){body.classList.add('search-open','lock');setTimeout(()=>$('#q')&&$('#q').focus(),200);runSearch('')}});
addEventListener('keydown',e=>{if(e.key==='Escape')closeAll()});
const idx=[...P.map(p=>({p:p,h:p.n,m:`Project · ${p.l}${p.y?' · '+p.y:''}`,u:'project-'+p.s+'.html',k:p.k,e:p.e,t:(p.n+' '+p.l+' '+p.t+' '+(p.d||'')).toLowerCase()})),
 ...NEWS.map(n=>({n:n,h:n.h,m:`${n.c} · ${n.d}`,u:n.u,k:'region',e:3,t:(n.h+' '+n.c).toLowerCase()})),
 ...PAGES.map(([n,u])=>({h:n,m:'Page',u,k:'region',e:n.length,t:n.toLowerCase()})),
 ...STAFF.map(s=>({n:{img:STAFF_IMG[s[0]]+'.jpg'},h:s[0],m:'People · '+s[1],u:'people.html',k:'people',e:3,t:(s[0]+' '+s[1]).toLowerCase()}))];
function runSearch(v){const out=$('#sres');if(!out)return;v=v.trim().toLowerCase();
  const res=(v?idx.filter(i=>i.t.includes(v)):idx.filter(i=>i.m==='Page'||i.p&&i.p.f)).slice(0,14);
  out.innerHTML=(v?`<div class="meta" style="padding-bottom:8px">${res.length} result${res.length===1?'':'s'}</div>`:'<div class="meta" style="padding-bottom:8px">Suggested</div>')+res.map(i=>`<a href="${i.u}"><div class="th">${i.p?pimg(i.p):i.n?nthumb(i.n):art(i.k,i.e)}</div><div><div class="lbl">${esc(i.m)}</div><h4>${esc(i.h)}</h4></div><span class="meta">→</span></a>`).join('')}
$('#q')&&$('#q').addEventListener('input',e=>runSearch(e.target.value));

/* =============== GENERIC =============== */
$$('[data-art]').forEach(el=>{el.innerHTML=art(el.dataset.art,+el.dataset.seed||1,+(el.dataset.w||400),+(el.dataset.h||300))});
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.1,rootMargin:'0px 0px -5% 0px'});
const watch=()=>$$('.rv:not(.in)').forEach(el=>io.observe(el));
const runCount=el=>{cancelAnimationFrame(el._raf);const end=+el.dataset.count,suf=el.dataset.suf||'',from=+(el.dataset.from||0);if(RM){el.textContent=end+suf;return}const t0=performance.now();const st=t=>{const k=Math.min(1,(t-t0)/1600);el.textContent=Math.round(from+(end-from)*(1-Math.pow(1-k,3)))+(k>=1?suf:'');if(k<1)el._raf=requestAnimationFrame(st)};el._raf=requestAnimationFrame(st)};
const co=new IntersectionObserver(es=>es.forEach(e=>{const el=e.target;if(e.isIntersecting){if(!el._on){el._on=1;runCount(el)}}else{el._on=0;cancelAnimationFrame(el._raf);if(!RM)el.textContent=String(+(el.dataset.from||0))}}),{threshold:.35});
$$('[data-count]').forEach(el=>co.observe(el));

function carousel(root){
  const track=$('.car-track',root),n=$('.car-n',root),[prev,next]=$$('.arrows button',root);
  const upd=()=>{const cards=$$('.card',track);if(!cards.length)return;const w=cards[0].offsetWidth;const per=Math.max(1,Math.round(track.clientWidth/w));const pages=Math.max(1,Math.ceil(cards.length/per));const pg=Math.min(pages,Math.round(track.scrollLeft/(w*per))+1);n.textContent=`${String(pg).padStart(2,'0')}/${String(pages).padStart(2,'0')}`};
  prev&&prev.addEventListener('click',()=>{track.scrollBy({left:-track.clientWidth*.9})});
  next&&next.addEventListener('click',()=>{track.scrollBy({left:track.clientWidth*.9})});
  track.addEventListener('scroll',()=>requestAnimationFrame(upd),{passive:true});addEventListener('resize',upd);upd();
}

/* =============== HOME =============== */
const slider=$('#heroSlider');
if(slider){
  const slides=[
   {l:'60 Years · Cairo Media City, Giza',h:'Sixty years of building sustainable cities — the legacy continues, the future begins.',u:'60-years.html',p:'cairo-media-city'},
   {l:'Project',h:'Pyramids Plateau Destination: timeless heritage, future destination.',u:'project-pyramids-plateau.html',p:'pyramids-plateau'},
   {l:'Project',h:'Al Mashaaer Al Mugaddassah: a year-round, resilient destination for the Holy Sites.',u:'project-al-mashaaer.html',p:'al-mashaaer'},
   {l:'Project',h:'Alamein Riviera: a year-round Mediterranean icon on Egypt’s North Coast.',u:'project-alamein-riviera.html',p:'alamein-riviera'},
   {l:'Project',h:'Sumou Boulevard: the region’s first regenerative city-making development.',u:'project-sumou-boulevard.html',p:'sumou-boulevard'}];
  slider.insertAdjacentHTML('afterbegin',slides.map((s,i)=>`<div class="slide${i?'':' on'}${s.scene?' sc':' ph'}" aria-hidden="${i?'true':'false'}"><div class="bg">${s.scene?'<div class="scene"><div class="sun"></div><div class="layer l-far" style="bottom:22%"></div><div class="layer l-mid" style="bottom:12%"></div><div class="layer l-near" style="bottom:2%"></div><div class="layer l-front" style="bottom:-4%"></div></div>':`<img src="img/${s.p}.jpg" alt="" ${i?'loading="lazy"':''} style="object-position:${s.pos||'50% 50%'}">`}</div><div class="shade"></div><div class="cap"><a href="${s.u}"><div class="lbl o">${s.l}</div><h2>${s.h}</h2></a></div></div>`).join(''));
  const dots=$('.dots',slider);dots.innerHTML=slides.map((s,i)=>`<button aria-label="Show slide ${i+1}" class="${i?'':'on'}"><i></i></button>`).join('');
  let cur=0,playing=!RM,timer;const sl=$$('.slide',slider),db=$$('button',dots);
  const go=i=>{sl[cur].classList.remove('on');sl[cur].setAttribute('aria-hidden','true');db[cur].classList.remove('on');cur=(i+sl.length)%sl.length;sl[cur].classList.add('on');sl[cur].setAttribute('aria-hidden','false');db[cur].classList.add('on');slider.classList.toggle('onph',sl[cur].classList.contains('ph'))};
  const play=()=>{clearInterval(timer);if(playing)timer=setInterval(()=>go(cur+1),6500)};
  db.forEach((b,i)=>b.addEventListener('click',()=>{go(i);play()}));
  const pb=$('.pause',slider);const icon=()=>{pb.innerHTML=playing?'<svg viewBox="0 0 12 12"><rect x="2" y="1" width="3" height="10"/><rect x="7" y="1" width="3" height="10"/></svg>':'<svg viewBox="0 0 12 12"><path d="M2 1l9 5-9 5z"/></svg>';pb.setAttribute('aria-label',playing?'Pause slideshow':'Play slideshow')};
  pb.addEventListener('click',()=>{playing=!playing;icon();play()});icon();play();slider.classList.toggle('onph',sl[0].classList.contains('ph'));
}
const newsCar=$('#newsCar');if(newsCar){$('.car-track',newsCar).innerHTML=NEWS.slice(0,8).map(ncard).join('');carousel(newsCar)}
const storyCar=$('#storyCar');if(storyCar){$('.car-track',storyCar).innerHTML=CHAPTERS.map((c,ci)=>`<a class="card" href="60-years.html#${c[3]}"><div class="th"><img src="img/${CH_IMG[ci]}" alt="" loading="lazy"></div><div class="lbl">Story · ${c[0]}</div><h3>${c[1]}</h3><p>${c[2]}</p></a>`).join('');carousel(storyCar)}
const featCar=$('#featCar');if(featCar){$('.car-track',featCar).innerHTML=(window.PUD_FEATURED||[]).map(bySlug).filter(Boolean).map(p=>`<a class="card" href="project-${p.s}.html"><div class="th">${pimg(p)}</div><div class="lbl">${esc(p.t)}</div><h3>${esc(p.n)}</h3><div class="meta">${esc(p.l)}</div></a>`).join('');carousel(featCar)}


/* ===== Snøhetta-inspired home ===== */
const liteBtn=$('#liteBtn'),litePanel=$('#litePanel'),liteSw=$('#liteSw');
if(liteBtn){liteSw.checked=LITE;liteBtn.addEventListener('click',()=>{const o=litePanel.hidden;litePanel.hidden=!o;liteBtn.setAttribute('aria-expanded',o)});
  liteSw.addEventListener('change',()=>{try{localStorage.setItem('pudlite',liteSw.checked?'1':'0')}catch(e){}location.reload()});
  document.addEventListener('click',e=>{if(!e.target.closest('.lite'))litePanel.hidden=true})}
const disc=$('#disc');
if(disc){const DL=[['Urban & Regional Planning','Urban & Regional Planning'],['Master Planning','Master Planning'],['Architecture','Architecture'],['Landscape','Landscape'],['Coastal & Tourism','Coastal & Tourism'],['Strategic Advisory','Strategic Advisory']];
  const slug=t=>'type-'+t.toLowerCase().replace(/&/g,'and').replace(/[^a-z]+/g,'-');
  disc.innerHTML=DL.map(([label,t])=>{const ps=P.filter(p=>p.t===t);const im=(ps.find(p=>p.f&&p.i)||ps.find(p=>p.i)||{}).s;return `<a href="projects.html#${slug(t)}" data-img="${im?'img/'+im+'-t.jpg':''}"><span class="nm">${label}<sup>${ps.length}</sup></span><span class="ar">→</span></a>`}).join('');
  const fl=$('#discFloat'),fi=$('img',fl);let tx=0,ty=0,cx=0,cy=0,on=false;
  disc.addEventListener('mouseover',e=>{const a=e.target.closest('a');if(!a||!a.dataset.img)return;fi.src=a.dataset.img;fl.classList.add('on');on=true});
  disc.addEventListener('mouseleave',()=>{fl.classList.remove('on');on=false});
  addEventListener('mousemove',e=>{tx=e.clientX;ty=e.clientY},{passive:true});
  (function mv(){cx+=(tx-cx)*(RM?1:.18);cy+=(ty-cy)*(RM?1:.18);if(on)fl.style.left=cx+'px',fl.style.top=cy+'px';requestAnimationFrame(mv)})();}
const wide=$('#wideNews');
if(wide){const tr=$('.wide-track',wide);tr.innerHTML=NEWS.slice(0,8).map(n=>`<a class="w-card" href="${n.u}"${/^http/.test(n.u)?' target="_blank" rel="noopener"':''}><div class="th">${nthumb(n).replace('-t.jpg','.jpg')}</div><div class="meta">${n.d} · ${n.c}</div><h3>${esc(n.h)}</h3></a>`).join('');
  const step=()=>($('.w-card',tr)||{offsetWidth:400}).offsetWidth*.9;
  $('.prev',wide).addEventListener('click',()=>tr.scrollBy({left:-step()}));$('.next',wide).addEventListener('click',()=>tr.scrollBy({left:step()}));}
const jt=$('.jt');
if(jt&&$('#jtRail')){
  const M=[[1966,'Founding','Every legacy begins with a vision','Prof. Abdallah Abdel Aziz Attia founds PUD on the synergy between people and their natural and cultural environments.','founder.jpg','60-years.html#ch1'],
   [1978,'Regional planning','Planning Egypt’s North-West Coast','An early regional vision for tourism development along the Mediterranean coast.','nw-coast-1978.jpg','project-nw-coast-1978.html'],
   [1981,'Architecture','Egypt’s first tourist village','Tut Amoun Village on Lake Nasser, designed in harmony with Nubian character.','tut-amoun-village.jpg','project-tut-amoun-village.html'],
   [1986,'Coastal & tourism','The North Coast takes shape','Marina El-Alamein begins: a two-decade landmark of Egyptian tourism.','marina-el-alamein.jpg','project-marina-el-alamein.html'],
   [1991,'Hospitality','On the Gulf of Aqaba','Hilton Dahab Village, among Dahab’s early international resorts.','hilton-dahab.jpg','project-hilton-dahab.html'],
   [2010,'Recognition','International Star for Leadership in Quality','Paris, 2010 — one of 20+ awards and first prizes across six decades.','founder-2.jpg','about.html#awards'],
   [2012,'City planning','Jeddah Spatial Framework Plan','Delivered in a tight six-month window to guide critical planning decisions for Jeddah, with AECOM for MOMRAH.','jeddah-spatial-framework.jpg','project-jeddah-spatial-framework.html'],
   [2013,'Industrial cities','Jazan Economic City','Programme management, master plan update and city management for Saudi Aramco, 2013–2016.','jazan-economic-city.jpg','project-jazan-economic-city.html'],
   [2015,'Infrastructure','Suez Canal Tunnels','Feasibility, design and tender documents for three tunnels under the Suez Canal at Port Said.','suez-canal-tunnels.jpg','project-suez-canal-tunnels.html'],
   [2017,'Architecture','Al Jawhara Residence, Jeddah','A modern yet culturally anchored residential landmark, with Khatib & Alami for Al Mozaini.','al-jawhara-residence.jpg','project-al-jawhara-residence.html'],
   [2018,'A new base','PUD Saudi is founded','Prof. Dr. Amr A. Attia founds PUD Saudi in Riyadh, expanding the firm’s regional impact.','amr-attia-2.jpg','60-years.html#ch2'],
   [2019,'Heritage regions','AlUla County Framework Plan','Policy and planning advisory to safeguard AlUla’s landscapes and heritage, with AECOM for the Royal Commission for AlUla.','alula-framework.jpg','project-alula-framework.html'],
   [2020,'Heritage','Khaybar Heritage Area Master Plan','With WATG, part of the Royal Commission for AlUla’s vision for a world-class cultural destination.','khaybar-heritage.jpg','project-khaybar-heritage.html'],
   [2021,'Smart & green cities','Heliopark, New Cairo','A 7 km² smart and green community of 10,000 homes for Hassan Allam Properties.','heliopark.jpg','project-heliopark.html'],
   [2022,'Coastal','Alamein Riviera','A year-round Mediterranean icon of almost 10 million m², with WATG for the Ministry of Housing.','alamein-riviera.jpg','project-alamein-riviera.html'],
   [2023,'Healing landscapes','NEOM Royal Hospital Landscape','Healing through nature: the landscape masterplan for NEOM’s Royal Hospital, with Saudi Diyar.','neom-hospital.jpg','project-neom-hospital.html'],
   [2024,'Holy Sites','Al Mashaaer Al Mugaddassah','A year-round, resilient vision for Mina, Muzdalifah and Arafat, welcoming 50,000+ pilgrims daily.','al-mashaaer.jpg','project-al-mashaaer.html'],
   [2025,'Global minds','Pyramids Plateau & the New Capital','A global model for heritage tourism at Giza, and strategic advisory for New Administrative Capital Phases 2–4.','pyramids-plateau.jpg','project-pyramids-plateau.html'],
   [2026,'60 years','What should we build next?','Sumou Boulevard and Cairo Media City open the next chapter.','sumou-boulevard.jpg','project-sumou-boulevard.html']];
  const Y0=1966,Y1=2026,YE=2010,PE=42,pct=y=>y<=YE?(y-Y0)/(YE-Y0)*PE:PE+(y-YE)/(Y1-YE)*(100-PE),unpct=q=>q<=PE?Y0+q/PE*(YE-Y0):YE+(q-PE)/(100-PE)*(Y1-YE);
  const media=$('#jtMedia'),rail=$('#jtRail'),handle=$('#jtHandle'),fill=$('#jtFill'),yearEl=$('#jtYear');
  media.innerHTML=M.map((m,i)=>`<img src="img/${m[4]}" alt="" class="${i?'':'on'}" loading="${i?'lazy':'eager'}">`).join('');
  let t='',lastLab=-99;for(let y=Y0;y<=Y1;y++){const m=M.findIndex(x=>x[0]===y);let show=m>=0&&(m===0||m===M.length-1||y-lastLab>=(y>YE?2:4))&&(m===M.length-1||Y1-y>=2);if(show)lastLab=y;
    t+=m>=0?`<button class="jt-m${show?'':' nolab'}" style="left:${pct(y)}%" data-i="${m}" aria-label="${y}: ${M[m][2]}"><b>${y}</b></button>`:`<i class="jt-t${y%10===0?' dec':''}" style="left:${pct(y)}%">${y%10===0?`<em>${y}</em>`:''}</i>`}
  $('#jtTicks').innerHTML=t;
  let cur=0,shownYear=Y0,anim,timer;
  const imgs=$$('img',media),mk=$$('.jt-m',jt);
  function setPos(y){const p=pct(y);handle.style.left=p+'%';fill.style.width=p+'%'}
  function countTo(to){cancelAnimationFrame(anim);if(RM){yearEl.textContent=to;shownYear=to;return}const from=shownYear,t0=performance.now();(function st(n){const k=Math.min(1,(n-t0)/700),e=1-Math.pow(1-k,3);shownYear=Math.round(from+(to-from)*e);yearEl.textContent=shownYear;if(k<1)anim=requestAnimationFrame(st)})(t0)}
  function go(i,fromDrag){cur=(i+M.length)%M.length;const m=M[cur];
    imgs.forEach((im,k)=>im.classList.toggle('on',k===cur));mk.forEach((b,k)=>b.classList.toggle('on',k===cur));
    $('#jtKicker').textContent=m[1];$('#jtTitle').textContent=m[2];$('#jtDesc').textContent=m[3];media.href=m[5];
    $('#jtCount').textContent=`${String(cur+1).padStart(2,'0')} / ${String(M.length).padStart(2,'0')}`;
    jt.querySelector('.jt-text').classList.remove('in');void jt.offsetWidth;jt.querySelector('.jt-text').classList.add('in');
    if(!fromDrag)setPos(m[0]);countTo(m[0]);rail.setAttribute('aria-valuenow',m[0]);rail.setAttribute('aria-valuetext',`${m[0]}: ${m[2]}`)}
  const nearest=y=>M.reduce((b,m,i)=>Math.abs(m[0]-y)<Math.abs(M[b][0]-y)?i:b,0);
  const yAt=x=>{const r=rail.getBoundingClientRect();return unpct(clamp((x-r.left)/r.width,0,1)*100)};
  let drag=false;
  rail.addEventListener('pointerdown',e=>{if(e.target.closest('.jt-m'))return;drag=true;rail.setPointerCapture(e.pointerId);handle.classList.add('drag');const y=yAt(e.clientX);setPos(y);go(nearest(y),true);stop()});
  rail.addEventListener('pointermove',e=>{if(!drag)return;const y=yAt(e.clientX);setPos(y);const n=nearest(y);if(n!==cur)go(n,true)});
  const end=()=>{if(!drag)return;drag=false;handle.classList.remove('drag');setPos(M[cur][0])};
  rail.addEventListener('pointerup',end);rail.addEventListener('pointercancel',end);
  mk.forEach(b=>b.addEventListener('click',()=>{go(+b.dataset.i);stop()}));
  $('#jtPrev').addEventListener('click',()=>{go(cur-1);stop()});$('#jtNext').addEventListener('click',()=>{go(cur+1);stop()});
  rail.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='ArrowUp'){e.preventDefault();go(cur+1);stop()}else if(e.key==='ArrowLeft'||e.key==='ArrowDown'){e.preventDefault();go(cur-1);stop()}else if(e.key==='Home'){go(0);stop()}else if(e.key==='End'){go(M.length-1);stop()}});
  let user=false;function stop(){clearInterval(timer);timer=null;user=true}
  go(0);
  if(!RM){const io2=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting&&!timer&&!user){timer=setInterval(()=>go(cur+1),4200)}else if(!en.isIntersecting&&timer){clearInterval(timer);timer=null}}),{threshold:.4});io2.observe(jt);jt.addEventListener('pointerenter',stop)}
}

/* =============== PROJECT INDEX =============== */
const pIndex=$('#pIndex');
if(pIndex){
  const st={r:'all',t:'all'};
  pIndex.innerHTML=P.map(pcard).join('');
  const types=$('#ptypes');types.innerHTML=`<button class="on" data-t="all">All projects<sup>${P.length}</sup></button>`+TYPES.map(t=>`<button data-t="${esc(t)}">${t}<sup>${P.filter(p=>p.t===t).length}</sup></button>`).join('');
  const fp=$('#fpanel'),fb=$('#fbtn');
  fb.addEventListener('click',()=>{fp.classList.toggle('open');fb.setAttribute('aria-expanded',fp.classList.contains('open'))});
  $('#fRegion').innerHTML=['all','egypt','ksa','intl'].map(k=>`<button class="chip${k==='all'?' on':''}" data-r="${k}">${k==='all'?'All regions':REG[k]}</button>`).join('');
  $('#fType').innerHTML=['all',...TYPES].map(k=>`<button class="chip${k==='all'?' on':''}" data-t="${esc(k)}">${k==='all'?'All types':k}</button>`).join('');
  $('#fEra').innerHTML=['all','2020s','2010s','2000s','Before 2000'].map(k=>`<button class="chip${k==='all'?' on':''}" data-e="${k}">${k==='all'?'All years':k}</button>`).join('');
  st.e='all';
  const era=y=>{const n=parseInt(y);if(!n)return'';return n>=2020?'2020s':n>=2010?'2010s':n>=2000?'2000s':'Before 2000'};
  function apply(){let c=0;$$('.pc',pIndex).forEach((el,i)=>{const p=P[i];const ok=(st.r==='all'||p.r===st.r)&&(st.t==='all'||p.t===st.t)&&(st.e==='all'||era(p.y)===st.e);el.classList.toggle('hide',!ok);if(ok)c++});
    $$('#ptypes button').forEach(b=>b.classList.toggle('on',b.dataset.t===st.t));
    $$('#fRegion .chip').forEach(b=>b.classList.toggle('on',b.dataset.r===st.r));$$('#fType .chip').forEach(b=>b.classList.toggle('on',b.dataset.t===st.t));$$('#fEra .chip').forEach(b=>b.classList.toggle('on',b.dataset.e===st.e));
    const act=[st.r!=='all'&&REG[st.r],st.t!=='all'&&st.t,st.e!=='all'&&st.e].filter(Boolean);
    $('#fsum').innerHTML=`${c} project${c===1?'':'s'}${act.length?' · '+act.join(', ')+'<button id="fclear">Clear all</button>':''}`;
    const cl=$('#fclear');cl&&cl.addEventListener('click',()=>{st.r='all';st.t='all';st.e='all';apply()});
    $('#pEmpty').hidden=c>0;
    try{localStorage.setItem('pudf',JSON.stringify(st))}catch(e){}}
  types.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;st.t=b.dataset.t;apply();$('#fbar').scrollIntoView({behavior:RM?'auto':'smooth'})});
  fp.addEventListener('click',e=>{const b=e.target.closest('.chip');if(!b)return;if(b.dataset.r)st.r=b.dataset.r;if(b.dataset.t)st.t=b.dataset.t;if(b.dataset.e)st.e=b.dataset.e;apply()});
  const h=location.hash.slice(1);if(REG[h])st.r=h;if(h.startsWith('type-')){const t=TYPES.find(t=>'type-'+t.toLowerCase().replace(/&/g,'and').replace(/[^a-z]+/g,'-')===h);if(t)st.t=t}
  apply();
}

/* =============== PROJECT DETAIL =============== */
let pxEls=[];
const pd=$('#pDetail');
function renderProject(){
  if(!pd)return;const s=pd.dataset.slug||location.hash.slice(1);const i=Math.max(0,P.findIndex(p=>p.s===s));const p=P[i];
  if(!pd.dataset.slug)document.title=`${p.n} — PUD Consultants`;
  const facts=[['Location',p.l],['Year',p.y],['Type',p.t],['Region',REG[p.r]],['Client',p.c]].filter(f=>f[1]);
  const prev=P[(i-1+P.length)%P.length],next=P[(i+1)%P.length];
  pd.innerHTML=`<div class="pd-top gut"><div class="crumb"><a href="projects.html">Projects</a> / <a href="projects.html#${p.r}">${REG[p.r]}</a></div><h1 class="rv">${esc(p.n)}</h1><div class="meta rv d1">${esc(p.l)}${p.y?' · '+p.y:''}</div></div>
  <div class="pd-hero" data-px="0.12">${pimg(p,1)}</div>
  <div class="pd-body gut">
    <dl class="facts rv">${facts.map(f=>`<dt>${f[0]}</dt><dd>${esc(f[1])}</dd>`).join('')}</dl>
    <div class="rv d1">${p.d?`<p class="lead">${esc(p.d)}</p>`:`<p class="lead">${esc(p.n)} is part of PUD’s ${esc(p.t.toLowerCase())} portfolio in ${esc(REG[p.r]==='International'?p.l:REG[p.r])}.</p>`}
      ${p.sc?`<h4 class="lbl" style="margin:28px 0 10px">Scope of services by PUD</h4><ul>${p.sc.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>`:''}</div>
    <div class="rv d2">${p.q?`<p class="pd-quote">“${esc(p.q)}”</p>`:''}</div>
  </div>
  <div class="gut" style="display:flex;justify-content:space-between;gap:20px;border-top:1px solid var(--rule);padding-top:20px;padding-bottom:20px;flex-wrap:wrap">
    <a href="project-${prev.s}.html" class="btn">${arrowL.replace('<svg','<svg width=16')} ${esc(prev.n)}</a><a href="project-${next.s}.html" class="btn">${esc(next.n)} ${arrowR.replace('<svg','<svg width=16')}</a></div>`;
  const rel=P.filter(x=>x!==p&&(x.t===p.t||x.r===p.r)).slice(0,6);
  const rc=$('#relCar');if(rc){$('.car-track',rc).innerHTML=rel.map(x=>`<a class="card" href="project-${x.s}.html"><div class="th">${pimg(x)}</div><div class="lbl">${esc(x.t)}</div><h3>${esc(x.n)}</h3><div class="meta">${esc(x.l)}</div></a>`).join('');$('.car-track',rc).scrollLeft=0;carousel(rc)}
  pxEls=$$('[data-px]');watch();scrollTo(0,0);
}
/* 60 years film strip */
$$('.film').forEach(f=>{const t=$('.fm-track',f);const step=()=>{const c=$('.fm-c',t);return c?c.offsetWidth+18:300};
  const pv=$('.fm-prev',f),nx=$('.fm-next',f);pv&&pv.addEventListener('click',()=>t.scrollBy({left:-step()}));nx&&nx.addEventListener('click',()=>t.scrollBy({left:step()}));
  let down=false,sx=0,sl=0,moved=false;t.addEventListener('pointerdown',e=>{if(e.pointerType!=='mouse')return;down=true;moved=false;sx=e.clientX;sl=t.scrollLeft;t.style.scrollSnapType='none';t.style.scrollBehavior='auto'});
  addEventListener('pointermove',e=>{if(!down)return;const d=e.clientX-sx;if(Math.abs(d)>4)moved=true;t.scrollLeft=sl-d});
  addEventListener('pointerup',()=>{if(!down)return;down=false;t.style.scrollSnapType='';t.style.scrollBehavior=''});
  t.addEventListener('click',e=>{if(moved){e.preventDefault();e.stopPropagation();moved=false}},true);
  t.addEventListener('dragstart',e=>e.preventDefault())});
/* sustainability commitment: swap image as each block reaches the middle */
const cmI=$$('.cm-img'),cmB=$$('.cm-b');
if(cmB.length){const cio=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){const i=e.target.dataset.i;cmI.forEach(m=>m.classList.toggle('on',m.dataset.i===i));cmB.forEach(b=>b.classList.toggle('on',b.dataset.i===i))}}),{rootMargin:'-45% 0px -45% 0px'});cmB.forEach(b=>cio.observe(b))}
/* legacy hash URLs (project.html#slug, article.html#slug) -> static, indexable pages */
(()=>{const f=location.pathname.split('/').pop(),h=location.hash.slice(1);if(!h)return;
  if(f==='project.html'&&P.some(p=>p.s===h))location.replace('project-'+h+'.html');
  if(f==='article.html'&&NEWS.some(n=>n.s===h))location.replace('article-'+h+'.html')})();
const ad=$('#aDetail');
function renderArticle(){
  if(!ad)return;const s=ad.dataset.slug||location.hash.slice(1);const i=Math.max(0,NEWS.findIndex(n=>n.s===s));const n=NEWS[i];
  if(!ad.dataset.slug)document.title=`${n.h} — PUD Consultants`;
  const prev=NEWS[(i-1+NEWS.length)%NEWS.length],next=NEWS[(i+1)%NEWS.length];
  ad.innerHTML=`<div class="pd-top gut"><div class="crumb"><a href="news.html">News</a> / ${esc(n.c)}</div><h1 class="rv art-h">${esc(n.h)}</h1><div class="meta rv d1">${esc(n.d)} · ${esc(n.c)}</div></div>
  <div class="pd-hero" data-px="0.12">${nthumb(n).replace('-t.jpg','.jpg')}</div>
  <div class="pd-body gut art-body">
    <dl class="facts rv">${(n.f||[]).map(f=>`<dt>${esc(f[0])}</dt><dd>${esc(f[1])}</dd>`).join('')}</dl>
    <div class="art-txt rv d1">${n.b.map((t,k)=>`<p${k?'':' class="lead"'}>${esc(t)}</p>`).join('')}
      ${n.l?`<div class="art-links">${n.l.map(l=>`<a class="btn" href="${l[1]}">${esc(l[0])} ${arrowR.replace('<svg','<svg width=16')}</a>`).join('')}</div>`:''}</div>
  </div>
  <div class="gut" style="display:flex;justify-content:space-between;gap:20px;border-top:1px solid var(--rule);padding-top:20px;padding-bottom:20px;flex-wrap:wrap">
    <a href="article-${prev.s}.html" class="btn">${arrowL.replace('<svg','<svg width=16')} Previous</a><a href="news.html" class="btn ghost" style="margin:0">All news</a><a href="article-${next.s}.html" class="btn">Next ${arrowR.replace('<svg','<svg width=16')}</a></div>`;
  const more=$('#moreNews');if(more)more.innerHTML=NEWS.filter(x=>x!==n).slice(0,3).map(x=>`<a class="w-card" href="${x.u}"><div class="th">${nthumb(x)}</div><div class="meta">${x.d} · ${x.c}</div><h3>${esc(x.h)}</h3></a>`).join('');
  pxEls=$$('[data-px]');watch();
}
if(ad){renderArticle();addEventListener('hashchange',()=>{renderArticle();scrollTo({top:0,behavior:'instant'})})}
if(pd){renderProject();addEventListener('hashchange',()=>{renderProject();scrollTo({top:0,behavior:'instant'})})}

/* =============== 60 YEARS =============== */
['#mq1','#mq2','#mq3'].forEach((id,k)=>{const el=$(id);if(!el)return;const html=PARTNERS[k].map((p,i)=>`<span class="${i%5===0?'k':''}">${p}</span><i></i>`).join('');el.innerHTML=html+html});
const tlTrack=$('#tlTrack');if(tlTrack)tlTrack.innerHTML=TL.map(t=>`<div class="tl-i${t[3]?' k':''}"><b>${t[0]}</b><i></i><h4>${t[1]}</h4><p>${t[2]}</p></div>`).join('')+'<div style="flex:0 0 var(--gut)"></div>';
const mapEl=$('#map');let setStep=()=>{},curView,targetView;
if(mapEl){
  const PJ=(lon,lat)=>[(lon-24)*28,(37-lat)*28];
  const poly=pts=>pts.map((p,i)=>(i?'L':'M')+PJ(p[0],p[1]).map(v=>v.toFixed(1)).join(' ')).join(' ')+'Z';
  const W={med:[[24,31.9],[25.2,31.6],[27.2,31.4],[28.9,30.95],[29.9,31.2],[30.4,31.5],[31.0,31.6],[32.3,31.3],[33.6,31.1],[34.2,31.3],[34.6,31.8],[34.9,32.5],[35.1,33.3],[35.5,33.9],[35.9,34.6],[35.9,35.5],[36.2,36.6],[36.0,37],[24,37]],
   red:[[32.55,29.95],[32.7,29.2],[33.3,28.3],[33.8,27.6],[34.25,27.75],[34.45,28.2],[34.8,29.45],[34.98,29.5],[34.75,28.6],[35.2,28.0],[35.6,27.5],[36.5,26.0],[37.2,25.0],[38.1,24.0],[38.8,22.7],[39.15,21.5],[40.0,20.4],[40.8,19.2],[41.6,18.0],[42.5,16.6],[42.8,15.2],[43.3,13.0],[43.4,12.6],[43.0,12.6],[41.6,13.6],[40.0,15.4],[39.2,16.4],[38.5,18.0],[37.4,20.6],[37.1,21.9],[36.4,22.4],[35.6,23.9],[35.0,25.0],[34.5,25.9],[33.9,27.0],[33.4,27.7],[32.9,28.6],[32.55,29.95]],
   gulf:[[47.9,30.0],[48.4,28.6],[48.9,27.6],[49.6,26.9],[50.15,26.1],[50.6,25.3],[50.8,24.8],[51.6,24.2],[52.5,24.15],[53.8,24.1],[54.6,24.6],[55.3,25.3],[56.05,26.0],[56.4,26.4],[57,26.6],[57,27.0],[56.5,27.15],[55.5,26.7],[54.4,26.6],[53.2,27.0],[52.0,27.8],[50.9,28.9],[50.2,30.0],[49.0,30.4],[48.0,30.1]]};
  const nile=[[31.4,22],[32.3,23.0],[32.9,24.1],[32.75,25.2],[32.65,25.7],[32.3,26.1],[31.7,26.6],[31.2,27.2],[30.8,28.1],[31.1,29.0],[31.25,30.05],[30.9,30.6],[30.4,31.4]];
  const pins=[['egypt','Giza Pyramids Plateau',31.13,29.98,1],['egypt','Cairo Media City',30.95,29.85],['egypt','New Administrative Capital',31.75,30.02,1],['egypt','Royal Oasis · Sheikh Zayed',30.98,30.1],['egypt','Sumou Blvd · Mostakbal City',31.6,30.15],['egypt','Alamein Riviera',28.95,30.83,1],['egypt','Marassi',28.75,30.92],['egypt','Ras El Hekma',27.9,31.15,1],['egypt','Marsa Matrouh',27.24,31.35,1],['egypt','Sokhna Heights',32.35,29.6],['egypt','Samatour · Gulf of Suez',32.7,29.15],['egypt','Hilton Dahab',34.51,28.5,1],['egypt','Port Ghalib',34.86,25.53,1],['egypt','Gargoub',33.55,26.6],['egypt','Castle Zaman',33.8,27.26],['egypt','Tut Amoun · Aswan',32.88,24.0,1],['egypt','Assiut',31.18,27.18],['egypt','Sohag',31.7,26.56],['egypt','Tanta',31.0,30.79],
   ['ksa','Riyadh · Diriyah · Taj Al Riyadh',46.7,24.7,1],['ksa','Jeddah',39.2,21.5,1,'L'],['ksa','Makkah · Al Mashaaer',39.95,21.7,1],['ksa','Madinah Hotels',39.6,24.47,1],['ksa','AlUla',37.92,26.62],['ksa','Khaybar Heritage',39.3,25.7,1],['ksa','Jazan Economic City',42.55,16.9,1],['ksa','NEOM',35.2,28.0,1],['ksa','Al Khafji · Gulf Coast',48.49,28.44,1],['ksa','Najran',44.13,17.49],['ksa','Taif',40.42,21.27,0,'N'],['ksa','Yanbu · YUWDDA',38.06,24.09],['ksa','Red Sea Project',36.6,25.6],
   ['intl','Kuwait',47.98,29.37,1],['intl','Al-Aqeelah Oasis · Damascus',36.3,33.5,1],['intl','Marina Latakia',35.78,35.52,1],['intl','Homs',36.72,34.73],['intl','New Najaf City',44.33,32.0,1],['intl','FAO Port · Basrah',48.5,29.97],['intl','Dubai',55.27,25.2,1],['intl','Tehran Laleh Hotel',51.39,35.69,1],['intl','Gaza & West Bank',34.45,31.5]];
  let s=`<defs><pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse"><path d="M0 6 L6 0" stroke="#d9e2e7" stroke-width=".6"/></pattern></defs><rect x="-600" y="-600" width="2200" height="1900" fill="#F7F5F2"/>`;
  for(let x=-588;x<=1512;x+=28)s+=`<line x1="${x}" y1="-588" x2="${x}" y2="1288" stroke="#EEEAE4" stroke-width=".4"/>`;
  for(let y=-588;y<=1288;y+=28)s+=`<line x1="-588" y1="${y}" x2="1512" y2="${y}" stroke="#EEEAE4" stroke-width=".4"/>`;
  Object.values(W).forEach(w=>{s+=`<path d="${poly(w)}" fill="#E8EDF0"/><path d="${poly(w)}" fill="url(#hatch)" stroke="#bccad2" stroke-width=".6"/>`});
  s+=`<path d="${nile.map((p,i)=>(i?'L':'M')+PJ(p[0],p[1]).join(' ')).join(' ')}" fill="none" stroke="#9fb6c2" stroke-width="1.4"/>`;
  const lab=(t,lon,lat,z=9)=>{const[x,y]=PJ(lon,lat);return `<text x="${x}" y="${y}" font-family="Roboto" font-size="${z}" letter-spacing="2" fill="#a59c90" text-anchor="middle">${t}</text>`};
  s+=lab('EGYPT',28.5,26.5,12)+lab('SAUDI ARABIA',44.5,23.5,13)+lab('MEDITERRANEAN SEA',29.5,34,7)+lab('RED SEA',38.2,20.0,7)+lab('ARABIAN GULF',51.6,27.4,6)+lab('IRAQ',43.5,33.6,10)+lab('SYRIA',38.6,35.2,9)+lab('IRAN',53.5,33.0,10)+lab('UAE',54.2,23.5,8);
  pins.forEach(p=>{const[x,y]=PJ(p[2],p[3]);const left=(p[2]<32&&p[0]==='egypt')||p[5]==='L';
    s+=`<g class="pin" data-reg="${p[0]}"><circle class="h" cx="${x}" cy="${y}" r="3"/><circle class="c" cx="${x}" cy="${y}" r="${p[4]?3:2}"/><text x="${left?x-6:x+6}" y="${y+2.5}" text-anchor="${left?'end':'start'}">${p[5]==='N'?'':p[1]}</text></g>`});
  mapEl.innerHTML=s;
  ['egypt','ksa','intl'].forEach(k=>{const el=$(`[data-tags="${k}"]`);if(el)el.innerHTML=pins.filter(p=>p[0]===k&&p[5]!=='N').map(p=>`<span>${p[1]}</span>`).join('')});
  /* fit each view to its pins *including labels*, so nothing is cut at the edges */
  const fit=(sel,d)=>{try{let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;$$(sel,mapEl).forEach(g=>{const b=g.getBBox();if(!b.width)return;x0=Math.min(x0,b.x);y0=Math.min(y0,b.y);x1=Math.max(x1,b.x+b.width);y1=Math.max(y1,b.y+b.height)});if(x1<x0)return d;const px=(x1-x0)*.08+14,py=(y1-y0)*.08+14;return[x0-px,y0-py,x1-x0+2*px,y1-y0+2*py]}catch(e){return d}};
  const views=[fit('.pin[data-reg="egypt"]',[0,140,364,280]),fit('.pin[data-reg="ksa"]',[270,130,520,500]),fit('.pin',[180,0,744,616])];
  /* size the steps box to the tallest step so its tags are never clipped */
  const stepsBox=$('.steps');const sizeSteps=()=>{if(!stepsBox)return;let m=0;$$('.step',stepsBox).forEach(x=>m=Math.max(m,x.scrollHeight));if(m)stepsBox.style.minHeight=m+'px'};sizeSteps();addEventListener('resize',sizeSteps);curView=views[0].slice();targetView=views[0].slice();let cs=-1;
  setStep=n=>{if(n===cs)return;cs=n;$$('.step').forEach(x=>x.classList.toggle('on',+x.dataset.step===n));$$('.j-tabs .chip').forEach(b=>b.classList.toggle('on',+b.dataset.go===n));
    const reg=['egypt','ksa','intl'][n];$$('.pin').forEach(p=>{const on=p.dataset.reg===reg;p.classList.toggle('on',on);p.classList.toggle('dim',!on&&n!==2)});$('#far')&&$('#far').classList.toggle('on',n===2);targetView=views[n].slice()};
  setStep(0);
  $$('.j-tabs .chip').forEach(b=>b.addEventListener('click',()=>{const n=+b.dataset.go,j=$('#journey');if(innerWidth>900)scrollTo({top:j.offsetTop+(j.offsetHeight-innerHeight)*(n/3+.12),behavior:RM?'auto':'smooth'});setStep(n)}));
}

/* cover layers */
function buildScene(cv){const Wd=1600;
  const ridge=(h,base,amp,n,seed,fill)=>{const r=rng(seed);let d=`M0 ${h} L0 ${base}`;for(let i=1;i<=n;i++){const x=Wd*i/n;d+=` Q ${x-Wd/n/2} ${base-amp*r()} ${x} ${base-amp*(.4+r()*.6)*Math.abs(Math.sin(i*1.3+seed))}`}return `<path d="${d} L${Wd} ${h} Z" fill="${fill}"/>`};
  const L=(sel,h,inner)=>{const el=$(sel,cv);if(el)el.innerHTML=`<svg viewBox="0 0 ${Wd} ${h}" preserveAspectRatio="none" aria-hidden="true">${inner}</svg>`};
  L('.l-far',300,ridge(300,230,60,8,3,'#EFEDEA')+'<g fill="#E4E0DA"><path d="M980 230 L1080 120 L1180 230Z"/><path d="M1150 230 L1225 150 L1300 230Z"/><path d="M1290 230 L1335 185 L1380 230Z"/></g>');
  (()=>{const r=rng(21);let b='';let x=0;while(x<Wd){const w=24+r()*60,h=40+r()*(x>500&&x<1000?190:110);b+=`<rect x="${x}" y="${300-h}" width="${w}" height="${h}" fill="${r()>.84?'#FBD7CF':'#E9E9E9'}"/>`;if(r()>.6)for(let yy=300-h+10;yy<290;yy+=14)b+=`<line x1="${x+5}" x2="${x+w-5}" y1="${yy}" y2="${yy}" stroke="#fff" stroke-width="1.2"/>`;x+=w+2+r()*10}L('.l-mid',300,b)})();
  L('.l-near',260,ridge(260,150,70,6,9,'#F1ECE5')+'<g fill="none" stroke="#E0D9CF">'+Array.from({length:7},(_,i)=>`<path d="M0 ${170+i*14} Q 400 ${150+i*14} 800 ${175+i*14} T 1600 ${165+i*14}"/>`).join('')+'</g>');
  L('.l-front',200,'<path d="M0 200 L0 90 Q 300 60 600 95 T 1200 85 T 1600 80 L1600 200Z" fill="#fff"/><g stroke="#E6E6E6">'+Array.from({length:24},(_,i)=>`<line x1="${i*70}" y1="200" x2="${800+(i*70-800)*.35}" y2="96"/>`).join('')+'</g><path d="M0 90 Q 300 60 600 95 T 1200 85 T 1600 80" fill="none" stroke="#EE4223" stroke-width="1.5"/>');
}
$$('.st-cover,.scene').forEach(buildScene);

/* =============== PEOPLE / ABOUT / NEWS =============== */
const ini=n=>n.replace(/^(Prof\. Dr\.|Dr\.|Eng\.|Arch\.)\s*/,'').split(' ').map(w=>w[0]).join('');
const staff=$('#staff');if(staff)staff.innerHTML=STAFF.map((p,i)=>`<div class="pp rv d${i%4}"><div class="portrait ph"><img src="img/${STAFF_IMG[p[0]]}.jpg" alt="${p[0]}" loading="lazy"></div><h4>${p[0]}</h4><p>${p[1]}</p><p style="color:var(--o)">${p[2]} years of experience</p></div>`).join('');
const net=$('#networkWrap');if(net)net.innerHTML=NETWORK.map(n=>`<div><h4>${n[0]}</h4><p>${n[1]}</p></div>`).join('');
const aw=$('#awardList');if(aw)aw.innerHTML=AWARDS.map(a=>`<div><span>${a[0]}</span><span>${a[1]}</span></div>`).join('');
const nl=$('#newsList');
if(nl){const cats=['All',...new Set(NEWS.map(n=>n.c))];const nf=$('#newsF');let cur='All';
  const draw=()=>{nl.innerHTML=NEWS.filter(n=>cur==='All'||n.c===cur).map(n=>`<a class="nrow rv" href="${n.u}"${/^http/.test(n.u)?' target="_blank" rel="noopener"':''}><div class="th">${nthumb(n)}</div><div><div class="lbl o">${n.c}</div><h3>${esc(n.h)}</h3>${n.x?`<p>${esc(n.x)}</p>`:''}</div><div class="meta">${n.d}</div></a>`).join('');nf.innerHTML=cats.map(c=>`<button class="chip${c===cur?' on':''}">${c}</button>`).join('');watch()};
  nf.addEventListener('click',e=>{const b=e.target.closest('.chip');if(b){cur=b.textContent;draw()}});draw()}

/* form */
/* =============== ENQUIRIES (contact form + floating chat) =============== */
const MAIL_TO='0da4bada9ef65bbe295f6ada2514de50' /* FormSubmit alias of inas.bakeer@wai-s.com (keeps the address out of public code) */,MAIL_CC='m.sawaf@risepersonal.com';
const THANKS='Thank you for contacting us. Our team will respond and get back to you within 48 hours.';
const sendEnquiry=async(d,source)=>{
  const fd=new FormData();
  Object.entries(d).forEach(([k,v])=>fd.append(k,v||'—'));
  fd.append('Source',source+' · '+location.href);
  fd.append('_subject','PUD website enquiry: '+(d.Enquiry||'General')+' — '+(d.Name||''));
  fd.append('_cc',MAIL_CC);fd.append('_template','table');fd.append('_captcha','false');
  if(d.Email)fd.append('_replyto',d.Email);
  const r=await fetch('https://formsubmit.co/ajax/'+MAIL_TO,{method:'POST',headers:{Accept:'application/json'},body:fd});
  const j=await r.json().catch(()=>({}));if(!r.ok||String(j.success)==='false')throw new Error(j.message||'Send failed');return j};
const failMsg=err=>/activ/i.test(err&&err.message||'')?'Almost ready: this form is waiting for a one-time activation by the site owner. Please try again shortly, or call +20 2 2414 7537.':'Sorry, your message could not be sent. Please try again or call +20 2 2414 7537.';
const okEmail=v=>/^\S+@\S+\.\S+$/.test(v.trim());

const form=$('#cform');form&&form.addEventListener('submit',async e=>{e.preventDefault();const f=e.target;const note=$('#fnote');
  if(f._honey&&f._honey.value)return;
  if(!f.fn.value.trim()||!okEmail(f.em.value)||!f.msg.value.trim()){note.textContent='Please add your name, a valid email and a message.';return}
  const b=f.querySelector('button[type=submit]');b.disabled=true;note.textContent='Sending…';
  try{await sendEnquiry({Name:(f.fn.value+' '+f.ln.value).trim(),Email:f.em.value,Enquiry:f.ty.value,Message:f.msg.value},'Contact page');f.reset();note.textContent=THANKS}
  catch(err){note.textContent=failMsg(err)}
  finally{b.disabled=false}});

/* floating chat */
(()=>{
  const w=document.createElement('div');w.className='pchat';w.innerHTML=`
  <button class="pc-btn" type="button" aria-label="Chat with PUD" aria-expanded="false" aria-controls="pcPanel">
    <svg class="pc-i1" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5h16v11H9l-5 4z"/></svg>
    <svg class="pc-i2" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
  <section class="pc-panel" id="pcPanel" role="dialog" aria-label="Send PUD a message" hidden>
    <header class="pc-h"><img src="img/pud-logo-v.png" alt=""><div><b>PUD Consultants</b><span>We usually reply within 48 hours</span></div></header>
    <div class="pc-body">
      <div class="pc-msg">Hello 👋 How can we help? Leave your details and our team will get back to you.</div>
      <form class="pc-form" novalidate>
        <input type="text" name="_honey" tabindex="-1" autocomplete="off" class="pc-hp" aria-hidden="true">
        <label>Name<input name="name" autocomplete="name" required></label>
        <label>Email<input name="email" type="email" autocomplete="email" required></label>
        <label>Phone <em>(optional)</em><input name="phone" type="tel" autocomplete="tel"></label>
        <label>Topic<select name="topic"><option>New project</option><option>Strategic advisory</option><option>Partnership</option><option>Careers</option><option>Media</option><option>Other</option></select></label>
        <label>Message<textarea name="message" rows="3" required></textarea></label>
        <button class="pc-send" type="submit">Send message <svg viewBox="0 0 16 10" width="16" aria-hidden="true"><path d="M0 5h14M10 1l4 4-4 4"/></svg></button>
        <p class="pc-note" aria-live="polite"></p>
      </form>
      <div class="pc-done" hidden><div class="pc-tick">✓</div><p></p><button type="button" class="pc-again">Send another message</button></div>
    </div>
  </section>`;
  document.body.appendChild(w);
  const btn=$('.pc-btn',w),panel=$('.pc-panel',w),f=$('.pc-form',w),note=$('.pc-note',w),done=$('.pc-done',w);
  const setOpen=o=>{w.classList.toggle('open',o);panel.hidden=!o;btn.setAttribute('aria-expanded',String(o));if(o&&done.hidden)setTimeout(()=>f.elements.name.focus(),60)};
  btn.addEventListener('click',()=>setOpen(panel.hidden));
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!panel.hidden)setOpen(false)});
  $('.pc-again',w).addEventListener('click',()=>{done.hidden=true;f.hidden=false;f.elements.name.focus()});
  f.addEventListener('submit',async e=>{e.preventDefault();if(f._honey.value)return;
    const v=n=>f.elements[n].value.trim();
    if(!v('name')||!okEmail(v('email'))||!v('message')){note.textContent='Please add your name, a valid email and a message.';return}
    const sb=$('.pc-send',w);sb.disabled=true;note.textContent='Sending…';
    try{await sendEnquiry({Name:v('name'),Email:v('email'),Phone:v('phone'),Enquiry:v('topic'),Message:v('message')},'Website chat');
      f.reset();note.textContent='';f.hidden=true;$('p',done).textContent=THANKS;done.hidden=false}
    catch(err){note.textContent=failMsg(err)}
    finally{sb.disabled=false}});
})();

watch();

/* =============== SCROLL ENGINE =============== */
pxEls=$$('[data-px]');
const isHero=!!slider||!!$('.st-cover');
const z60=$('.z60'),z60m=z60&&$('.z60-mask',z60),z60e=z60&&$('.z60-end',z60),z60c=z60&&$('.z60-cap',z60);
if(z60){/* find a point inside the solid stroke of the "6" so the zoom lands fully inside the photo */
  const setOrigin=()=>{const sp=$('span',z60m);const mr=z60m.getBoundingClientRect(),r=sp.getBoundingClientRect();if(!r.width)return;
    const c=document.createElement('canvas'),W=Math.ceil(r.width),H=Math.ceil(r.height);c.width=W;c.height=H;const x=c.getContext('2d');const cs=getComputedStyle(sp);
    x.font=`${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;x.textBaseline='middle';x.textAlign='center';x.fillStyle='#000';x.fillText(sp.textContent,W/2,H/2);
    const d=x.getImageData(0,0,W,H).data;let best=null;
    for(const fy of [.5,.55,.45,.6,.4]){const y=Math.round(H*fy);let run=0,st=0;for(let i=0;i<W/2;i++){const a=d[(y*W+i)*4+3]>128;if(a){if(!run)st=i;run++}else if(run){if(!best||run>best.w)best={w:run,x:st+run/2,y};run=0;break}}if(best&&best.w>W*.05)break}
    if(best){const ox=r.left-mr.left+best.x,oy=r.top-mr.top+best.y;z60m.style.transformOrigin=`${ox}px ${oy}px`}};
  const prev=z60m.style.transform;z60m.style.transform='';(document.fonts&&document.fonts.ready||Promise.resolve()).then(()=>{setOrigin();z60m.style.transform=prev});
  addEventListener('resize',()=>{const t=z60m.style.transform;z60m.style.transform='';setOrigin();z60m.style.transform=t});}
if(z60){const ims=$$('.z60-ph img',z60),names=['Pyramids Plateau Destination · Giza','Alamein Riviera · North Coast','Al Mashaaer Al Mugaddassah · Makkah','Cairo Media City · Giza','Khaybar Heritage Area · AlUla'];let zi=0;const nm=$('#z60Name');setInterval(()=>{if(document.hidden)return;ims[zi].classList.remove('on');zi=(zi+1)%ims.length;ims[zi].classList.add('on');if(nm)nm.textContent=names[zi]},2600)}
const cover=$('.st-cover'),coverLayers=$$('.st-cover [data-depth]'),journey=$('#journey'),tl=$('#timeline'),qs=$('.y60'),qsl=$$('.y60-w span'),qsd=$$('.y60-dots i'),big=$('.big60');
let mx=0,my=0,smx=0,smy=0;addEventListener('mousemove',e=>{mx=e.clientX/innerWidth-.5;my=e.clientY/innerHeight-.5},{passive:true});
function frame(){
  const sy=scrollY,vh=innerHeight;
  if(hdr&&!hdr.classList.contains('always'))hdr.classList.toggle('solid',sy>20||body.classList.contains('menu-open')||body.classList.contains('search-open'));
  smx+=(mx-smx)*.06;smy+=(my-smy)*.06;
  if(!RM){
    pxEls.forEach(el=>{const r=el.getBoundingClientRect();if(r.bottom<-100||r.top>vh+100)return;const f=+el.dataset.px;const t=el.firstElementChild;if(t)t.style.transform=`translate3d(0,${(r.top+r.height/2-vh/2)*-f}px,0)`});
    if(slider){const bgs=$$('.slide .bg',slider);bgs.forEach(b=>b.style.translate=`${-smx*18}px ${sy*.3-smy*10}px`);if(big)big.style.transform=`translate3d(${smx*-24}px,${sy*-.2}px,0)`}
    if(cover){const r=cover.getBoundingClientRect();const p=clamp(-r.top/cover.offsetHeight,0,1);coverLayers.forEach(l=>{const d=+l.dataset.depth;l.style.transform=`translate3d(${-smx*d*40}px,${p*d*-260+smy*d*-12}px,0)${l.classList.contains('num')?` scale(${1+p*.3})`:''}`})}
    $$('[data-mx]').forEach(el=>{const r=el.getBoundingClientRect();if(r.bottom<-200||r.top>vh+200)return;el.style.transform=`translate3d(${-el.scrollWidth/4+(r.top-vh/2)*+el.dataset.mx}px,0,0)`});
  }
  const strip=document.getElementById('strip');
  if(strip&&innerWidth>760){const r=strip.getBoundingClientRect();const p=RM?1:clamp(-r.top/(strip.offsetHeight-vh+64),0,1);const e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;
    const m=$('.s-main',strip);m.style.width=(56+44*e)+'vw';m.style.height=(66+34*e)+'%';
    $('.s-l',strip).style.transform=`translate(${-e*32}vw,-50%)`;$('.s-r',strip).style.transform=`translate(${e*32}vw,-50%)`;
    $$('.s-side',strip).forEach(s=>s.style.opacity=1-e*1.2);strip.classList.toggle('full',e>.82)}
  if(journey&&innerWidth>900){const r=journey.getBoundingClientRect();if(r.top<vh&&r.bottom>0)setStep(Math.floor(clamp(-r.top/(journey.offsetHeight-vh),0,.999)*3))}
  if(mapEl&&curView){for(let i=0;i<4;i++)curView[i]+=(targetView[i]-curView[i])*(RM?1:.07);mapEl.setAttribute('viewBox',curView.map(v=>v.toFixed(2)).join(' '))}
  if(tl&&tlTrack){const r=tl.getBoundingClientRect();if(r.top<vh&&r.bottom>0){const p=clamp(-r.top/(tl.offsetHeight-vh),0,1);tlTrack.style.transform=`translate3d(${-p*(tlTrack.scrollWidth-innerWidth)}px,0,0)`;$('#tlBar').style.width=p*100+'%'}}
  if(z60){const r=z60.getBoundingClientRect();const p=clamp(-r.top/(z60.offsetHeight-vh),0,1);const e=p*p*p;z60m.style.transform=RM?'':`scale(${1+e*60})`;z60m.style.visibility=p>.985?'hidden':'visible';z60e.style.opacity=String(clamp((p-.8)/.15,0,1));z60e.style.transform=`translate3d(0,${(1-clamp((p-.8)/.15,0,1))*30}px,0)`;z60c.style.opacity=String(1-clamp(p/.2,0,1))}
  if(qs){const r=qs.getBoundingClientRect();const p=clamp(-r.top/(qs.offsetHeight-vh),0,1);const k=Math.min(qsl.length-1,Math.floor(p*qsl.length*.999));qsl.forEach((d,i)=>{d.classList.toggle('on',i===k);d.classList.toggle('past',i<k)});qsd.forEach((d,i)=>d.classList.toggle('on',i<=k));const bg=qs.querySelector('.y60-bg');if(bg&&!RM)bg.style.transform=`translate3d(0,${(p-.5)*-80}px,0) scale(${1+p*.08})`}
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
})();
