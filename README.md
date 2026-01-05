# 🎓 Okul Öncesi Eğitim İçin Oyunlaştırılmış Simülasyon Platformu

## 👋 Giriş ve Hakkımda
Merhaba! Ben **Kenan Birlik**. Ankara Üniversitesi, Bilgisayar ve Öğretim Teknolojileri Öğretmenliği (BÖTE) bölümü öğrencisiyim. Bu proje, Nesne Yönelimli Programlama (BOZ213) dersi kapsamında, okul öncesi dönemdeki (3-6 yaş) çocukların temel kavramları eğlenerek öğrenmesi amacıyla geliştirdiğim kapsamlı bir simülasyon çalışmasıdır.

Teknolojinin eğitimdeki yerini pekiştirmek amacıyla, renkler, şekiller, sayılar ve harfler gibi soyut kavramların oyunlaştırma (gamification) teknikleriyle somutlaştırılmasını ve çocukların interaktif bir ortamda gelişimlerini desteklemeyi hedefledim.

## 📝 Proje Özeti
"Okul Öncesi Eğitim Simülasyonu", Python programlama dili ve Pygame kütüphanesi temel alınarak geliştirilmiş, tamamen modüler yapıda tasarlanmış bir eğitim setidir. Proje, çocukların bilişsel ve motor becerilerini geliştirmeye odaklanan 10 farklı interaktif modülden oluşmaktadır.

## 🎮 Modüller ve Eğitimsel Kazanımlar
Oyunun her bir modülü, okul öncesi müfredatına uygun belirli bir beceriyi kazandırmak üzerine kurgulanmıştır:

| Oyun Modülü | Odaklanılan Beceri / Kazanım |
| :--- | :--- |
| **Meyve Toplama** | Sayma Becerisi ve Temel Matematik |
| **Renk Eşleştirme** | Görsel Algı ve Sürükle-Bırak (Motor Beceri) |
| **Sesli Harfler** | Dil Gelişimi ve Nesne Tanıma |
| **Şekil Bulma** | Geometrik Algı ve Gölge Eşleştirme |
| **Büyük-Küçük** | Boyut Algısı ve Sıralama Mantığı |
| **Balık Sayma** | Hareketli Nesne Takibi ve Dikkat |
| **Nesne Bulma** | İşitsel Yönerge Takibi ve Odaklanma |
| **Hafıza Oyunu** | Görsel Bellek Egzersizi |
| **Puzzle** | Parça-Bütün İlişkisi Kurma |
| **Hedef Bul (Labirent)** | Yön Kavramı ve Stratejik Düşünme |

## 🛠️ Teknik Mimari ve Özellikler
* **Programlama Dili:** Python 3.x
* **Kütüphaneler:** Pygame, gTTS (Google Text-to-Speech)
* **OOP Mimari:** Tüm modüller `BaseScene` sınıfından türetilerek (Inheritance) %100 modüler ve genişletilebilir bir yapıda tasarlanmıştır.
* **Ses Teknolojisi:** Hamle sayısı ve başarı durumu **gTTS** teknolojisi ile dinamik olarak seslendirilmektedir.
* **Veri Yönetimi:** Kullanıcı tercihleri ve ilerlemesi **JSON** formatında kalıcı olarak saklanır.
* **Algoritmalar:**
    * **Safe-Zone:** Labirent modülünde çözümün matematiksel olarak garanti edilmesi.
    * **Subsurface Motoru:** Puzzle modülünde görsellerin kod tabanlı dinamik parçalanması.

## 🚀 Kurulum ve Başlatma

## 🚀 Kurulum ve Başlatma

Projeyi bilgisayarınıza indirmek ve oyunu başlatmak için aşağıdaki komutların tamamını kopyalayıp terminale yapıştırmanız yeterlidir:

```bash
git clone [https://github.com/kenanbirlik/Okul-Oncesi-Oyun-Simulasyonu.git](https://github.com/kenanbirlik/Okul-Oncesi-Oyun-Simulasyonu.git)
cd Okul-Oncesi-Oyun-Simulasyonu
pip install -r requirements.txt
python main.py

Geliştirici: Kenan Birlik

Kurum: Ankara Üniversitesi, Bilgisayar ve Öğretim Teknolojileri Eğitimi (BÖTE) Bölümü
