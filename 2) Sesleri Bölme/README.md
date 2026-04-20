# 🎙️ AI Destekli Hassas Ses Bölücü (Whisper & Forced Alignment)

Bu proje, uzun bir ses kaydını (`.wav`), önceden yazılmış bir metin transkriptindeki (`.txt`) diyalog sırasına göre otomatik, kayıpsız ve milisaniye hassasiyetinde parçalara bölen bir otomasyon aracıdır.

## 🧠 Arkasındaki Zeka: Nasıl Çalışıyor?

Sistem, sesi nefes aralıklarına veya tahmini sürelere göre **bölmez**. Bunun yerine yapay zeka alanındaki en gelişmiş metotlardan biri olan **Text-to-Text Forced Alignment (Zorunlu Metin Hizalama)** tekniğini kullanır:

1. **Kelime Haritalama:** Sistem önce `metin.txt` dosyanızı okur. Duygu etiketlerini (`[cheerful]` vb.) ve noktalama işaretlerini temizleyerek arayacağı saf kelimelerin bir listesini çıkarır.
2. **Word-Level Dinleme (Whisper AI):** OpenAI'ın Whisper (Base) modeli, ses dosyasını dinler ve duyduğu her kelimenin hangi milisaniyede başlayıp bittiğini çıkarır.
3. **Birebir Eşleştirme (`difflib`):** Sizin yazdığınız metin ile yapay zekanın duyduğu metin üst üste konur. Sistem, transkriptteki her cümlenin seste tam olarak nerede bittiğini bulur.
4. **Cerrahi Kesim (Midpoint Cutting):** Son kelimenin yutulmasını veya bir sonraki konuşmacının nefesinin sızmasını engellemek için, iki cümle arasındaki sessizlik payı bulunur ve ses tam ortadan jilet gibi kesilir. Sıfır örtüşme (zero-overlap) garantisi sağlanır.

---

## 🛠️ Kurulum Gereksinimleri

Sistemin Mac üzerinde çalışması için Terminal üzerinden aşağıdaki bağımlılıkların kurulması gerekir:

* **Ses İşleme Motoru:**
    ```bash
    brew install ffmpeg
    ```
* **Yapay Zeka ve Python Kütüphaneleri:**
    ```bash
    pip install openai-whisper pydub
    ```

---

## 📂 Dosya Düzeni

İşlemi başlatmak için çalışma klasörünüzün içinde şu üç dosyanın yan yana bulunması yeterlidir:

1.  `a.wav` (Orijinal, kesilmemiş ses dosyası)
2.  `metin.txt` (Konuşma metinlerinin bulunduğu dosya)
3.  `otomatik_kesici.py` (Çalıştırıcı Python betiği)

---

## 📝 Transkript Formatı (`metin.txt`)

Sistem, konuşmaları otomatik algılayıp `1.1.wav`, `1.2.wav`, `1.3.wav`, `2.1.wav` şeklinde sıralı bir isimlendirme yapar. Bunun çalışması için metin dosyanızın şu yapıda olması gerekir:

```text
Speaker 1: [cheerful] "Esselamü aleyküm çocuklar! Beni tanıyor musunuz? Ben sıradan bir deve değilim!"
Speaker 2: [proud] "Ben, Allah’ın mucizesi olan Salih Peygamber’in devesiyim!"
Speaker 1: [narrating] "Çooook uzun zaman önce, Semud Kavmi diye inatçı bir topluluk vardı."