import streamlit as st
from FSM import FashionFSM

# Konfigurasi Halaman
st.set_page_config(page_title="FashionBot", page_icon="👕", layout="centered")

# Custom CSS untuk Premium Dark Glassmorphism Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

    /* Global styles */
    .stApp, html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Outfit', sans-serif;
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%) !important;
        color: #f8fafc !important;
    }
    
    /* Header and titles */
    h1 {
        text-align: center;
        font-family: 'Outfit', sans-serif !important;
        background: linear-gradient(90deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    h2, h3, h4, h5, h6, p, label {
        font-family: 'Outfit', sans-serif !important;
        color: #f8fafc !important;
    }

    /* Style Streamlit Chat Messages */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 16px !important;
        padding: 1rem !important;
        margin-bottom: 1rem !important;
        backdrop-filter: blur(12px) !important;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.15) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        animation: fadeIn 0.5s ease-out;
    }

    [data-testid="stChatMessage"]:hover {
        border-color: rgba(255, 255, 255, 0.12) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25) !important;
        transform: translateY(-2px);
    }
    
    /* Chat Input styling */
    [data-testid="stChatInput"] {
        border-radius: 24px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background-color: rgba(15, 23, 42, 0.6) !important;
        backdrop-filter: blur(8px) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
    }
    
    [data-testid="stChatInput"] textarea {
        color: #f8fafc !important;
        font-family: 'Outfit', sans-serif !important;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

st.write("# 👕 FashionBot")

if "fsm" not in st.session_state:
    st.session_state.fsm = FashionFSM()

# Pesan sambutan tanpa "(Kampus, Kerja, Pesta)"
welcome_content = (
    "Selamat datang di **FashionBot**! 👕\n\n"
    "Saya asisten fashion pribadi berbasis otomata yang siap merekomendasikan "
    "padu padan pakaian terbaik untuk berbagai kegiatan Anda.\n\n"
    "Silakan ketik **halo** atau **hai** untuk mulai menyapa!"
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": welcome_content,
            "image": None
        }
    ]

if "saved_outfits" not in st.session_state:
    st.session_state.saved_outfits = {}
    # Rekonstruksi wardrobe dari riwayat pesan yang ada
    for msg in st.session_state.messages:
        if msg["role"] == "assistant" and msg.get("image"):
            title = msg["content"].strip().split("\n")[0]
            st.session_state.saved_outfits[title] = {
                "text": msg["content"],
                "image": msg["image"]
            }

# Fungsi kirim input yang DRY
def send_input(user_input):
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    response = st.session_state.fsm.process(user_input)
    
    if isinstance(response, dict):
        response_text = response.get("text", "")
        response_image = response.get("image", None)
        
        # Simpan ke lemari pakaian jika ada rekomendasi outfit visual
        if response_image:
            title = response_text.strip().split("\n")[0]
            st.session_state.saved_outfits[title] = {
                "text": response_text,
                "image": response_image
            }
    else:
        response_text = str(response)
        response_image = None

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response_text,
            "image": response_image
        }
    )
    st.rerun()

# Sidebar untuk Pengaturan & Lemari Pakaian
with st.sidebar:
    st.header("⚙️ Pengaturan")
    st.write("Gunakan tombol di bawah untuk mereset status mesin otomata & percakapan.")
    if st.button("Reset Chat", use_container_width=True):
        st.session_state.fsm = FashionFSM()
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": welcome_content,
                "image": None
            }
        ]
        st.session_state.saved_outfits = {}
        st.rerun()

    st.markdown("---")
    st.header("👚 Lemari Pakaian")
    st.write("Daftar outfit yang telah Anda temukan dalam obrolan:")
    if not st.session_state.saved_outfits:
        st.info("Lemari pakaian Anda kosong. Pilih outfit di obrolan untuk menyimpannya!")
    else:
        for title, outfit in st.session_state.saved_outfits.items():
            with st.expander(title, expanded=False):
                st.write(outfit["text"])
                if outfit["image"]:
                    st.image(outfit["image"], use_container_width=True)

# Menampilkan Riwayat Pesan
for message in st.session_state.messages:
    role = message["role"]
    avatar = "😎" if role == "user" else "👕"
    
    with st.chat_message(role, avatar=avatar):
        st.write(message["content"])
        if "image" in message and message["image"]:
            st.image(message["image"], caption="Rekomendasi Outfit Anda", use_container_width=True)

# Tampilkan tombol opsi interaktif sesuai status FSM saat ini (Quick Replies)
current_state = st.session_state.fsm.state
if current_state == "ASK_EVENT":
    st.write("Pilih salah satu acara:")
    cols1 = st.columns(3)
    if cols1[0].button("🏫 Kampus", use_container_width=True):
        send_input("kampus")
    if cols1[1].button("💼 Kerja", use_container_width=True):
        send_input("kerja")
    if cols1[2].button("🎉 Pesta", use_container_width=True):
        send_input("pesta")
        
    cols2 = st.columns(2)
    if cols2[0].button("☕ Nongkrong", use_container_width=True):
        send_input("nongkrong")
    if cols2[1].button("📝 Seminar", use_container_width=True):
        send_input("seminar")
        
elif current_state == "ASK_WEATHER":
    cols = st.columns(2)
    if cols[0].button("☀️ Panas", use_container_width=True):
        send_input("panas")
    if cols[1].button("❄️ Dingin", use_container_width=True):
        send_input("dingin")
elif current_state == "ASK_GENDER":
    cols = st.columns(2)
    if cols[0].button("👨 Pria", use_container_width=True):
        send_input("pria")
    if cols[1].button("👩 Wanita", use_container_width=True):
        send_input("wanita")
elif current_state == "ASK_COLOR":
    cols = st.columns(2)
    if cols[0].button("⚪ Putih", use_container_width=True):
        send_input("putih")
    if cols[1].button("⚫ Hitam", use_container_width=True):
        send_input("hitam")
elif current_state == "SHOW_OUTFIT":
    if st.button("🏁 Selesai", use_container_width=True):
        send_input("selesai")
elif current_state == "ASK_LOOP":
    cols = st.columns(2)
    if cols[0].button("👍 Ingin", use_container_width=True):
        send_input("ingin")
    if cols[1].button("👎 Tidak", use_container_width=True):
        send_input("tidak")

user_input = st.chat_input("Ketik pesan...")
if user_input:
    send_input(user_input)