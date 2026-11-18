# dictjeen — เว็บไซต์ของแอป "ดิกจีน"

เว็บไซต์ static (HTML + CSS) สำหรับ GitHub Pages: หน้าแรก, ช่วยเหลือ (Support URL), นโยบายความเป็นส่วนตัว, เงื่อนไขการใช้งาน, ข้อมูลและลิขสิทธิ์

## แก้ไขเนื้อหา
- เอกสาร: `content/privacy.md`, `content/terms.md`, `content/credits.md` (ต้นฉบับอยู่ใน repo แอปที่ `docs/legal/`)
- หน้าแรก / ช่วยเหลือ: `content/index.body.html`, `content/support.body.html` (บรรทัดแรกของไฟล์ `.meta` = title, บรรทัดสอง = description)
- แล้วรัน `python3 build.py` เพื่อสร้างไฟล์ `.html` ใหม่ แล้ว commit

## เผยแพร่ (GitHub Pages)
Settings → Pages → Source: Deploy from a branch → `main` / `/ (root)`
URL: https://thiravadhano.github.io/dictjeen/
- Privacy Policy URL: https://thiravadhano.github.io/dictjeen/privacy.html
- Terms: https://thiravadhano.github.io/dictjeen/terms.html
- Support URL: https://thiravadhano.github.io/dictjeen/support.html
