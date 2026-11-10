# -*- coding: utf-8 -*-
# เนื้อหาของหน้าอ่านโค้ด: คำอธิบายทุกไฟล์ · พื้นฐาน · ตามรอย · ไฟล์ทดสอบ
# โค้ดตัวอย่างอ้างเป็น (ไฟล์, บรรทัดเริ่ม, บรรทัดจบ) หรือ ('method', ไฟล์, 'ข้อความหัวเมธอด') ให้ gen.py ตัดจากไฟล์จริง

# ---------- คำอธิบายภาษาง่ายของทุกไฟล์ (model/dao สร้างอัตโนมัติจากชื่อตาราง) ----------
PLAIN = {
    'BonusSuki': 'จุดเริ่มโปรแกรม กด F6 แล้วมาเริ่มที่นี่ ตั้งหน้าตา ฟอนต์ไทย แล้วเปิดหน้า Login',
    'TestMemberDao': 'โปรแกรมทดสอบเล็ก ๆ ลองนับ ค้น เพิ่ม ลบ สมาชิกกับฐานข้อมูลจริง แล้วพิมพ์ผลออกมา',
    'TestPosService': 'ทดสอบทั้งวงจรหน้าร้าน: ล็อกอิน เปิดโต๊ะ สั่งอาหาร จ่ายเงิน ตัดสต็อก แต้มสมาชิก รายงาน ลงเวลา ตรวจนับ',
    'DatabaseHelper': 'ประตูเข้าฐานข้อมูลบานเดียวของโปรแกรม เปิดไฟล์ bonus_suki.db ครั้งเดียวแล้วให้ทุก DAO ยืมใช้ สร้างรหัสถัดไป (M006) และช่วยปิด rs/stmt',
    'DateUtil': 'ทำให้วันที่และเวลาเป็นข้อความรูปแบบเดียวกันทั้งโปรแกรม เช่น วันนี้ = 2026-11-10 เวลา = 18:20:05',
    'Session': 'จำว่าตอนนี้ใครล็อกอินอยู่ และเป็นผู้จัดการหรือพนักงาน ทุกหน้าจอถามได้',
    'Dao': 'ใบสัญญาว่า DAO ทุกตัวต้องมี 6 เมธอด: get, getAll ×2, save, update, delete',
    'BillLine': 'ไม่ใช่ตาราง เป็นกล่องรวม "รายการในบิล + ชื่อเมนู + ราคา" ที่ได้จากการ JOIN สองตาราง ใช้โชว์ในหน้า POS และใบเสร็จ',
    'ReportRow': 'ไม่ใช่ตาราง เป็นจุด 1 จุดบนกราฟ Dashboard: ป้าย (เดือน/หมวด) + ตัวเลข',
    'ReportDao': 'SQL สำหรับ Dashboard: ยอดขาย จำนวนบิล จำนวนลูกค้า ยอดรายเดือน นับเฉพาะบิลที่จ่ายแล้ว',
    'BillService': 'ดูบิลย้อนหลังและรายการในบิล (หน้า BillPanel และใบเสร็จ) การเปิดและจ่ายบิลอยู่ใน PosService',
    'CheckStockService': 'ตรวจนับสต็อก: เริ่มรอบ (จดยอดในระบบ) → กรอกยอดที่นับได้จริง → ยืนยันแล้วปรับยอดคงเหลือให้ตรง',
    'EmployeeService': 'กฎของพนักงาน (ชื่อ เบอร์ เงินเดือน) และบัญชีล็อกอินของพนักงานคนนั้น',
    'ExpenseService': 'กฎของค่าใช้จ่าย และคัดลอกรูปใบเสร็จเข้าโฟลเดอร์ images/receipts',
    'LoginService': 'เช็กชื่อผู้ใช้ รหัสผ่าน และบทบาท ถ้าถูกหมดก็จดลง Session',
    'MemberService': 'กฎของสมาชิก: ชื่อห้ามว่าง เบอร์ 10 หลัก ห้ามซ้ำ และบวกแต้มตอนจ่ายเงิน (25 บาท = 1 แต้ม)',
    'PayrollService': 'กฎเงินเดือน: ยอดสุทธิ = ฐานเงินเดือน + OT − ยอดหัก แล้วผูกวันทำงานเข้ากับรอบจ่าย',
    'PosService': 'หัวใจหน้าร้าน: เปิดโต๊ะ เพิ่ม/ลดเมนู รวมยอด และชำระเงินแบบ transaction (พังขั้นไหนย้อนกลับหมด)',
    'ProductService': 'กฎของสินค้า/เมนู และค้นหาตามหมวดกับคำค้น',
    'PromotionService': 'คิดส่วนลดตามโปรที่เลือก 1 บิลใช้ได้ 1 โปร และจำนวนคนต้องถึงเงื่อนไข',
    'ReportService': 'ส่งต่อตัวเลขและข้อมูลกราฟจาก ReportDao ให้หน้า Dashboard (หน้าจอห้ามเรียก DAO เอง)',
    'StockItemService': 'กฎของวัตถุดิบ และตัดสต็อกตามสูตร BOM ตอนขาย',
    'UserAccountService': 'เพิ่ม แก้ ลบ บัญชีล็อกอิน (แยกจาก LoginService ที่ใช้ตอนเข้าสู่ระบบ)',
    'VendorService': 'กฎของผู้จัดจำหน่าย: ชื่อห้ามว่าง เบอร์ถูกรูปแบบ',
    'WorkTimeService': 'ลงเวลาเข้า-ออกงาน 1 คนลงได้วันละ 1 แถว',
    'BillDetailDialog': 'หน้าต่างใบเสร็จ 1 ใบ: หัวบิล รายการ ยอดรวม ส่วนลด สุทธิ เงินรับ เงินทอน',
    'BillPanel': 'ตารางบิลย้อนหลัง ดูอย่างเดียว ดับเบิลคลิกแถวเพื่อเปิดใบเสร็จ',
    'CheckStockPanel': 'หน้าตรวจนับสต็อก: เริ่มรอบ แก้ช่อง "นับได้" ในตาราง แล้วยืนยัน',
    'DashboardPanel': 'หน้าสรุปของผู้จัดการ: การ์ดตัวเลข 3 ใบ กราฟเส้นรายเดือน กราฟวงกลม (ใช้ไลบรารี jfreechart)',
    'EmployeePanel': 'หน้า CRUD พนักงาน และบัญชีล็อกอินของพนักงานคนนั้นในหน้าเดียวกัน',
    'ExpensePanel': 'หน้า CRUD ค่าใช้จ่าย แนบรูปใบเสร็จได้',
    'HomePanel': 'หน้าแรกหลังล็อกอิน: ทักทาย สรุปของวันนี้ วัตถุดิบใกล้หมด ปุ่มลัดไปหน้าขาย',
    'LoginFrame': 'หน้าต่างเข้าสู่ระบบ: เลือกบทบาท กรอกชื่อผู้ใช้และรหัสผ่าน',
    'MainFrame': 'หน้าต่างหลัก: แถบเมนูซ้าย แถบชื่อผู้ใช้ด้านบน และพื้นที่ตรงกลางที่สลับหน้าได้ (CardLayout)',
    'MemberPanel': 'หน้า CRUD สมาชิก เป็นแม่แบบของหน้า CRUD ทุกหน้า (ฟอร์มซ้าย ตารางขวา)',
    'OpenTableDialog': 'หน้าต่างเลือกโต๊ะและจำนวนคนก่อนสั่งอาหาร โต๊ะที่เปิดอยู่แล้วกลับมาสั่งต่อได้',
    'PaymentDialog': 'หน้าต่างชำระเงิน: ค้นสมาชิกด้วยเบอร์ เลือกโปร เลือกเงินสด/QR โชว์เงินทอนทันที',
    'PayrollPanel': 'หน้า CRUD เงินเดือน ยอดสุทธิคำนวณให้เอง',
    'PosPanel': 'หน้าขาย: ปุ่มหมวด การ์ดเมนู 3 คอลัมน์ และรายการในบิลฝั่งขวา',
    'ProductPanel': 'หน้า CRUD สินค้า/เมนู และรูปเมนู',
    'StockItemPanel': 'หน้า CRUD วัตถุดิบ โชว์ว่าตัวไหนใกล้หมด',
    'VendorPanel': 'หน้า CRUD ผู้จัดจำหน่าย หน้าตาแบบเดียวกับ MemberPanel',
    'WorkTimePanel': 'หน้าลงเวลาเข้า-ออกงาน มีนาฬิกาเดินอยู่ พนักงานลงเวลาของตัวเองได้',
    'Form': 'ตัวช่วยของหน้า CRUD: ตารางที่แก้ในเซลล์ไม่ได้ ช่องว่างกลายเป็น null แปลงข้อความเป็นตัวเลข',
    'ImageLoader': 'โหลดรูปจากโฟลเดอร์ images/ ถ้าไม่มีรูปก็วาดรูปแทนให้ (กล่องสีเทา หรือวงกลมตัวอักษร)',
    'OrderLinePanel': 'แถวรายการอาหาร 1 แถวในหน้า POS: ชื่อ ราคา ปุ่ม − จำนวน + และปุ่มลบ',
    'ProductItemPanel': 'การ์ดเมนู 1 ใบในหน้า POS: รูป ชื่อ ราคา ปุ่ม +',
    'Refreshable': 'สัญญาว่า "หน้านี้โหลดข้อมูลใหม่ได้" MainFrame เรียก refresh() ทุกครั้งที่เปิดหน้า',
    'ThaiFont': 'ตั้งฟอนต์ที่อ่านภาษาไทยได้ให้ทั้งโปรแกรม เรียกครั้งเดียวใน main',
    'Theme': 'เก็บสีทั้งหมดจาก Figma และวิธีแต่งปุ่ม ตาราง การ์ด หัวข้อ ทุกหน้าจอเรียกที่นี่ ห้ามพิมพ์สีเอง',
}

LAYER_INFO = [
    # (id, ชื่อ, เทียบกับร้าน, หน้าที่, ห้ามทำ)
    ('ui', 'ui — หน้าจอ', 'พนักงานหน้าร้าน', 'รับการกดปุ่ม อ่านช่องกรอก โชว์ผล ไม่รู้กฎร้าน ไม่รู้ SQL', 'ห้ามเรียก DAO ตรง ๆ ห้ามเขียน SQL'),
    ('service', 'service — กฎร้าน', 'ผู้จัดการร้าน', 'ตัดสินว่าทำได้ไหม (เบอร์ซ้ำ? เงินพอ? โต๊ะว่าง?) แล้วสั่ง DAO', 'ห้ามแตะ JButton/JTable ห้ามเขียน SQL'),
    ('dao', 'dao — คุยกับฐานข้อมูล', 'คนเฝ้าคลัง', 'เขียน SQL 1 ตาราง = 1 DAO แปลงแถวเป็นออบเจกต์', 'ห้ามตัดสินกฎร้าน ห้ามเปิดหน้าต่าง'),
    ('db', 'bonus_suki.db — ฐานข้อมูล', 'คลังสินค้า', 'ไฟล์ SQLite ไฟล์เดียว เก็บ 18 ตาราง', ''),
]

# ---------- ตามรอย ----------
# step: (หัวข้อ, ไฟล์, ช่วง, คำอธิบาย) · ช่วง = (start, end) หรือ ('method', 'หัวเมธอด')
TRACE_PAY = [
    ('คนกดปุ่ม "ชำระเงิน"', 'PosPanel', (219, 220),
     'ปุ่ม btnCheckout ถูกผูกกับเมธอดนี้ไว้ใน initComponents พอกดก็เข้ามาที่นี่ ถ้ามีบิลอยู่ เปิดหน้าต่างชำระเงิน'),
    ('หน้าต่างชำระเงินเปิดขึ้นและรอ', 'PaymentDialog', (283, 287),
     'หน้าต่างแบบ modal: <code>setVisible(true)</code> จะค้างอยู่บรรทัดนี้จนกว่าหน้าต่างจะปิด แล้วค่อยตอบกลับว่าจ่ายสำเร็จ (paid) หรือไม่'),
    ('พนักงานกด "ยืนยัน"', 'PaymentDialog', (254, 265),
     'อ่านวิธีจ่ายและเงินที่รับ แปลงเป็นตัวเลข แล้วส่งทุกอย่างให้ <code>posService.checkout(...)</code> หน้าจอไม่คิดเงินเอง'),
    ('เริ่ม transaction', 'PosService', (85, 89),
     'ปิด auto-commit: จากนี้ทุกคำสั่ง SQL ยังไม่ถูกบันทึกจริง จนกว่าจะ commit'),
    ('รวมยอด คิดส่วนลด เช็กเงิน', 'PosService', (90, 100),
     'รวมยอดจากรายการในบิล ให้ PromotionService คิดส่วนลด หักได้ยอดสุทธิ ถ้าเงินไม่พอ throw ทันที (ยังไม่มีอะไรถูกบันทึก)'),
    ('PromotionService คิดส่วนลด', 'PromotionService', ('method', 'public double calcDiscount('),
     'เลือกตามรหัสโปรด้วย <code>switch</code> เช่น สมาชิกลด 10% · ไม่ใช้โปร = ส่วนลด 0'),
    ('เติมข้อมูลลงบิล แล้วบันทึก', 'PosService', (101, 113),
     'ตั้งค่าทุกช่องของบิล แล้วสั่ง <code>billDao.update(bill)</code> ถ้าได้ null → require โยนข้อผิดพลาด'),
    ('BillDao เขียน UPDATE', 'BillDao', ('method', 'public Bill update('),
     'SQL ตัวจริงที่แก้แถวบิล ใช้ ? หลายตัวเรียงตามคอลัมน์ ใช้ connection ตัวเดียวกับ PosService จึงอยู่ใน transaction เดียวกัน'),
    ('ตัดสต็อกตามสูตร', 'StockItemDao', ('method', 'public boolean deductByBom('),
     'คำสั่งเดียวตัดวัตถุดิบทุกตัวที่เมนูในบิลใช้: จำนวนที่สั่ง × ปริมาณต่อจานในตาราง BOM (บุฟเฟต์หมู 4 ชุด × 0.15 กก. = หมู 0.6 กก.)'),
    ('บวกแต้มสมาชิก', 'MemberService', (59, 66),
     'ถ้ามีสมาชิก: ยอดสุทธิ ÷ 25 ปัดเศษทิ้ง บวกเข้าแต้มเดิม แล้ว update'),
    ('คืนโต๊ะ', 'DiningTableDao', ('method', 'public boolean updateStatus('),
     'โต๊ะกลับเป็น "ว่าง" ให้ลูกค้าโต๊ะถัดไป'),
    ('commit หรือ rollback', 'PosService', (118, 126),
     'ทุกขั้นผ่าน → <code>commit()</code> บันทึกพร้อมกันทีเดียว · พังขั้นไหน → <code>rollback()</code> ย้อนกลับทั้งหมด แล้วส่งข้อผิดพลาดต่อ · สุดท้ายเปิด auto-commit คืน'),
    ('กลับมาที่หน้าต่างชำระเงิน', 'PaymentDialog', (266, 276),
     'ถ้ามีข้อผิดพลาด จับแล้วเด้งข้อความ (เช่น "รับเงินไม่พอ ขาดอีก 871.00 บาท") ถ้าสำเร็จ <code>paid = true</code> แล้วปิดหน้าต่าง'),
    ('กลับมาที่หน้าขาย', 'PosPanel', (220, 229),
     '<code>PaymentDialog.show</code> ตอบ true → ล้างบิล โชว์บิลว่าง ถามว่าจะดูใบเสร็จไหม จบการเดินทาง'),
]

TRACE_LOGIN = [
    ('เปิดโปรแกรม', 'BonusSuki', (12, 22), 'main เปิดหน้า LoginFrame'),
    ('กดปุ่ม Login', 'LoginFrame', (201, 206), 'อ่านบทบาท ชื่อผู้ใช้ รหัสผ่าน ส่งให้ LoginService'),
    ('LoginService ตรวจ', 'LoginService', (19, 23), 'หาบัญชีจากชื่อผู้ใช้ แล้วเช็กรหัสและบทบาท'),
    ('UserAccountDao หาบัญชี', 'UserAccountDao', ('method', 'public UserAccount getByUsername('),
     'SELECT … WHERE Username = ? แบบ Lab 8 เจอแถว → แปลงด้วย fromRS'),
    ('แปลงแถวเป็นออบเจกต์', 'UserAccount', ('method', 'public static UserAccount fromRS('),
     'หยิบทีละคอลัมน์ใส่ทีละช่อง'),
    ('หาข้อมูลพนักงาน', 'LoginService', (24, 26), 'ดึงชื่อจริงของพนักงานเจ้าของบัญชี แล้วจดลง Session'),
    ('จดลง Session', 'Session', (15, 18), 'เก็บไว้ในตัวแปร static ทุกหน้าจอถามได้'),
    ('ผ่าน → เปิดหน้าหลัก', 'LoginFrame', (207, 214), 'ไม่ผ่านเด้งข้อความ ผ่านเปิด MainFrame แล้วปิดหน้า Login'),
    ('MainFrame ดูบทบาท', 'MainFrame', (66, 82), 'ผู้จัดการได้หน้าเพิ่ม 10 หน้า พนักงานเห็นแค่หน้าแรก หน้าขาย และลงเวลา'),
]

# ---------- พื้นฐาน ----------
# (id, กลุ่ม, หัวข้อ, คำอธิบาย HTML, ตัวอย่าง [(ไฟล์, ช่วง)] หรือ [('raw', ภาษา, ข้อความ)])
BASICS = [
    # ---------------- Java
    ('b-package', 'java', 'package และ import',
     '<p><b>package</b> คือที่อยู่ของไฟล์ เหมือนเลขห้อง ไฟล์ <code>MemberDao.java</code> อยู่โฟลเดอร์ <code>dao</code> จึงเขียน <code>package com.example.bonussuki.dao;</code></p>'
     '<p><b>import</b> คือบอกว่า "จะใช้คลาสจากห้องอื่นนะ" เขียนไว้บนสุด ถ้า NetBeans ขีดเส้นแดงว่าหาคลาสไม่เจอ กด <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>I</kbd> (Mac: <kbd>⌘</kbd>+<kbd>Shift</kbd>+<kbd>I</kbd>) ให้มันเติม import ให้</p>',
     [('MemberDao', (1, 13))]),
    ('b-class', 'java', 'class กับ object',
     '<p><b>class</b> คือแบบพิมพ์ <b>object</b> คือของที่พิมพ์ออกมาจากแบบ</p>'
     '<p>คลาส <code>Member</code> คือแบบฟอร์มบัตรสมาชิก มีช่องชื่อ เบอร์ แต้ม ส่วน <code>new Member("สมชาย", "081…", null)</code> คือบัตร 1 ใบที่กรอกแล้ว สร้างกี่ใบก็ได้จากแบบเดียว</p>'
     '<p>ในโปรเจกต์นี้ 1 คลาส = 1 ไฟล์ และชื่อไฟล์ต้องตรงกับชื่อคลาส</p>',
     [('raw', 'java', 'Member somchai = new Member("สมชาย ใจดี", "0812345678", null);   // object ใบที่ 1\nMember suda   = new Member("สุดา แสงทอง", "0898765432", null);  // object ใบที่ 2\nSystem.out.println(somchai.getMemberName());                      // สมชาย ใจดี')]),
    ('b-field', 'java', 'ตัวแปรและชนิดข้อมูล',
     '<p>ทุกตัวแปรต้องบอกชนิดก่อนชื่อเสมอ</p>'
     '<table class="mini"><tr><th>ชนิด</th><th>เก็บอะไร</th><th>ตัวอย่างในโปรเจกต์</th></tr>'
     '<tr><td><code>String</code></td><td>ข้อความ</td><td>รหัส "M001", ชื่อ, วันที่ "2026-11-10"</td></tr>'
     '<tr><td><code>int</code></td><td>จำนวนเต็ม</td><td>แต้มสะสม, จำนวนคน</td></tr>'
     '<tr><td><code>double</code></td><td>ตัวเลขมีทศนิยม</td><td>ราคา 299.0, ยอดเงิน</td></tr>'
     '<tr><td><code>boolean</code></td><td>จริง/เท็จ</td><td><code>isManager()</code></td></tr>'
     '<tr><td><code>Integer</code>, <code>Double</code></td><td>ตัวเลขแบบที่เป็น <code>null</code> ได้</td><td>เงินที่รับ (ยังไม่จ่าย = null)</td></tr></table>'
     '<p><code>null</code> = "ไม่มีอะไรอยู่เลย" ถ้าเรียกเมธอดของตัวแปรที่เป็น null โปรแกรมพังด้วย <code>NullPointerException</code></p>',
     [('Member', (9, 13))]),
    ('b-ctor', 'java', 'constructor',
     '<p>เมธอดพิเศษที่ชื่อเหมือนคลาส ไม่มีชนิดที่คืน ทำงานตอน <code>new</code> มีไว้เติมค่าเริ่มต้น</p>'
     '<p>คลาสเดียวมีได้หลายตัว ขอแค่รับของต่างกัน <code>Member</code> มี 3 ตัว: ครบทุกช่อง / ไม่มีรหัส / ว่างเปล่า</p>'
     '<p><code>this.memberId = memberId;</code> → <code>this.memberId</code> คือช่องของกล่อง ส่วน <code>memberId</code> เฉย ๆ คือค่าที่ส่งเข้ามา</p>',
     [('Member', (15, 30))]),
    ('b-method', 'java', 'method: รับของ ทำงาน คืนของ',
     '<p>หัวเมธอดอ่านได้แบบนี้: <code>public Member get(String memberId)</code> = ใครก็เรียกได้ (public) · คืน Member · ชื่อ get · รับ String 1 ตัว</p>'
     '<p><code>void</code> = ไม่คืนอะไร · <code>return</code> = ส่งค่ากลับแล้วออกจากเมธอดทันที</p>',
     [('MemberService', (27, 33))]),
    ('b-getset', 'java', 'private + getter/setter',
     '<p>ช่องในกล่องตั้งเป็น <code>private</code> คนนอกแตะตรง ๆ ไม่ได้ ต้องผ่าน <code>getX()</code> (ขอดู) และ <code>setX()</code> (ขอเปลี่ยน)</p>'
     '<p>ทำไมต้องยุ่งยาก? วันหนึ่งถ้าอยากเพิ่มการเช็ก เช่น "แต้มห้ามติดลบ" ก็แก้ใน setter ที่เดียว ไม่ต้องไล่แก้ทุกไฟล์</p>',
     [('Member', (32, 38))]),
    ('b-static', 'java', 'static และค่าคงที่',
     '<p><code>static</code> = เป็นของคลาส ไม่ใช่ของ object แต่ละตัว มีชุดเดียวทั้งโปรแกรม เรียกผ่านชื่อคลาสได้เลย เช่น <code>DatabaseHelper.getConnect()</code>, <code>Session.isManager()</code></p>'
     '<p><code>static final</code> = ค่าคงที่ เปลี่ยนไม่ได้ ตั้งชื่อตัวใหญ่ เช่น <code>BAHT_PER_POINT = 25</code></p>',
     [('MemberService', (10, 11)), ('DatabaseHelper', (23, 23))]),
    ('b-interface', 'java', 'interface และ implements',
     '<p><b>interface</b> = ใบสัญญา บอกแค่ชื่อเมธอดที่ต้องมี ไม่มีเนื้อในเมธอด</p>'
     '<p><b>implements</b> = เซ็นสัญญา คลาสนั้นต้องเขียนเมธอดครบทุกตัว ไม่งั้น compile ไม่ผ่าน</p>'
     '<p>ในโปรเจกต์มี 2 ใบสัญญา: <code>Dao&lt;T&gt;</code> (DAO ทุกตัว) และ <code>Refreshable</code> (หน้าจอที่โหลดใหม่ได้)</p>',
     [('Dao', (9, 22)), ('MemberDao', (16, 16))]),
    ('b-list', 'java', 'List และ ArrayList',
     '<p><code>List&lt;Member&gt;</code> = รายการของ Member หลายตัวเรียงกัน <code>&lt;Member&gt;</code> บอกว่าข้างในเป็นอะไร</p>'
     '<p><code>new ArrayList&lt;&gt;()</code> สร้างรายการว่าง · <code>list.add(x)</code> เพิ่ม · <code>list.size()</code> นับ · <code>list.get(0)</code> หยิบตัวแรก</p>',
     [('MemberDao', (46, 46)), ('MemberDao', (54, 56))]),
    ('b-loop', 'java', 'if และ loop',
     '<p><code>if (เงื่อนไข) { … } else { … }</code> = ถ้าจริงทำอันแรก ไม่งั้นทำอันหลัง</p>'
     '<p><code>for (BillLine line : lines)</code> = "หยิบทีละ line จาก lines" ทำซ้ำจนครบ · <code>while (rs.next())</code> = ทำซ้ำตราบที่ยังมีแถว</p>'
     '<p>ตัวเชื่อม: <code>&amp;&amp;</code> และ · <code>||</code> หรือ · <code>!</code> ไม่</p>',
     [('PosService', (73, 79))]),
    ('b-equals', 'java', '== กับ .equals()',
     '<p>ตัวเลขเทียบด้วย <code>==</code> ได้ แต่ <b>ข้อความต้องใช้ <code>.equals()</code></b></p>'
     '<p><code>==</code> กับข้อความถามว่า "เป็นกระดาษแผ่นเดียวกันไหม" ส่วน <code>.equals()</code> ถามว่า "เขียนเหมือนกันไหม" รหัสผ่านที่พิมพ์มากับที่อ่านจากฐานข้อมูลเป็นคนละแผ่น ใช้ == จะได้ false ทั้งที่รหัสถูก</p>',
     [('LoginService', (21, 23))]),
    ('b-throw', 'java', 'throw: โยนข้อผิดพลาด',
     '<p>เมื่อ service เจอข้อมูลผิดกฎ มันจะ <code>throw new IllegalArgumentException("ข้อความ")</code> = หยุดทำงานตรงนั้น แล้วโยนกระดาษข้อความขึ้นไปให้คนที่เรียก</p>'
     '<p>หน้าจอรับกระดาษด้วย <code>catch</code> แล้วเอาข้อความไปโชว์ ผู้ใช้จึงเห็น "เบอร์โทรต้องเป็นตัวเลข 10 หลัก" แทนโปรแกรมค้าง</p>',
     [('MemberService', (72, 79))]),
    ('b-try', 'java', 'try-catch: ลองทำ ถ้าพังให้รับมือ',
     '<p><code>try { โค้ดที่อาจพัง } catch (ชนิดข้อผิดพลาด ex) { ทำอะไรเมื่อพัง }</code></p>'
     '<p>ถ้าบรรทัดใดใน try พัง Java กระโดดไป catch ทันที บรรทัดที่เหลือใน try ไม่ทำ <code>ex.getMessage()</code> = ข้อความที่ถูกโยนมา</p>',
     [('MemberPanel', (191, 201))]),
    ('b-finally', 'java', 'finally: ทำเสมอ (แบบ Lab 8)',
     '<p><code>finally { … }</code> ต่อท้าย try-catch ทำ<b>ทุกครั้ง</b> ไม่ว่าจะสำเร็จ พัง หรือ return ไปแล้ว เหมาะกับ "เก็บกวาด"</p>'
     '<p>DAO ทุกตัวในโปรเจกต์ใช้รูปเดียวกัน:</p><ol><li>ยืม <code>conn</code> จาก DatabaseHelper</li><li>ประกาศ <code>stmt</code>, <code>rs</code> = null ไว้นอก try</li><li>try: เตรียม SQL ใส่ค่า ส่งไป อ่านผล</li><li>catch: จด Log คืน null / -1</li><li>finally: <code>closeQuietly(rs, stmt)</code> <b>ไม่ปิด conn</b></li></ol>',
     [('MemberDao', (20, 37))]),
    ('b-lambda', 'java', 'lambda และ this::method',
     '<p>บางครั้งเราต้อง "ส่งงาน" ให้คนอื่นไว้ทำทีหลัง เช่น "ถ้าปุ่มถูกกด ให้ทำสิ่งนี้"</p>'
     '<p><code>e -&gt; { … }</code> คือ <b>lambda</b> = งานสั้น ๆ ไม่มีชื่อ · <code>this::btnSaveActionPerformed</code> คือ <b>method reference</b> = "ส่งเมธอดนี้ของฉันไป" NetBeans ใช้แบบหลังผูกปุ่มทุกปุ่ม</p>',
     [('MemberPanel', (31, 31)), ('PosPanel', (248, 252))]),
    # ---------------- Swing
    ('b-swing', 'swing', 'JFrame, JPanel, JDialog',
     '<ul><li><b>JFrame</b> = หน้าต่างจริง มีแถบชื่อและปุ่มปิด (LoginFrame, MainFrame)</li>'
     '<li><b>JPanel</b> = แผ่นกระดานวางของ ต้องอยู่ในหน้าต่างอื่น (MemberPanel ถูกวางใน MainFrame)</li>'
     '<li><b>JDialog</b> = หน้าต่างเด้งเล็ก ๆ ที่รอให้ตอบก่อน (PaymentDialog, OpenTableDialog)</li></ul>'
     '<p>บนแผ่นมีชิ้นส่วน: <code>JButton</code> ปุ่ม · <code>JLabel</code> ป้ายข้อความ · <code>JTextField</code> ช่องกรอก · <code>JTable</code> ตาราง · <code>JComboBox</code> กล่องเลือก · <code>JSpinner</code> ช่องตัวเลขมีลูกศร</p>',
     [('MemberPanel', (13, 14))]),
    ('b-names', 'swing', 'ชื่อชิ้นส่วนบอกชนิด',
     '<p>ทีมตั้งชื่อตัวแปรให้ขึ้นต้นด้วยชนิด อ่านชื่อแล้วรู้เลยว่าเป็นอะไร</p>'
     '<table class="mini"><tr><th>ขึ้นต้น</th><th>ชนิด</th><th>ตัวอย่าง</th></tr>'
     '<tr><td>btn</td><td>JButton ปุ่ม</td><td>btnSave</td></tr><tr><td>txt</td><td>JTextField ช่องกรอก</td><td>txtMemberName</td></tr>'
     '<tr><td>txa</td><td>JTextArea ช่องกรอกหลายบรรทัด</td><td>txaMemberAddress</td></tr><tr><td>lbl</td><td>JLabel ป้าย</td><td>lblTitle</td></tr>'
     '<tr><td>tbl</td><td>JTable ตาราง</td><td>tblMember</td></tr><tr><td>cmb</td><td>JComboBox กล่องเลือก</td><td>cmbPromotion</td></tr>'
     '<tr><td>spn</td><td>JSpinner ช่องตัวเลข</td><td>spnPointBalance</td></tr><tr><td>pnl</td><td>JPanel แผง</td><td>pnlForm</td></tr>'
     '<tr><td>scr</td><td>JScrollPane แถบเลื่อน</td><td>scrMember</td></tr><tr><td>tgl</td><td>JToggleButton ปุ่มกดค้าง</td><td>tglManager</td></tr></table>',
     []),
    ('b-form', 'swing', 'ไฟล์ .form และ initComponents',
     '<p>ทุกหน้าจอมี 2 ไฟล์คู่กัน: <code>MemberPanel.form</code> (สิ่งที่ลากวางในแท็บ <b>Design</b>) และ <code>MemberPanel.java</code></p>'
     '<p>NetBeans อ่าน .form แล้ว<b>เขียนโค้ดให้เอง</b>ในเมธอด <code>initComponents()</code> ส่วนที่มีพื้นเทาใน NetBeans (อยู่ระหว่าง <code>GEN-BEGIN</code> กับ <code>GEN-END</code>) <b>ห้ามแก้ด้วยมือ</b> แก้ไปก็โดนเขียนทับ</p>'
     '<p>เราเขียนได้ 2 ที่: ใน constructor หลัง <code>initComponents()</code> (แต่งสี โหลดข้อมูล) และในเมธอดของปุ่ม (ระหว่าง <code>GEN-FIRST</code> กับ <code>GEN-LAST</code>)</p>',
     [('LoginFrame', (20, 21)), ('LoginFrame', (43, 45))]),
    ('b-event', 'swing', 'กดปุ่มแล้วเกิดอะไร (event)',
     '<p>ในแท็บ Design ดับเบิลคลิกปุ่ม NetBeans จะสร้าง 2 อย่าง:</p><ol><li>บรรทัดผูกปุ่ม <code>btnLogin.addActionListener(this::btnLoginActionPerformed);</code> ใน initComponents</li><li>เมธอดว่าง <code>btnLoginActionPerformed</code> ให้เราเขียนข้างใน</li></ol>'
     '<p>พอผู้ใช้กดปุ่ม Swing จะเรียกเมธอดนั้นให้</p>',
     [('LoginFrame', (113, 113)), ('LoginFrame', (201, 215))]),
    ('b-jtable', 'swing', 'JTable และ TableModel (แบบ Lab 11)',
     '<p>JTable เป็นแค่ "จอ" ข้อมูลจริงอยู่ใน <b>TableModel</b> วิธีของ Lab 11: ทุกครั้งที่โหลด สร้าง <code>DefaultTableModel</code> ใหม่ ใส่หัวตาราง เติมทีละแถวด้วย <code>addRow(new Object[]{…})</code> แล้ว <code>tbl.setModel(model)</code></p>'
     '<p>อยากรู้ว่าคลิกแถวไหน: <code>tbl.getSelectedRow()</code> · อ่านค่าในเซลล์: <code>getValueAt(แถว, คอลัมน์)</code> นับจาก 0</p>',
     [('MemberPanel', (235, 242))]),
    ('b-dialog', 'swing', 'JOptionPane กล่องข้อความ',
     '<p><code>showMessageDialog(this, "ข้อความ")</code> เด้งบอก · <code>showConfirmDialog(…, YES_NO_OPTION)</code> เด้งถาม ใช่/ไม่ใช่ แล้วคืนว่ากดอะไร</p>',
     [('MemberPanel', (209, 212))]),
    ('b-layout', 'swing', 'Layout: วางของยังไง',
     '<ul><li><b>GroupLayout</b> (Free Design) = ที่ NetBeans ใช้ตอนลากวาง จัดเป็นกลุ่มแนวนอน/แนวตั้ง</li>'
     '<li><b>GridLayout</b> = ตารางช่องเท่ากัน (การ์ดเมนู 3 คอลัมน์, Login แบ่ง 2 ซีก)</li>'
     '<li><b>CardLayout</b> = สำรับไพ่ โชว์ทีละใบ (MainFrame สลับหน้า)</li></ul>',
     [('MainFrame', (330, 341))]),
    # ---------------- SQL
    ('b-db', 'sql', 'ตาราง แถว คอลัมน์ PK FK',
     '<p>ฐานข้อมูลคือสมุดหลายเล่ม 1 เล่ม = 1 <b>ตาราง</b> 1 บรรทัดในสมุด = 1 <b>แถว</b> หัวข้อแต่ละช่อง = <b>คอลัมน์</b></p>'
     '<table class="mini"><tr><th>Member_ID (PK)</th><th>Member_Name</th><th>Member_PhoneNo</th><th>Point_Balance</th></tr>'
     '<tr><td>M001</td><td>สมชาย ใจดี</td><td>0812345678</td><td>120</td></tr>'
     '<tr><td>M002</td><td>สุดา แสงทอง</td><td>0898765432</td><td>45</td></tr>'
     '<tr><td>M003</td><td>วิชัย ปัญญาดี</td><td>0623456789</td><td>300</td></tr></table>'
     '<p><b>PK (Primary Key)</b> = ช่องที่ห้ามซ้ำ ใช้ชี้ตัวแถว (Member_ID) · <b>FK (Foreign Key)</b> = ช่องที่ชี้ไปตารางอื่น เช่น บิลมี Member_ID บอกว่าเป็นของใคร ฐานข้อมูลจึงไม่ยอมให้ลบสมาชิกที่ยังมีบิลอยู่</p>',
     []),
    ('b-select', 'sql', 'SELECT: อ่าน',
     '<p><code>SELECT * FROM Member WHERE Member_ID = \'M001\'</code> = "เอาทุกคอลัมน์ (*) จากตาราง Member เฉพาะแถวที่รหัสเป็น M001"</p>'
     '<p><code>ORDER BY</code> เรียงลำดับ · <code>LIMIT 1</code> เอาแค่แถวแรก</p>',
     [('MemberDao', (22, 22))]),
    ('b-insert', 'sql', 'INSERT: เพิ่ม',
     '<p><code>INSERT INTO ตาราง (คอลัมน์1, คอลัมน์2) VALUES (ค่า1, ค่า2)</code> ลำดับค่าต้องตรงกับลำดับคอลัมน์</p>',
     [('MemberDao', (70, 71))]),
    ('b-update', 'sql', 'UPDATE: แก้',
     '<p><code>UPDATE ตาราง SET คอลัมน์ = ค่าใหม่ WHERE เงื่อนไข</code> <b>ลืม WHERE = แก้ทุกแถวในตาราง</b></p>',
     [('MemberDao', (93, 94))]),
    ('b-delete', 'sql', 'DELETE: ลบ',
     '<p><code>DELETE FROM ตาราง WHERE เงื่อนไข</code> ลืม WHERE = ลบหมดทั้งตาราง</p>',
     [('MemberDao', (115, 115))]),
    ('b-prepared', 'sql', 'PreparedStatement และเครื่องหมาย ?',
     '<p>แทนที่จะเอาข้อความมาต่อกันเป็น SQL เราเขียน <code>?</code> ไว้ แล้วใส่ค่าทีหลังด้วย <code>stmt.setString(1, ค่า)</code></p>'
     '<p>ทำไม? ถ้าต่อข้อความเอง แล้วมีคนพิมพ์ชื่อผู้ใช้ว่า <code>\' OR \'1\'=\'1</code> SQL จะกลายเป็น "เอาทุกบัญชี" แล้วล็อกอินได้โดยไม่รู้รหัส นี่เรียกว่า <b>SQL Injection</b> ใช้ ? แล้วฐานข้อมูลจะถือว่าค่าที่ใส่เป็นข้อความธรรมดาเสมอ</p>'
     '<p>ใช้ <code>executeQuery()</code> กับ SELECT · ใช้ <code>executeUpdate()</code> กับ INSERT / UPDATE / DELETE</p>',
     [('MemberDao', (27, 29))]),
    ('b-resultset', 'sql', 'ResultSet: ผลที่ได้จาก SELECT',
     '<p>ResultSet เหมือนเคอร์เซอร์ชี้ "ก่อนแถวแรก" <code>rs.next()</code> เลื่อนลง 1 แถว คืน true ถ้ามีแถว แล้วอ่านค่าด้วย <code>rs.getString("ชื่อคอลัมน์")</code>, <code>rs.getInt(…)</code>, <code>rs.getDouble(…)</code></p>',
     [('MemberDao', (51, 56)), ('Member', (72, 80))]),
    ('b-join', 'sql', 'JOIN: เอา 2 ตารางมาต่อกัน',
     '<p>ตาราง Bill_Product เก็บแค่ "บิลไหน สั่งเมนูรหัสอะไร กี่จาน" ไม่มีชื่อและราคา ต้อง JOIN กับตาราง Product โดยจับคู่ด้วย Product_ID</p>',
     [('BillProductDao', (126, 128))]),
    ('b-transaction', 'sql', 'Transaction: ทั้งหมดหรือไม่เลย',
     '<p>การจ่ายเงิน 1 ครั้งต้องแก้ 4 ตาราง (บิล สต็อก แต้ม โต๊ะ) ถ้าแก้ไปแล้ว 2 ตารางแล้วพัง ข้อมูลจะเพี้ยน</p>'
     '<p>Transaction แก้ปัญหานี้: <code>setAutoCommit(false)</code> เริ่ม → ทำทุกขั้น → <code>commit()</code> บันทึกพร้อมกัน · ถ้าพัง <code>rollback()</code> ย้อนกลับทั้งหมด</p>',
     [('PosService', (87, 88)), ('PosService', (119, 123))]),
]

BASIC_GROUPS = [('java', 'Java'), ('swing', 'Swing (หน้าจอ)'), ('sql', 'SQL + ฐานข้อมูล')]

# ไฟล์ที่อธิบายทีละบรรทัด เรียงตามบท
LAYER_KEYFILES = [
    ('helper', 'ชั้น helper: ตัวช่วยที่ทุกชั้นใช้', 'ของใช้ร่วมกัน ไม่ใช่ชั้นหลัก DatabaseHelper คือประตูเข้าฐานข้อมูล Session จำว่าใครล็อกอิน', ['DatabaseHelper', 'Session']),
    ('model', 'ชั้น model: กล่องใส่ข้อมูล', '1 คลาส = 1 ตาราง 1 object = 1 แถว มีแค่ช่องเก็บของ getter/setter และ fromRS ไม่มีกฎ ไม่มี SQL ทุก model หน้าตาเหมือน Member ต่างแค่ชื่อช่อง', ['Member']),
    ('dao', 'ชั้น dao: คนเฝ้าคลัง', 'ที่เดียวที่เขียน SQL 1 ตาราง = 1 DAO ทุกตัวใช้แบบ try-catch-finally ของ Lab 8 เหมือน MemberDao ทุกบรรทัด ต่างแค่ชื่อตาราง คอลัมน์ และเมธอดพิเศษ', ['Dao', 'MemberDao']),
    ('service', 'ชั้น service: กฎของร้าน', 'หน้าจอเรียก service เท่านั้น service เช็กกฎ แล้วสั่ง DAO ผิดกฎ = throw ข้อความภาษาไทยให้หน้าจอโชว์', ['MemberService', 'LoginService', 'PosService']),
    ('ui', 'ชั้น ui: หน้าจอ', 'ทุกหน้าลากวางใน NetBeans (ไฟล์ .form) โค้ดที่เราเขียนเองมีแค่ใน constructor กับในเมธอดของปุ่ม หน้า CRUD ทุกหน้าลอกแบบ MemberPanel', ['LoginFrame', 'MainFrame', 'MemberPanel', 'PosPanel', 'ProductItemPanel']),
]
