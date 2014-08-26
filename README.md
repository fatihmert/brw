BinaryReaderWriter
==================

Paketlenmiş verileri belirttiğiniz C tipi değerlere dönüştürerek okuma ve yazma işlemi yapar. “exe,iso,dxf,blend,rar” gibi dosyaları okuyabilir, kendi dosya türlerinizi oluşturabilirsiniz. Günümüzde .xml her ne kadar tercih edilsede, bilgilerin korunması gerekiyor. 

## Global değişkenler ##

### getSeek ###

brw sizin için okuma işlemini otomatik atlatır. Bir dosya okuduğunuzda `dosya.seek(<int>)` fonksiyonuyla, dosyanın hangi karakterden sonra başlayacağı komutunu verir. 

`brw.getSeek` değişkeni hem çağırılabilir hemde değiştirilebilirdir. 

### memo ###

Verilerin okuma şekli işlemciye göre değişir. Günümüz bilgisayarları bilgileri **little-endian** denilen küçükten büyüğe doğru giden byte aralığında okuma işlemi yapar. little-endian sembolü `<` işaretidir.

Varsayılan değer, **little-endian**'dır. İstenilirse bu değişken üzerinden yada `brw.setMem()` fonksiyonuyla değiştirme yapabilirsiniz.

## Fonksiyonlar ##

brw aynı dosya okuma/yazma fonksiyonu `open()` gibi çalışır. Bu demek oluyor ki `with` ifadesiyle de kullanabilirsiniz.

Örnek brw objesi oluşturmak için, 

    brw("yeni.fmd","unpack")
    brw("yeni.fmd","rb")
    
Yukarıda ki iki satırda aynı anlamı ifade etmektedir. İlk parametre dosyamız **yeni.fmd**, ikinci parametremiz ise dosyaya uygulanacak işlemler, unpack yada **rb** ise veri okuma işlemi yapacağınız anlamına gelir. Ama 

    brw("yeni.fmd","pack")
    brw("yeni.fmd","wb")
    
**pack** yada **wb** ise yeni veriler oluşturacağınız anlamına gelir.

Yukarıdaki tanımlarda, işlemlerinizi bitirdiğinizde `brw.close()` fonksiyonunu çalıştırmanız gerekmektedir. Aksi takdirde okuduğunuz/yazdığınız dosya yarım kalacak veya IO hatası alacaksınızdır.

Bu nedenle `with` parametresinin daha sağlıklı olduğunu düşünüyorum.

    with brw("yeni.fmd","pack") as paket:
    with brw("yeni.fmd","unpack") as acikPaket:
    
gibi.

### pack() ###

Bilgilerinizi paketlemenizi sağlar, ilk parametresi byte ikinci parametresi ise değeridir. Peki bu byte nedir? Somutlandırmadan önce aşağıdaki tabloya bir göz atmanızı istiyorum. 

![](https://1.downloader.disk.yandex.com.tr/disk/46880a2cf09e55c0f1faa23562052793/mpfs/KMWYogB4N9LGeJ-OAeyVpERzg9H-7JxlSEaTw2UTQ3k6OB7ORl3vHgKNph0jZf7Q9oY4i-5XdNb3HdOgrFaLCg%3D%3D?uid=0&filename=2014-08-26%2020-13-51%20Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng)

Paketleme işlemi yaparken yukarıdaki tabloya gereğinden fazla ihtiyacımız olacak. Zamanla bu tabloya bakma gereksiniminiz bile kalmıyor. 

- **Format**: Aslında `struct` modülünde tabloya bakıp C tipine karşılık gelen formatı **byte** diye bahsettiğimiz yere yazmanız gerekiyordu. brw ile bu problem ortadan kalkmış oldu. brw de birbirine karşılık gelen formatlar aşağıdaki gibidir.


    brw.pack(byte,io)


- **byte**: Veriler ve karşılıkları aşağıdaki tablodaki gibidir.
- **io**: Girdiğiniz veri tipinin değeri. Değerleri yukarıdaki tabloda bulunan *Python Türü* adlı sütuna göre girdi yapmalısınız. Aksi takdirde hata almanız kaçınılmazdır.

![](https://1.downloader.disk.yandex.com.tr/disk/ad3e15b35fdeec325dda8f0726bdda1a/mpfs/fXha71Avn9yeJgPC4LpqgqXKbc8Zg5_9qhwIamEuHdsVgVyXJlvacV4HpJS88esfWXew5pVNhrj0rTLDL60Vtg%3D%3D?uid=0&filename=2014-08-26%2020-17-52%20Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng)

- **Uzunluk**: Veri tiplerinin bellekte kapladığı boyuttur. Aynı zamanda oluşturduğunuz dosya yapısında da kapladığı alanı ifade eder. Mesela `short` *h* tanımlanmış bir sırayı `char[2]` *2s* şeklinde okumaya kalktığınızda aslında short değerini char tipinde okumuş olacaksınız, haliyle karşınıza ansii olmayan bir karakter çıkacak.

brw nesnesi oluştururken ikinci parametreye yani dosyanın moduna, **rb** yada **pack** girdiyseniz `brw.pack()` fonksiyonunu kullanabilirsiniz demektir.

Örneğin, ilk 5 karakteri **eXec!** ile başlayan bir dosya formatı oluşturalım.

    with brw('yeni.exc','pack') as exx:
      exx.pack('char[5]','eXec!')

İşlem tamamlandıktan sonra **yeni.exc** dosyasını editör programlarıyla açtığınızda **eXec!** yazısını rahatlıkla görebileceksiniz. String veriler şifrelenmeden dosyaya işleniyor ama diğer verileri girdiğinizde aldığınız çıktı ansii olmayacaktır. 

### unpack() ###

İşlenmiş verileri dosyadan okuma işlevi görür. Tek parametreleridir. Bu parametreye okunacak değerin brw tablosundaki değer tipi girilerek değer okunulur. 

Örneğin,

    with brw("yeni.exc","unpack") as ex_open:
      ex_open.unpack("char[5]") #eXec!

### ``__len__()`` ###

Belgenin toplam karakter uzunluğunu verir.

**yeni.exc** dosyamızın içinde 5 karakterlik bir string değer olduğunu bilmediğimizi var sayarsak, 

    with brw("yeni.exc","unpack") as ex_open:
      ex_open.unpack("char[%s]"%(ex_open.__len__())) #eXec!

    

