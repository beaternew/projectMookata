#!/usr/bin/env python3
"""เพิ่มส่วน "ใครสร้างไฟล์ไหน ไว้โฟลเดอร์ไหน" ลงคู่มือทั้ง 4 ไฟล์ (รันซ้ำได้ ไม่แทรกซ้ำ)

ข้อมูลมาจากแท็บ "แผนผังโปรเจกต์" (PM_FILES ใน site/index.html) โดยเจ้าของ = เจ้าของงานตัวแรกของไฟล์นั้น
"""
import html, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PEOPLE = ["โอ๊ต", "เปรม", "นุ", "บิ๊ก", "บาส", "เต้", "นิว", "ต๊ะ"]

# (ไฟล์, ชั้น, เจ้าของ) ชั้น: model dao service ui comp helper root sql
F = """
Member model ต๊ะ|MemberDao dao ต๊ะ|MemberService service ต๊ะ|MemberPanel ui ต๊ะ
Vendor model นิว|VendorDao dao นิว|VendorService service นิว|VendorPanel ui นิว
Product model บาส|ProductDao dao บาส|ProductService service บาส|ProductPanel ui บาส
StockItem model บาส|StockItemDao dao บาส|StockItemService service บาส|StockItemPanel ui เต้
Employee model นิว|UserAccount model นิว|EmployeeDao dao นิว|UserAccountDao dao นิว|EmployeeService service นิว|EmployeePanel ui นิว|UserAccountService service นิว
Payroll model ต๊ะ|PayrollDao dao ต๊ะ|PayrollService service ต๊ะ|PayrollPanel ui ต๊ะ
Expense model เปรม|ExpenseDao dao เปรม|ExpenseService service เปรม|ExpensePanel ui เปรม
Bill model นุ|BillProduct model นุ|BillDao dao นุ|BillProductDao dao นุ|BillService service นุ|BillPanel ui นุ|BillLine model นุ
WorkTime model บิ๊ก|WorkTimeDao dao บิ๊ก|WorkTimeService service บิ๊ก|WorkTimePanel ui บิ๊ก
CheckStock model บาส|CheckStockDetail model บาส|CheckStockDao dao บาส|CheckStockDetailDao dao บาส|CheckStockService service บาส|CheckStockPanel ui เต้
DiningTable model โอ๊ต|DiningTableDao dao โอ๊ต|Promotion model โอ๊ต|PromotionDao dao โอ๊ต|PosService service โอ๊ต|PromotionService service โอ๊ต
ProductItemPanel comp โอ๊ต|OrderLinePanel comp โอ๊ต|OpenTableDialog ui โอ๊ต|PaymentDialog ui โอ๊ต|PosPanel ui โอ๊ต
Session helper เปรม|LoginService service เปรม|LoginFrame ui เปรม|MainFrame ui เปรม|HomePanel ui เปรม|BonusSuki root เปรม
ReportRow model บิ๊ก|ReportDao dao บิ๊ก|ReportService service บิ๊ก|DashboardPanel ui บิ๊ก
BillDetailDialog ui นุ
DatabaseHelper helper เต้|DateUtil helper เต้|Dao dao เต้|Theme comp เต้|ThaiFont comp เต้|bonus_suki_sqlite.sql sql เต้|bonus_suki.db db เต้
"""

# โฟลเดอร์จริงในโปรเจกต์ (relative จาก src/main/java/com/example/bonussuki/)
PKG = "src/main/java/com/example/bonussuki"
FOLDER = {
    "model": f"{PKG}/model",
    "dao": f"{PKG}/dao",
    "service": f"{PKG}/service",
    "ui": f"{PKG}/ui",
    "comp": f"{PKG}/ui/component",
    "helper": f"{PKG}/helper",
    "root": PKG,
    "sql": "sql",
    "db": "(รากโปรเจกต์)",
}
ORDER = ["root", "helper", "model", "dao", "service", "ui", "comp", "sql", "db"]

# โฟลเดอร์ที่ "ต้องสร้างเอง" นอกเหนือจากไฟล์ .java (ไม่มีไฟล์ให้ commit ตั้งแต่แรก)
EXTRA = {
    "โอ๊ต": [("images/products/", "รูปเมนู ตั้งชื่อตามรหัสสินค้า เช่น PD001.jpg (เต้ใส่ mock data, โอ๊ตใช้โหลดในหน้า POS)")],
    "เปรม": [("images/receipts/2026-11/", "รูปใบเสร็จค่าใช้จ่าย (ใช้ในหน้า Expense)"),
             ("images/logo.png", "โลโก้ร้านที่หน้า Login ใช้")],
    "เต้": [("images/", "สร้างโฟลเดอร์ + logo.png"), ("sql/", "เก็บสคริปต์ฐานข้อมูล"), ("pom.xml", "ใส่ dependency 2 ตัว")],
}

UNOWNED = [("Bom, BomDao", "model + dao", "สูตร BOM"), ("StockImport, StockImportDao, LotDetail, LotDetailDao", "model + dao", "รับของเข้า (Import + Lot_Detail)")]


def parse():
    rows = []
    for chunk in F.strip().replace("\n", "|").split("|"):
        name, pkg, who = chunk.split()
        rows.append((name, pkg, who))
    return rows


def esc(s):
    return html.escape(s, quote=False)


def build(p):
    """p = '' (manual.html, docs) หรือ 'm-' (index.html, web)"""
    rows = parse()
    out = [f'  <section class="{p}block" id="{p}who">',
           '    <h3>ใครสร้างไฟล์ไหน ไว้โฟลเดอร์ไหน</h3>',
           '    <p>ทุกคน <b>ไม่ต้องสร้างโปรเจกต์เอง</b> เต้ push โครงโฟลเดอร์ขึ้น Git วันที่ 7 พ.ย. แล้วทุกคน pull ไปทำต่อ '
           'ตารางนี้บอกว่าไฟล์ของแต่ละคนต้องเพิ่ม (New → Java Class) ในโฟลเดอร์ไหน '
           'พาธเริ่มจาก <code>src/main/java/com/example/bonussuki/</code> ยกเว้นที่ระบุว่าเป็นพาธอื่น</p>',
           f'    <nav class="{p}minitoc">' + "".join(f'<a href="#{p}who-{i}">{n}</a>' for i, n in enumerate(PEOPLE)) + '<a href="#' + p + 'who-none">ยังไม่มีเจ้าของ</a></nav>']
    for i, who in enumerate(PEOPLE):
        mine = [r for r in rows if r[2] == who]
        by = {}
        for name, pkg, _ in mine:
            by.setdefault(pkg, []).append(name)
        out.append(f'    <h4 id="{p}who-{i}">{who} · {len(mine)} ไฟล์</h4>')
        out.append(f'    <div class="{p}scroll"><table><thead><tr><th>โฟลเดอร์</th><th>ไฟล์ที่สร้างในโฟลเดอร์นี้</th></tr></thead><tbody>')
        for pkg in ORDER:
            if pkg not in by:
                continue
            if pkg == "sql":
                names = by[pkg]
            elif pkg == "db":
                names = by[pkg]
            else:
                names = [n + ".java" for n in by[pkg]]
            fld = FOLDER[pkg]
            shown = fld.replace(PKG + "/", "").replace(PKG, "(โฟลเดอร์ bonussuki)") if fld.startswith(PKG) else fld
            out.append(f'      <tr><td><code>{esc(shown)}/</code></td><td>' + " · ".join(f"<code>{esc(n)}</code>" for n in names) + '</td></tr>'
                       if pkg not in ("root", "db") else
                       f'      <tr><td>{esc(shown)}</td><td>' + " · ".join(f"<code>{esc(n)}</code>" for n in names) + '</td></tr>')
        for path, why in EXTRA.get(who, []):
            out.append(f'      <tr><td><code>{esc(path)}</code> <span class="{p}muted">(นอก src)</span></td><td>{esc(why)}</td></tr>')
        out.append('    </tbody></table></div>')
    out.append(f'    <h4 id="{p}who-none">ยังไม่มีเจ้าของ (ข้อ 13)</h4>')
    out.append(f'    <div class="{p}scroll"><table><thead><tr><th>ไฟล์</th><th>โฟลเดอร์</th><th>งาน</th></tr></thead><tbody>')
    for names, where, what in UNOWNED:
        out.append(f'      <tr><td>{esc(names)}</td><td>{where} (<code>model/</code> กับ <code>dao/</code>)</td><td>{esc(what)} · ทีมต้องแบ่งงานก่อน</td></tr>')
    out.append('    </tbody></table></div>')
    out.append(f'    <p class="{p}muted">เจ้าของไฟล์ = เจ้าของงานตัวแรกของไฟล์นั้นในแผนผังโปรเจกต์ · '
               '<code>BillDetailDialog</code> ชีทมี 2 งานซ้ำ (1-8 ของนุ กับ 18 ของเต้) ใส่ไว้ที่นุ ตามข้อ 12 · '
               'ถ้าต้องแก้ไฟล์ของคนอื่น บอกเจ้าของก่อน</p>')
    out.append('  </section>')
    return "\n".join(out) + "\n"


def patch(path, p):
    s = path.read_text(encoding="utf-8")
    if f'id="{p}who"' in s:
        # รันซ้ำ: แทนที่ของเดิม
        s = re.sub(rf'  <section class="{p}block" id="{p}who">.*?</section>\n', "", s, flags=re.S)
    m = re.search(rf'<section class="{p}block" id="{p}tree">.*?</section>\n', s, flags=re.S)
    if not m:
        sys.exit(f"ไม่เจอส่วน tree ใน {path}")
    s = s[: m.end()] + "\n" + build(p) + s[m.end():]
    link = f'<a href="#{p}who">ใครสร้างอะไร</a>'
    toc = f'<a href="#{p}tree">โครงไฟล์</a>'
    if link not in s:
        s = s.replace(toc, toc + link, 1)
    path.write_text(s, encoding="utf-8")
    print("ok", path.relative_to(ROOT))


patch(ROOT / "site/index.html", "m-")
patch(ROOT / "web/โปรเจกต์โบนัสสุกี้.html", "m-")
patch(ROOT / "site/manual.html", "")
patch(ROOT / "docs/คู่มือรวมโปรเจกต์-BonusSuki-JavaSwing.html", "")
