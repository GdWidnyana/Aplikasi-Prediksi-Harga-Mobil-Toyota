import pickle
import streamlit as st
import time
import pandas as pd
import matplotlib.pyplot as plt


# Load the trained model
modelLR = pickle.load(open('LinearRegressionModel.pkl', 'rb'))

st.set_page_config(page_title="WebApp Prediksi Harga Mobil", page_icon="🚗")

# Center-align the title using CSS
st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Use the centered-title CSS class for the title
st.markdown("<h1 class='centered-title'>Aplikasi Prediksi Harga Mobil Toyota</h1>", unsafe_allow_html=True)
st.image('mobil.png', use_column_width=True)

# Dictionary mapping for encoded model values to actual model names
model_mapping = {
    0: 'GT86',
    1: 'Corolla',
    2: 'RAV4',
    3: 'Yaris',
    4: 'Auris',
    5: 'Aygo',
    6: 'C-HR',
    7: 'Prius',
    8: 'Avensis',
    9: 'Verso',
    10: 'Hilux',
    11: 'PROACE VERSO',
    12: 'Land Cruiser',
    13: 'Supra',
    14: 'Camry',
    15: 'Verso-S',
    16: 'IQ',
    17: 'Urban Cruiser'
}

transmission_mapping = {
    0: 'Manual',
    1: 'Automatic',
    2: 'Semi-Auto',
    3: 'Other',
}

fuelType_mapping = {
    0: 'Petrol',
    1: 'Other',
    2: 'Hybrid',
    3: 'Diesel',
}

# Input fields
model = st.selectbox('Input Nama Model Mobil', list(model_mapping.keys()), format_func=lambda x: f"Kode: {x} ➡️ {model_mapping[x]}")
year = st.number_input('Input Tahun Keluaran Mobil', min_value=0, step=1, format="%d")
transmission = st.selectbox('Input Jenis Transmisi Mobil ', list(transmission_mapping.keys()), format_func=lambda x: f"Kode: {x} ➡️ {transmission_mapping[x]}")
mileage = st.number_input('Input Jarak Tempuh Mobil (Kilometer)')
fuelType = st.selectbox('Input Jenis Bahan Bakar Mobil', list(fuelType_mapping.keys()), format_func=lambda x: f"Kode: {x} ➡️ {fuelType_mapping[x]}")
tax = st.number_input('Input Biaya Pajak Mobil (Euro)')
mpg = st.number_input('Input Konsumsi BBM Mobil (Liter)')
engineSize = st.number_input('Input Engine Size Mobil')

# Format number with dots as thousands separator
def format_number_with_dots(number):
    integer_value = int(number)
    return "{:,}".format(integer_value).replace(",", ".")

if st.button('Prediksi Harga Mobil', key='predict_button'):
    if year == 0 or mileage == 0 or tax == 0 or mpg == 0 or engineSize == 0:
        st.warning("Input data terlebih dahulu")
    else:
        # Create input data DataFrame
        input_data = pd.DataFrame({
            'model': [model],
            'year': [year],
            'transmission': [transmission],
            'mileage': [mileage],
            'fuelType': [fuelType],
            'tax': [tax],
            'mpg': [mpg],
            'engineSize': [engineSize]
        })

        # Process prediction
        with st.empty():
            st.info("Sedang memproses prediksi...")
            with st.spinner():
                time.sleep(2)
            st.success("Selesai!")
            time.sleep(1)

        predict = modelLR.predict(input_data)
        predicted_price_in_rupiah = predict[0] * 16741

        st.write('Prediksi Harga Mobil dalam EURO adalah', format_number_with_dots(predict[0]))
        st.write('Prediksi Harga Mobil dalam Rupiah adalah', format_number_with_dots(predicted_price_in_rupiah))

        formatted_price = format_number_with_dots(predicted_price_in_rupiah)
        st.success(f"Kesimpulan: Prediksi harga mobil berdasarkan data di atas adalah Rp {formatted_price}.")
        st.snow()
        
st.image('mobil.png', use_column_width=True)

# Jika Anda membaca dataset dari CSV
data = pd.read_csv('toyota.csv')


# Pilihan visualisasi
visualization_option = st.selectbox("Pilih Visualisasi:", ["Distribusi Data", "Hubungan dengan Harga"])

if visualization_option == "Distribusi Data":
    st.subheader("Distribusi Tahun Keluaran Mobil")
    plt.figure(figsize=(10, 6))
    plt.hist(data['year'], bins=20, density=True, alpha=0.6, color='blue')
    plt.xlabel('Tahun Keluaran')
    plt.ylabel('Frekuensi')
    plt.title('Distribusi Tahun Keluaran Mobil')
    st.pyplot()

    st.subheader("Distribusi Jenis Transmisi Mobil")
    plt.figure(figsize=(8, 5))
    plt.bar(data['transmission'].value_counts().index, data['transmission'].value_counts().values)
    plt.xlabel('Jenis Transmisi')
    plt.ylabel('Frekuensi')
    plt.title('Distribusi Jenis Transmisi Mobil')
    st.pyplot()

    st.subheader("Distribusi Jenis Bahan Bakar Mobil")
    plt.figure(figsize=(8, 5))
    plt.bar(data['fuelType'].value_counts().index, data['fuelType'].value_counts().values)
    plt.xlabel('Jenis Bahan Bakar')
    plt.ylabel('Frekuensi')
    plt.title('Distribusi Jenis Bahan Bakar Mobil')
    st.pyplot()

    # ... (Visualisasi lainnya) ...

elif visualization_option == "Hubungan dengan Harga":
    st.subheader("Hubungan Antara Tahun Keluaran dan Harga")
    plt.figure(figsize=(10, 6))
    plt.scatter(data['year'], data['price'], alpha=0.5)
    plt.xlabel('Tahun Keluaran')
    plt.ylabel('Harga')
    plt.title('Hubungan Antara Tahun Keluaran dan Harga')
    st.pyplot()

    st.subheader("Hubungan Antara Jenis Transmisi dan Harga")
    plt.figure(figsize=(8, 5))
    transmission_avg_price = data.groupby('transmission')['price'].mean()
    plt.bar(transmission_avg_price.index, transmission_avg_price.values)
    plt.xlabel('Jenis Transmisi')
    plt.ylabel('Rata-rata Harga')
    plt.title('Hubungan Antara Jenis Transmisi dan Harga')
    st.pyplot()

    st.subheader("Hubungan Antara Jenis Bahan Bakar dan Harga")
    plt.figure(figsize=(8, 5))
    fuelType_avg_price = data.groupby('fuelType')['price'].mean()
    plt.bar(fuelType_avg_price.index, fuelType_avg_price.values)
    plt.xlabel('Jenis Bahan Bakar')
    plt.ylabel('Rata-rata Harga')
    plt.title('Hubungan Antara Jenis Bahan Bakar dan Harga')
    st.pyplot()

    # ... (Visualisasi lainnya) ...
# Background image styling
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://images.unsplash.com/photo-1483401757487-2ced3fa77952?ixlib=rb-4.0.3");
             background-attachment: fixed;
             background-size: cover;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()

st.set_option('deprecation.showPyplotGlobalUse', False)
