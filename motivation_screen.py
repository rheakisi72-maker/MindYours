from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty, ListProperty
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
import random
import os
from kivy.metrics import dp,sp

# Load file KV secara manual
# Pastikan path-nya sesuai. Jika satu folder, cukup nama file saja.
# Jika file python ini ada di folder 'screen', maka pathnya 'screen/motivation_screen.kv' 
# atau cukup 'motivation_screen.kv' tergantung dari mana main.py dijalankan.
Builder.load_file('screen/motivation_screen.kv') 

# Widget Custom untuk Tombol Mood
class MoodButton(ButtonBehavior, BoxLayout):
    mood_name = StringProperty('')
    image_source = StringProperty('')
    bg_color = ListProperty([1, 1, 1, 1])

class MotivationScreen(Screen):
    current_theme_color = ListProperty([0, 0, 0, 1])
    is_card_open = BooleanProperty(False)
    current_mood = StringProperty('')

    # DATABASE QUOTES
    # Masukkan data dari Google Sheet kamu di sini
    quotes_db = {
        'Anger': [
            ("Marah itu wajar, tapi jangan biarkan ia mengendalikanmu.", "Self Care"),
            ("Setiap menit kamu marah, kamu kehilangan 60 detik kedamaian.", "Ralph Waldo Emerson"),
            ("Tenangkan pikiranmu, dan solusinya akan terlihat.", "Anonim"),
            ("Setiap menit kamu marah, kamu kehilangan 60 detik kedamaian.", "Ralph Waldo Emerson"),
            ("Menyimpan amarah itu seperti menggenggam bara api untuk dilemparkan ke orang lain; kamu yang terbakar duluan.", "Buddha"),
            ("Bicaralah saat kamu marah, dan kamu akan membuat pidato terbaik yang akan kamu sesali selamanya.", "Ambrose Bierce"),
            ("Marah adalah asam yang lebih merusak wadah tempat ia disimpan daripada objek yang dituangi.", "Mark Twain"),
            ("Pejuang terbaik adalah dia yang tidak pernah marah.", "Lao Tzu"),
            ("Siapapun yang bisa membuatmu marah, dia telah menaklukkanmu.", "Elizabeth Kenny"),
            ("Apa yang dimulai dengan kemarahan, akan berakhir dengan rasa malu.", "Benjamin Franklin"),
            ("Jika kamu sabar di satu saat kemarahan, kamu akan terhindar dari seratus hari penyesalan.", "Pepatah Cina"),
            ("Obat terbaik untuk kemarahan adalah penundaan.", "Seneca"),
            ("Marah itu gampang. Tapi marah pada orang yang tepat, dengan kadar yang tepat, di waktu yang tepat, itu susah.", "Aristoteles"),
            
            # --- PENGENDALIAN DIRI ---
            ("Jangan pernah merespons pesan saat sedang marah. Tarik napas dulu.", "Self Reminder"),
            ("Ketika marah, hitung sampai sepuluh sebelum bicara. Jika sangat marah, hitung sampai seratus.", "Thomas Jefferson"),
            ("Orang yang kuat bukanlah yang jago bergulat, tapi yang bisa menahan dirinya saat marah.", "Nabi Muhammad SAW"),
            ("Kemarahan tidak menyelesaikan masalah, ia hanya menaikkan tekanan darahmu.", "Fajri"),
            ("Jangan biarkan perilaku buruk orang lain menghancurkan kedamaian batinmu.", "Dalai Lama"),
            ("Kamu tidak dihukum *karena* kemarahanmu, kamu akan dihukum *oleh* kemarahanmu.", "Buddha"),
            ("Semakin keras suaramu saat marah, semakin sedikit orang yang mendengarkan logikamu.", "Ramadhani"),
            ("Diam adalah benteng terbaik saat api amarah sedang menyala.", "Mitha"),
            ("Orang yang cepat marah akan segera menjadi bodoh.", "Bruce Lee"),
            ("Marah hanya akan membuatmu terlihat lemah, bukan kuat.", "Bunga"),

            # --- PERSPEKTIF & KETENANGAN ---
            ("Di balik setiap kemarahan, selalu ada rasa sakit yang belum sembuh.", "Eckhart Tolle"),
            ("Marah adalah caramu menghukum diri sendiri atas kesalahan orang lain.", "Immanuel Kant"),
            ("Balas dendam terbaik adalah dengan tidak menjadi seperti orang yang menyakitimu.", "Marcus Aurelius"),
            ("Hati yang penuh kemarahan tidak punya ruang untuk kebahagiaan.", "widhi"),
            ("Jadilah seperti air. Tenang, mengalir, tapi bisa menghancurkan batu tanpa perlu marah.", "Filosofi Air"),
            ("Kemarahan adalah angin yang memadamkan lampu akal pikiran.", "Robert Green Ingersoll"),
            ("Orang yang 'terbang' karena marah, biasanya akan mendarat dengan buruk.", "Will Rogers"),
            ("Jangan jadikan harimu buruk hanya karena 5 menit yang menyebalkan.", "Daily Reminder"),
            ("Memaafkan bukan berarti mereka benar, itu berarti kamu ingin hatimu tenang.", "Healing"),
            ("Marah itu manusiawi. Memilih untuk tetap marah itu keputusan.", "chyrni"),

            # --- SHORT & PUNCHY (Untuk yang malas baca panjang) ---
            ("Tarik napas. Hembuskan. Lepaskan.", "Relax"),
            ("Ini tidak sepadan dengan energimu.", "Focus"),
            ("Jaga hatimu, jangan biarkan meledak.", "Peace"),
            ("Sabar itu ilmu tingkat tinggi.", "Life Lesson"),
            ("Tenang. Ini hanya sementara.", "Hope"),
            ("Jangan terpancing umpan mereka.", "Stay Cool"),
            ("Kemarahanmu adalah musuhmu.", "Warrior Mindset"),
            ("Senyum lebih menakutkan daripada teriakan.", "Psikologi"),
            ("Dunia tidak berputar di sekeliling egomu.", "Reality Check"),
            ("Jadilah tuan atas emosimu sendiri.", "Control"),
            
            # --- TAMBAHAN ---
            ("Sebuah momen kesabaran bisa mencegah bencana besar.", "Anonim"),
            ("Jangan membuat keputusan permanen untuk emosi yang sementara.", "Wisdom"),
            ("Api tidak bisa dipadamkan dengan api.", "Leo Tolstoy"),
            ("Kamu lebih besar dari masalah yang membuatmu marah.", "Affirmation"),
            ("Apakah masalah ini akan penting 5 tahun lagi? Jika tidak, jangan marah lebih dari 5 menit.", "5 by 5 Rule"),
            ("Orang yang bahagia tidak punya waktu untuk membenci.", "Unknown"),
            ("Mencari kedamaian lebih baik daripada mencari kebenaran dalam argumen.", "Relationship Advice"),
            ("Ubah kemarahan menjadi energi untuk berkarya.", "Productivity"),
            ("Maafkan diri sendiri karena pernah marah, lalu coba lagi.", "Self Love"),
            ("Hari ini terlalu indah untuk dirusak oleh amarah.", "Good Vibes")
        ],
        'Anxiety': [
            ("Kamu tidak harus mengontrol segalanya. Bernafaslah.", "Mindfulness"),
            ("Kecemasan adalah bunga dari masa depan yang belum mekar.", "Anonim"),
            ("Kamu aman. Perasaan ini hanya sementara.", "Self Talk"),
            ("Tarik napas. Kamu aman. Kamu di sini sekarang. Semuanya baik-baik saja.", "Grounding"),
            ("Kecemasan adalah bunga dari masa depan yang belum mekar. Fokuslah pada hari ini.", "Anonim"),
            ("Bernafaslah. Kamu tidak harus menyelesaikan semua masalah hidupmu hari ini.", "Self Care"),
            ("Perasaan ini hanya sementara. Seperti awan yang lewat, ia akan berlalu.", "Mindfulness"),
            ("Kaki di tanah. Udara di paru-paru. Kamu hidup. Kamu kuat.", "Anonim"),
            ("Jangan lupa bernafas. Itu adalah hal pertama yang harus kamu lakukan saat panik menyerang.", "Unknown"),
            ("Tarik napas keberanian, hembuskan ketakutan.", "Mantra"),
            ("Kamu tidak sedang dalam bahaya, kamu hanya sedang merasa tidak nyaman. Ada bedanya.", "Dr. Claire Weekes"),
            ("Satu napas pada satu waktu. Satu langkah pada satu waktu.", "Anonim"),
            ("Istirahatkan pikiranmu yang lelah. Dunia bisa menunggu.", "Rest"),

            # --- MELAWAN OVERTHINKING (Logika vs Cemas) ---
            ("Khawatir itu seperti kursi goyang. Memberimu sesuatu untuk dilakukan, tapi tidak membawamu ke mana-mana.", "Erma Bombeck"),
            ("Jangan percaya semua yang kamu pikirkan. Pikiran cemas adalah pembohong yang hebat.", "Psikologi"),
            ("Skenario buruk yang kamu bayangkan di kepalamu itu hanyalah fiksi, bukan ramalan.", "Reality Check"),
            ("Kamu sudah melewati 100% hari-hari terburukmu. Peluangmu bagus.", "Fakta"),
            ("Mengkhawatirkan masa depan hanya merusak kedamaian hari ini.", "Anonim"),
            ("Fokus pada apa yang bisa kamu kendalikan, lepaskan apa yang tidak bisa.", "Stoic"),
            ("Apakah ini akan menjadi masalah 5 tahun lagi? Jika tidak, jangan habiskan 5 menit untuk mengkhawatirkannya.", "5 by 5 Rule"),
            ("Kamu tidak bisa menghentikan ombak, tapi kamu bisa belajar berselancar.", "Jon Kabat-Zinn"),
            ("Masalah yang kamu takutkan seringkali tidak seburuk yang kamu bayangkan.", "Seneca"),
            ("Berhenti bertanya 'Bagaimana jika...?' dan mulailah berkata 'Aku akan baik-baik saja'.", "Shift"),

            # --- VALIDASI & PENERIMAAN (Pelukan Virtual) ---
            ("Tidak apa-apa untuk merasa takut. Tapi lakukanlah dengan takut.", "Carrie Fisher"),
            ("Kamu tidak lemah karena merasa cemas. Kamu hanya manusia yang peduli.", "Unknown"),
            ("Berlemah-lembutlah pada dirimu sendiri. Kamu sedang melakukan yang terbaik yang kamu bisa.", "Self Compassion"),
            ("Kecemasanmu tidak mendefinisikan siapa dirimu.", "Identity"),
            ("Tidak perlu menjadi sempurna. Cukup menjadi ada.", "Anonim"),
            ("Kadang 'baik-baik saja' adalah pencapaian yang cukup untuk hari ini.", "Healing"),
            ("Kamu diizinkan untuk mengambil jeda dan tidak melakukan apa-apa.", "Permission"),
            ("Maafkan dirimu karena merasa cemas. Itu bukan salahmu.", "Self Love"),
            ("Dunia ini berisik. Wajar jika kamu butuh hening.", "Introvert Power"),
            ("Kamu berharga, bahkan saat kamu merasa berantakan.", "Truth"),

            # --- KEKUATAN & KEBERANIAN ---
            ("Keberanian bukan berarti tidak takut, tapi bertindak meski gemetar.", "Mark Twain"),
            ("Badai pasti berlalu. Kamu hanya perlu bertahan sampai hujan reda.", "Hope"),
            ("Kamu lebih kuat daripada kecemasanmu. Selalu begitu.", "Warrior"),
            ("Rasa takut adalah reaksi. Keberanian adalah keputusan.", "Winston Churchill"),
            ("Di sisi lain ketakutan, ada kebebasan.", "Unknown"),
            ("Percayalah pada dirimu sendiri. Kamu telah bertahan sejauh ini.", "Survivors"),
            ("Kecemasan itu kecil, kamu itu semesta.", "Perspective"),
            ("Jadikan ketakutanmu sebagai bahan bakar untuk berhati-hati, bukan untuk berhenti.", "Strategy"),
            ("Setiap kali kamu menghadapi ketakutanmu, kamu mendapatkan kekuatan.", "Eleanor Roosevelt"),
            ("Bangunlah. Hadapi. Kamu bisa.", "Morning Spark"),

            # --- PENDEK & MANTRA (Untuk Panik Mendadak) ---
            ("Ini juga akan berlalu.", "Persia Kuno"),
            ("Aku aman. Aku tenang. Aku siap.", "Affirmation"),
            ("Fokus pada sekarang.", "Now"),
            ("Lepaskan.", "Let Go"),
            ("Satu hal satu waktu.", "Focus"),
            ("Aku memilih kedamaian.", "Choice"),
            ("Tarik napas...", "Breathe"),
            ("Aku memegang kendali.", "Control"),
            ("Semesta menjagaku.", "Faith"),
            ("Semuanya akan membaik.", "Optimism")
        ],
        'Joy': [
            ("Kebahagiaanmu menular! Bagikan senyummu hari ini.", "Daily Spark"),
            ("Nikmati momen ini, karena inilah hidup.","widhi"),
            # --- BERSYUKUR & MENIKMATI MOMEN ---
            ("Kebahagiaan bukanlah memiliki apa yang kamu inginkan, tapi menginginkan apa yang kamu miliki.", "Dale Carnegie"),
            ("Nikmati hal-hal kecil, karena suatu hari kamu mungkin menoleh ke belakang dan menyadari itu adalah hal-hal besar.", "Robert Brault"),
            ("Bersyukur mengubah apa yang kita miliki menjadi cukup.", "Melody Beattie"),
            ("Hari ini adalah hadiah. Itulah mengapa disebut 'Present'.", "Eleanor Roosevelt"),
            ("Jangan menunda kebahagiaanmu menunggu waktu yang sempurna. Waktunya adalah sekarang.", "Desmitha"),
            ("Berhenti sejenak dan sadari betapa indahnya hidup ini sekarang.", "Mindfulness"),
            ("Hitunglah pelangimu, bukan badaimu.", "Alyssa Knight"),
            ("Kebahagiaan adalah bentuk tertinggi dari kesehatan.", "Dalai Lama"),
            ("Simpan momen ini dalam hatimu selamanya.", "Memory"),
            ("Terkadang kebahagiaan itu sederhana: secangkir teh dan hati yang tenang.", "Bunga"),

            # --- MENYEBARKAN KEBAIKAN (Sharing Joy) ---
            ("Kebahagiaan adalah satu-satunya hal yang bertambah jika dibagi.", "Albert Schweitzer"),
            ("Jadilah alasan seseorang tersenyum hari ini.", "Kindness"),
            ("Senyummu adalah tanda tanganmu. Gunakan itu untuk mengubah dunia.", "Destin"),
            ("Kebahagiaan itu seperti parfum; kamu tidak bisa menuangkannya ke orang lain tanpa terkena percikannya sendiri.", "Ralph Waldo Emerson"),
            ("Dunia butuh lebih banyak cahaya sepertimu.", "Validation"),
            ("Energi positif itu menular. Teruslah bersinar!", "Vibes"),
            ("Satu senyuman hangat adalah bahasa kebaikan yang universal.", "William Arthur Ward"),
            ("Berbuat baiklah, dan kebahagiaan akan mengejarmu.", "Karma"),
            ("Biarkan cahayamu bersinar begitu terang sehingga orang lain tidak punya pilihan selain ikut bersinar.", "Unknown"),
            ("Tebarkan konfeti kebaikan ke mana pun kamu pergi.", "Fun"),

            # --- ENERGI & SEMANGAT ---
            ("Kamu terlihat cantik/tampan saat bahagia!", "Compliment"),
            ("Gunakan energi ini untuk memulai sesuatu yang hebat.", "Productivity"),
            ("Tidak ada kosmetik untuk kecantikan seperti kebahagiaan.", "Maria Mitchell"),
            ("Hidup itu singkat. Makan kue itu. Beli sepatu itu. Tertawalah yang keras.", "YOLO"),
            ("Rayakan setiap kemenangan kecil. Kamu pantas mendapatkannya.", "Self Love"),
            ("Ini adalah harimu! Lakukan apa yang membuat jiwamu menyala.", "Passion"),
            ("Optimisme adalah magnet kebahagiaan.", "Mary Lou Retton"),
            ("Menarilah seolah tidak ada yang melihat.", "Mark Twain"),
            ("Tertawa adalah liburan instan.", "Milton Berle"),
            ("Jadikan kebahagiaan sebagai prioritas, bukan pilihan.", "Priority"),

            # --- VALIDASI DIRI (You Deserve It) ---
            ("Kamu pantas merasa bahagia. Jangan merasa bersalah karenanya.", "Affirmation"),
            ("Kebahagiaan terlihat cocok sekali padamu.", "Truth"),
            ("Izinkan dirimu untuk bersinar sepenuhnya hari ini.", "Permission"),
            ("Kamu telah bekerja keras untuk sampai di titik ini. Nikmatilah.", "Pride"),
            ("Dirimu yang bahagia adalah versi terbaik dirimu.", "Growth"),
            ("Jangan biarkan siapapun meredupkan cahayamu hari ini.", "Boundary"),
            ("Kebahagiaanmu adalah tanggung jawabmu, dan kamu melakukannya dengan baik!", "Self Care"),
            ("Hati yang gembira adalah obat yang manjur.", "Amsal"),
            ("Kamu adalah karya seni yang sedang berbahagia.", "Art"),
            ("Teruslah melangkah dengan senyuman itu.", "Keep Going"),

            # --- PENDEK & MANIS (Short Quotes) ---
            ("Life is good.", "Optimism"),
            ("Good vibes only.", "Mantra"),
            ("Pilih bahagia.", "Choice"),
            ("Senyum!", "Action"),
            ("Hari yang indah.", "Gratitude"),
            ("Kamu bersinar!", "Glow"),
            ("Syukuri hari ini.", "Blessed"),
            ("Bahagia itu sederhana.", "Simple"),
            ("Stay happy.", "Wish"),
            ("Yay!", "Cheer")
        ],
        'Sadness': [
            ("Hujan diperlukan agar pelangi bisa muncul.", "Hope"),
            ("Peluk dirimu sendiri. Kamu sudah berjuang hebat.", "Self Love"),
            ("Tidak apa-apa untuk tidak baik-baik saja. Kamu manusia, bukan robot.", "Self Compassion"),
            ("Menangislah. Air mata adalah cara hatimu menyiram jiwamu agar tumbuh kembali.", "Healing"),
            ("Jangan minta maaf karena merasa hancur. Itu tanda kamu punya hati yang tulus.", "Yoga"),
            ("Izinkan dirimu merasakan kesedihan ini agar ia bisa berlalu.", "Mindfulness"),
            ("Kesedihan ibarat awan mendung; ia menutupi matahari, tapi tidak menghilangkannya.", "Perspektif"),
            ("Kamu tidak lemah karena menangis. Kamu sedang melepas beban.", "Strength"),
            ("Merasakan sakit itu bukti bahwa kamu masih hidup dan peduli.", "Unknown"),
            ("Tidak perlu pura-pura kuat setiap saat. Istirahatlah dari topengmu.", "Rest"),
            ("Hari yang buruk tidak berarti kehidupan yang buruk.", "Perspective"),
            ("Validasi perasaanmu. Apa yang kamu rasakan itu nyata dan penting.", "Psychology"),

            # --- HARAPAN & WAKTU (Hope) ---
            ("Hujan diperlukan agar pelangi bisa muncul.", "Hope"),
            ("Malam yang paling gelap menghasilkan bintang yang paling terang.", "Martin Luther King Jr."),
            ("Ini hanya satu bab yang buruk, bukan seluruh buku kehidupanmu.", "Story"),
            ("Segala sesuatu berubah. Perasaan ini juga akan berubah.", "Impermanence"),
            ("Matahari akan tetap terbit esok hari, apa pun yang terjadi.", "Nature"),
            ("Luka adalah tempat di mana cahaya masuk.", "Rumi"),
            ("Badai pasti berlalu. Bertahanlah sedikit lagi.", "Resilience"),
            ("Kamu akan tersenyum lagi. Mungkin tidak hari ini, tapi nanti.", "Promise"),
            ("Tidak ada musim dingin yang berlangsung selamanya; musim semi akan datang.", "Hal Borland"),
            ("Rasa sakit hari ini adalah kekuatanmu di masa depan.", "Growth"),

            # --- DUKUNGAN LEMBUT (Gentle Hugs) ---
            ("Kamu sudah bertahan sejauh ini. Aku bangga padamu.", "Validation"),
            ("Satu hari pada satu waktu. Jika terlalu berat, satu napas pada satu waktu.", "Slow Down"),
            ("Penyembuhan itu tidak lurus. Ada hari baik, ada hari buruk. Teruslah berjalan.", "Process"),
            ("Jadilah lembut pada hatimu yang sedang lebam.", "Self Care"),
            ("Kamu lebih kuat daripada yang kamu bayangkan, bahkan saat kamu merasa rapuh.", "Truth"),
            ("Istirahatlah jika lelah, tapi jangan menyerah.", "Banksy"),
            ("Dunia butuh kamu, bahkan saat kamu sedih.", "Worth"),
            ("Waktu menyembuhkan apa yang akal tidak bisa jelaskan.", "Time"),
            ("Kamu tidak sendirian. Semesta memelukmu dalam diam.", "Universe"),
            ("Perlakukan dirimu seperti kamu memperlakukan sahabat yang sedang sedih.", "Friendship"),

            # --- METAFORA & PUISI ---
            ("Tuliskan lukamu di pasir, ukir bahagiamu di batu.", "Wisdom"),
            ("Air mata adalah kata-kata yang tidak bisa diucapkan oleh mulut.", "Joker"),
            ("Bunga butuh hujan untuk mekar. Begitu juga jiwamu.", "Nature"),
            ("Laut yang tenang tidak melahirkan pelaut yang tangguh.", "Proverb"),
            ("Bintang tidak bisa bersinar tanpa kegelapan.", "Light"),
            ("Tarik napas... hembuskan kesedihan.", "Breathe"),
            ("Hati yang retak membiarkan cahaya masuk lebih banyak.", "Aghniansyah"),
            ("Setiap akhir adalah awal yang baru.", "Cycle"),
            ("Jangan biarkan hari kemarin menyita terlalu banyak dari hari ini.", "Will Rogers"),
            ("Kesedihan hanyalah pengunjung, jangan biarkan ia menjadi penghuni tetap.", "Guest"),

            # --- PENDEK & MENENANGKAN (Short Comfort) ---
            ("This too shall pass.", "Classic"),
            ("Peluk jauh.", "Virtual Hug"),
            ("Kamu berharga.", "Affirmation"),
            ("Menangislah, lalu bangkit.", "Action"),
            ("Semua akan membaik.", "Faith"),
            ("Aku bersamamu.", "Support"),
            ("Tetap bernafas.", "Focus"),
            ("Sayangi dirimu.", "Love"),
            ("Kamu aman.", "Safety"),
            ("Bertahanlah.", "Hope")
        ],
        'Envy': [
            ("Rumput tetangga lebih hijau karena mereka menyiramnya.", "Focus"),
            ("Jalan hidupmu unik. Jangan bandingkan.", "Wisdom"),
            ("Perbandingan adalah pencuri kebahagiaan. Fokuslah pada kertas ujianmu sendiri.", "Theodore Roosevelt"),
            ("Jangan bandingkan Chapter 1-mu dengan Chapter 20 orang lain.", "Wisdom"),
            ("Rumput tetangga terlihat lebih hijau karena mereka rajin menyiramnya. Siramlah rumputmu sendiri.", "Focus"),
            ("Bunga tidak berpikir untuk bersaing dengan bunga di sebelahnya. Ia hanya mekar.", "Zen Shin"),
            ("Matahari dan Bulan tidak bersaing. Mereka bersinar pada gilirannya masing-masing.", "Nature"),
            ("Menjadi iri berarti menghina bakat unik yang Tuhan berikan padamu.", "Self Worth"),
            ("Hidup bukanlah perlombaan lari, tapi perjalanan menikmati pemandangan.", "Perspective"),
            ("Kamu tidak bisa menjadi orang lain, dan orang lain tidak bisa menjadi kamu. Itu kekuatanmu.", "Authenticity"),
            ("Fokus pada langkah kakimu sendiri, bukan pada seberapa cepat orang lain berlari.", "Unknown"),
            ("Iri hati adalah pengakuan bahwa kamu merasa kalah. Jangan mengaku kalah.", "Napoleon Bonaparte"),

            # --- MENGUBAH IRI JADI INSPIRASI ---
            ("Jangan bilang 'Aku ingin jadi dia', tapi katakan 'Aku terinspirasi olehnya'.", "Mindset Shift"),
            ("Jika kamu melihat seseorang sukses, itu bukti bahwa sukses itu mungkin. Giliranmu akan tiba.", "Hope"),
            ("Kagumi keindahan orang lain tanpa mempertanyakan keindahanmu sendiri.", "Self Love"),
            ("Matikan rasa iri dengan menyalakan rasa ingin tahu: 'Bagaimana cara dia melakukannya?'", "Growth"),
            ("Kesuksesan orang lain tidak mengurangi jatah kesuksesanmu. Semesta itu melimpah.", "Abundance"),
            ("Daripada iri pada panen orang lain, mulailah menanam benihmu sendiri.", "Action"),
            ("Jadikan keberhasilan temanmu sebagai motivasi, bukan ancaman.", "Friendship"),
            ("Energi yang kamu pakai untuk iri, lebih baik dipakai untuk berkarya.", "Productivity"),
            ("Belajarlah dari mereka, jangan membenci mereka.", "Strategy"),
            ("Tepuk tangan untuk orang lain sampai giliranmu tiba.", "Support"),

            # --- BERSYUKUR (Antidote to Envy) ---
            ("Hitunglah berkahmu, bukan masalahmu atau milik orang lain.", "Gratitude"),
            ("Kamu punya sesuatu yang orang lain impikan. Sadarilah itu.", "Perspective"),
            ("Kekayaan sejati adalah merasa cukup dengan apa yang ada.", "Contentment"),
            ("Iri hati buta terhadap apa yang kamu miliki, tapi tajam melihat apa yang orang lain punya.", "Mochi"),
            ("Bahagia dimulai ketika kamu berhenti menghitung milik orang lain.", "Truth"),
            ("Rasa syukur mengubah apa yang kita miliki menjadi cukup.", "Melody Beattie"),
            ("Jangan biarkan apa yang kamu inginkan membuatmu lupa apa yang kamu miliki.", "Milky"),
            ("Fokus pada *progres*-mu, bukan pada *posisi* orang lain.", "Self Improvement"),
            ("Kamu tepat berada di tempat yang seharusnya kamu berada saat ini.", "Trust"),
            ("Setiap orang punya ujiannya sendiri yang tidak kamu lihat di media sosial.", "Reality Check"),

            # --- HARGA DIRI (Self Worth) ---
            ("Lilin tidak kehilangan cahayanya dengan menyalakan lilin lain.", "Sharing"),
            ("Kamu adalah edisi terbatas. Tidak ada duplikatnya.", "Unique"),
            ("Jalan hidupmu didesain khusus untukmu. Sepatu orang lain tidak akan muat di kakimu.", "Destiny"),
            ("Kecantikan orang lain bukan berarti ketiadaan kecantikanmu.", "Confidence"),
            ("Kamu berharga bukan karena kamu lebih baik dari orang lain, tapi karena kamu adalah kamu.", "Self Acceptance"),
            ("Dunia butuh bakatmu, bukan tiruanmu terhadap orang lain.", "Purpose"),
            ("Standar kesuksesanmu ditentukan oleh dirimu, bukan Instagram orang lain.", "Define Success"),
            ("Percayalah pada waktumu sendiri. Bunga mekar di musim yang berbeda.", "Timing"),
            ("Jangan tukar kedamaianmu dengan rasa iri.", "Peace"),
            ("Jadilah versi terbaik dari dirimu, bukan versi KW dari orang lain.", "Originality"),

            # --- PENDEK & TAJAM (Short & Sharp) ---
            ("Stay in your lane.", "Focus"),
            ("Eyes on your own paper.", "Teacher"),
            ("You are enough.", "Affirmation"),
            ("Bersyukurlah.", "Gratitude"),
            ("Giliranmu akan datang.", "Hope"),
            ("Fokus pada dirimu.", "Self Care"),
            ("Cintai prosesmu.", "Love"),
            ("Jangan bandingkan.", "Stop"),
            ("Kamu unik.", "Truth"),
            ("Be you.", "Authentic"),
        ],
        'Fear': [
            ("Satu-satunya hal yang harus kita takuti adalah ketakutan itu sendiri.", "Franklin D. Roosevelt"),
            ("Keberanian bukanlah ketiadaan rasa takut, melainkan penilaian bahwa ada hal lain yang lebih penting daripada rasa takut.", "Ambrose Redmoon"),
            ("Lakukan satu hal setiap hari yang membuatmu takut.", "Eleanor Roosevelt"),
            ("Ketakutan adalah penjara; keberanian adalah kuncinya.", "Marianne Williamson"),
            ("Jangan biarkan rasa takutmu memutuskan masa depanmu.", "Shalane Flanagan"),
            ("Pria pemberani bukanlah dia yang tidak merasa takut, tapi dia yang menaklukkan rasa takut itu.", "Nelson Mandela"),
            ("Rasa takut tidak ada di mana pun kecuali di dalam pikiran.", "Dale Carnegie"),
            ("Terlalu banyak dari kita yang tidak mewujudkan impian karena kita menjalani ketakutan kita.", "Les Brown"),
            ("Ketakutan memotong lebih dalam dari pedang.", "George R.R. Martin"),
            ("Ketakutan hanyalah bayangan; hadapi dan ia akan menghilang.", "Akbar"),
            ("Risiko terbesar adalah tidak mengambil risiko sama sekali.", "Mark Zuckerberg"),
            ("Apa yang kamu takutkan adalah indikator apa yang harus kamu lakukan selanjutnya.", "Tim Ferriss"),
            ("Jangan takut gagal, takutlah tidak pernah mencoba.", "Anonim"),
            ("Musuh terbesar kesuksesan bukanlah kegagalan, melainkan ketakutan.", "Snoop Dogg"),
            ("Rasa takut bersifat sementara. Penyesalan bersifat selamanya.", "Anonim"),
            ("Gua yang kamu takut masuki menyimpan harta karun yang kamu cari.", "Joseph Campbell"),
            ("Bertindaklah seolah-olah apa yang kamu lakukan membuat perbedaan. Karena memang begitu.", "William James"),
            ("Hambatan adalah hal-hal menakutkan yang kamu lihat ketika kamu mengalihkan pandangan dari tujuanmu.", "Henry Ford"),
            ("Jika impianmu tidak menakutkanmu, impian itu terlalu kecil.", "Richard Branson"),
            ("Ketakutan membunuh lebih banyak mimpi daripada kegagalan.", "Suzy Kassem"),
            ("Jangan takut berjalan lambat, takutlah jika hanya berdiri diam.", "Pepatah Cina"),
            ("Keberanian adalah ketakutan yang telah memanjatkan doa.", "Paulo Coelho"),
            ("Di sisi lain dari ketakutanmu adalah kebebasan.", "Marilyn Ferguson"),
            ("Jangan biarkan ketakutan akan serangan menghalangimu bermain di lapangan.", "Babe Ruth"),
            ("Seseorang yang memindahkan gunung mulai dengan membawa batu-batu kecil.", "Confucius"),
            ("Aku belajar bahwa keberanian bukan berarti tidak takut, tetapi menang melawannya.", "Nelson Mandela"),
            ("Hidup menyusut atau berkembang sebanding dengan keberanian seseorang.", "Anais Nin"),
            ("Kekhawatiran adalah penyalahgunaan imajinasi.", "Dan Zadra"),
            ("Jangan takut pada bayangan, itu berarti ada cahaya di dekatnya.", "Ruth Renkel"),
            ("Segala sesuatu yang kamu inginkan ada di sisi lain ketakutan.", "George Addair"),
            ("Ketakutan itu nyata, tetapi bahaya itu tidak.", "Will Smith"),
            ("Kunci untuk berubah adalah melepaskan ketakutan.", "Rosanne Cash"),
            ("Ubah ketakutanmu menjadi kehati-hatian, bukan kepanikan.", "Anonim"),
            ("Jangan takut membuat kesalahan, takutlah jika tidak belajar darinya.", "Anonim"),
            ("Ketakutan adalah reaksi. Keberanian adalah keputusan.", "Winston Churchill"),
            ("Masa-masa sulit tidak pernah bertahan lama, tetapi orang-orang tangguh bertahan.", "Robert H. Schuller"),
            ("Anda tidak bisa menyeberangi laut hanya dengan berdiri dan memandangi air.", "Rabindranath Tagore"),
            ("Setiap kemajuan dimulai dengan keputusan berani.", "Anonim"),
            ("Ketakutan akan penderitaan lebih buruk daripada penderitaan itu sendiri.", "Paulo Coelho"),
            ("Jangan takut badai, karena itu melatihmu menahkodai kapal.", "Louisa May Alcott"),
            ("Semakin kamu lari dari ketakutan, semakin besar ia tumbuh.", "Anonim"),
            ("Tenang adalah kekuatan super saat menghadapi ketakutan.", "Anonim"),
            ("Keraguan membunuh lebih banyak mimpi daripada kegagalan.", "Karim Seddiki"),
            ("Ketakutan hanyalah soal perspektif.", "Anonim"),
            ("Jadilah takut, tapi lakukanlah juga.", "Carrie Fisher"),
            ("Ketakutan berasal dari ketidaktahuan.", "Ralph Waldo Emerson"),
            ("Fokus pada tujuan, bukan pada rasa takut.", "Anonim"),
            ("Tindakan menyembuhkan ketakutan.", "David J. Schwartz"),
            ("Jangan biarkan ketakutan mendikte langkahmu.", "Anonim"),
            ("Kamu lebih kuat dari yang kamu tahu, lebih berani dari yang kamu yakini.", "A.A. Milne")
        ],
        'Disgust': [
            ("Perubahan terjadi ketika rasa sakit untuk tetap sama lebih besar daripada rasa sakit untuk berubah.", "Tony Robbins"),
            ("Jijik pada keadaanmu adalah langkah pertama untuk memperbaikinya.", "Anonim"),
            ("Standarmu menentukan kualitas hidupmu.", "Tony Robbins"),
            ("Jangan turunkan standarmu untuk siapa pun atau apa pun.", "Anonim"),
            ("Hargai dirimu cukup untuk menjauh dari apa pun yang tidak lagi melayanimu.", "Steve Maraboli"),
            ("Jika kamu tidak menyukainya, ubahlah. Jika kamu tidak bisa mengubahnya, ubah sikapmu.", "Maya Angelou"),
            ("Terkadang kamu harus merasa muak dulu sebelum kamu bisa bangkit.", "Anonim"),
            ("Kebencian pada kebiasaan buruk adalah awal dari kebiasaan baik.", "Anonim"),
            ("Jangan biarkan orang beracun menyewa ruang di kepalamu secara gratis.", "Anonim"),
            ("Bersihkan hidupmu dari apa yang mengotori jiwamu.", "Anonim"),
            ("Menjauh dari hal negatif bukanlah kelemahan, itu kecerdasan.", "Cleanseeker"),
            ("Jijik adalah penjaga gerbang jiwamu; dengarkan dia.", "Anonim"),
            ("Kamu adalah rata-rata dari lima orang yang paling sering bersamamu. Pilih dengan bijak.", "Jim Rohn"),
            ("Jangan minum racun hanya karena kamu haus.", "Anonim"),
            ("Berhenti menoleransi apa yang kamu benci.", "Anonim"),
            ("Ubah rasa jijikmu menjadi bahan bakar untuk transformasi.", "Anonim"),
            ("Kesabaran ada batasnya, dan itu hal yang baik.", "Anonim"),
            ("Jangan biarkan dunia mengubah senyummu.", "Anonim"),
            ("Kesehatan bukan hanya apa yang kamu makan, tapi apa yang kamu pikirkan dan katakan.", "Anonim"),
            ("Buanglah sampah mentalmu.", "Anonim"),
            ("Jika itu membuatmu merasa buruk, itu tidak layak untuk waktumu.", "Anonim"),
            ("Harga diri adalah kemampuan untuk mengatakan tidak pada pola yang tidak sehat.", "Anonim"),
            ("Kamu layak mendapatkan yang lebih baik daripada yang membuatmu muak.", "Anonim"),
            ("Jadilah selektif dalam pertarunganmu, kadang kedamaian lebih baik daripada kebenaran.", "Anonim"),
            ("Kualitas hidupmu tergantung pada apa yang kamu tolak.", "Anonim"),
            ("Perasaan muak adalah alarm untuk bangun.", "Anonim"),
            ("Jangan kompromikan integritasmu demi kenyamanan.", "Fjrytr"),
            ("Memaafkan bukan berarti menerima perilaku buruk.", "Anonim"),
            ("Batas yang kuat menciptakan kedamaian yang kuat.", "Anonim"),
            ("Tidak adalah kalimat lengkap.", "Anne Lamott"),
            ("Kebenaran mungkin pahit, tapi kebohongan itu menjijikkan.", "Dhani"),
            ("Cuci hatimu dengan tawa, cuci jiwamu dengan air mata.", "Anonim"),
            ("Jangan biarkan hal-hal jelek mengubahmu menjadi jelek.", ""),
            ("Kepahitan adalah racun yang kamu minum sambil berharap orang lain mati.", "Nelson Mandela"),
            ("Fokus pada membersihkan kebunmu sendiri.", "Anonim"),
            ("Detoksifikasi hidupmu: teman, kebiasaan, dan pikiran.", "Anonim"),
            ("Kejahatan menang ketika orang baik tidak melakukan apa-apa.", "Edmund Burke"),
            ("Ubah 'aku benci ini' menjadi 'aku tidak akan membiarkan ini lagi'.", "Anonim"),
            ("Rasa jijik melindungi kita dari apa yang tidak sehat.", "Anonim"),
            ("Standar tinggi melindungi dari pengalaman kualitas rendah.", "Ramdhani"),
            ("Jadilah perubahan yang ingin kamu lihat di dunia.", "Mahatma Gandhi"),
            ("Pilih kedamaian daripada drama.", "Anonim"),
            ("Energi negatif itu menular, pakailah masker emosional.", "Anonim"),
            ("Cintai dirimu cukup untuk menetapkan batas.", "Anonim"),
            ("Jangan menjadi tempat sampah bagi emosi orang lain.", "Anonim"),
            ("Kemarahan dan kejijikan adalah energi. Gunakan untuk membangun, bukan menghancurkan.", "Anonim"),
            ("Keanggunan adalah penolakan terhadap hal yang vulgar.", "Coco Chanel"),
            ("Kebaikan adalah respon terbaik terhadap kekasaran.", "Anonim"),
            ("Jangan biarkan perilaku buruk orang lain menghancurkan kedamaian batinmu.", "Dalai Lama"),
            ("Hiduplah sedemikian rupa sehingga kamu menghormati dirimu sendiri.", "Anonim")
        ],
        'Embarrassment': [
            ("Tidak ada yang bisa membuatmu merasa rendah diri tanpa izinmu.", "Eleanor Roosevelt"),
            ("Rasa malu adalah perasaan bahwa ada sesuatu yang salah dengan dirimu. Itu tidak benar.", "Mel Robbins"),
            ("Orang yang tidak pernah melakukan kesalahan tidak pernah mencoba sesuatu yang baru.", "Albert Einstein"),
            ("Berani berarti bersedia menjadi rentan.", "Brené Brown"),
            ("Jangan biarkan rasa malu masa lalu mencuri kedamaian masa kini.", "Rhea"),
            ("Kamu tidak bertanggung jawab atas versi dirimu yang ada di kepala orang lain.", "Anonim"),
            ("Kesalahanmu tidak mendefinisikanmu.", "Anonim"),
            ("Hanya karena kamu gagal, bukan berarti kamu pecundang.", "Marilyn Monroe"),
            ("Hidup dimulai di akhir zona nyamanmu.", "Neale Donald Walsch"),
            ("Kecanggunganku adalah bukti bahwa aku sedang mencoba hal baru.", "Anonim"),
            ("Tertawalah pada kesalahanmu sendiri dan kamu tidak akan pernah kehabisan hiburan.", "Anonim"),
            ("Jangan sembunyikan bekas lukamu, itu bukti kamu sembuh.", "Anonim"),
            ("Rasa malu itu mematikan jiwa. Bunuhlah dengan menertawakannya.", "Rhea"),
            ("Menjadi diri sendiri di dunia yang berusaha menjadikanmu orang lain adalah prestasi terbesar.", "Ralph Waldo Emerson"),
            ("Orang lain terlalu sibuk memikirkan diri mereka sendiri untuk memperhatikan rasa malumu.", "Anonim"),
            ("Rasa malu hanyalah ego yang terluka.", "Anonim"),
            ("Jadilah versi terbaik dari dirimu, bukan versi orang lain.", "Judy Garland"),
            ("Miliki ceritamu, jangan biarkan ceritamu memilikimu.", "Brené Brown"),
            ("Sikap adalah perbedaan kecil yang membuat perbedaan besar.", "Winston Churchill"),
            ("Jangan meminta maaf karena menjadi diri sendiri.", "Anonim"),
            ("Kritik adalah harga yang harus kita bayar untuk sukses.", "W. Clement Stone"),
            ("Fokus pada perbaikan, bukan pada pengakuan.", "Anonim"),
            ("Rasa malu hilang saat kita berbagi cerita.", "Kisi"),
            ("Kegagalan adalah bumbu yang memberi rasa pada kesuksesan.", "Truman Capote"),
            ("Lebih baik dipermalukan karena mencoba daripada menyesal karena diam.", "Anonim"),
            ("Kelemahanmu bisa menjadi kekuatan terbesarmu jika kamu menerimanya.", "Anonim"),
            ("Jangan biarkan opini orang lain menenggelamkan suara hatimu.", "Steve Jobs"),
            ("Malu bertanya sesat di jalan.", "Pepatah Indonesia"),
            ("Jadilah dirimu sendiri; orang lain sudah diambil.", "Oscar Wilde"),
            ("Kepala tegak, hati kuat. Kamu mampu.", "Anonim"),
            ("Jangan malu dengan perjuanganmu. Itu adalah bagian dari ceritamu.", "Alma"),
            ("Rasa malu adalah guru yang keras tapi jujur.", "Anonim"),
            ("Tidak ada orang yang sempurna, itu sebabnya pensil punya penghapus.", "Anonim"),
            ("Berhenti mencari validasi dari orang yang tidak memahami nilaimu.", "Anonim"),
            ("Lupakan kesalahannya, ingat pelajarannya.", "Anonim"),
            ("Kepercayaan diri adalah pakaian terbaik.", "Anonim"),
            ("Rasa malu tidak bisa bertahan di hadapan empati pada diri sendiri.", "Brené Brown"),
            ("Setiap ahli dulunya adalah pemula.", "Robin Sharma"),
            ("Jangan biarkan satu momen canggung merusak harimu.", "Anonim"),
            ("Tumbuh itu menyakitkan dan canggung, tapi itu perlu.", "Anonim"),
            ("Nilai dirimu tidak ditentukan oleh ketidakmampuanmu saat ini.", "Anonim"),
            ("Jika kamu merasa malu, ingatlah bahwa kamu manusia.", "Anonim"),
            ("Keaslian adalah melatih melepaskan siapa yang kita pikir seharusnya kita jadi.", "Brené Brown"),
            ("Jangan takut terlihat bodoh demi menjadi pintar.", "Anonim"),
            ("Orang sukses membangun fondasi dari batu yang dilemparkan pada mereka.", "David Brinkley"),
            ("Rasa malu adalah beban yang tidak perlu kamu bawa.", "Anonim"),
            ("Cintai ketidaksempurnaanmu.", "Anonim"),
            ("Dunia menghargai keberanian, bukan kesempurnaan.", "Simon"),
            ("Bangkitlah di atas rasa malu dan tunjukkan sinarmu.", "Anonim"),
            ("Kamu cukup, apa adanya.", "Meghan Markle")
        ],
        'Ennui': [
            ("Kebosanan adalah panggilan untuk bertindak.", "Tony Robbins"),
            ("Obat untuk kebosanan adalah rasa ingin tahu. Tidak ada obat untuk rasa ingin tahu.", "Dorothy Parker"),
            ("Hanya orang yang membosankan yang merasa bosan.", "Charles Bukowski"),
            ("Hidup tidak pernah membosankan, tetapi beberapa orang memilih untuk bosan.", "Wayne Dyer"),
            ("Kebosanan hanyalah sisi lain dari daya tarik.", "Arthur Schopenhauer"),
            ("Lakukan apa yang kamu bisa, dengan apa yang kamu punya, di mana kamu berada.", "Theodore Roosevelt"),
            ("Kebosanan adalah akar dari semua kejahatan dan juga penemuan.", "Søren Kierkegaard"),
            ("Jangan menunggu inspirasi. Kejarlah dengan tongkat pemukul.", "Jack London"),
            ("Kreativitas adalah kecerdasan yang bersenang-senang.", "Albert Einstein"),
            ("Waktu yang kamu nikmati untuk dihabiskan bukanlah waktu yang terbuang.", "John Lennon"),
            ("Kebosanan adalah sinyal otak bahwa sudah waktunya untuk tumbuh.", "Anonim"),
            ("Dunia penuh dengan hal-hal ajaib yang menunggu indra kita menjadi lebih tajam.", "W.B. Yeats"),
            ("Jadilah penasaran, bukan menghakimi.", "Walt Whitman"),
            ("Jika kamu bosan dengan hidup, kamu tidak memiliki cukup tujuan.", "Lou Holtz"),
            ("Kebosanan adalah perasaan bahwa segalanya membuang-buang waktu; ketenangan, bahwa tidak ada yang demikian.", "Thomas Szasz"),
            ("Ubah rutinitasmu, ubah hidupmu.", "Anonim"),
            ("Petualangan terbaik ada di dalam pikiranmu.", "Anonim"),
            ("Jangan biarkan hari kemarin menyita terlalu banyak hari ini.", "Will Rogers"),
            ("Kebosanan melahirkan kreativitas.", "Anonim"),
            ("Temukan kegembiraan dalam hal-hal biasa.", "Anonim"),
            ("Jelajahi, bermimpi, temukan.", "Mark Twain"),
            ("Diam bukan berarti kosong, itu penuh jawaban.", "Anonim"),
            ("Ketika kamu bosan, belajarlah sesuatu yang baru.", "Anonim"),
            ("Hidup adalah petualangan yang berani atau tidak sama sekali.", "Helen Keller"),
            ("Kebosanan adalah awal dari setiap karya seni otentik.", "Friedrich Nietzsche"),
            ("Jangan hanya menghitung hari, buatlah hari itu berarti.", "Muhammad Ali"),
            ("Mulailah di mana kamu berada.", "Anonim"),
            ("Inspirasi ada di mana-mana jika kamu membuka mata.", "Anonim"),
            ("Rasa bosan adalah undangan untuk berimajinasi.", "Anonim"),
            ("Bergeraklah, buatlah riak di air yang tenang.", "Bruno"),
            ("Kebosanan adalah tanda kurangnya imajinasi.", "Anonim"),
            ("Setiap momen adalah awal yang baru.", "T.S. Eliot"),
            ("Carilah keajaiban di sekitarmu.", "Anonim"),
            ("Kebosanan adalah penyakit orang yang bahagia.", "Abel Dufresne"),
            ("Isi hidupmu dengan pengalaman, bukan barang.", "Anonim"),
            ("Berhenti scroll, mulai buat.", "Anonim"),
            ("Jika kamu tidak menyukai di mana kamu berada, pindahlah. Kamu bukan pohon.", "Jim Rohn"),
            ("Tindakan adalah kunci dasar untuk semua kesuksesan.", "Pablo Picasso"),
            ("Bosan? Baca buku.", "Anonim"),
            ("Dunia ini terlalu besar untuk diam di satu tempat.", "Anonim"),
            ("Antusiasme adalah listrik kehidupan.", "Gordon Parks"),
            ("Masa depan milik mereka yang percaya pada keindahan mimpi mereka.", "Eleanor Roosevelt"),
            ("Kebosanan hilang saat kamu punya tujuan.", "Anonim"),
            ("Jadilah pahlawan dalam hidupmu sendiri.", "Ibnu"),
            ("Jangan mati sebelum kamu benar-benar hidup.", "Anonim"),
            ("Kebosanan adalah debu di lensa kehidupan. Bersihkan.", "Anonim"),
            ("Ciptakan keseruanmu sendiri.", "Anonim"),
            ("Rasa ingin tahu adalah sumbu dalam lilin pembelajaran.", "William Arthur Ward"),
            ("Bangun dan wujudkan mimpimu.", "Anonim"),
            ("Hidup itu singkat, jangan habiskan dengan mengeluh bosan.", "Anonim")
        ]
    }

    def select_mood(self, mood):
        """Saat tombol mood diklik"""
        self.is_card_open = False
        
        # Mapping warna border kartu sesuai mood
        colors = {
            'Anger': [1, 0.4, 0.4, 1],         # Merah
            'Anxiety': [1, 0.85, 0.2, 1],      # Orange/Kuning
            'Joy': [1, 0.96, 0.6, 1],          # Kuning Pucat
            'Sadness': [0.5, 0.8, 1, 1],       # Biru
            'Envy': [0.5, 0.8, 0.7, 1],        # Teal
            'Fear': [0.8, 0.6, 0.8, 1],        # Ungu
            'Disgust': [0.6, 0.8, 0.6, 1],     # Hijau
            'Embarrassment': [0.9, 0.6, 0.7, 1], # Pink
            'Ennui': [0.6, 0.6, 0.8, 1]        # Indigo
        }
        self.current_theme_color = colors.get(mood, [0,0,0,1])
        self.current_mood = mood

        # Animasi Grid Keluar (Turun)
        anim_grid = Animation(pos_hint={'center_y': -0.5}, opacity=0, duration=0.4, t='in_back')
        anim_grid.start(self.ids.mood_selection_area)

        # Animasi Kartu Masuk (Naik)
        self.ids.cover_text.opacity = 1
        self.ids.content_box.opacity = 0
        self.ids.card_area.opacity = 1
        
        anim_card = Animation(pos_hint={'center_y': 0.5}, duration=0.5, t='out_back')
        anim_card.start(self.ids.card_area)

    def reveal_card(self):
        """Saat kartu diklik (Flip Effect)"""
        if self.is_card_open:
            return
        
        self.is_card_open = True
        
        # Ambil data random
        quotes = self.quotes_db.get(self.current_mood, [("Tetap Semangat!", "Admin")])
        text, author = random.choice(quotes)
        
        self.ids.quote_text.text = f'"{text}"'
        self.ids.author_text.text = f"- {author}"

        # Animasi Flip (Menipis lalu melebar)
        card = self.ids.magic_card
        anim = Animation(size_hint_x=0.01, duration=0.15)
        
        def on_half_flip(anim, widget):
            self.ids.cover_text.opacity = 0
            self.ids.content_box.opacity = 1
            
            anim_back = Animation(size_hint_x=1, duration=0.15)
            anim_back.start(widget)
            
            # Munculkan tombol reset
            self.ids.reset_btn.disabled = False
            anim_btn = Animation(opacity=1, duration=0.5)
            anim_btn.start(self.ids.reset_btn)

        anim.bind(on_complete=on_half_flip)
        anim.start(card)

    def reset_view(self):
        """Kembali ke pilihan mood"""
        # Kartu Turun
        anim_card = Animation(pos_hint={'center_y': -0.8}, opacity=0, duration=0.4, t='in_back')
        anim_card.start(self.ids.card_area)
        
        # Grid Naik
        anim_grid = Animation(pos_hint={'center_y': 0.45}, opacity=1, duration=0.4, t='out_back')
        anim_grid.start(self.ids.mood_selection_area)
        
        self.ids.reset_btn.opacity = 0
        self.ids.reset_btn.disabled = True

    def go_back(self):
        print("Back to Menu")
        self.manager.current = 'menu'