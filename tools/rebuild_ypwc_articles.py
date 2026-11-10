from pathlib import Path
import re,html,zipfile,xml.etree.ElementTree as ET
root=Path.cwd()
meta={
1:('entropy','The Arrow in the Coffee Cup: How Entropy Gives Time Its Direction','Abdullah Shaker Abdullah','STEM 6-October for Boys','Thermodynamics','Gold','01_coffee_milk.jpg','The Arrow in the Coffee Cup — Entropy connects microscopic possibility with the direction of time, from cooling coffee to the organization of life.'),
2:('non-newtonian-fluids','From Ketchup to Oobleck: Non-Newtonian Fluids and Their Behavior','Adham Mohamed Khairy','STEM High School for Boys – 6th of October','Fluid Mechanics','Silver','02 non-newtonian Fluids.jpg','Why do ketchup, toothpaste, and Oobleck flow so differently? Follow viscosity, shear response, and the models used to describe complex fluids.'),
3:('gps-relativity','GPS & Relativity','Kenzy Raafat Eltablawy','Menofia STEM School','Physics in Daily Life','Bronze','03_gps_satellite.jpg','GPS depends on precise clocks. Einstein’s relativity explains why satellite time must be corrected for motion and gravity.'),
4:('microwave-physics','The Physics of Microwaves: Why Metal Sparks and Water Dances Inside Your Kitchen','Somaya Yasser ElSawaf','STEM Gharbiya','Physics in Daily Life','Finalist','04_lab_microwave.jpg','Explore how microwave ovens heat food, why pointed metal can spark, and how the door mesh keeps waves inside.'),
5:('sound-to-electricity','Can Sound Become Electricity? Turning Everyday Vibrations into Energy','Malak','Alexandria STEM School','Waves and Sound','Finalist','05_acoustic_energy_harvesting.jpg','Sound carries mechanical energy. Follow the piezoelectric and electromagnetic methods used to convert vibrations into small amounts of electricity.')}
figs={
1:{'rId10':('figure-1.jpg','Figure 1. More accessible microscopic arrangements correspond to a higher entropy.'),'unknown':('figure-entropy.gif','Figure 2. Microscopic trajectories can be followed forward or backward under the same apparent initial conditions.')},
2:{'rId4':('figure-5.jpeg','Figure 1. Ketchup is shear-thinning: shaking helps it flow.'),'rId5':('figure-4.jpeg','Figure 2. Oobleck thickens under a sudden force.'),'rId6':('figure-3.jpeg','Figure 3. Toothpaste illustrates yield-stress behavior: it stays in place until squeezed.'),'rId7':('figure-2.png','Figure 4. Flow curves compare the shear response predicted by the fluid models.'),'rId8':('figure-1.png','Figure 5. Calculated velocity profiles for Newtonian and non-Newtonian fluids in a pipe.')},
5:{'rId6':('figure-3.png','Figure 1. Sound travels through a medium as alternating compressions and rarefactions.'),'rId7':('figure-4.png','Figure 2. Amplitude affects wave size, while frequency relates to pitch.'),'rId8':('figure-5.png','Figure 3. A piezoelectric harvester converts diaphragm vibration into a voltage.'),'rId9':('figure-2.png','Figure 4. A moving magnet changes the magnetic flux through a coil, inducing a voltage.'),'rId10':('figure-1.png','Figure 5. The ear converts sound-driven movement into biological signals.')}}

def get_body(n):
 slug=meta[n][0]; text=(root/'content'/'articles'/f'rank-{n:02}-{slug}.md').read_text(encoding='utf-8')
 parts=text.split('\n\n',3); body=parts[3] if len(parts)>3 else ''
 lines=body.splitlines()
 if n in (1,2,5):
  filename_to_key={filename:key for key,(filename,caption) in figs[n].items()}
  seen=set()
  def convert_markdown_image(match):
   filename=Path(match.group(2).split('/')[-1]).name
   key=filename_to_key.get(filename)
   if not key or filename in seen: return ''
   seen.add(filename)
   return f'[[IMAGE:{key}]]'
  body=re.sub(r'!\[[^]]*\]\(([^)]*/)?([^/)]+)\)',convert_markdown_image,body)
  lines=body.splitlines()
 if n==1:
  if lines and lines[0].strip()=='The Arrow in the Coffee Cup': lines=lines[1:]
  lines=[line for line in lines if line.strip()!='By Abdullah Shaker']
  body='\n'.join(lines)
  body=body.replace('[[IMAGE:rId10]][[IMAGE:rId10]]','')
  body=body.replace('Whatever this [[IMAGE:unknown]][[IMAGE:unknown]]direction leads, it leads to greater entropy.','Whatever this direction leads, it leads to greater entropy. [[IMAGE:unknown]]')
  body=re.sub(r'\[\[IMAGE:rId11\]\]', '', body)
  body=re.sub(r'\n\nFigure 2\.living systems maintain internal organization by exchanging energy with their surroundings, while total entropy increases\.','',body,flags=re.I)
  body=body.replace('Even the most organized form of life exists not by stopping the changing, but by flowing energy through it.','Even the most organized form of life exists not by stopping the changing, but by flowing energy through it.')
  body=body.replace('Why Does Entropy  increase','Why Does Entropy Increase').replace('The arrow of time','The Arrow of Time').replace('Entropy and the life','Entropy and Life').replace('conclusion','Conclusion').replace('REFRENCES','References')
  body=body.replace('$$S=k_B ln(ω) $$','$$S = k_B \\ln(\\Omega)$$').replace('$$ΔS(universe)≥0$$','$$\\Delta S_{\\text{universe}} \\ge 0$$').replace('$$ΔS_unv=Q/T(cold)- Q/T(hot)$$','$$\\Delta S_{\\text{universe}} = \\frac{Q}{T_{\\text{cold}}} - \\frac{Q}{T_{\\text{hot}}}$$')
  body=body.replace("Equation 1.Boltzman' s equation","Equation 1. Boltzmann’s entropy relation.").replace('Equation 2. The second low of thermodynamics','Equation 2. The second law of thermodynamics.')
 if n==2:
  if lines and lines[0].strip()==meta[n][1]: lines=lines[1:]
  body='\n'.join(lines)
  body=body.replace('$$τ=μ\\hat{γ}$$','$$\\tau = \\mu \\dot{\\gamma}$$').replace('$$τ=K \\hat{γ}^{n}$$','$$\\tau = K \\dot{\\gamma}^{n}$$').replace('$$μ=K \\hat{γ}^{\\left(n-1\\right)}$$','$$\\mu_{\\text{app}} = K \\dot{\\gamma}^{n-1}$$')
  body=body.replace('$$τ=\\left{τ_{y}+μ\\hat{γ}τ>τ_{y}\\hat{γ}=0τ≤τ_{y}\\right$$','$$\\dot{\\gamma} = \\begin{cases} (\\tau-\\tau_y)/\\mu, & \\tau>\\tau_y \\\\ 0, & \\tau\\le\\tau_y \\end{cases}$$')
  body=body.replace('$$τ=\\left{τ_{y}+K\\hat{γ}^{n}τ>τ_{y}\\hat{γ}=0τ≤τ_{y}\\right$$','$$\\dot{\\gamma} = \\begin{cases} ((\\tau-\\tau_y)/K)^{1/n}, & \\tau>\\tau_y \\\\ 0, & \\tau\\le\\tau_y \\end{cases}$$')
  body=body.replace('$$μ=K\\hat{γ}^{n-1}+\\frac{τ_{y}}{\\hat{γ}}$$','$$\\mu_{\\text{app}} = K\\dot{\\gamma}^{n-1}+\\frac{\\tau_y}{\\dot{\\gamma}}$$')
  body=body.replace('$$Picard (fixed-point) iteration:$$','Picard (fixed-point) iteration:').replace('$$tridiagonal coefficients:$$','Tridiagonal coefficients:')
  body=body.replace('$$μ_{i+\\frac{1}{2}}^{(k)}=μ\\left(\\frac{u_{i+1}^{(k)}-u_{i}^{(k)}}{Δy}\\right),     u_{i}^{(k+1)}=TridiagonalSolve\\left(a^{(k)}, b^{(k)}, c^{(k)}, d\\right)$$','$$\\mu_{i+\\frac{1}{2}}^{(k)} = \\mu\\!\\left(\\frac{u_{i+1}^{(k)}-u_i^{(k)}}{\\Delta y}\\right), \\qquad u_i^{(k+1)} = \\text{TridiagonalSolve}(a^{(k)},b^{(k)},c^{(k)},d)$$')
  body=body.replace('$$a_{i}=\\frac{μ_{i-\\frac{1}{2}}}{Δy^{2}}     b_{i}=-\\frac{μ_{i-\\frac{1}{2}}+μ_{i+\\frac{1}{2}}}{Δy^{2}}     c_{i}=\\frac{μ_{i+\\frac{1}{2}}}{Δy^{2}}     d_{i}=-G$$','$$\\begin{aligned}a_i&=\\frac{\\mu_{i-1/2}}{\\Delta y^2}, & b_i&=-\\frac{\\mu_{i-1/2}+\\mu_{i+1/2}}{\\Delta y^2},\\\\ c_i&=\\frac{\\mu_{i+1/2}}{\\Delta y^2}, & d_i&=-G.\\end{aligned}$$')
  body=body.replace('$$ stopping criterion:     max_{i}\\left|u_{i}^{(k+1)}-u_{i}^{(k)}\\right| < tol$$','Stopping criterion: $$\\max_i \\left|u_i^{(k+1)}-u_i^{(k)}\\right| < \\mathrm{tol}.$$')
  body=body.replace('[[IMAGE:rId4]][[IMAGE:rId5]]','These everyday examples are shown in Figures 1 and 2.\n\n[[IMAGE:rId4]][[IMAGE:rId5]]')
  body=body.replace('[[IMAGE:rId6]]where 𝜏ᵧ is the yield stress.','Toothpaste illustrates this yield-stress behavior in Figure 3.\n\n[[IMAGE:rId6]]\n\nwhere 𝜏ᵧ is the yield stress.')
  body=body.replace('A notable example is fresh concrete (Sochi, 2015).\n\n[[IMAGE:rId7]]','A notable example is fresh concrete (Sochi, 2015).\n\nThe predicted flow curves are compared in Figure 4.\n\n[[IMAGE:rId7]]')
  body=body.replace('[[IMAGE:rId8]]After some computational analysis of those models in a pipe, this graph was obtained:','The computed pipe velocity profiles appear in Figure 5.\n\n[[IMAGE:rId8]]\n\nAfter computational analysis of these models in a pipe, the following graph was obtained:')
 if n==3:
  if lines and lines[0].strip()=='The Clock That Lies: Why Does GPS Need Einstein’s': lines=lines[1:]
  body='\n'.join(lines)
  body=body.replace('Relativity?\nKenzy Raafat Eltablawy\nPhysBA Competition Essay Entry\n','')
  body=body.replace('d = c · Δt','$$d = c\\,\\Delta t$$')
  body=body.replace('γ = 1 / √(1 - v² / c²)','$$\\gamma = \\frac{1}{\\sqrt{1-\\frac{v^2}{c^2}}}$$')
  body=re.sub(r'Kenzy Raafat Eltablawy — PhysBA Submission Page [12] of 2','',body)
 if n==4:
  if lines and (lines[0].strip()==meta[n][1] or lines[0].strip()==meta[n][1]+':'): lines=lines[1:]
  body='\n'.join(lines)
 if n==5:
  if lines and lines[0].strip()==meta[n][1]: lines=lines[1:]
  if lines and lines[0].strip()=='Turning Everyday Vibrations into Energy.': lines=lines[1:]
  body='\n'.join(lines)
  body=body.replace('Fig(1) How sound travels','').replace('Fig(2) Amplitude and frequency','').replace('Fig(3) Piezoelectric effect','').replace('Fig(4) Electromagnetic induction','').replace('Fig(5) Sound into signals','')
  body=body.replace('Sound and seismic waves are examples of mechanical waves.[[IMAGE:rId6]]','Sound and seismic waves are examples of mechanical waves. Their motion is illustrated in Figure 1.\n\n[[IMAGE:rId6]]')
  body=body.replace('What Makes Sound Different?[[IMAGE:rId7]]','What Makes Sound Different?\n\nFigure 2 compares amplitude and frequency.\n\n[[IMAGE:rId7]]')
  body=body.replace('Two methods are the piezoelectric effect and electromagnetic induction.\n\n[[IMAGE:rId8]]','Two methods are the piezoelectric effect and electromagnetic induction. Figure 3 shows a piezoelectric harvester.\n\n[[IMAGE:rId8]]')
  body=body.replace('2. Electromagnetic Induction[[IMAGE:rId9]]','2. Electromagnetic Induction\n\nFigure 4 shows the magnet-and-coil arrangement.\n\n[[IMAGE:rId9]]')
  body=body.replace('[[IMAGE:rId10]]\n\nA Similar Process Happens Inside Our Ears','Figure 5 follows the conversion of vibration into signals in the ear.\n\n[[IMAGE:rId10]]\n\nA Similar Process Happens Inside Our Ears')
 return body

headings={1:{'Why Does Entropy  increase','The second law of thermodynamics','The arrow of time','Entropy and the life','conclusion','REFRENCES :'},2:{'Newtonian Fluids','Non-Newtonian Fluids','Time-Independent Non-Newtonian Fluids','Power Law Model','Bingham Fluid','Herschel-Bulkley Model','Time-Dependent Non-Newtonian Fluids','References'},3:{'The Clock That Lies: Why Does GPS Need Einstein’s Relativity?','How Does GPS Find Your Position?','This Brings Us to Einstein','General Relativity and Gravitational Dilation','Conclusion'},4:set(),5:{'But how does a wave transfer energy?','What Makes Sound Different?','How Can Sound Be Converted into Electricity?','1. The Piezoelectric Effect','2. Electromagnetic Induction','A Similar Process Happens Inside Our Ears','What are the Limitations of generating electricity from sound?','References:-'}}

# Mappings generated by the previous extract pass. Resolve source IDs against the copied local image names.
def image_map(n):
 data={}
 if n in (1,2,5):
  src={1:'The_Arrow_in_the_Coffee_Cup_How_Entropy_Gives_Time_Its_Direc_Abdullah_Shaker_Abdullah.docx',2:'From_Ketchup_to_Oobleck_Non_Newtonian_Fluids_and_Their_Behav_Adham_Mohamed_Khairy.docx',5:'Can Sound Become Electricity _.docx'}[n]
  source_names={1:'rank-01-entropy.docx',2:'rank-02-non-newtonian-fluids.docx',5:'rank-05-sound-to-electricity.docx'}
  with zipfile.ZipFile(root/'content'/'source-manuscripts'/source_names[n]) as z:
   rels=ET.fromstring(z.read('word/_rels/document.xml.rels')); ix=1
   for rel in rels:
    if rel.attrib.get('Type','').endswith('/image'):
     ext=Path(rel.attrib['Target']).suffix.lower() or '.png'; data[rel.attrib['Id']]=f'/assets/articles/rank-{n:02}/figure-{ix}{ext}'; ix+=1
 if n==1: data['unknown']='/assets/articles/rank-01/figure-entropy.gif'; data['rId11']='/assets/articles/rank-01/figure-entropy.gif'
 return data

def fig_html(n,key,urls):
 if key not in urls: return ''
 entry=figs.get(n,{}).get(key)
 if not entry: return ''
 filename,caption=entry;url=f'/assets/articles/rank-{n:02}/{filename}';alt=caption.split(' (Figure')[0]
 return f'<figure class="article-figure"><img src="{html.escape(url,quote=True)}" alt="{html.escape(alt,quote=True)}" loading="lazy"><figcaption>{html.escape(caption)}</figcaption></figure>'

def safe_inline(text):
 escaped=html.escape(text,quote=False)
 escaped=re.sub(r'(https?://[^\s<>]+)',lambda m:f'<a href="{html.escape(m.group(1),quote=True)}" target="_blank" rel="noopener noreferrer">{m.group(1)}</a>',escaped)
 return escaped

def render_block(n,block):
 t=block.strip()
 if not t:return ''
 if n==3 and re.fullmatch(r'\$\$.+?\$\$',t,re.S): return f'<div class="equation">{t}</div>'
 if re.fullmatch(r'\$\$.+?\$\$',t,re.S): return f'<div class="equation">{t}</div>'
 if n==3 and re.match(r'^Relativistic Effect\s+Physical Cause\s+Clock Offset Rate',t):
  rows=[('Special Relativity','Orbital velocity (~14,000 km/h)','−7 microseconds / day'),('General Relativity','Weaker gravitational field at 20,200 km','+45 microseconds / day'),('Net Effect','Combined relativistic drift','+38 microseconds / day')]
  return '<table class="article-table"><caption>Table 1. Daily clock-rate shifts that combine in GPS.</caption><thead><tr><th>Relativistic effect</th><th>Physical cause</th><th>Clock offset rate</th></tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{html.escape(c)}</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table>'
 if t in headings.get(n,set()): return f'<h2>{html.escape(t.rstrip(":"))}</h2>'
 # Short standalone, title-style paragraphs become subsection headings when appropriate.
 if len(t)<90 and ('?' in t or (t.istitle() and not t.endswith('.'))): return f'<h2>{html.escape(t.rstrip(":"))}</h2>'
 text=' '.join(part.strip() for part in t.splitlines() if part.strip())
 return f'<p>{safe_inline(text)}</p>'

def render_body(n,body):
 urls=image_map(n)
 # Ranks 1, 2 and 5 contain local figure markers. Convert them into captioned local figures, grouping adjacent images.
 if n in (1,2,5):
  parts=re.split(r'(\[\[IMAGE:[^]]+\]\])',body)
  out=[];i=0
  while i<len(parts):
   if re.fullmatch(r'\[\[IMAGE:[^]]+\]\]',parts[i]):
    keys=[]
    while i<len(parts) and re.fullmatch(r'\[\[IMAGE:[^]]+\]\]',parts[i]):
     keys.append(parts[i][8:-2]);i+=1
    figs_html=[fig_html(n,k,urls) for k in keys]
    figs_html=[x for x in figs_html if x]
    if len(figs_html)>1: out.append('<div class="figure-pair">'+''.join(figs_html)+'</div>')
    elif figs_html: out.append(figs_html[0])
   else:
    segment=parts[i]
    # collapse duplicate line breaks but preserve paragraph boundaries
    for b in re.split(r'\n\s*\n',segment):
     rendered=render_block(n,b)
     if rendered: out.append(rendered)
    i+=1
  return '\n'.join(out)
 if n==3:
  lines=body.splitlines(); paragraphs=[];buf=[]
  for line in lines:
   t=line.strip()
   if not t:
    if buf: paragraphs.append(' '.join(buf));buf=[]
    continue
   if t.startswith('Kenzy Raafat Eltablawy — PhysBA Submission Page'): continue
   if re.fullmatch(r'\$\$.+?\$\$',t):
    if buf: paragraphs.append(' '.join(buf));buf=[]
    paragraphs.append(t);continue
   if t in headings[3] or t.startswith('Relativistic Effect Physical Cause') or t in ('Special Relativity Orbital velocity (~14,000 km/h) -7 microseconds / day','General Relativity Weaker gravitational field at 20,200 km +45 microseconds / day','Net Effect Combined Relativistic Drift +38 microseconds / day'):
    if buf: paragraphs.append(' '.join(buf));buf=[]
    if t.startswith('Relativistic Effect Physical Cause'):
     paragraphs.append('Relativistic Effect Physical Cause Clock Offset Rate\nSpecial Relativity Orbital velocity (~14,000 km/h) −7 microseconds / day\nGeneral Relativity Weaker gravitational field at 20,200 km +45 microseconds / day\nNet Effect Combined Relativistic Drift +38 microseconds / day')
    elif t in headings[3]: paragraphs.append(t)
    continue
   if t.startswith('The Clock That Lies: Why Does GPS Need Einstein’s') or t in ('Relativity?','Kenzy Raafat Eltablawy','PhysBA Competition Essay Entry'): continue
   buf.append(t)
  if buf: paragraphs.append(' '.join(buf))
  # Equations are separate display lines; join source's visual line wraps inside paragraphs.
  return '\n'.join(render_block(3,x) for x in paragraphs if x)
 # Rank 4 has no figures/equations; use source's paragraph breaks and retain the whole article.
 out=[]
 for b in re.split(r'\n\s*\n',body):
  if not b.strip():continue
  t=' '.join(x.strip() for x in b.splitlines() if x.strip())
  if n==4 and t.endswith(':') and len(t)<110:out.append(f'<h2>{html.escape(t.rstrip(":"))}</h2>')
  else:out.append(f'<p>{safe_inline(t)}</p>')
 return '\n'.join(out)

for n,(slug,title,author,school,track,award,cover,summary) in meta.items():
 body=get_body(n)
 # Rank 3 body begins with title and author boilerplate; begin at the opening story paragraph.
 if n==3:
  body=body[body.find('Imagine you are on an unfamiliar street'):]
 rendered=render_body(n,body)
 path=root/'articles'/'ypwc'/f'rank-{n:02}-{slug}.html';page=path.read_text(encoding='utf-8')
 page=re.sub(r'(?s)<article class="article-body">.*?</article>',lambda m:f'<article class="article-body">{rendered}</article>',page,count=1)
 page=page.replace('max-width:min(100%,560px);max-height:360px','max-width:min(100%,440px);max-height:290px').replace('max-width:min(100%,420px);max-height:290px','max-width:min(100%,370px);max-height:245px')
 css='''.article-body figure.article-figure{margin:1.45rem auto;display:flex;flex-direction:column;align-items:center;gap:8px;max-width:100%;background:#101216;border:1px solid #30343a;padding:12px}.article-body figure.article-figure img{display:block;width:auto;height:auto;max-width:min(100%,440px);max-height:290px;object-fit:contain;margin:0 auto}.article-body figure figcaption{width:min(100%,620px);margin:0 auto;color:#aeb5bf;font-size:.78rem;line-height:1.55;text-align:center}.figure-pair{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;max-width:760px;margin:1.4rem auto}.figure-pair figure.article-figure{margin:0;padding:10px}.figure-pair figure img{max-width:100%;max-height:220px}.article-table{width:100%;border-collapse:collapse;margin:1.5rem 0;background:#11151b;font-size:.88rem}.article-table caption{text-align:left;color:#c4cbd5;padding:0 0 9px;font-weight:600}.article-table th,.article-table td{padding:11px 12px;border:1px solid #30343a;text-align:left}.article-table th{color:#eef1f5;background:#1a2029}.article-table td{color:#c9ced6}.article-body .equation{overflow-x:auto;text-align:center;padding:17px 12px;margin:1.25rem auto;background:#10141a;border-left:2px solid #8ba1bc;font-size:1.05rem}.article-body h2{margin-top:1.8em}@media(max-width:600px){.figure-pair{grid-template-columns:1fr}.figure-pair figure img{max-height:230px}.article-body figure.article-figure img{max-width:min(100%,370px);max-height:245px}.article-table{font-size:.76rem}.article-table th,.article-table td{padding:8px 7px}}'''
 if '.article-figure{' not in page:
  page=page.replace('</style>',css+'\n</style>',1)
 path.write_text(page,encoding='utf-8')
 # Keep an editable Markdown source with local images and numbered captions, matching the rendered article.
 sourcebody=body
 urls=image_map(n)
 if n in (1,2,5):
  for key,(filename,caption) in figs[n].items():
   marker=f'[[IMAGE:{key}]]'
   if marker in sourcebody:
    sourcebody=sourcebody.replace(marker,f'\n\n![{caption}](/assets/articles/rank-{n:02}/{filename})\n\n',1)
  sourcebody=re.sub(r'\[\[IMAGE:[^]]+\]\]','',sourcebody)
 (root/'content'/'articles'/f'rank-{n:02}-{slug}.md').write_text(f'# {title}\n\n**{author} · {school}**  \n**Rank {n} · {track} · {award}**\n\n{summary}\n\n{sourcebody.strip()}\n',encoding='utf-8')
print('Rebuilt scientific article bodies, display equations, numbered local figures, captions and source Markdown.')
