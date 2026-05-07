# Metro Passenger Counting System

Bu proje, metro veya toplu taşıma giriş-çıkış görüntülerinde yolcu hareketlerini tespit etmek, takip etmek ve yön bazlı saymak için hazırlanmış Python tabanlı bir bilgisayarlı görü uygulamasıdır.

Projenin ana fikri; video akışından kişi ve kapı tespiti yapmak, tespit edilen kişileri takip etmek ve kapı bölgesi içinde hareket yönüne göre **binen** ve **inen** yolcu sayılarını hesaplamaktır.

---

## Proje Amacı

Toplu taşıma sistemlerinde yolcu yoğunluğunu ölçmek; kapasite planlama, güvenlik, operasyonel verimlilik ve istasyon yönetimi açısından önemlidir. Bu proje, kamera görüntüsü üzerinden otomatik yolcu sayımı yapmaya yönelik temel bir görüntü işleme ve nesne takip mimarisi sunar.

Sistem genel olarak şu sorulara cevap vermeyi hedefler:

- Videoda kişi tespiti yapılabiliyor mu?
- Kapı bölgesi belirlenebiliyor mu?
- Tespit edilen kişiler takip edilebiliyor mu?
- Kişinin hareket yönüne göre binen/inen ayrımı yapılabiliyor mu?
- Yolcu sayımı frame bazlı olarak güncellenebiliyor mu?

---

## Repository Yapısı

Mevcut proje yapısı aşağıdaki gibidir:

```text
metropassenger/
│
├── detectors/
│   ├── __init__.py
│   └── yolo_detector.py
│
├── logic/
│   ├── __init__.py
│   └── direction_counter.py
│
├── trackers/
│   ├── __init__.py
│   └── deepsort_tracker.py
│
├── config.yaml
└── main.py
```

---

## Klasörlerin Görevleri

### `detectors/`

Bu klasör, nesne tespiti için kullanılan modülleri içerir.

#### `yolo_detector.py`

`YOLODetector` sınıfı, Ultralytics YOLO modelini kullanarak video frame'leri üzerinde tespit yapar.

Bu sınıfın temel görevleri:

- YOLO modelini yüklemek
- Frame üzerinde inference çalıştırmak
- Güven skoruna göre düşük kaliteli tespitleri elemek
- `person` sınıfını yolcu tespiti için kullanmak
- `door` sınıfını kapı bölgesi tespiti için kullanmak
- Kişi tespitlerini tracker formatına uygun hale getirmek

Kodda hedef sınıflar şu şekilde belirlenmiştir:

```python
self.target_classes = ['person', 'door']
```

Bu yapı, sistemin yalnızca insanları değil, kapı bölgesini de algılayacak şekilde tasarlandığını gösterir.

---

### `trackers/`

Bu klasör, tespit edilen nesnelerin frame'ler arasında takip edilmesi için ayrılmıştır.

#### `deepsort_tracker.py`

Bu dosyada `DeepSortTracker` sınıfı yer almaktadır. Mevcut haliyle bu sınıf bir placeholder durumundadır:

```python
class DeepSortTracker:
    def update(self, detections, frame):
        return []
```

Bu yapı, proje mimarisinde tracker katmanının planlandığını ancak henüz tam olarak geliştirilmediğini gösterir.

İdeal kullanımda bu sınıfın görevi:

- YOLO'dan gelen kişi tespitlerini almak
- Her kişiye kalıcı bir track ID atamak
- Frame'ler arasında aynı kişiyi takip etmek
- Takip edilen kişileri direction counter modülüne aktarmak

Bu katman tamamlandığında sistem, tek frame'lik tespit yerine zaman içinde sürekliliği olan kişi takibi yapabilir.

---

### `logic/`

Bu klasör, sayım mantığını ve yön tespitini içerir.

#### `direction_counter.py`

`DirectionCounter` sınıfı, takip edilen kişilerin kapı bölgesindeki hareket yönünü analiz eder.

Bu sınıfın temel görevleri:

- Kapı bölgesi içinde hareket eden kişileri izlemek
- Kişinin önceki ve mevcut konumunu karşılaştırmak
- Giriş ve çıkış çizgilerinin geçilip geçilmediğini kontrol etmek
- Hareket yönüne göre yolcuyu `binen` veya `inen` olarak saymak
- Aynı kişinin kısa sürede tekrar sayılmasını engellemek için cooldown mekanizması kullanmak

Sayım çıktısı şu iki değerden oluşur:

```python
binen_count, inen_count
```

Burada:

- `binen_count`: Araca/metroya binen yolcu sayısı
- `inen_count`: Araçtan/metrodan inen yolcu sayısı

---

## Sistem Akışı

Projenin hedeflenen çalışma akışı aşağıdaki gibidir:

```text
Video Input
    ↓
Frame Okuma
    ↓
YOLO ile Person/Door Detection
    ↓
DeepSORT ile Object Tracking
    ↓
Kapı ROI ve Yön Çizgileri Üzerinden Hareket Analizi
    ↓
Binen / İnen Yolcu Sayımı
    ↓
Sonuçların Görselleştirilmesi
```

---

## Kullanılan Teknolojiler

Projede kullanılan veya kullanılması planlanan temel teknolojiler:

- Python
- OpenCV
- Ultralytics YOLO
- NumPy
- DeepSORT
- YAML tabanlı konfigürasyon

---

## Konfigürasyon

Projede `config.yaml` dosyası bulunmaktadır. Mevcut içerikte video yolu, cooldown frame sayısı, model yolu ve confidence threshold gibi ayarlar yer almaktadır.

Daha okunabilir ve standart YAML formatı için dosya aşağıdaki yapıya getirilebilir:

```yaml
video_settings:
  path: "metro_sample.mp4"

counter_settings:
  cooldown_frames: 45

detector_settings:
  model_path: "yolov8n_person_door.pt"
  confidence_threshold: 0.3
```

Bu ayarlar şu amaçlarla kullanılır:

| Ayar | Açıklama |
|---|---|
| `video_settings.path` | İşlenecek video dosyasının yolu |
| `counter_settings.cooldown_frames` | Aynı kişinin tekrar sayılmasını engelleyen bekleme süresi |
| `detector_settings.model_path` | Kullanılacak YOLO model dosyası |
| `detector_settings.confidence_threshold` | Minimum tespit güven skoru |

---

## Kurulum

Projeyi lokal ortamda çalıştırmak için önce repository'yi klonlayın:

```bash
git clone https://github.com/ElanurBUZLUK/metropassenger.git
cd metropassenger
```

Sanal ortam oluşturmanız önerilir:

```bash
python -m venv venv
```

Windows için:

```bash
venv\Scripts\activate
```

Linux/macOS için:

```bash
source venv/bin/activate
```

Gerekli kütüphaneleri yükleyin:

```bash
pip install ultralytics opencv-python numpy pyyaml
```

DeepSORT entegrasyonu tamamlandığında aşağıdaki paketlerden biri de gerekebilir:

```bash
pip install deep-sort-realtime
```

---

## Çalıştırma

Projenin ana giriş dosyası `main.py` olarak belirlenmiştir.

```bash
python main.py
```

Ancak mevcut repository durumunda `main.py` dosyası boş göründüğü için çalıştırma akışının tamamlanması gerekir.

Önerilen `main.py` akışı şu modülleri bağlamalıdır:

1. `config.yaml` dosyasını oku
2. Video dosyasını OpenCV ile aç
3. `YOLODetector` sınıfını başlat
4. Tracker sınıfını başlat
5. Kapı ROI ve giriş/çıkış çizgilerini belirle
6. Her frame için detection → tracking → counting akışını çalıştır
7. Sonuçları frame üzerine yazdır
8. Video penceresinde göster veya çıktı videosu olarak kaydet

---

## Geliştirme Durumu

Mevcut repository, modüler mimari açısından iyi bir başlangıç yapısına sahiptir. Ancak bazı parçalar henüz tamamlanmamıştır.

| Bileşen | Durum |
|---|---|
| YOLO detector | Hazır |
| Direction counter | Hazır |
| DeepSORT tracker | Placeholder |
| Config dosyası | Var, biçimlendirme iyileştirilebilir |
| Main pipeline | Boş / tamamlanmalı |
| Görselleştirme | Henüz ayrı modül olarak görünmüyor |
| Test yapısı | Henüz eklenmemiş |

---

## Tamamlanması Önerilen Geliştirmeler

Projeyi daha güçlü ve çalıştırılabilir hale getirmek için aşağıdaki geliştirmeler yapılabilir:

### 1. `main.py` pipeline'ının tamamlanması

Ana dosya, detector, tracker ve counter modüllerini bir araya getirmelidir.

### 2. DeepSORT entegrasyonu

`DeepSortTracker` sınıfı gerçek bir tracking algoritmasıyla tamamlanmalıdır.

Örneğin:

- `deep-sort-realtime`
- ByteTrack
- SORT
- Norfair

gibi tracker alternatifleri kullanılabilir.

### 3. ROI seçiminin dinamik hale getirilmesi

Kapı bölgesi manuel veya otomatik olarak belirlenebilir.

Öneriler:

- İlk frame üzerinden mouse ile ROI seçimi
- YOLO door detection sonucuna göre otomatik ROI
- Config dosyasında sabit ROI koordinatları

### 4. Görselleştirme modülü eklenmesi

Frame üzerine şu bilgiler yazdırılabilir:

- Bounding box
- Track ID
- Kapı ROI
- Entry line
- Exit line
- Binen yolcu sayısı
- İnen yolcu sayısı

### 5. Çıktı videosu kaydetme

Analiz edilen videonun anotasyonlu hali `.mp4` olarak kaydedilebilir.

### 6. Requirements dosyası eklenmesi

Projeye `requirements.txt` eklenerek kurulum daha kolay hale getirilebilir.

Örnek:

```txt
ultralytics
opencv-python
numpy
pyyaml
deep-sort-realtime
```

---

## Örnek Kullanım Senaryosu

Bu proje aşağıdaki senaryolarda kullanılabilir:

- Metro kapısından binen ve inen yolcuların sayılması
- Otobüs veya tramvay giriş-çıkış yoğunluğunun analizi
- Toplu taşıma istasyonlarında yolcu akışının ölçülmesi
- Kamera tabanlı insan sayımı sistemleri için prototip geliştirme
- Computer vision portfolio projesi olarak nesne tespiti + tracking + sayım pipeline'ı gösterimi

---

## Model Notu

Projede `yolov8n_person_door.pt` adlı bir model yolu belirtilmiştir. Bu, özel eğitilmiş veya fine-tune edilmiş bir YOLO modeli kullanılması planlandığını gösterir.

Eğer bu model dosyası repository içinde yer almıyorsa, çalıştırma öncesinde ilgili model dosyasının proje dizinine eklenmesi gerekir.

Alternatif olarak yalnızca insan tespiti için standart YOLO modeli kullanılabilir:

```python
YOLO("yolov8n.pt")
```

Ancak standart COCO modeli `door` sınıfını doğrudan içermeyebilir. Bu nedenle kapı tespiti gerekiyorsa özel eğitilmiş bir model daha uygun olur.

---

## Projenin Güçlü Yönleri

Bu proje, basit bir görüntü işleme uygulamasından daha fazlasını hedefler. Detection, tracking ve counting adımlarını ayrı modüller halinde düşünmesi nedeniyle genişletilebilir bir yapıya sahiptir.

Öne çıkan güçlü yönler:

- Modüler klasör yapısı
- YOLO tabanlı nesne tespiti
- Tracker katmanı için ayrılmış mimari
- Kapı bölgesi bazlı yön analizi
- Binen/inen yolcu ayrımı
- Cooldown mekanizması ile tekrar sayımı azaltma
- Toplu taşıma ve akıllı şehir uygulamalarına uygun problem seçimi

---

## Gelecek Çalışmalar

Projeye ileride şu özellikler eklenebilir:

- Gerçek zamanlı kamera desteği
- Çoklu kapı desteği
- İstasyon bazlı yoğunluk analizi
- Saatlik/günlük yolcu sayımı raporu
- CSV/JSON çıktı kaydı
- FastAPI ile servisleştirme
- Streamlit dashboard
- Docker desteği
- Unit test yapısı
- FPS ve performans optimizasyonu
- Edge cihazlarda çalıştırma desteği

---

## Sonuç

Metro Passenger Counting System, toplu taşıma görüntülerinde yolcu hareketlerini analiz etmek için geliştirilmiş modüler bir computer vision projesidir. YOLO ile nesne tespiti, tracker mimarisi ve yön bazlı sayım mantığı sayesinde proje; nesne tespiti, takip, hareket analizi ve gerçek dünya uygulaması bağlantısını aynı yapı içinde göstermektedir.

Mevcut haliyle proje geliştirme aşamasındadır. Özellikle `main.py` pipeline'ının ve tracker entegrasyonunun tamamlanmasıyla daha güçlü, çalıştırılabilir ve portfolyo değeri yüksek bir uygulamaya dönüşebilir.
