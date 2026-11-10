# -*- coding: utf-8 -*-
"""สร้าง site/code.html (หน้าอ่านโค้ด) จาก holyfkingbonussukiforu commit ที่กำหนด

รัน:  python3 .tools/code-page/gen.py [commit]
ต้องมี repo holyfkingbonussukiforu ที่ ~/NetBeansProjects/ และมี node (ใช้อ่านเจ้าของไฟล์จาก site/index.html)
แก้คำอธิบายทีละบรรทัดใน notes.py · เนื้อหาอื่นใน content.py · หน้าตาใน template.html
ถ้าเปลี่ยน commit ต้องเช็กเลขบรรทัดใน notes.py / content.py ใหม่ (gen.py จะ assert ถ้าเลขบรรทัดเกินไฟล์)
"""
import html, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from notes import NOTES, KEYLINES
from content import PLAIN, LAYER_INFO, TRACE_PAY, TRACE_LOGIN, BASICS, BASIC_GROUPS, LAYER_KEYFILES

REPO = os.path.expanduser('~/NetBeansProjects/holyfkingbonussukiforu')
REV = sys.argv[1] if len(sys.argv) > 1 else 'ccbf3f0'
HERE = os.path.dirname(__file__)
SITE = os.path.normpath(os.path.join(HERE, '..', '..', 'site'))
OUT = os.path.join(SITE, 'code.html')
E = html.escape


def git(*a):
    return subprocess.run(['git', '-C', REPO, *a], capture_output=True, text=True, check=True).stdout


# ---------------------------------------------------------------- โหลดไฟล์
PATHS = [p for p in git('ls-tree', '-r', '--name-only', REV, 'src').split('\n') if p.endswith('.java')]
FORMS = {os.path.basename(p)[:-5] for p in git('ls-tree', '-r', '--name-only', REV, 'src').split('\n') if p.endswith('.form')}
SRC, PATH = {}, {}
for p in PATHS:
    n = os.path.basename(p)[:-5]
    SRC[n] = git('show', f'{REV}:{p}').rstrip('\n')
    PATH[n] = p.replace('src/main/java/com/example/bonussuki/', '')


def layer(n):
    p = PATH[n]
    if '/' not in p:
        return 'root'
    d = p.split('/')[0]
    if p.startswith('ui/component/'):
        return 'comp'
    return d


LAYER_TH = {'root': 'จุดเริ่ม + ทดสอบ', 'helper': 'helper', 'model': 'model', 'dao': 'dao', 'service': 'service', 'ui': 'ui', 'comp': 'ui/component'}
LAYER_ORDER = ['root', 'helper', 'model', 'dao', 'service', 'ui', 'comp']


def load_owners():
    """อ่านเจ้าของไฟล์ (PM_FILES + OWNER) จากสคริปต์ใน site/index.html ด้วย node"""
    lines = open(os.path.join(SITE, 'index.html'), encoding='utf-8').read().split('\n')
    s = next(i for i, l in enumerate(lines) if l.startswith('const TABLES = '))
    e = next(i for i, l in enumerate(lines) if l.startswith('const PM_BY_NAME = '))
    js = '\n'.join(lines[s:e]) + """
const out = {};
PM_FILES.forEach(f => { const k = f.tasks[0]; out[f.name] = {task: k || '', owner: k ? ownerFallback(k) : ''}; });
process.stdout.write(JSON.stringify(out));"""
    return json.loads(subprocess.run(['node', '-e', js], capture_output=True, text=True, check=True).stdout)


OWNERS = load_owners()

# ---------------------------------------------------------------- ระบายสีโค้ด
KW = set('''abstract boolean break byte case catch char class continue default do double else enum extends final finally float for
if implements import instanceof int interface long new package private protected public return short static super switch
synchronized this throw throws try void while null true false var'''.split())
TOK = re.compile(r'(/\*[\s\S]*?\*/)|(//[^\n]*)|("(?:\\.|[^"\\\n])*")|(\'(?:\\.|[^\'\\\n])\')|(@\w+)|(\b\d+(?:\.\d+)?[fFdDL]?\b)|([A-Za-z_]\w*)|(\n)|([^\w\s"\'/@]+|/|\s+|.)')


def highlight(text):
    """คืน list ของ HTML ทีละบรรทัด"""
    lines, cur = [], []

    def push(cls, s):
        parts = s.split('\n')
        for i, part in enumerate(parts):
            if i:
                lines.append(''.join(cur)); cur.clear()
            if part:
                cur.append(f'<span class="{cls}">{E(part)}</span>' if cls else E(part))
    for m in TOK.finditer(text):
        bc, lc, st, ch, an, nu, wd, nl, ot = m.groups()
        if bc: push('c', bc)
        elif lc: push('c', lc)
        elif st or ch: push('s', st or ch)
        elif an: push('a', an)
        elif nu: push('n', nu)
        elif wd: push('k' if wd in KW else ('t' if wd[0].isupper() else ''), wd)
        elif nl: push('', '\n')
        else: push('', ot)
    lines.append(''.join(cur))
    return lines


HL = {n: highlight(s) for n, s in SRC.items()}
RAW = {n: s.split('\n') for n, s in SRC.items()}


def method_range(n, head):
    lines = RAW[n]
    start = next(i for i, l in enumerate(lines) if head in l)
    depth, seen = 0, False
    for i in range(start, len(lines)):
        code = re.sub(r'"(?:\\.|[^"\\])*"', '""', lines[i].split('//')[0])
        depth += code.count('{') - code.count('}')
        seen = seen or '{' in code
        if seen and depth == 0:
            return start + 1, i + 1
    raise ValueError(head)


def rng(n, r):
    return method_range(n, r[1]) if r and r[0] == 'method' else r


def snippet(n, s, e, link=True):
    rows = ''.join(f'<span class="sl"><i>{i}</i>{HL[n][i - 1] or " "}</span>' for i in range(s, e + 1))
    head = f'<a href="{href(n, s)}">{E(PATH[n])}</a>' if link else E(PATH[n])
    return f'<figure class="snip"><figcaption>{head}<span>บรรทัด {s}{"–" + str(e) if e != s else ""}</span></figcaption><pre><code>{rows}</code></pre></figure>'


def raw_snip(lang, text):
    rows = ''.join(f'<span class="sl"><i>{i + 1}</i>{h or " "}</span>' for i, h in enumerate(highlight(text)))
    return f'<figure class="snip"><figcaption>ตัวอย่าง</figcaption><pre><code>{rows}</code></pre></figure>'


def href(n, line=None):
    if n in NOTES:
        return f'#v-{n}-{line or 1}'
    return f'#file-{n}'


# ---------------------------------------------------------------- คำอธิบายอัตโนมัติในโค้ดที่ NetBeans สร้าง
KIND = {'JButton': 'ปุ่ม', 'JLabel': 'ป้ายข้อความ', 'JTextField': 'ช่องกรอก', 'JPasswordField': 'ช่องกรอกรหัสผ่าน (โชว์เป็นจุด)',
        'JTextArea': 'ช่องกรอกหลายบรรทัด', 'JTable': 'ตาราง', 'JComboBox': 'กล่องเลือก', 'JSpinner': 'ช่องตัวเลขมีลูกศร',
        'JPanel': 'แผง (กล่องใส่ชิ้นอื่น)', 'JScrollPane': 'แถบเลื่อน', 'JToggleButton': 'ปุ่มกดค้าง', 'ButtonGroup': 'กลุ่มปุ่ม (เลือกได้ทีละปุ่ม)',
        'JCheckBox': 'ช่องติ๊ก', 'JRadioButton': 'ปุ่มวงกลมเลือก 1 อัน', 'JSeparator': 'เส้นคั่น', 'JProgressBar': 'แถบความคืบหน้า', 'JList': 'รายการ'}


def auto_note(n, line, handlers):
    t = line.strip()
    m = re.match(r'(\w+) = new javax\.swing\.(\w+)(<[^>]*>)?\(\);', t)
    if m:
        return 'สร้างชิ้นส่วน', f'สร้าง{KIND.get(m[2], "ชิ้นส่วน")}ชื่อ <code>{m[1]}</code> (ชนิด <code>{m[2]}</code>) ตามที่ลากมาวางในแท็บ Design'
    m = re.match(r'(\w+)\.addActionListener\(this::(\w+)\);', t)
    if m:
        ln = handlers.get(m[2])
        to = f'<a href="#v-{n}-{ln}">{m[2]}</a>' if ln else m[2]
        return 'ผูกปุ่มกับเมธอด', f'กด <code>{m[1]}</code> แล้ว Swing จะเรียกเมธอด {to} ให้ บรรทัดนี้เกิดตอนดับเบิลคลิกปุ่มในแท็บ Design <a href="#b-event">อ่านเพิ่ม</a>'
    if 'Mouse' in t:
        return 'ผูกการคลิกเมาส์', 'JLabel ไม่มีเหตุการณ์ "กด" แบบปุ่ม จึงฟังการคลิกเมาส์แทน (เลือกในแท็บ Events → Mouse → mouseClicked)'
    m = re.match(r'(\w+)\.setText\("(.*)"\);', t)
    if m:
        return 'ตั้งข้อความ', f'ข้อความบน <code>{m[1]}</code> คือ "{E(m[2])}" (ช่อง text ในหน้าต่าง Properties)' if m[2] else f'ให้ <code>{m[1]}</code> ไม่มีข้อความ'
    rules = [
        (r'createParallelGroup', 'กลุ่มขนาน', 'ชิ้นในกลุ่มนี้อยู่ "แนวเดียวกัน" (ซ้อนกันคนละแถว หรือเรียงชิดขอบเดียวกัน) เกิดจากการลากวางแบบ Free Design'),
        (r'createSequentialGroup', 'กลุ่มเรียงต่อ', 'ชิ้นในกลุ่มนี้เรียงต่อกันทีละชิ้น (ซ้ายไปขวา หรือบนลงล่าง)'),
        (r'setHorizontalGroup', 'ตำแหน่งแนวนอน', 'เริ่มบอก GroupLayout ว่าแนวนอน (ซ้าย-ขวา) วางอะไรไว้ตรงไหน'),
        (r'setVerticalGroup', 'ตำแหน่งแนวตั้ง', 'เริ่มบอก GroupLayout ว่าแนวตั้ง (บน-ล่าง) วางอะไรไว้ตรงไหน'),
        (r'new javax\.swing\.GroupLayout', 'ตัวจัดวาง', 'สร้าง GroupLayout ให้แผงนี้ = ตัวจัดวางที่ NetBeans ใช้ตอนลากวาง <a href="#b-layout">Layout</a>'),
        (r'\.addComponent\((\w+)', 'วางชิ้นส่วน', 'วาง <code>{0}</code> ลงในกลุ่มนี้ ตัวเลขข้างหลังคือขนาด (เล็กสุด, ที่อยากได้, ใหญ่สุด)'),
        (r'\.addGap\((\d+)', 'เว้นช่องว่าง', 'เว้นช่องว่าง {0} พิกเซล (Short.MAX_VALUE = ยืดได้เต็มที่ ใช้ดันของไปตรงกลาง)'),
        (r'\.addPreferredGap', 'เว้นช่องว่างมาตรฐาน', 'ช่องว่างตามที่ NetBeans แนะนำ'),
        (r'\.addContainerGap', 'เว้นขอบ', 'ช่องว่างระหว่างของกับขอบแผง'),
        (r'^\)+;?$|^\.addGroup\(|^\);$', 'ปิด/เปิดกลุ่ม', 'วงเล็บของกลุ่มใน GroupLayout'),
        (r'\.setLayout\(', 'ตั้งตัวจัดวาง', 'บอกว่าแผงนี้ใช้ layout แบบไหน'),
        (r'setViewportView\((\w+)\)', 'ใส่ในแถบเลื่อน', 'ใส่ <code>{0}</code> ไว้ในแถบเลื่อน ถ้าของยาวเกินจะเลื่อนดูได้'),
        (r'\.add\((\w+)', 'ใส่ชิ้นลงในแผง', 'ใส่ <code>{0}</code> ลงในแผง'),
        (r'setFont\(', 'ฟอนต์', 'ตั้งฟอนต์ตามที่เลือกในหน้าต่าง Properties (เช่น ตัวหนา ใหญ่ขึ้น 8)'),
        (r'setModel\(', 'ค่าเริ่มต้น', 'ตั้งข้อมูลเริ่มต้น (model) เช่น ช่องตัวเลข 0 ถึง 1,000,000 เพิ่มทีละ 1'),
        (r'setHorizontalAlignment', 'จัดข้อความ', 'ข้อความชิดซ้าย/กึ่งกลาง'),
        (r'setPreferredSize|setMinimumSize|setMaximumSize', 'ขนาด', 'ขนาดที่อยากได้ / เล็กสุด / ใหญ่สุด (กว้าง, สูง)'),
        (r'setTitle', 'ชื่อหน้าต่าง', 'ข้อความบนแถบหัวหน้าต่าง'),
        (r'setDefaultCloseOperation', 'กดปิดหน้าต่าง', 'กดปุ่มปิดแล้วทำอะไร (EXIT = จบโปรแกรม, DISPOSE = ปิดแค่หน้าต่างนี้)'),
        (r'setSelected\(true\)', 'เลือกไว้ก่อน', 'ตอนเปิดหน้าจอ ปุ่มนี้ถูกเลือกอยู่แล้ว'),
        (r'setColumns|setRows|setLineWrap|setWrapStyleWord', 'ขนาดช่องข้อความ', 'จำนวนคอลัมน์/แถว และการตัดบรรทัดอัตโนมัติ'),
        (r'setEditable|setEnabled', 'แก้ได้ไหม', 'ช่องนี้แก้หรือกดได้หรือไม่'),
        (r'setBackground|setOpaque|setBorder|setForeground', 'สี/ขอบ', 'สีหรือขอบที่ตั้งในหน้าต่าง Properties'),
        (r'pack\(\)', 'ปรับขนาดหน้าต่าง', 'ปรับขนาดให้พอดีของข้างใน'),
        (r'getContentPane', 'พื้นที่ของหน้าต่าง', 'content pane = พื้นที่ข้างในหน้าต่าง (ไม่รวมแถบหัว)'),
        (r'^private void initComponents', 'initComponents()', 'เมธอดที่ NetBeans สร้างให้ทั้งก้อน constructor เรียกเป็นบรรทัดแรก'),
        (r'GEN-END:initComponents', 'จบโค้ดที่ NetBeans สร้าง', 'ถัดจากนี้เป็นโค้ดที่เราเขียนเองได้'),
    ]
    for pat, title, body in rules:
        m = re.search(pat, t)
        if m:
            return title, body.format(*m.groups())
    return 'ตั้งค่าจากแท็บ Design', 'NetBeans เขียนบรรทัดนี้จากค่าที่ตั้งในหน้าต่าง Properties ห้ามแก้ด้วยมือ'


def build_viewer_data(n):
    lines = RAW[n]
    notes = [list(x) + [0] for x in NOTES[n]]
    gb = next((i + 1 for i, l in enumerate(lines) if 'GEN-BEGIN:initComponents' in l), None)
    ge = next((i + 1 for i, l in enumerate(lines) if 'GEN-END:initComponents' in l), None)
    vb = next((i + 1 for i, l in enumerate(lines) if 'GEN-BEGIN:variables' in l), None)
    ve = next((i + 1 for i, l in enumerate(lines) if 'GEN-END:variables' in l), None)
    handlers = {}
    for i, l in enumerate(lines):
        m = re.search(r'private void (\w+)\(', l)
        if m:
            handlers[m[1]] = i + 1
    gen = None
    if gb and ge:
        gen = [gb + 1, ge]
        big = max(e - s for s, e, *_ in notes if s <= gb + 1 and e >= ge - 1) if any(s <= gb + 1 and e >= ge - 1 for s, e, *_ in notes) else 10 ** 6
        for ln in range(gb + 1, ge + 1):
            if not lines[ln - 1].strip():
                continue
            if any(s <= ln <= e and (e - s) < big for s, e, *_ in notes):
                continue
            t, b = auto_note(n, lines[ln - 1], handlers)
            notes.append([ln, ln, t, b, 1])
    if vb and ve:
        for ln in range(vb + 1, ve):
            m = re.search(r'private javax\.swing\.(\w+)(?:<[^>]*>)? (\w+);', lines[ln - 1])
            if m:
                notes.append([ln, ln, 'ตัวแปร ' + m[2], f'ตัวแปรของ{KIND.get(m[1], "ชิ้นส่วน")} <code>{m[2]}</code> ชนิด <code>{m[1]}</code> ใช้ได้ทุกเมธอดในไฟล์นี้', 1])
    for s, e, *_ in notes:
        assert 1 <= s <= e <= len(lines), (n, s, e, len(lines))
    return {'id': n, 'path': PATH[n], 'notes': notes, 'gen': gen, 'key': KEYLINES.get(n, [])}


def viewer_html(n):
    d = build_viewer_data(n)
    gen = d['gen']
    rows = []
    for i, h in enumerate(HL[n], 1):
        if gen and i == gen[0]:
            rows.append(f'<button class="gen-toggle" type="button" data-gen="{n}" aria-expanded="false"><b>▸</b> บรรทัด {gen[0]}–{gen[1]} · โค้ดที่ NetBeans สร้างจากแท็บ Design <span>กดเพื่อกาง</span></button>')
        cls = 'ln' + (' g' if gen and gen[0] <= i <= gen[1] else '') + (' key' if i in d['key'] else '')
        rows.append(f'<span class="{cls}" data-n="{i}" id="L-{n}-{i}"><i>{i}</i>{h or " "}</span>')
    meta = file_meta(n)
    own = meta['owner'] or '—'
    return f'''<div class="viewer" id="v-{n}" data-file="{n}">
  <div class="vhead"><div><code class="vpath">{E(PATH[n])}</code><span class="vmeta">{len(RAW[n])} บรรทัด · ทีมมอบให้ {E(own)}{' · มีไฟล์ .form' if n in FORMS else ''}</span></div>
  <p class="vhint">กดบรรทัดไหนก็ได้ หรือกด <b>ถัดไป</b> เพื่ออ่านทีละก้อน</p></div>
  <div class="vbody">
    <pre class="code" tabindex="0" aria-label="โค้ด {E(PATH[n])}"><code>{"".join(rows)}</code></pre>
    <aside class="note" aria-live="polite"><div class="nbar"><button type="button" class="prev" aria-label="ก้อนก่อนหน้า">‹ ก่อนหน้า</button><span class="count"></span><button type="button" class="next" aria-label="ก้อนถัดไป">ถัดไป ›</button></div>
      <p class="nlines"></p><h4 class="ntitle"></h4><div class="nbody"></div></aside>
  </div>
</div>''', d


# ---------------------------------------------------------------- ข้อมูลทุกไฟล์
def class_doc(n):
    m = re.search(r'/\*\*([\s\S]*?)\*/\s*(?:@\w+\s*)*public\s+(?:final\s+)?(?:abstract\s+)?(?:class|interface)', SRC[n])
    if not m:
        return ''
    return ' '.join(x.strip().lstrip('*').strip() for x in m[1].split('\n')).strip()


def methods(n):
    ms = re.findall(r'^    public (?:static )?(?:[\w<>\[\], ]+ )?(\w+)\(', SRC[n], re.M)
    out = []
    for x in ms:
        if x == n or x in out:
            continue
        if layer(n) == 'model' and re.match(r'(get|set|is)[A-Z]', x):
            continue
        out.append(x)
    return out


def used_by(n):
    pat = re.compile(r'\b' + re.escape(n) + r'\b')
    return sorted(o for o in SRC if o != n and pat.search(re.sub(r'/\*[\s\S]*?\*/|//[^\n]*', '', SRC[o])))


_meta = {}


def file_meta(n):
    if n in _meta:
        return _meta[n]
    doc = class_doc(n)
    lay = layer(n)
    plain = PLAIN.get(n)
    ms = methods(n)
    if not plain and lay == 'model':
        m = re.match(r'ตาราง (\w+)\s*·\s*([^(·]+)', doc)
        plain = f'กล่องเก็บข้อมูล 1 แถวของตาราง {m[1]} ({m[2].strip()}) มีช่องตรงกับคอลัมน์ getter/setter และ fromRS หน้าตาเหมือน Member' if m else doc
    if not plain and lay == 'dao':
        m = re.search(r'ตาราง (\w+)', doc)
        tbl = m[1] if m else n[:-3]
        plain = f'SQL ทั้งหมดของตาราง {tbl} เขียนแบบ try-catch-finally เหมือน MemberDao'
        if 'จึงไม่ implements' in doc:
            plain += ' · PK มีหลายคอลัมน์ จึงไม่ implements Dao&lt;T&gt; (get/delete ต้องส่งหลายค่า)'
        extra = [x for x in ms if x not in ('get', 'getAll', 'save', 'update', 'delete')]
        if extra:
            plain += ' · เมธอดพิเศษ: ' + ', '.join(f'<code>{x}</code>' for x in extra)
    o = OWNERS.get(n + '.java', {})
    _meta[n] = {'name': n, 'layer': lay, 'path': PATH[n], 'plain': plain or doc, 'doc': doc, 'methods': ms,
                'usedBy': used_by(n), 'owner': o.get('owner', ''), 'task': o.get('task', ''), 'form': n in FORMS,
                'key': n in NOTES, 'lines': len(RAW[n])}
    return _meta[n]


def file_card(n):
    f = file_meta(n)
    task = f['task'].split('|')
    task_txt = f'Task {E(task[0])}' + (f' · {E(task[1])}' if len(task) > 1 else '') if f['task'] else 'ยังไม่มีงานในชีท'
    ub = ', '.join(f'<a href="{href(u)}">{u}</a>' for u in f['usedBy']) or '<span class="muted">ไม่มี (เป็นจุดเริ่มหรือโปรแกรมทดสอบ)</span>'
    ms = ', '.join(f'<code>{m}</code>' for m in f['methods']) or '<span class="muted">—</span>'
    readbtn = f'<a class="btn" href="#v-{n}-1">อธิบายทีละบรรทัด</a>' if f['key'] else ''
    formtxt = '<li><b>หน้าจอ</b> มีไฟล์ <code>' + n + '.form</code> คู่กัน เปิดแท็บ Design ใน NetBeans เพื่อลากวาง</li>' if f['form'] else ''
    search = ' '.join([n, f['path'], re.sub('<[^>]+>', '', f['plain']), f['owner']]).lower()
    return f'''<details class="fcard" id="file-{n}" data-layer="{f['layer']}" data-s="{E(search)}">
  <summary><code>{n}</code><span class="ftag">{LAYER_TH[f['layer']]}</span>{'<span class="ftag solid">ทีละบรรทัด</span>' if f['key'] else ''}<span class="fplain">{f['plain']}</span><span class="fown">{E(f['owner'] or '—')}</span></summary>
  <div class="fbody"><ul>
    <li><b>ไฟล์</b> <code>{E(f['path'])}</code> · {f['lines']} บรรทัด</li>
    {f'<li><b>คอมเมนต์หัวไฟล์</b> {E(f["doc"])}</li>' if f['doc'] else ''}
    <li><b>เมธอดหลัก</b> {ms}</li>
    <li><b>ใครเรียกใช้</b> {ub}</li>
    {formtxt}
    <li><b>ในทีม</b> {E(f['owner'] or '—')} · {task_txt} · <a href="index.html#f-{n}">ดูในแผนผังโปรเจกต์</a></li>
  </ul>{readbtn}</div>
</details>'''


# ---------------------------------------------------------------- ส่วนต่าง ๆ ของหน้า
def section_start(viewers):
    counts = {l: sum(1 for n in SRC if layer(n) == l) for l in LAYER_ORDER}
    lay = ''.join(
        f'<div class="lbox"><b>{E(t)}</b><span class="like">เหมือน{E(like)}</span><p>{E(job)}</p>{f"<p class=no>{E(no)}</p>" if no else ""}</div>'
        + ('<div class="larrow" aria-hidden="true">↓ เรียกใช้</div>' if i < len(LAYER_INFO) - 1 else '')
        for i, (lid, t, like, job, no) in enumerate(LAYER_INFO))
    tree_rows = [('BonusSuki.java', 'จุดเริ่มโปรแกรม'), ('TestMemberDao.java · TestPosService.java', 'โปรแกรมทดสอบ'),
                 (f'helper/ ({counts["helper"]})', 'ตัวช่วย: ฐานข้อมูล วันที่ ใครล็อกอิน'), (f'model/ ({counts["model"]})', 'กล่องข้อมูล 1 คลาส = 1 ตาราง'),
                 (f'dao/ ({counts["dao"]})', 'SQL 1 ตาราง = 1 DAO'), (f'service/ ({counts["service"]})', 'กฎร้าน'),
                 (f'ui/ ({counts["ui"]})', 'หน้าจอ (.java + .form)'), (f'ui/component/ ({counts["comp"]})', 'ชิ้นส่วนหน้าจอและสี')]
    tree = ''.join(f'<li><code>{E(a)}</code><span>{E(b)}</span></li>' for a, b in tree_rows)
    return f'''<section class="part" id="start" data-toc="เริ่มที่นี่">
<div class="phero"><span class="pnum">0</span><div><h2>เริ่มที่นี่</h2><p>โปรแกรมนี้คืออะไร เปิดยังไง และควรอ่านไฟล์ไหนก่อน</p></div></div>
<div class="cols2">
  <div class="card"><h3>โปรแกรมนี้คืออะไร</h3>
    <p>โปรแกรมขายหน้าร้าน (POS) ของร้านโบนัสสุกี้ เขียนด้วย <b>Java Swing</b> (หน้าต่างโปรแกรมบนคอม) เก็บข้อมูลใน <b>SQLite</b> (ไฟล์ฐานข้อมูลไฟล์เดียว <code>bonus_suki.db</code>)</p>
    <p>พนักงานเปิดโต๊ะ สั่งอาหาร รับเงิน ผู้จัดการดูยอดขาย จัดการเมนู วัตถุดิบ สมาชิก พนักงาน เงินเดือน ค่าใช้จ่าย</p>
    <p class="muted">ทั้งหมด {len(SRC)} ไฟล์ .java และ {len(FORMS)} ไฟล์ .form อ้างอิงจาก repo <a href="https://gitlab.com/68160255/holyfkingbonussukiforu">holyfkingbonussukiforu</a> commit <code>{REV}</code></p></div>
  <div class="card"><h3>เปิดโปรแกรมยังไง</h3><ol class="steps">
    <li>NetBeans → File → Open Project → เลือกโฟลเดอร์ <code>holyfkingbonussukiforu</code></li>
    <li>กด <kbd>F6</kbd> (Run Project) โปรแกรมเริ่มที่ <code>BonusSuki.java</code></li>
    <li>ครั้งแรกจะสร้างไฟล์ <code>bonus_suki.db</code> พร้อมข้อมูลตัวอย่างให้เอง</li>
    <li>ล็อกอิน: กดปุ่ม <b>ผู้จัดการ</b> แล้วใช้ <code>manager</code> / <code>1234</code> หรือกด <b>พนักงาน</b> แล้วใช้ <code>staff</code> / <code>1234</code></li></ol></div>
</div>
<h3 class="sh">โปรแกรมแบ่งเป็นชั้น เหมือนคนในร้าน</h3>
<p class="lead">ทุกครั้งที่กดปุ่ม งานจะส่งต่อลงไปทีละชั้น แต่ละชั้นทำแค่หน้าที่ของตัวเอง แก้ที่ไหนก็รู้ว่าต้องไปไฟล์ไหน วิธีแบ่งนี้มาจาก Lab 8</p>
<div class="layers">{lay}<p class="lnote"><b>model</b> คือกล่องใส่ข้อมูลที่ส่งไปมาระหว่างทุกชั้น · <b>helper</b> คือของใช้ร่วม เช่น กุญแจเข้าฐานข้อมูล</p></div>
<div class="cols2">
  <div class="card"><h3>โฟลเดอร์ในโปรเจกต์</h3><p class="muted"><code>src/main/java/com/example/bonussuki/</code></p><ul class="tree">{tree}</ul></div>
  <div class="card"><h3>อ่านตามลำดับนี้</h3><ol class="steps">
    <li><a href="#basics">พื้นฐาน</a> ถ้ายังไม่คุ้นกับ class, try-catch, SELECT</li>
    <li><a href="#v-BonusSuki-1">BonusSuki.java</a> ข้างล่างนี้ สั้นที่สุด</li>
    <li>ไล่ชั้นจากล่างขึ้นบน: <a href="#helper">helper</a> → <a href="#model">model</a> → <a href="#dao">dao</a> → <a href="#service">service</a> → <a href="#ui">ui</a></li>
    <li><a href="#trace-pay">ตามรอยการกดชำระเงิน</a> เห็นทุกชั้นทำงานต่อกัน</li>
    <li>เปิด <a href="#files">ทุกไฟล์</a> หาไฟล์ที่ตัวเองต้องทำ</li></ol></div>
</div>
<h3 class="sh">ไฟล์แรก: BonusSuki.java</h3>
{viewers['BonusSuki']}
</section>'''


def section_basics():
    out = []
    for gid, gname in BASIC_GROUPS:
        items = []
        for bid, g, title, body, ex in BASICS:
            if g != gid:
                continue
            exs = ''
            for x in ex:
                if x[0] == 'raw':
                    exs += raw_snip(x[1], x[2])
                else:
                    s, e = rng(x[0], x[1])
                    exs += snippet(x[0], s, e)
            items.append(f'<article class="basic" id="{bid}"><h4>{E(title)}</h4><div class="bbody">{body}</div>{f'<div class="bex">{exs}</div>' if exs else ''}</article>')
        out.append(f'<h3 class="sh" id="basics-{gid}">{E(gname)}</h3><div class="basics">{"".join(items)}</div>')
    chips = ''.join(f'<a class="chip" href="#{bid}">{E(t)}</a>' for bid, g, t, *_ in BASICS)
    return f'''<section class="part" id="basics" data-toc="พื้นฐาน">
<div class="phero"><span class="pnum">1</span><div><h2>พื้นฐานก่อนอ่านโค้ด</h2><p>ทุกเรื่องใช้ตัวอย่างจากโค้ดจริงในโปรเจกต์ กดชื่อไฟล์บนตัวอย่างเพื่อไปดูในไฟล์เต็ม</p></div></div>
<nav class="chips" aria-label="หัวข้อพื้นฐาน">{chips}</nav>
{"".join(out)}
</section>'''


def section_layer(i, lid, title, intro, files, viewers):
    others = [n for n in sorted(SRC) if layer(n) == lid and n not in files]
    if lid == 'ui':
        others += [n for n in sorted(SRC) if layer(n) == 'comp' and n not in files]
    rows = ''.join(f'<li><a href="#file-{n}"><code>{n}</code></a><span>{file_meta(n)["plain"]}</span></li>' for n in others)
    body = ''.join(f'<h3 class="sh">{n}.java</h3><p class="lead">{file_meta(n)["plain"]}</p>{viewers[n]}' for n in files)
    return f'''<section class="part" id="{lid}" data-toc="{E(title.split(':')[0])}">
<div class="phero"><span class="pnum">{i}</span><div><h2>{E(title)}</h2><p>{E(intro)}</p></div></div>
{body}
<div class="card"><h3>ไฟล์อื่นในชั้นนี้ ({len(others)})</h3><p class="muted">เขียนแบบเดียวกับไฟล์ข้างบน ต่างแค่ชื่อตาราง ชื่อช่อง และกฎ กดชื่อเพื่อดูรายละเอียด</p><ul class="others">{rows}</ul></div>
</section>'''


def trace_html(tid, title, intro, steps):
    lis = []
    for k, (t, n, r, body) in enumerate(steps, 1):
        s, e = rng(n, r)
        lis.append(f'<li class="tstep"><span class="tno">{k}</span><div class="tmain"><h4>{E(t)} <span class="ftag">{LAYER_TH[layer(n)]}</span></h4><p>{body}</p>{snippet(n, s, e)}</div></li>')
    return f'<h3 class="sh" id="{tid}">{E(title)}</h3><p class="lead">{intro}</p><ol class="trace">{"".join(lis)}</ol>'


def section_trace():
    return f'''<section class="part" id="trace" data-toc="ตามรอย 1 คลิก">
<div class="phero"><span class="pnum">7</span><div><h2>ตามรอย 1 คลิก</h2><p>กดปุ่มเดียว โค้ดวิ่งผ่านไฟล์ไหนบ้าง ทีละขั้นจนถึงฐานข้อมูลและกลับมา</p></div></div>
{trace_html('trace-pay', 'กดปุ่ม "ชำระเงิน"', 'ผ่าน 3 ชั้น 7 ไฟล์ แก้ 4 ตารางใน transaction เดียว ลองนึกภาพ: โต๊ะ T02 มา 4 คน สั่งบุฟเฟต์หมู 4 ชุด จ่ายเงินสด 1,000 บาท ใช้โปร P001', TRACE_PAY)}
{trace_html('trace-login', 'เข้าสู่ระบบ', 'จากเปิดโปรแกรม จนเห็นเมนูตามบทบาท', TRACE_LOGIN)}
</section>'''


def section_files():
    chips = '<button class="chip" type="button" data-layer="" aria-pressed="true">ทั้งหมด</button>' + ''.join(
        f'<button class="chip" type="button" data-layer="{l}" aria-pressed="false">{LAYER_TH[l]} ({sum(1 for n in SRC if layer(n) == l)})</button>' for l in LAYER_ORDER)
    groups = ''.join(f'<div class="fgroup" data-layer="{l}"><h3 class="sh">{LAYER_TH[l]}</h3>{"".join(file_card(n) for n in sorted(SRC) if layer(n) == l)}</div>' for l in LAYER_ORDER)
    return f'''<section class="part" id="files" data-toc="ทุกไฟล์">
<div class="phero"><span class="pnum">8</span><div><h2>ทุกไฟล์ ({len(SRC)})</h2><p>แต่ละไฟล์ทำอะไร ใครเรียกใช้ และเป็นงานของใครในทีม กดแถวเพื่อดูรายละเอียด</p></div></div>
<div class="ftools"><input id="fq" class="in" type="search" placeholder="ค้นชื่อไฟล์ ชื่อคน หรือคำ เช่น สมาชิก, นิว, Vendor" aria-label="ค้นหาไฟล์"><div class="chips" id="fl" role="group" aria-label="กรองตามชั้น">{chips}</div></div>
<p class="muted" id="fcount"></p>
{groups}
</section>'''


TEST_OUT = {
    'TestMemberDao': [
        ('สมาชิกทั้งหมด: 5', 'ข้อมูลตัวอย่างมี 5 คน'),
        ('M001: สมชาย ใจดี (0812345678)', 'get ได้ และ toString ทำงาน'),
        ('เพิ่มได้รหัส: M006', 'nextId สร้างรหัสถัดไปถูก'),
        ('กันเบอร์ซ้ำได้: เบอร์ 0911111111 เป็นสมาชิกอยู่แล้ว', 'กฎใน MemberService ทำงาน'),
        ('org.sqlite.SQLiteException: [SQLITE_CONSTRAINT_FOREIGNKEY] A foreign key constraint failed …', '<b>ไม่ใช่โปรแกรมพัง</b> คือ Log ที่ MemberDao จดไว้ตอนลบไม่ได้ (ตัวหนังสือแดงยาว ๆ ใน Output) ตามมาด้วยบรรทัดถัดไป'),
        ('ลบ M001 (มีบิล): false', 'FK กันไม่ให้ลบสมาชิกที่มีบิล ถูกต้อง'),
        ('ลบตัวทดสอบ: true', 'ลบคนที่เพิ่งเพิ่มได้ ฐานข้อมูลกลับเหมือนเดิม'),
    ],
    'TestPosService': [
        ('login manager: manager (ผู้จัดการ)', 'รหัสถูก บทบาทถูก'),
        ('login ผิด role: null', 'staff กดปุ่มผู้จัดการ → ไม่ให้เข้า'),
        ('เปิดโต๊ะ T02 ได้บิล: B0007 · สถานะโต๊ะ: กำลังใช้งาน', 'openTable สร้างบิลและเปลี่ยนสถานะโต๊ะ'),
        ('กันเปิดโต๊ะซ้ำ: โต๊ะนี้ไม่ว่าง', 'เปิดซ้ำไม่ได้'),
        ('ยอดรวม: 1270.0', '299 × 4 + 49 + 25'),
        ('เงินไม่พอ rollback: รับเงินไม่พอ ขาดอีก 871.00 บาท', 'checkout throw แล้ว rollback ไม่มีอะไรถูกบันทึก'),
        ('ส่วนลด P001: 299.0 · สุทธิ: 971.0 · เงินทอน: 29.0', 'จ่ายรอบสองผ่าน'),
        ('โต๊ะ T02 หลังจ่าย: ว่าง', 'คืนโต๊ะแล้ว'),
        ('หมูสามชั้นถูกตัด: 0.6000000000000014', '4 × 0.15 = 0.6 ตัวเลขยาวเพราะคอมเก็บทศนิยมแบบประมาณ (double) เป็นเรื่องปกติ เวลาโชว์เงินเลยต้องปัด 2 ตำแหน่ง'),
        ('แต้ม M004: 38', '971 ÷ 25 = 38.84 ตัดเศษได้ 38'),
        ('ใบเสร็จมี 3 รายการ', 'PD008 สั่ง 2 ลด 1 ยังอยู่ในแถวเดิม'),
        ('รายงาน: บิล 6 · คน 21 · รายได้ 6447.3', 'Dashboard นับบิลที่จ่ายแล้วรวมบิลใหม่'),
        ('เข้างาน E003: 18:19:48', 'เวลาตอนรัน (ของคุณจะต่างไป)'),
        ('ออกงาน E003: 18:19:48', ''),
        ('ตรวจนับ C001 กุ้งคงเหลือ: 5.5', 'ยืนยันการตรวจนับแล้วยอดตรงกับที่นับ'),
    ],
}


def section_tests(viewers):
    def out(n):
        return '<table class="tout"><tr><th>ที่พิมพ์ออกมา</th><th>แปลว่า</th></tr>' + ''.join(
            f'<tr><td><code>{E(a)}</code></td><td>{b}</td></tr>' for a, b in TEST_OUT[n]) + '</table>'
    return f'''<section class="part" id="tests" data-toc="ไฟล์ทดสอบ">
<div class="phero"><span class="pnum">9</span><div><h2>ไฟล์ทดสอบ</h2><p>ลองเรียกโค้ดจริงกับฐานข้อมูลจริง แล้วดูว่าผลตรงกับที่ควรเป็นไหม</p></div></div>
<div class="card"><h3>รันยังไง</h3><ol class="steps">
  <li>ในแผง Projects ของ NetBeans เปิด <code>Source Packages → com.example.bonussuki</code></li>
  <li>คลิกขวาที่ <code>TestMemberDao.java</code> → <b>Run File</b> (หรือเปิดไฟล์แล้วกด <kbd>Shift</kbd>+<kbd>F6</kbd>)</li>
  <li>ผลขึ้นในหน้าต่าง <b>Output</b> ด้านล่าง เทียบกับคอมเมนต์ท้ายบรรทัดในไฟล์ ที่บอกว่าควรได้อะไร</li>
  <li><code>TestPosService</code> เพิ่มบิลจริงลงฐานข้อมูล อยากเริ่มใหม่ให้ปิดโปรแกรม ลบไฟล์ <code>bonus_suki.db</code> แล้วรันใหม่ (สร้างใหม่ให้เอง)</li></ol>
  <p class="muted">ผลข้างล่างได้จากการรันจริงกับฐานข้อมูลที่สร้างใหม่ ที่ commit <code>{REV}</code></p></div>
<h3 class="sh">TestMemberDao.java</h3>{viewers['TestMemberDao']}
<h3 class="sh">ผลของ TestMemberDao</h3>{out('TestMemberDao')}
<h3 class="sh">ผลของ TestPosService</h3><p class="lead">ทดสอบทั้งวงจร ดูโค้ดได้ที่ <a href="#file-TestPosService">TestPosService</a></p>{out('TestPosService')}
</section>'''


# ---------------------------------------------------------------- รวมหน้า
def main():
    key = ['BonusSuki', 'TestMemberDao'] + [n for *_, fs in LAYER_KEYFILES for n in fs]
    viewers, data = {}, {}
    for n in key:
        viewers[n], data[n] = viewer_html(n)
    parts = [section_start(viewers), section_basics()]
    for i, (lid, title, intro, files) in enumerate(LAYER_KEYFILES, 2):
        parts.append(section_layer(i, lid, title, intro, files, viewers))
    parts += [section_trace(), section_files(), section_tests(viewers)]
    tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    page = tpl.replace('{{BODY}}', '\n'.join(parts)).replace('{{DATA}}', json.dumps(data, ensure_ascii=False).replace('</', '<\\/'))
    page = page.replace('{{NFILES}}', str(len(SRC))).replace('{{REV}}', REV)
    open(OUT, 'w', encoding='utf-8').write(page)
    print('wrote', OUT, len(page) // 1024, 'KB', len(SRC), 'files', sum(len(d['notes']) for d in data.values()), 'notes')


main()
