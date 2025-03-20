
https://nokline.github.io/bugbounty/2024/02/04/ChatGPT-ATO.html  && https://www.shockwave.cloud/blog/shockwave-works-with-openai-to-fix-critical-chatgpt-vulnerability



Web Cache Deception (WCD), web uygulamalarındaki önbellekleme (caching) mekanizmalarının yanlış yapılandırılması sonucu oluşan bir güvenlik açığıdır. Bu zafiyet, bir saldırganın hassas verileri önbelleğe aldırarak, daha sonra bu verilere erişmesini mümkün kılar. Bu yazıda, ChatGPT üzerinde tespit edilen bu tür bir saldırıyı ve etkilerini inceleyeceğiz.

CDN (Content Delivery Network), statik ve sık kullanılan içerikleri önbelleğe alarak (cache) sitelerin daha hızlı yüklenmesini sağlar.


✅ Cache’lenebilir içerikler: Resimler, CSS dosyaları, JavaScript dosyaları.
❌ Cache’lenmemesi gerekenler: Oturum açma bilgileri, özel API yanıtları (örneğin: /api/auth/session gibi).

Last year Nagli discovered a web cache deception vulnerability in ChatGPT   =  web cache deception ? 




Shockwave Identifies Web Cache Deception and Account Takeover Vulnerability affecting OpenAI's ChatGPT 



While exploring the requests that handle ChatGPT's authentication flow I was looking for any anomaly that might expose user information.The following GET request caught my attention:https://chat.openai[.]com/api/auth/session



Zafiyetin Temeli: Web Cache Deception
Web Cache Deception saldırısı, bir sistemin istemeden hassas verileri önbelleğe almasını sağlayarak saldırganın bu önbelleğe alınmış verilere erişmesini mümkün kılar.

1.ChatGPT'nin oturum yönetimi için kullandığı bir endpoint tespit ediliyor }Bu istek, kullanıcının oturum bilgilerini JSON formatında döndürüyor (email, isim, JWT token vs.).

2.Önbellek Kurallarını Bypass Etme:
Cloudflare gibi CDN hizmetleri belirli dosya uzantılarını otomatik olarak önbelleğe alır (örneğin, .css, .js, .png).
Ancak, bu tür API endpoint’leri genellikle dinamik (DYNAMIC) olarak işaretlendiği için varsayılan olarak önbelleğe alınmaz.
Önbelleğe Alınabilecek Bir Yöntem Bulma:

Saldırgan, oturum bilgisi döndüren API isteğini, CSS dosya uzantısı ekleyerek çağırıyor

chat.openai.com/api/auth/session.css   → 400 Hatası
chat.openai.com/api/auth/session/test.css → 200 Başarılı!

Cloudflare’ın yanıt başlığındaki CF-Cache-Status değeri, isteğin önbelleğe alınıp alınmadığını gösterir.
Normalde dinamik içerikler "DYNAMIC" olarak işaretlenir ve önbelleğe alınmaz.
Ancak, .css uzantısı eklendiğinde Cloudflare bunu statik bir dosya gibi önbelleğe aldı ve "HIT" olarak döndü.


yani, session endpoint’i .css gibi bir uzantı eklendiğinde hala hassas JSON verisini döndürüyordu.


Attack Flow:

1. Attacker crafts a dedicated .css path of the /api/auth/session endpoint.

2. Attacker distributes the link (either directly to a victim or publicly)

3. Victims visit the legitimate link.

4. Response is cached.

5. Attacker harvests JWT Credentials.Access Granted.

-----------------------------------------




The impact of this was critical, as it lead to the leak of user’s auth tokens and subsequently, an account takeover.




In this writeup, I will explain how I was able to abuse a path traversal URL parser confusion to achieve what I like to call a “wildcard” cache deception vulnerability, in order to steal user’s auth tokens and take over their accounts





"Wildcard" Web Cache Deception




While playing around with ChatGPT’s newly implemented “share” feature, which allows users to publicly share their chats with others

I noticed something weird. None of my shared chat links would update as I continued talking with ChatGPT. After dealing with bugs like this for a while, the first thing that came to mind was a caching issue



, I saw the Cf-Cache-Status: HIT header. This was pretty interesting to me, as this was not a static file

I checked out the URL, and saw that the path did not have a static extension as expected:




Bir web sitesinde önbellekleme (caching) olduğunda, gelen istekler önce CDN (Content Delivery Network) üzerinden geçer. Yani, URL iki kez parse edilir:

Önce CDN tarafından
Sonra web sunucusu tarafından



ChatGPT'nin sisteminde, iki bileşenin URL'yi yorumlama farkı şudur:

Cloudflare CDN → "%2F" ve ".." gibi path traversal ifadelerini decode ETMEZ
Web Sunucusu → "%2F" ve ".." gibi ifadeleri decode EDER
Bu fark, saldırganın önbelleğe hassas içerikler koymasına ve bunları daha sonra çalmasına neden oluyor.



Saldırgan, özel olarak hazırlanmış bir link oluşturur:

Örnek kötü amaçlı URL:

https://chat.openai.com/share/%2F..%2Fapi/auth/session?cachebuster=123
Burada ne oluyor?
%2F..%2F → /../ anlamına gelir (path traversal).
CDN, bu URL'yi decode etmeden cache’e alır.
Ancak web sunucusu bu URL'yi çözümler ve /api/auth/session endpoint’ine yönlendirir.
Kurban bu linke tıklıyor:

Kurban, saldırganın gönderdiği linke tıklarsa, tarayıcısı /api/auth/session API’sine istek yapar.
Sunucu, kurbanın auth token'ını içeren bir JSON yanıt döndürür.
Önemli nokta: CDN, bu yanıtı cache'ler çünkü /share/ altında olduğu için cacheleme kurallarına uygundur.
Saldırgan cache’den auth token’ı alıyor:

Saldırgan, aynı URL'ye kendisi giderek önbelleğe alınmış yanıtı görür:

https://chat.openai.com/share/%2F..%2Fapi/auth/session?cachebuster=123
CDN, cache’den daha önce saklanan yanıtı getirir.
Yanıtta kurbanın auth token'ı vardır.
Saldırgan artık kurbanın auth token’ını çalmış oldu.



