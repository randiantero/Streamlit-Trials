import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Membuat judul halaman dashboard
st.header('E-Commerce Sales Dashboard')

# Input dataset
data_final = pd.read_csv("data_final.csv")

# Membuat filter tanggal
datetime_columns = ["order_approved_at"]
data_final.sort_values(by="order_approved_at", inplace=True)
data_final.reset_index(inplace=True)

for column in datetime_columns:
    data_final[column] = pd.to_datetime(data_final[column])

min_date = data_final["order_approved_at"].min()
max_date = data_final["order_approved_at"].max()

with st.sidebar:
    
    start_date, end_date = st.date_input(
        label='Periode Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

filtered_data = data_final[
    (data_final['order_approved_at'] >= pd.to_datetime(start_date)) & 
    (data_final['order_approved_at'] <= pd.to_datetime(end_date))
]

# Menghitung total pendapatan berdasarkan Payment Value yang didapatkan
revenue = filtered_data['payment_value'].sum()
produk_terjual = filtered_data['product_id'].nunique() 

st.metric(label="Revenue", value=format_currency(revenue, 'USD', locale='en_US'))
st.metric(label="Product Sold", value=produk_terjual)


# Produk Dengan Penjualan Tertinggi
product = filtered_data.groupby('product_category_name_english').agg({'product_id': 'count'}).reset_index()
product.columns = ['Product Category', 'Total Sales'] 

# Kota Dengan Penjualan Tertinggi
city_distribution = filtered_data.groupby('customer_city').agg({'product_id': 'count'}).reset_index()
city_distribution.columns = ['City', 'Total Sales'] 

# Visualisasi Data Produk dan Kota dengan Penjualan Tertinggia
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))

# Warna yang digunakan untuk visualisasi
colors = ["#1A5319", "#508D4E", "#80AF81", "#D6EFD8", "#DEF9C4"]

# Produk dengan penjualan tertinggi
sns.barplot(x="Total Sales", y="Product Category", data=product.sort_values(by="Total Sales", ascending=False).head(10), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=15)
ax[0].set_title("Produk dengan Penjualan Tertinggi", loc="center", fontsize=20)
ax[0].tick_params(axis='y', labelsize=12)
ax[0].tick_params(axis='x', labelsize=12)

# Kota dengan penjualan tertinggi
sns.barplot(x="Total Sales", y="City", data=city_distribution.sort_values(by="Total Sales", ascending=False).head(10), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=15)
ax[1].set_title("Kota dengan Penjualan Tertinggi", loc="center", fontsize=20)
ax[1].tick_params(axis='y', labelsize=12)
ax[1].tick_params(axis='x', labelsize=12)

st.pyplot(fig)

# Performa Penjualan Produk
performa_penjualan = filtered_data.groupby('order_approved_at').agg({'product_id': 'count'}).reset_index()
performa_penjualan.columns = ['Date', 'Total Sales']

# Visualisasi Performa Penjualan Produk
st.subheader("Performa Penjualan Harian")
plt.figure(figsize=(14, 6))
sns.lineplot(x='Date', y='Total Sales', data=performa_penjualan, marker='o')
plt.title("Performa Penjualan Harian dari {} - {}".format(start_date, end_date), fontsize=20)
plt.xlabel("Tanggal", fontsize=15)
plt.ylabel("Jumlah Penjualan", fontsize=15)
plt.xticks(rotation=45)
plt.grid()
st.pyplot(plt)


