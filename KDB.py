import base64
import streamlit as st
import pandas as pd
from datetime import datetime

# Function to load image as base64
@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Replace 'nyoba.png' with the path to your PNG file
img_base64 = get_img_as_base64("BG2.png")
img_base65 = get_img_as_base64("sidebar1.png")

# Use base64 image data as background
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url('data:image/png;base64,{img_base64}');
    background-size: cover;
}}

[data-testid="stHeader"]  {{ 
    background-color: rgba(0, 0, 0, 0)
}}


[data-testid="stSidebar"] {{
    background-image: url('data:image/png;base64,{img_base65}');
    background-size: cover;
}}

</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


# Sidebar for navigation
st.sidebar.title("Navigasi")
page = st.sidebar.radio("Pilih halaman", ["Dashboard", "Kalkulator Diet & Bulking", "Progress Tracker", "Database", "Komunitas"])

# Initialize session state for storing user data and subpage status
if "calculator_data" not in st.session_state:
    st.session_state.calculator_data = []

if "progress_data" not in st.session_state:
    st.session_state.progress_data = []

if "show_result" not in st.session_state:
    st.session_state.show_result = False

# Function to calculate age from date of birth
def calculate_age(birth_date):
    today = datetime.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

# Dashboard page
if page == "Dashboard":
    st.title("Selamat datang di aplikasi saya")
    st.write("Ini adalah aplikasi untuk menghitung kebutuhan tubuh Anda untuk diet dan bulking.")
    st.write("Gunakan navigasi di samping untuk berpindah halaman.")

    # Kutipan Motivasi
    st.markdown("---")
    st.subheader("Kutipan Motivasi")
    st.write("“Mulailah hari ini dengan tekad yang baru, dan jadilah orang yang lebih sehat besok.”")

    # Fakta Menarik
    st.markdown("---")
    st.subheader("Fakta Menarik")
    st.write("Fakta: Jus wortel dapat membantu memperbaiki penglihatan malam.")

    # Tips Sehat
    st.markdown("---")
    st.subheader("Tips Sehat")
    st.write("Tip: Minumlah setidaknya 8 gelas air putih setiap hari.")

# Kalkulator Diet & Bulking page
if page == "Kalkulator Diet & Bulking":
    if not st.session_state.show_result:
        st.title("Kalkulator Diet & Bulking")

        # User inputs
        name = st.text_input("Nama")
        birth_date = st.date_input("Tanggal Lahir", min_value=datetime(1900, 1, 1), max_value=datetime.today())
        gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])

        height = st.number_input("Tinggi Badan (cm)", min_value=0.0, max_value=250.0, step=0.1)
        weight = st.number_input("Berat Badan (kg)", min_value=0.0, max_value=300.0, step=0.1)

        # Input for activity level
        activity_level = st.selectbox(
            "Pilih tingkat intensitas aktivitas fisik Anda",
            ["Sangat sedikit atau tidak ada aktivitas", 
             "Aktivitas ringan (olahraga ringan/sedang 1-3 hari/minggu)",
             "Aktivitas sedang (olahraga sedang 3-5 hari/minggu)",
             "Aktivitas tinggi (olahraga intensif 6-7 hari/minggu)",
             "Aktivitas sangat tinggi (olahraga intensif dan pekerjaan fisik yang sangat berat)"]
        )

        goal = st.selectbox("Pilih Tujuan", ["Diet", "Bulking"])

        # Button to calculate
        if st.button("HITUNG"):
            if name and birth_date and height and weight and activity_level and goal:
                # Calculate age from birth date
                age = calculate_age(birth_date)

                # Calculate needs based on input
                if goal == "Diet":
                    base_calories = weight * 25
                    protein_needs = weight * 1.2
                    carb_needs = weight * 2.5
                    fat_needs = weight * 0.8
                else:  # Bulking
                    base_calories = weight * 35
                    protein_needs = weight * 1.5
                    carb_needs = weight * 3.5
                    fat_needs = weight * 1.0

                # Adjust calories based on activity level
                if activity_level == "Sangat sedikit atau tidak ada aktivitas":
                    calorie_multiplier = 1.2
                elif activity_level == "Aktivitas ringan (olahraga ringan/sedang 1-3 hari/minggu)":
                    calorie_multiplier = 1.375
                elif activity_level == "Aktivitas sedang (olahraga sedang 3-5 hari/minggu)":
                    calorie_multiplier = 1.55
                elif activity_level == "Aktivitas tinggi (olahraga intensif 6-7 hari/minggu)":
                    calorie_multiplier = 1.725
                else:  # Aktivitas sangat tinggi
                    calorie_multiplier = 1.9

                calorie_needs = base_calories * calorie_multiplier

                # Check body condition
                if goal == "Diet" and weight < height - 100:
                    body_condition = "maaf tubuh anda tidak berada di fase normal, disarankan untuk Bulking saja"
                elif goal == "Bulking" and weight > height - 100:
                    body_condition = "maaf tubuh anda tidak berada di fase normal, disarankan untuk Diet saja"
                else:
                    body_condition = "tubuh anda berada di fase normal"

                # Save data to session state
                st.session_state.calculator_data.append({
                    "Nama": name,
                    "Tanggal Lahir": birth_date,
                    "Umur": age,
                    "Jenis Kelamin": gender,
                    "Tinggi Badan": height,
                    "Berat Badan": weight,
                    "Tingkat Aktivitas": activity_level,
                    "Tujuan": goal,
                    "Kalori": calorie_needs,
                    "Protein": protein_needs,
                    "Karbohidrat": carb_needs,
                    "Lemak": fat_needs,
                    "Kondisi Tubuh": body_condition
                })

                # Show result page
                st.session_state.show_result = True
    else:
        # Result page
        st.title("Hasil Perhitungan")
        if st.session_state.calculator_data:
            user_data = st.session_state.calculator_data[-1]

            st.subheader(f"Kebutuhan Tubuh untuk {user_data['Tujuan']}")
            st.write(f"Nama: {user_data['Nama']}")
            st.write(f"Tanggal Lahir: {user_data['Tanggal Lahir']}")
            st.write(f"Umur: {user_data['Umur']} tahun")
            st.write(f"Jenis Kelamin: {user_data['Jenis Kelamin']}")
            st.write(f"Tinggi Badan: {user_data['Tinggi Badan']} cm")
            st.write(f"Berat Badan: {user_data['Berat Badan']} kg")
            st.write(f"Kalori yang dibutuhkan: {user_data['Kalori']:.2f} kalori")
            st.write(f"Protein yang dibutuhkan: {user_data['Protein']:.2f} gram")
            st.write(f"Karbohidrat kompleks yang dibutuhkan: {user_data['Karbohidrat']:.2f} gram")
            st.write(f"Lemak sehat yang dibutuhkan: {user_data['Lemak']:.2f} gram")
            st.write(f"Kondisi Tubuh: {user_data['Kondisi Tubuh']}")

            st.subheader("Rekomendasi Makanan dan Minuman Sehat")
            if user_data['Tujuan'] == "Diet":
                st.write("- Sayuran hijau (bayam, brokoli)")
                st.write("- Buah-buahan (apel, berries)")
                st.write("- Ikan tanpa lemak (salmon, tuna)")
                st.write("- Yogurt rendah lemak")
            else:  # Bulking
                st.write("- Daging merah (sapi, ayam)")
                st.write("- Susu dan produk olahan susu")
                st.write("- Kacang-kacangan dan biji-bijian")
                st.write("- Nasi merah atau pasta gandum")

            st.subheader("Rekomendasi Olahraga Sehat")
            if user_data['Tujuan'] == "Diet":
                st.write("- Jogging")
                st.write("- Bersepeda")
                st.write("- Yoga")
                st.write("- Pilates")
            else:  # Bulking
                st.write("- Angkat beban")
                st.write("- Latihan kekuatan")
                st.write("- Push-up")
                st.write("- Pull-up")

            st.subheader("Rekomendasi Resep")
            if user_data['Tujuan'] == "Diet":
                st.write("- Salad bayam dengan ayam panggang")
                st.write("- Smoothie buah dengan yogurt rendah lemak")
                st.write("- Sup sayuran dengan quinoa")
            else:  # Bulking
                st.write("- Steak sapi dengan kentang manis")
                st.write("- Smoothie protein dengan pisang dan susu")
                st.write("- Omelet dengan sayuran dan keju")

            st.subheader("Rekomendasi Tambahan")
            st.write("Pastikan Anda mendapatkan cukup serat setiap hari, minum air yang cukup, dan mengonsumsi makanan yang kaya akan vitamin dan mineral. Jangan lupa untuk beristirahat yang cukup dan menjaga keseimbangan hormon dengan pola hidup yang sehat.")

            if st.button("Kembali"):
                st.session_state.show_result = False

# Progress Tracker page
if page == "Progress Tracker":
    st.title("Progress Tracker")
    st.write("Lacak kemajuan diet dan bulking Anda di sini.")
    
    if st.session_state.calculator_data:
        user_data = st.session_state.calculator_data[-1]
        
        st.write(f"Nama: {user_data['Nama']}")
        st.write(f"Umur: {user_data['Umur']} tahun")
        st.write(f"Tinggi Badan: {user_data['Tinggi Badan']} cm")
        st.write(f"Berat Badan: {user_data['Berat Badan']} kg")
        st.write(f"Tujuan: {user_data['Tujuan']}")

        progress_weight = st.number_input("Perubahan Berat Badan (kg)", min_value=-50.0, max_value=50.0, step=0.1)
        progress_note = st.text_area("Catatan Kemajuan", help="Masukkan catatan kemajuan Anda di sini. Tidak ada auto-correction.")
        
        if st.button("Simpan Progress"):
            st.session_state.progress_data.append({
                "Nama": user_data["Nama"],
                "Tanggal Lahir": user_data["Tanggal Lahir"],
                "Umur": user_data["Umur"],
                "Tinggi Badan": user_data["Tinggi Badan"],
                "Berat Badan": user_data["Berat Badan"] + progress_weight,
                "Tingkat Aktivitas": user_data["Tingkat Aktivitas"],
                "Tujuan": user_data["Tujuan"],
                "Kalori": user_data["Kalori"],
                "Protein": user_data["Protein"],
                "Karbohidrat": user_data["Karbohidrat"],
                "Lemak": user_data["Lemak"],
                "Progress Weight": progress_weight,
                "Progress Note": progress_note
            })
            st.success("Progress berhasil disimpan!")

        # Pengingat Waktu Makan
        st.markdown("---")
        st.subheader("Pengingat Waktu Makan")
        st.write("Waktu Makan: Sarapan - 07:00, Makan Siang - 12:00, Makan Malam - 18:00")

        # Pengingat Aktivitas Fisik
        st.markdown("---")
        st.subheader("Pengingat Aktivitas Fisik")
        st.write("Aktivitas Fisik: Berolahraga ringan selama 30 menit setiap hari.")

# Database page
if page == "Database":
    st.title("Database")
    
    st.subheader("Database Kalkulator Diet dan Bulking")
    if st.session_state.calculator_data:
        df_calculator = pd.DataFrame(st.session_state.calculator_data)
        st.write(df_calculator)

    st.subheader("Database Progress Tracker")
    if st.session_state.progress_data:
        df_progress = pd.DataFrame(st.session_state.progress_data)
        st.write(df_progress)

# Community page
if page == "Komunitas":
    st.title("Komunitas")
    st.write("Bergabunglah dengan komunitas untuk berbagi tips, cerita sukses, dan saling mendukung.")
    
    st.subheader("Forum Diskusi")
    st.text_area("Tulis pesan Anda di sini...")
    if st.button("Kirim"):
        st.success("Pesan terkirim!")
