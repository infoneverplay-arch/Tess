# One dict per page. To add a tool: append a dict and run `python3 build.py`.
REC_TOOL='''<div class="tool"><div>
<label>Codec / format</label><select id="codec"></select>
<label>Frame rate (fps)</label><input id="fps" type="number" value="24" step="0.001">
<label>Bitrate (Mbps) <span id="note"></span></label><input id="mbps" type="number" value="0">
<label>Card / drive size (GB)</label><input id="card" type="number" value="256">
<label>Footage length (minutes)</label><input id="mins" type="number" value="60">
</div><div class="out">
<div>Recording time on card</div><div class="big" id="rt">-</div>
<div class="row"><span>Storage for your footage</span><b id="st">-</b></div>
<div class="row"><span>Per minute</span><b id="pm">-</b></div>
<div class="row"><span>Per hour</span><b id="ph">-</b></div>
<div class="row"><span>With 2 backups (3 copies)</span><b id="bk">-</b></div></div></div>'''
REC_JS='''
// Approximate bitrates in Mbps at 29.97 fps (Apple ProRes white paper values for UHD/1080). Scale linearly with fps.
const C={"ProRes 4444 - UHD 4K":1061,"ProRes 422 HQ - UHD 4K":707,"ProRes 422 - UHD 4K":471,"ProRes 422 LT - UHD 4K":328,"ProRes 422 Proxy - UHD 4K":145,"ProRes 422 HQ - 1080p":176,"ProRes 422 - 1080p":117,"ProRes 422 LT - 1080p":82,"H.265 - 4K (typical 150 Mbps)":-150,"H.264 - 4K (typical 100 Mbps)":-100,"H.264 - 1080p (typical 50 Mbps)":-50,"Custom bitrate":0};
const s=document.getElementById("codec");for(const k in C){const o=document.createElement("option");o.textContent=k;s.appendChild(o)}
const $=i=>document.getElementById(i);
function gb(x){return x>=1000?(x/1000).toFixed(2)+" TB":x.toFixed(1)+" GB"}
function setRate(){const v=C[s.value],f=+$("fps").value||24;if(v>0)$("mbps").value=Math.round(v*f/29.97);else if(v<0)$("mbps").value=-v;$("note").textContent=v>0?"(scaled to frame rate)":v<0?"(set by camera)":"(enter yours)";calc()}
function calc(){const m=+$("mbps").value||0,gbm=m*60/8/1000;$("pm").textContent=gb(gbm);$("ph").textContent=gb(gbm*60);const t=gbm?($("card").value/gbm):0;$("rt").textContent=gbm?Math.floor(t/60)+" h "+Math.round(t%60)+" min":"-";const st=gbm*($("mins").value||0);$("st").textContent=gb(st);$("bk").textContent=gb(st*3)}
s.onchange=setRate;$("fps").oninput=setRate;["mbps","card","mins"].forEach(i=>$(i).oninput=calc);setRate();'''
DOF_TOOL='''<div class="tool"><div>
<label>Sensor</label><select id="sensor"><option value="0.030">Full frame (CoC 0.030 mm)</option><option value="0.025">Super 35 / ~1.3x (CoC 0.025 mm)</option><option value="0.020" selected>APS-C 1.5x (CoC 0.020 mm)</option><option value="0.015">Micro Four Thirds (CoC 0.015 mm)</option><option value="0.011">1-inch (CoC 0.011 mm)</option></select>
<label>Focal length (mm)</label><input id="f" type="number" value="35">
<label>Aperture (f-stop)</label><input id="n" type="number" value="2.8" step="0.1">
<label>Focus distance</label><input id="d" type="number" value="3" step="0.1">
<label>Units</label><select id="u"><option value="1">meters</option><option value="0.3048">feet</option></select>
</div><div class="out"><div>Total depth of field</div><div class="big" id="tot">-</div>
<div class="row"><span>Near limit</span><b id="near">-</b></div><div class="row"><span>Far limit</span><b id="far">-</b></div>
<div class="row"><span>In front of subject</span><b id="fr">-</b></div><div class="row"><span>Behind subject</span><b id="bh">-</b></div>
<div class="row"><span>Hyperfocal distance</span><b id="hf">-</b></div></div></div>'''
DOF_JS='''const $=i=>document.getElementById(i);
function calc(){const c=+$("sensor").value,f=+$("f").value,N=+$("n").value,u=+$("u").value,s=+$("d").value*u*1000;if(!f||!N||!s)return;
const H=f*f/(N*c)+f,near=s*(H-f)/(H+s-2*f),far=s<H?s*(H-f)/(H-s):Infinity;
const fm=x=>!isFinite(x)?"Infinity":(x/1000/u).toFixed(2)+($("u").value=="1"?" m":" ft");
$("near").textContent=fm(near);$("far").textContent=fm(far);$("tot").textContent=isFinite(far)?fm(far-near):"Infinity";
$("fr").textContent=fm(s-near);$("bh").textContent=isFinite(far)?fm(far-s):"Infinity";$("hf").textContent=fm(H)}
document.querySelectorAll("input,select").forEach(e=>e.oninput=calc);calc();'''
AR_TOOL='''<div class="tool"><div>
<label>Source width (px)</label><input id="w" type="number" value="3840"><label>Source height (px)</label><input id="h" type="number" value="2160">
<label>Target aspect ratio</label><select id="r"><option>2.39</option><option>2.35</option><option>2.00</option><option>1.85</option><option>1.78</option><option>1.66</option><option>1.33</option><option>1.00</option><option value="0.8">0.80 (4:5 Instagram)</option><option value="0.5625">0.5625 (9:16 vertical)</option></select>
</div><div class="out"><div>Crop to</div><div class="big" id="crop">-</div>
<div class="row"><span>Source ratio</span><b id="sr">-</b></div><div class="row"><span>Letterbox bars (each)</span><b id="lb">-</b></div>
<div class="row"><span>Pillarbox bars (each)</span><b id="pb">-</b></div><div class="row"><span>Pixels kept</span><b id="pk">-</b></div></div></div>'''
AR_JS='''const $=i=>document.getElementById(i);const ev=x=>Math.round(x/2)*2;
function calc(){const w=+$("w").value,h=+$("h").value,r=+$("r").value;if(!w||!h)return;const sr=w/h;let cw=w,ch=h;
if(r>sr){ch=ev(w/r)}else{cw=ev(h*r)}$("crop").textContent=cw+" x "+ch;$("sr").textContent=sr.toFixed(3)+":1";
$("lb").textContent=ch<h?(h-ch)/2+" px top & bottom":"none";$("pb").textContent=cw<w?(w-cw)/2+" px left & right":"none";$("pk").textContent=Math.round(cw*ch/(w*h)*100)+"%"}
document.querySelectorAll("input,select").forEach(e=>e.oninput=calc);calc();'''
TL_TOOL='''<div class="tool"><div>
<label>Real event duration (minutes)</label><input id="ev" type="number" value="120">
<label>Shooting interval (seconds between frames)</label><input id="iv" type="number" value="5" step="0.5">
<label>Playback frame rate</label><select id="fps"><option>24</option><option>25</option><option>30</option><option>60</option></select>
<label>Photo size (MB per frame)</label><input id="mb" type="number" value="25">
</div><div class="out"><div>Final clip length</div><div class="big" id="len">-</div>
<div class="row"><span>Frames to shoot</span><b id="fr">-</b></div><div class="row"><span>Speed-up</span><b id="sp">-</b></div>
<div class="row"><span>Storage needed</span><b id="st">-</b></div></div></div>'''
TL_JS='''const $=i=>document.getElementById(i);
function calc(){const e=+$("ev").value*60,i=+$("iv").value,f=+$("fps").value;if(!e||!i)return;const n=Math.floor(e/i),l=n/f;
$("len").textContent=Math.floor(l/60)+"m "+(l%60).toFixed(1)+"s";$("fr").textContent=n.toLocaleString();$("sp").textContent=Math.round(i*f)+"x";
const g=n*($("mb").value||0)/1000;$("st").textContent=g>=1000?(g/1000).toFixed(2)+" TB":g.toFixed(1)+" GB"}
document.querySelectorAll("input,select").forEach(e=>e.oninput=calc);calc();'''
ETSY_CTA=("Planning a shoot?","Grab ready-made call sheets, shot lists, budgets and schedules that work in Excel and Google Sheets.")
PAGES=[
dict(fn="index.html",title="Frame Math: Free Calculators for Filmmakers and Videographers",desc="Free filmmaking calculators: recording time and storage, depth of field, aspect ratio crop and timelapse. Fast, mobile friendly, no sign-up.",
 h1="Free calculators for filmmakers",lead="Quick answers on set and in prep. No sign-up, works on your phone.",
 tool='''<div class="cards"><a class="card" href="recording-time-calculator.html"><h3>Recording time & storage</h3><p>How many minutes fit on your card, and how many TB you need.</p></a>
<a class="card" href="depth-of-field-calculator.html"><h3>Depth of field</h3><p>Near and far focus limits for any lens, aperture and sensor.</p></a>
<a class="card" href="aspect-ratio-crop-calculator.html"><h3>Aspect ratio crop</h3><p>Exact crop and letterbox sizes for 2.39, 1.85, 9:16 and more.</p></a>
<a class="card" href="timelapse-calculator.html"><h3>Timelapse</h3><p>Interval, frame count, clip length and storage.</p></a></div>''',js="",article="",gear=[],cta=ETSY_CTA),
dict(fn="recording-time-calculator.html",title="Video Recording Time & Storage Calculator (ProRes, H.264, H.265)",desc="Calculate how much recording time fits on your card and how much storage your footage needs, for ProRes, H.264 and H.265 at any frame rate.",
 h1="Recording time & storage calculator",lead="Pick a codec and frame rate to see minutes per card and total storage, including backups.",tool=REC_TOOL,js=REC_JS,
 article='''<h2>How this works</h2><p>Video file size depends on bitrate: megabits per second. Divide by 8 to get megabytes per second, and multiply by your recording time. ProRes bitrates scale with frame rate, so 4K ProRes 422 HQ at 60 fps is about twice the size of 30 fps. Long-GOP codecs like H.264 and H.265 use whatever bitrate your camera is set to, so check your menu and type it in.</p>
<h2>Plan for three copies</h2><p>Most productions keep footage in three places: a working drive and two backups, one of them off site. The calculator shows that total so you can budget drives before the shoot, not after.</p>''',
 gear=[("Fast CFexpress Type B cards","CFexpress Type B card 512GB"),("Portable SSDs for on-set backup","portable SSD 2TB"),("Rugged hard drives for archive","rugged external hard drive 5TB")],cta=ETSY_CTA),
dict(fn="depth-of-field-calculator.html",title="Depth of Field Calculator for Video & Photo (Full Frame, S35, APS-C, MFT)",desc="Free depth of field calculator. Enter focal length, f-stop, focus distance and sensor size to get near and far limits and hyperfocal distance.",
 h1="Depth of field calculator",lead="See exactly how much of your scene will be sharp for any lens, aperture and sensor.",tool=DOF_TOOL,js=DOF_JS,
 article='''<h2>Reading the results</h2><p>Depth of field is the zone in front of and behind your focus point that looks acceptably sharp. Wider apertures (lower f-numbers), longer lenses and closer focus make it shallower. The hyperfocal distance is the focus point that keeps everything from half that distance to infinity sharp, which is handy for wides and landscapes.</p>
<h2>About circle of confusion</h2><p>Each sensor size uses a standard circle of confusion. Projecting on a big screen or pulling focus on a 6K+ image? Pick a smaller value (the next sensor down) to be safe.</p>''',
 gear=[("Wireless follow focus systems","wireless follow focus"),("Fast prime lenses","cine prime lens"),("Laser distance measure for focus pullers","laser distance measure")],cta=ETSY_CTA),
dict(fn="aspect-ratio-crop-calculator.html",title="Aspect Ratio Crop & Letterbox Calculator (2.39, 1.85, 9:16, 4:5)",desc="Find the exact crop size and letterbox bars to reframe any resolution to 2.39:1, 1.85:1, 9:16 vertical, 4:5 and more.",
 h1="Aspect ratio crop & letterbox calculator",lead="Get the exact pixel crop and bar sizes for any delivery ratio.",tool=AR_TOOL,js=AR_JS,
 article='''<h2>Crop or letterbox?</h2><p>To deliver 2.39:1 inside a 16:9 file, keep the full frame and add black bars (letterbox). To deliver a true 2.39:1 file, crop to the size shown. Cropping 4K to vertical 9:16 keeps only about a third of the pixels, so frame for it on set if social cutdowns matter.</p><p>Sizes are rounded to even numbers, which most codecs need.</p>''',
 gear=[("Monitors with frame-line overlays","on camera monitor 5 inch"),("Anamorphic lenses","anamorphic lens")],cta=ETSY_CTA),
dict(fn="timelapse-calculator.html",title="Timelapse Calculator: Interval, Frames, Clip Length & Storage",desc="Plan a timelapse: enter event length and interval to get frames, final clip duration, speed-up and storage.",
 h1="Timelapse calculator",lead="Work out your interval, frame count and final clip length before you set up.",tool=TL_TOOL,js=TL_JS,
 article='''<h2>Choosing an interval</h2><p>Fast clouds and traffic look good at 1 to 3 seconds. Sunsets and moving shadows work at 3 to 10 seconds. Construction and plants growing need minutes between frames. A 10 second clip at 24 fps needs 240 frames.</p>''',
 gear=[("Intervalometers","intervalometer"),("Sturdy travel tripods","carbon fiber tripod"),("Motion control sliders","motorized camera slider")],cta=ETSY_CTA),
]
