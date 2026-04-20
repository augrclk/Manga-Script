import whisper
import re
import os
import difflib
from pydub import AudioSegment

def metni_ayristir_kelimeler(transkript_yolu):
    with open(transkript_yolu, "r", encoding="utf-8") as f:
        metin = f.read()
        
    # "Speaker 1:", "Speaker 2:" gibi kısımlardan metni parçalara ayırır
    bloklar = re.split(r'Speaker \d+:', metin)
    
    hedef_kelime_listesi = []
    dosya_sirasi = []
    
    # 1.1, 1.2, 1.3 sayacını başlat
    ana_grup = 1
    alt_grup = 1

    for icerik in bloklar:
        if not icerik.strip(): 
            continue # Boşlukları atla
            
        # Dosya adını otomatik oluştur
        dosya_adi = f"{ana_grup}.{alt_grup}.wav"
        dosya_sirasi.append(dosya_adi)
        
        # [cheerful] gibi etiketleri ve noktalama işaretlerini tamamen temizle
        temiz_metin = re.sub(r'\[.*?\]', '', icerik)
        temiz_metin = re.sub(r'[^\w\s]', '', temiz_metin).lower().split()
        
        for kelime in temiz_metin:
            hedef_kelime_listesi.append({
                "word": kelime,
                "file": dosya_adi
            })
            
        # Sayacı güncelle (Her 3 parçada bir ana sayıyı artır)
        if alt_grup == 3:
            alt_grup = 1
            ana_grup += 1
        else:
            alt_grup += 1
            
    return hedef_kelime_listesi, dosya_sirasi

def tam_metin_hizalama(ses_yolu, transkript_yolu):
    if not os.path.exists(ses_yolu) or not os.path.exists(transkript_yolu):
        print("HATA: a.wav veya metin.txt bulunamadı!")
        return

    print("1. Yeni format okunuyor ve otomatik isimlendirme yapılıyor...")
    hedef_kelimeler, dosya_sirasi = metni_ayristir_kelimeler(transkript_yolu)
    
    print("2. Whisper sesi kelime kelime dinliyor (Lütfen bekleyin)...")
    model = whisper.load_model("base") 
    sonuc = model.transcribe(ses_yolu, word_timestamps=True)
    
    whisper_kelimeler = []
    for segment in sonuc["segments"]:
        if "words" in segment:
            for word_data in segment["words"]:
                w_clean = re.sub(r'[^\w\s]', '', word_data["word"]).lower().strip()
                if w_clean:
                    whisper_kelimeler.append({
                        "word": w_clean,
                        "start": word_data["start"],
                        "end": word_data["end"]
                    })
    
    print("3. Metin ile ses birebir eşleştiriliyor (Forced Alignment)...")
    w_words = [w["word"] for w in whisper_kelimeler]
    t_words = [t["word"] for t in hedef_kelimeler]
    
    matcher = difflib.SequenceMatcher(None, w_words, t_words)
    file_matches = {dosya: [] for dosya in dosya_sirasi}
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag in ('equal', 'replace'):
            match_length = min(i2 - i1, j2 - j1)
            for k in range(match_length):
                w_idx = i1 + k
                t_idx = j1 + k
                dosya = hedef_kelimeler[t_idx]["file"]
                file_matches[dosya].append(whisper_kelimeler[w_idx])
                
    raw_times = {}
    for dosya in dosya_sirasi:
        eslesenler = file_matches[dosya]
        if not eslesenler:
            print(f"UYARI: {dosya} için eşleşen kelime bulunamadı, boş geçiliyor.")
            raw_times[dosya] = {"start": 0, "end": 0}
            continue
            
        raw_times[dosya] = {
            "start": eslesenler[0]["start"],
            "end": eslesenler[-1]["end"] 
        }
        
    print("4. Kesim noktaları sıfır kayıpla optimize ediliyor...")
    final_times = {}
    for i, dosya in enumerate(dosya_sirasi):
        if i == 0:
            start_sn = max(0, raw_times[dosya]["start"] - 0.2)
        else:
            onceki_end = raw_times[dosya_sirasi[i-1]]["end"]
            suanki_start = raw_times[dosya]["start"]
            start_sn = (onceki_end + suanki_start) / 2
            
        if i == len(dosya_sirasi) - 1:
            end_sn = raw_times[dosya]["end"] + 0.3
        else:
            suanki_end = raw_times[dosya]["end"]
            sonraki_start = raw_times[dosya_sirasi[i+1]]["start"]
            end_sn = (suanki_end + sonraki_start) / 2
            
        final_times[dosya] = {"start_ms": int(start_sn * 1000), "end_ms": int(end_sn * 1000)}

    print("5. Ses dosyası bölünüyor...")
    ses_dosyasi = AudioSegment.from_file(ses_yolu)
    
    for dosya in dosya_sirasi:
        ms_bas = final_times[dosya]["start_ms"]
        ms_bit = final_times[dosya]["end_ms"]
        
        if ms_bas >= ms_bit: 
            ms_bit = ms_bas + 500 
            
        parca = ses_dosyasi[ms_bas:ms_bit]
        parca.export(dosya, format="wav")
        print(f"✅ {dosya} başarıyla kesildi! ({ms_bas/1000:.2f}s -> {ms_bit/1000:.2f}s)")
        
    print("\n🚀 İŞLEM TAMAM!")

# --- KULLANIM ---
orijinal_ses = "a.wav"
transkript_dosyasi = "metin.txt"

tam_metin_hizalama(orijinal_ses, transkript_dosyasi)