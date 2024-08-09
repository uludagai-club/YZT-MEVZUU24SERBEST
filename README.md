# YZT-MEVZUU24SERBEST

## Açıklama
Bu proje, [Acıkhack2024TDDİ](#) etkinliği için geliştirilmiştir.
Projede özgeçmişlerin analiz edilerek iş tanımına uygunluğuna göre ne kadar uygun bir aday olduğu ve diğer adayların özgeçmişlerine göre değerlendirme amaçlanmanktadır. Proje için gereken dosyalar internet üzerindeki örnek özgeçmişler ve tarafımızca oluşturulacak özgeçmişler ile sağlanacaktır.OCR ve hazır doküman okuma kütüphaneleri ile segmentlere göre özgeçmişteki veriler elde edilecek daha sonra bu veriler iş tanımındaki özelliklere göre puanlanacak ve özgeçmiş skoru elde edilecek aynı zamanda elde edilen sonuçlar daha sonra kullanılabilmesi için veri tabanında depolanacaktır.

## Kurulum ve Kullanım
```
conda create python=3.8 -n mevzuu24serbest 
conda activate mevzuu24serbest
```
* requirements.txt dosyasındaki kurulumları yapın.
```
pip install -r requirements.txt
```
* Kodun Açılması:
Kod kısmına tıklayarak Visual Studio ile projeyi açın.
* Demo Dosyasına Girme:
web_site/demo klasörüne girin.
```python
cd web_site/demo
```
* Manage.py Dosyasının Çalıştırılması:
```
python manage.py runserver
# Kodunu çalıştırdıktan sonra ekrana gelen http://127.0.0.1:8000/ kısmını kopyalayın. Arama çubuğuna yapıştırın. 
```
* Arayüz Kullanımı:
Karşınıza çıkan arayüz kısmında kriterlerinizi girin ve CV dosyalarını yükleyin.
* CV'lerin Filtrelenmesi:
Yüklediğiniz CV'ler, belirlediğiniz kriterlere uygun olarak filtrelenir ve sonuçlar size sunulur.

## Katkıda Bulunanlar
Bu proje, ekip çalışması ile geliştirilmiştir. Katkıda bulunanlar:

- **Muhammed Hüseyin Karazeybek** - (https://github.com/mhkarazeybek)
- **Mustafa Sungur Polater** - (https://github.com/MustafaSP)
- **Ayçanur Güç** - (https://github.com/aycanur25)
- **Aybüke Tunçkıran** - (https://github.com/aybuke13)

## Etiketler
Bu proje [Acıkhack2024TDDİ](#) etiketi ile yüklenmiştir.

## İletişim
Sorularınız veya geri bildirimleriniz için [yapayzekatoplulugu@uludag.edu.tr]
