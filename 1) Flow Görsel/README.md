# 🤖 Prompt Auto-Sender — AppleScript Otomasyon Aracı

Hazırlanan prompt dosyalarını otomatik olarak web arayüzüne gönderen AppleScript tabanlı otomasyon sistemi.

---

## 📁 Dosyalar

| Dosya | Açıklama |
|---|---|
| `manga_sender.applescript` | JSON veya Layout TXT formatı için sender |
| `simple_sender.applescript` | "Prompt 1, Prompt 2..." formatı için sender |
| `mouse_click.py` | Tıklama işlemlerini yapan Python yardımcısı |

---

## ⚙️ Gereksinimler

### macOS İzinleri
Sistem Tercihleri → Gizlilik ve Güvenlik → **Erişilebilirlik** bölümüne:
- Terminal
- Script Editor

ikisini de ekle ve aktif et.

### Python Kurulumu
```bash
pip3 install pyautogui
```

---

## 🚀 Kullanım

### 1. Script Editor ile Çalıştırma
1. `.applescript` dosyasını **Script Editor** ile aç
2. ▶️ Çalıştır butonuna bas
3. Önce `mouse_click.py` dosyasını seç
4. Sonra prompt dosyasını seç (`.txt` veya `.json`)
5. Kaç prompt bulunduğunu gösteren dialog çıkar → **Başlat**'a bas
6. **10 saniye** içinde hedef web sitesine geç
7. Script otomatik başlar

### 2. Terminal ile Çalıştırma
```bash
osascript manga_sender.applescript
```

---

## 📄 Desteklenen Prompt Formatları

### Format 1 — Düz TXT (`simple_sender.applescript`)
```
Prompt 1
Manga style composition...

Prompt 2
Another prompt here...
```

### Format 2 — Layout TXT (`manga_sender.applescript`)
```
Layout 1
Flow Master Image Prompt (EN):
Manga style composition...

Layout 2
...
```

### Format 3 — JSON (`manga_sender.applescript`)
```json
{
  "Image_Prompts": {
    "Prompt_1_Layout_1": "Manga style...",
    "Prompt_2_Layout_2": "..."
  }
}
```

---

## ⏱️ Zamanlama

| Adım | Süre |
|---|---|
| Başlatma öncesi bekleme | 10 saniye |
| Tıklamalar arası bekleme | 1.5 saniye |
| Prompt gönderimi sonrası bekleme | 40 saniye |

> 40 saniyelik bekleme, web arayüzünün görseli üretmesi için ayrılmıştır. Üretim süresi farklıysa script içinde `delay 40` satırını güncelle.

---

## 🖱️ Tıklama Koordinatları

Script şu koordinatlara tıklar (ekran çözünürlüğüne göre değişebilir):

| Adım | Koordinat | Açıklama |
|---|---|---|
| 1 | `582, 1054` | Ana buton |
| 2 | `710, 430` | Dosya adı alanı |
| 3 | `650, 1020` | Prompt giriş alanı |

> Koordinatlar senin ekran düzenine göre ayarlanmıştır. Farklı bir monitör veya çözünürlük kullanıyorsan güncellemen gerekebilir.

---

## 🔧 Sorun Giderme

**"System Events erişim izni yok" hatası**
→ Sistem Tercihleri → Erişilebilirlik → Terminal'e izin ver

**Script tıklamıyor**
→ `mouse_click.py` seçildiğinden emin ol
→ `pip3 install pyautogui` çalıştır

**Prompt bulunamadı**
→ TXT dosyasının `Prompt 1` veya `Layout 1` ile başladığını kontrol et
→ Dosya encoding'i UTF-8 olmalı

**40 saniye yetmiyor**
→ Script içinde `delay 40` satırını `delay 60` gibi artır

---

## 📝 Notlar

- Her çalıştırmada dosya seçici açılır, farklı dosya kullanabilirsin
- Script tamamlandığında kaç prompt gönderildiğini bildiren dialog çıkar
- İptal etmek için dialog'da **İptal**'e bas veya `Cmd + .` kullan