# โปรเจกต์โบนัสสุกี้: เอกสารและหน้าเว็บของทีม

เอกสารประกอบการทำระบบ POS ร้านโบนัสสุกี้ด้วย Java Swing + SQLite
รวมข้อมูลจาก 3 แหล่ง ได้แก่ Figma (หน้าจอ), Google Sheet แท็บ plan (งานและกำหนดส่ง) และรูปเล่มฐานข้อมูล (15 ตาราง)

## มีอะไรบ้าง

| ไฟล์ | คืออะไร |
|---|---|
| `docs/คู่มือรวมโปรเจกต์-BonusSuki-JavaSwing.html` | คู่มือ 7 พาร์ท: งานของแต่ละคน, กติกาตั้งชื่อ, ฐานข้อมูล, ชื่อตัวแปรทุกตาราง, โค้ดแม่แบบ, หน้าจอจาก Figma, กฎร้าน |
| `web/โปรเจกต์โบนัสสุกี้.html` | หน้าเดียว 3 แท็บ: ภาพรวมทีม · ไกด์ทำงานทีละขั้นพร้อม checkpoint · คู่มือโปรเจกต์ |
| `sql/bonus_suki_sqlite.sql` | CREATE TABLE สำหรับ SQLite (15 ตารางตามรูปเล่ม + User_Account, Check_Stock, Check_Stock_Detail) |
| `sql/bonus_suki_create_tables.sql` | CREATE TABLE ต้นฉบับ (MySQL) |
| `sql/bonus_suki_insert_mock_data.sql` | ข้อมูลตัวอย่าง |

## เปิดดูยังไง

- **คู่มือ:** ดาวน์โหลดไฟล์ HTML แล้วดับเบิลคลิกเปิดในเบราว์เซอร์ (GitHub ไม่แสดงไฟล์ HTML เป็นหน้าเว็บ)
- **หน้าโปรเจกต์:** ภาพรวมทีม การติ๊ก checkpoint และการเขียน % ลงชีท ทำงานได้เฉพาะตอนเปิดผ่านลิงก์ใน Claude ที่ทีมแชร์กัน ถ้าเปิดไฟล์นี้ตรง ๆ จะอ่านไกด์และคู่มือได้อย่างเดียว

## สร้างฐานข้อมูล bonus_suki.db

1. สร้างไฟล์ `bonus_suki.db` ที่รากโปรเจกต์ Java ด้วย Letos หรือ DB Browser for SQLite
2. รัน `sql/bonus_suki_sqlite.sql` ส่วน CREATE TABLE
3. เปิด `sql/bonus_suki_insert_mock_data.sql` ลบบรรทัด `USE bonus_suki;` แล้วรัน
4. รัน INSERT บัญชีทดสอบท้าย `bonus_suki_sqlite.sql`
5. ตรวจ: `PRAGMA foreign_key_check;` ต้องไม่มีผลลัพธ์ และ `SELECT COUNT(*) FROM Bill;` ได้ 6

ไฟล์ `.db` ไม่ถูก commit (อยู่ใน `.gitignore`) ให้สร้างจากสคริปต์ใน `sql/` ทุกครั้ง

## เว็บบน Cloudflare Pages

โฟลเดอร์ `site/` คือเว็บที่ deploy ขึ้น Cloudflare Pages (`index.html` = หน้าโปรเจกต์, `manual.html` = คู่มือ)
โปรเจกต์ `bonus-suki` บน Cloudflare เป็นแบบอัปโหลดตรง (ไม่ได้ผูก Git) การ push ขึ้น `main` ไม่ทำให้เว็บอัปเดต ต้อง deploy เอง:

```
npx wrangler pages deploy site --project-name bonus-suki --branch main
```

เว็บบน Cloudflare เป็นเวอร์ชันอ่านอย่างเดียว ภาพรวมทีม การติ๊ก checkpoint และการบันทึก % ลงชีท ใช้ได้ในหน้าโปรเจกต์บน Claude เท่านั้น
