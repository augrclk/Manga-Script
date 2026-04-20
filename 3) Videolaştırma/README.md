# Çizgi Roman Video Oluşturucu — Kullanım Kılavuzu

Bir klasördeki çizgi roman sayfalarını ve ses dosyalarını otomatik olarak **video**ya dönüştürür.

Her sayfa önce blurlu (bulanık) görünür, ardından paneller sırayla netleşir. Her panel açılırken kendi ses dosyası çalar.

---

## Gereksinimler

### Program
- Python 3
- ffmpeg

**Mac:**
```bash
brew install ffmpeg
```

**Windows:**
```bash
winget install ffmpeg
```

**Ubuntu/Linux:**
```bash
sudo apt install ffmpeg
```

---

## Dosya Yapısı

Tüm dosyalar **aynı klasörde** olmalıdır:

```
klasör/
├── gen_video_v2.py     ← script
├── 1.png               ← 1. sayfa görseli
├── 2.png               ← 2. sayfa görseli
├── 3.png               ← 3. sayfa görseli
├── ...
├── 1.1.wav             ← 1. sayfa, sol panel sesi
├── 1.2.wav             ← 1. sayfa, sağ panel sesi
├── 1.3.wav             ← 1. sayfa, alt panel sesi
├── 2.1.wav             ← 2. sayfa, sol panel sesi
├── 2.2.wav             ← 2. sayfa, sağ panel sesi
├── 2.3.wav             ← 2. sayfa, alt panel sesi
├── ...
├── kalem.wav           ← geçiş efekti (isteğe bağlı)
└── sayfa.wav           ← sayfa çevirme efekti (isteğe bağlı)
```

---

## Görseller

- Format: **PNG**
- Adlandırma: `1.png`, `2.png`, `3.png` ... şeklinde sıralı
- Tüm görseller aynı boyutta olmalıdır
- Script görselleri otomatik ölçekler

### Panel Düzeni

Script şu panel düzenini varsayar:

```
┌─────────────────┬──────────────────┐
│                 │                  │
│   Sol Panel     │   Sağ Panel      │
│   (X.1.wav)     │   (X.2.wav)      │
│                 │                  │
├─────────────────┴──────────────────┤
│                                    │
│         Alt Panel (X.3.wav)        │
│                                    │
└────────────────────────────────────┘
```

---

## Ses Dosyaları

- Format: **WAV** (MP3 de çalışır ama WAV önerilir)
- Her panel için ayrı ses dosyası gerekir
- **Ses süresi = o panelin ekranda kalma süresi**
  - `1.1.wav` 5 saniyeyse sol panel 5 saniye görünür, biter, sağ panel açılır

### Adlandırma Kuralı

```
SAYFA_NO.PANEL_NO.wav
```

| Dosya | Anlamı |
|-------|--------|
| `1.1.wav` | 1. sayfa, sol panel |
| `1.2.wav` | 1. sayfa, sağ panel |
| `1.3.wav` | 1. sayfa, alt panel |
| `2.1.wav` | 2. sayfa, sol panel |
| `5.3.wav` | 5. sayfa, alt panel |

---

## Efekt Dosyaları (İsteğe Bağlı)

| Dosya | Ne zaman çalar |
|-------|----------------|
| `kalem.wav` | Her panel açılmadan hemen önce |
| `sayfa.wav` | Her sayfa başında (blurlu görünürken) |

> Efekt sesleri panel sesleriyle **üst üste** çalar, zaman kaybettirmez.
> Bu dosyalar klasörde yoksa script yine çalışır.

---

## Kullanım

```bash
cd /klasörün/yolu
python3 gen_video_v2.py
```

Script çalışırken terminalde ilerlemeyi görebilirsin:

```
Boyut: 5504x3072  |  7 sayfa
  Sayfa 1: 1.1.wav=3.72s | 1.2.wav=6.94s | 1.3.wav=9.95s
  ...

Sayfa 1 render (20.61s)...
Sayfa 2 render (19.97s)...
...
Concat ediliyor...
Ses karistiriliyor...
Son birlesim...

OK: cizgi_roman_v2.mp4  (142.3 MB)
```

---

## Çıktı

Aynı klasörde `cizgi_roman_v2.mp4` oluşur.

Farklı bir isim istersen scriptin üstündeki şu satırı değiştir:

```python
OUTPUT = "cizgi_roman_v2.mp4"
```

---

## Ayarlar

Scriptin en üstünde değiştirebileceğin ayarlar:

```python
SABLON_DUR = 1.0   # Sayfa başında blurlu bekleme süresi (saniye)
FADE_DUR   = 0.5   # Blur → keskin geçiş süresi (saniye)
BLUR_STR   = 15    # Blur şiddeti (yükseldikçe daha bulanık)
FPS        = 30    # Video kare hızı
```

---

## Sık Karşılaşılan Hatalar

**`Eksik: 2.3.wav`**
→ Ses dosyası eksik veya yanlış adlandırılmış.

**`Hic sayfa bulunamadi`**
→ Doğru klasörde çalıştırdığından emin ol: `cd klasör/yolu`

**`ffmpeg: command not found`**
→ ffmpeg yüklü değil. Yukarıdaki kurulum adımlarını uygula.