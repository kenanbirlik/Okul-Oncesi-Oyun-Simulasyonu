# generate_final_sounds.py
from gtts import gTTS
import os
import time

def create_sound(text, filename):
    try:
        tts = gTTS(text=text, lang='tr', slow=False)
        tts.save(filename)
        print(f"✓ {filename.ljust(25)} -> '{text}'")
        return True
    except Exception as e:
        print(f"✗ {filename}: {e}")
        return False

def main():
    print("🔊 OYUN SESLERİ OLUŞTURULUYOR (FİNAL VERSİYON)...")
    sounds_dir = os.path.join("assets", "sounds")
    os.makedirs(sounds_dir, exist_ok=True)
    
    final_sounds = {
        # GENEL
        'bravo.wav': 'Harikasın!.',
        'bravo_short.wav': 'Bravo!',
        
        # BÖLÜM 1 (MEYVE)
        'level1.wav': 'Sepete 5 tane elma topla.',
        'level1_part2.wav': 'Harika! Şimdi de sepete iki tane muz ekle.',
        
        # BÖLÜM 2, 3, 4
        'level2.wav': 'Renkleri eşleştirelim. Aynı renkteki nesneleri kovalarına sürükle.',
        'level3.wav': 'Sadece sesli harfleri sepete topla.',
        'level4.wav': 'Şekilleri gölgeleriyle eşleştir.',
        'level4_daire.wav': 'Daire', 
        
        # BÖLÜM 5 (SIRALAMA)
        'level5_1.wav': 'Ayıları, en küçükten en büyüğe doğru sıralayalım.',
        'level5_2.wav': 'Harikasın! Şimdi de, büyükten küçüğe doğru sıralayalım.',
        
        # BÖLÜM 6 (BALIK - 3 AŞAMA)
        'l6_total.wav': 'Bakalım denizde toplam kaç balık var? Say ve kutuya yaz.',
        'l6_red.wav': 'Şimdi sadece kırmızı balıkları sayalım.',
        'l6_yellow.wav': 'Şimdi de sadece sarı balıkları sayalım.',
        
        # BÖLÜM 7 (NESNE BULMA)
        'bul_ELMA.wav': 'Hangisi Elma? Göster bakalım.',
        'bul_MUZ.wav': 'Hangisi Muz? Bulabilir misin?',
        'bul_AYI.wav': 'Hangisi Ayı? Tıkla bakalım.',
        'bul_ÜZÜM.wav': 'Hangisi Üzüm?',
        'bul_PORTAKAL.wav': 'Hangisi Portakal?',
        'bul_ÇİÇEK.wav': 'Hangisi Çiçek?',
        'bul_KOLTUK.wav': 'Hangisi Koltuk?',
        'bul_KIRMIZI BALIK.wav': 'Hangisi Kırmızı Balık?',
        'bul_SARI BALIK.wav': 'Hangisi Sarı Balık?',
        'bul_SEPET.wav': 'Hangisi Sepet?',
        'bul_KAZAK.wav': 'Hangisi Kazak?',
        'bul_PANTOLON.wav': 'Hangisi Pantolon?',
        'level7.wav': 'Söylediğim nesneyi bulabilir misin?',
        
        # BÖLÜM 8, 9, 10
        'level8.wav': 'Hafıza kartları karışmış! Eşlerini bulalım.',
        'level9.wav': 'Bu resim parçalanmış. Hadi parçaları yerine koyup resmi tamamlayalım.',
        'level10.wav': 'Labirenttesin! Ok tuşlarıyla kırmızı topa ulaş.'
    }
    
    # Eski gereksiz dosyaları temizle (transition.wav gibi)
    if os.path.exists(os.path.join(sounds_dir, "transition.wav")):
        os.remove(os.path.join(sounds_dir, "transition.wav"))

    count = 0
    for filename, text in final_sounds.items():
        filepath = os.path.join(sounds_dir, filename)
        if os.path.exists(filepath): os.remove(filepath)
        
        if create_sound(text, filepath):
            count += 1
            time.sleep(1.2)
            
    print(f"✅ {count} adet ses dosyası hazır.")

if __name__ == "__main__":
    main()