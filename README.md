# 🎓 Okul Öncesi Eğitim İçin Oyunlaştırılmış Simülasyon Platformu

Bu proje, **Ankara Üniversitesi BÖTE Bölümü, Nesne Yönelimli Programlama (BOZ213)** dersi kapsamında geliştirilmiştir.

3-6 yaş grubu çocukların temel kavramları (renkler, şekiller, sayılar, harfler) eğlenerek öğrenmesi için tasarlanmış, **Python** ve **Pygame** tabanlı modüler bir eğitim simülasyonudur.

---

## 🚀 Öne Çıkan Özellikler

* **🏗️ OOP Mimarisi:** Tüm oyun modülleri `BaseScene` sınıfından türetilerek (Inheritance) %100 modüler ve genişletilebilir bir yapıda tasarlanmıştır.
* **🗣️ Dinamik Seslendirme:** `gTTS` (Google Text-to-Speech) teknolojisi ile çocuğun hamle sayısı ve başarı durumu anlık olarak seslendirilir.
* **🧩 Akıllı Algoritmalar:**
    * **Labirent Modülü:** Çözümü matematiksel olarak garanti eden "Safe-Zone" engel yerleşimi.
    * **Puzzle Modülü:** Görselleri kod tabanlı dinamik olarak parçalayan `subsurface` motoru.
* **💾 Veri Yönetimi:** Kullanıcı tercihleri ve ilerlemesi JSON formatında kalıcı olarak saklanır.

---

## 🎮 Oyun Modülleri (10 Bölüm)

1.  **Meyve Toplama:** Sayma becerisi.
2.  **Renk Eşleştirme:** Görsel algı ve sürükle-bırak motoru.
3.  **Sesli Harfler:** Sepet ile doğru nesneleri yakalama.
4.  **Şekil Bulma:** Gölge eşleştirme ve "Mıknatıs" (Magnet) etkisi.
5.  **Büyük-Küçük:** Boyut algısı ve sıralama.
6.  **Balık Sayma:** Hareketli nesne takibi.
7.  **Nesne Bulma:** İşitsel yönerge takibi.
8.  **Hafıza Oyunu:** Görsel bellek egzersizi.
9.  **Puzzle:** Parça-bütün ilişkisi.
10. **Hedef Bul (Labirent):** Yön kavramı ve strateji.

---

## 🛠️ Kurulum ve Çalıştırma

Projeyi bilgisayarınızda çalıştırmak için sırasıyla şu adımları yapın:

1. **Projeyi indirin:**
   ```bash
   git clone [https://github.com/kenanbirlik/Okul-Oncesi-Oyun-Simulasyonu.git](https://github.com/kenanbirlik/Okul-Oncesi-Oyun-Simulasyonu.git)
   Oyunun klasörüne girin:

Bash

cd Okul-Oncesi-Oyun-Simulasyonu
Gerekli kütüphaneleri yükleyin:

Bash

pip install -r requirements.txt
Oyunu başlatın:

Bash

python main.py

---
**Geliştirici:** Kenan Birlik - Ankara Üniversitesi BÖTE
