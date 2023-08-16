import pickle
import streamlit as st
import time
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

modelLR = pickle.load(open('LinearRegressionModel.pkl', 'rb'))

st.set_page_config(page_title="WebApp Prediksi Harga Mobil", page_icon="🚗")

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

st.markdown("<h1 class='centered-title'>Aplikasi Prediksi Harga Mobil Toyota</h1>", unsafe_allow_html=True)
st.image('mobil.png', use_column_width=True)

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

model = st.selectbox('Input Nama Model Mobil', list(model_mapping.keys()), format_func=lambda x: f"Kode: {x} ➡️ {model_mapping[x]}")
year = st.number_input('Input Tahun Keluaran Mobil', min_value=0, step=1, format="%d")
transmission = st.selectbox('Input Jenis Transmisi Mobil ', list(transmission_mapping.keys()), format_func=lambda x: f"Kode: {x} ➡️ {transmission_mapping[x]}")
mileage = st.number_input('Input Jarak Tempuh Mobil (Kilometer)')
fuelType = st.selectbox('Input Jenis Bahan Bakar Mobil', list(fuelType_mapping.keys()), format_func=lambda x: f"Kode: {x} ➡️ {fuelType_mapping[x]}")
tax = st.number_input('Input Biaya Pajak Mobil (Euro)')
mpg = st.number_input('Input Konsumsi BBM Mobil (Liter)')
engineSize = st.number_input('Input Engine Size Mobil')

def format_number_with_dots(number):
    integer_value = int(number)
    return "{:,}".format(integer_value).replace(",", ".")

if st.button('Prediksi Harga Mobil', key='predict_button'):
    if year == 0 or mileage == 0 or tax == 0 or mpg == 0 or engineSize == 0:
        st.warning("Input data terlebih dahulu")
    else:
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

data = pd.read_csv('toyota.csv')

visualization_option = st.selectbox("Pilih Visualisasi:", ["Dashboard", "Distribusi Data", "Hubungan dengan Harga"])

if visualization_option == "Dashboard":
    selected_year = st.sidebar.slider("Select Year", int(data["year"].min()), int(data["year"].max()))
    transmission_options = data["transmission"].unique()
    selected_transmission = st.sidebar.selectbox("Select Transmission", transmission_options)
    fuel_type_options = data["fuelType"].unique()
    selected_fuel_type = st.sidebar.selectbox("Select Fuel Type", fuel_type_options)

    filtered_data = data[
        (data["year"] == selected_year) &
        (data["transmission"] == selected_transmission) &
        (data["fuelType"] == selected_fuel_type)
    ]

    st.write("Filtered Data:")
    st.write(filtered_data)

    scatter_plot = alt.Chart(filtered_data).mark_circle().encode(
        x='price',
        y='mileage',
        tooltip=['price', 'mileage']
    ).properties(
        width=600,
        height=400
    )
    st.write("Scatter Plot of Price vs Mileage:")
    st.altair_chart(scatter_plot)

    avg_price_by_mil = filtered_data.groupby ("mileage")["price"].mean()
    st.write("Average Price by Mileage:")
    st.bar_chart(avg_price_by_mil)
    
    avg_price_by_fuel = filtered_data.groupby ("fuelType")["price"].mean()
    st.write("Average Price by Fuel Type:")
    st.bar_chart(avg_price_by_fuel)
    
    avg_price_by_trans = filtered_data.groupby ("transmission")["price"].mean()
    st.write("Average Price by Transmission:")
    st.bar_chart(avg_price_by_trans)
    
    avg_price_by_tax = filtered_data.groupby ("tax")["price"].mean()
    st.write("Average Price by Tax in Euro:")
    st.bar_chart(avg_price_by_tax)
    
    avg_price_by_mpg = filtered_data.groupby ("mpg")["price"].mean()
    st.write("Average Price by MPG:")
    st.bar_chart(avg_price_by_mpg)
    
    avg_price_by_engineSize = filtered_data.groupby ("engineSize")["price"].mean()
    st.write("Average Price by Engine Size:")
    st.bar_chart(avg_price_by_engineSize)

if visualization_option == "Distribusi Data":
    st.subheader("Distribusi Model Mobil")
    plt.figure(figsize=(12, 6))
    plt.bar(data['model'].value_counts().index, data['model'].value_counts().values)
    plt.xlabel('Model Mobil')
    plt.ylabel('Frekuensi')
    plt.title('Distribusi Model Mobil')
    plt.xticks(rotation=45)
    st.pyplot()
    
    st.subheader("Distribusi Tahun Keluaran Mobil")
    plt.figure(figsize=(25, 6))
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
    
    st.subheader("Distribusi Jarak Tempuh Mobil")
    plt.figure(figsize=(10, 6))
    plt.hist(data['mileage'], bins=20, density=True, alpha=0.6, color='blue')
    plt.xlabel('Jarak Tempuh')
    plt.ylabel('Frekuensi')
    plt.title('Distribusi Jarak Tempuh Mobil')
    st.pyplot()

    st.subheader("Distribusi Jenis Bahan Bakar Mobil")
    plt.figure(figsize=(8, 5))
    plt.bar(data['fuelType'].value_counts().index, data['fuelType'].value_counts().values)
    plt.xlabel('Jenis Bahan Bakar')
    plt.ylabel('Frekuensi')
    plt.title('Distribusi Jenis Bahan Bakar Mobil')
    st.pyplot()
    
    st.subheader("Distribusi Biaya Pajak Mobil (Euro)")
    plt.figure(figsize=(10, 6))
    plt.hist(data['tax'], bins=20, density=True, alpha=0.6, color='green')
    plt.xlabel('Biaya Pajak (€)')
    plt.ylabel('Frekuensi')
    plt.title('Distribusi Biaya Pajak Mobil')
    st.pyplot()
    
    st.subheader("Distribusi Konsumsi BBM Mobil")
    plt.figure(figsize=(10, 6))
    plt.hist(data['mpg'], bins=20, density=True, alpha=0.6, color='purple')
    plt.xlabel('Konsumsi BBM')
    plt.ylabel('Frekuensi')
    plt.title('Distribusi Konsumsi BBM Mobil')
    st.pyplot()
    
    st.subheader("Distribusi Engine Size Mobil")
    plt.figure(figsize=(10, 6))
    plt.hist(data['engineSize'], bins=20, density=True, alpha=0.6, color='orange')
    plt.xlabel('Engine Size')
    plt.ylabel('Frekuensi')
    plt.title('Distribusi Engine Size Mobil')
    st.pyplot()

elif visualization_option == "Hubungan dengan Harga":
    
    st.subheader("Hubungan antara Model dan Harga Mobil (€)")
    plt.figure(figsize=(20, 10))
    model_avg_price = data.groupby('model')['price'].mean()
    bars = plt.bar(model_avg_price.index, model_avg_price.values)
    plt.xlabel('Jenis Model')
    plt.ylabel('Rata-rata Harga (€)')
    plt.title('Hubungan Antara Model Mobil dan Harga Mobil (€)')

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom', fontsize=8)
    st.pyplot()
    
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
    
    st.subheader("Hubungan antara Jarak Tempuh dan Harga Mobil (€)")
    plt.figure(figsize=(10, 6))
    plt.scatter(data['mileage'], data['price'], alpha=0.6, color='red')
    plt.xlabel('Jarak Tempuh')
    plt.ylabel('Harga Mobil (€)')
    plt.title('Hubungan antara Jarak Tempuh dan Harga Mobil (€)')
    st.pyplot()

    st.subheader("Hubungan Antara Jenis Bahan Bakar dan Harga")
    plt.figure(figsize=(8, 5))
    fuelType_avg_price = data.groupby('fuelType')['price'].mean()
    plt.bar(fuelType_avg_price.index, fuelType_avg_price.values)
    plt.xlabel('Jenis Bahan Bakar')
    plt.ylabel('Rata-rata Harga')
    plt.title('Hubungan Antara Jenis Bahan Bakar dan Harga')
    st.pyplot()
    
    st.subheader("Hubungan antara Pajak dan Harga Mobil (€)")
    plt.figure(figsize=(10, 6))
    plt.scatter(data['tax'], data['price'], alpha=0.6, color='blue')
    plt.xlabel('Pajak Mobil')
    plt.ylabel('Harga Mobil (€)')
    plt.title('Hubungan antara Pajak dan Harga Mobil (€)')
    st.pyplot()
    
    st.subheader("Hubungan antara Konsumsi BBM dan Harga Mobil (€)")
    plt.figure(figsize=(10, 6))
    plt.scatter(data['mpg'], data['price'], alpha=0.6, color='orange')
    plt.xlabel('Konsumsi BBM')
    plt.ylabel('Harga Mobil (€)')
    plt.title('Hubungan antara Konsumsi BBM dan Harga Mobil (€)')
    st.pyplot()
    
    st.subheader("Hubungan antara Ukuran Mesin dan Harga Mobil (€)")
    plt.figure(figsize=(10, 6))
    plt.scatter(data['engineSize'], data['price'], alpha=0.6, color='purple')
    plt.xlabel('Ukuran Mesin')
    plt.ylabel('Harga Mobil (€)')
    plt.title('Hubungan antara Ukuran Mesin dan Harga Mobil (€)')
    st.pyplot()

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
