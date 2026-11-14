import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# konfigurasi halaman
st.set_page_config(
    page_title="E-Commerce Data Analysis",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# tampilan dashboard
st.markdown("""
<style>
    .stApp {
        background-color: #F8F5F1;
        color: #33251D;
    }

    [data-testid="stHeader"] {
        background-color: rgba(248, 245, 241, 0.9);
    }

    .main-title {
        background: linear-gradient(120deg, #4A2818, #895431);
        padding: 30px 34px;
        border-radius: 18px;
        color: #FFFFFF;
        margin-bottom: 24px;
    }

    .main-title h1 {
        color: #FFFFFF;
        font-size: 34px;
        margin-bottom: 8px;
    }

    .main-title p {
        color: #F2E7DE;
        font-size: 16px;
        margin-bottom: 0;
    }

    .section-heading {
        color: #4A2818;
        font-size: 25px;
        font-weight: 700;
        margin-top: 18px;
        margin-bottom: 5px;
    }

    .section-description {
        color: #78675D;
        font-size: 15px;
        margin-bottom: 18px;
    }

    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #E8DCD1;
        border-left: 5px solid #895431;
        padding: 18px 20px;
        border-radius: 13px;
        min-height: 112px;
        box-shadow: 0 3px 12px rgba(74, 40, 24, 0.05);
    }

    .metric-label {
        color: #78675D;
        font-size: 14px;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #4A2818;
        font-size: 27px;
        font-weight: 700;
    }

    .content-card {
        background-color: #FFFFFF;
        border: 1px solid #E8DCD1;
        border-radius: 16px;
        padding: 20px 22px;
        margin-bottom: 18px;
        box-shadow: 0 3px 12px rgba(74, 40, 24, 0.04);    
    }

    .insight-card {
        background-color: #F0E5DA;
        border-radius: 13px;
        padding: 18px 20px;
        margin-top: 12px;
        margin-bottom: 14px;
        color: #4A2818;
    }

    .recommendation-card {
        background-color: #FFFFFF;
        border: 1px solid #E8DCD1;
        border-radius: 13px;
        padding: 17px 20px;
        margin-bottom: 12px;
        color: #4A2818;
    }

    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E8DCD1;
        border-left: 5px solid #895431;
        padding: 15px 18px;
        border-radius: 13px;
    }

    div[data-testid="stMetricLabel"] {
        color: #78675D;
    }

    div[data-testid="stMetricValue"] {
        color: #4A2818;
    }

    hr {
        border-color: #E5D7CB;
    }

    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Membaca data dari file CSV yang berada satu folder dengan dashboard.py.
csv_path = Path(__file__).parent / "main_data.csv"

if not csv_path.exists():
    st.error(f"File main_data.csv tidak ditemukan di folder: {csv_path.parent}")
    st.stop()

main_data = pd.read_csv(csv_path, encoding="utf-8-sig")

# Membersihkan nama kolom dari spasi atau karakter BOM.
main_data.columns = (
    main_data.columns.astype(str)
    .str.replace("\ufeff", "", regex=False)
    .str.strip()
)


# Memastikan kolom-kolom yang diperlukan tersedia.
required_columns = [
    "order_id",
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "payment_type"
]

missing_columns = [
    column for column in required_columns
    if column not in main_data.columns
]

if missing_columns:
    st.error(
        "Ada kolom yang tidak ditemukan di main_data.csv: "
        + ", ".join(missing_columns)
    )
    st.write("Kolom yang tersedia di CSV:", main_data.columns.tolist())
    st.stop()

# Mengubah kolom waktu menjadi datetime seperti pada notebook.
date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    main_data[column] = pd.to_datetime(
        main_data[column],
        errors="coerce"
    )

# Mengikuti proses cleaning pada notebook:
# menghapus baris yang memiliki missing value.
main_data.dropna(axis=0, inplace=True)

# Memilih data Januari–Desember 2017.
orders2017 = main_data[
    (main_data["order_purchase_timestamp"] >= "2017-01-01") &
    (main_data["order_purchase_timestamp"] < "2018-01-01")
].copy()

if orders2017.empty:
    st.error(
        "Tidak ada data untuk periode Januari–Desember 2017. "
        "Periksa kembali isi main_data.csv."
    )
    st.stop()

# prepare data
# Q1: menghitung durasi persetujuan pesanan.
orders_q1 = orders2017.drop_duplicates(
    subset="order_id"
).copy()

orders_q1["approval_duration_hours"] = (
    orders_q1["order_approved_at"] -
    orders_q1["order_purchase_timestamp"]
).dt.total_seconds() / 3600

mean_approval = orders_q1["approval_duration_hours"].mean()
median_approval = orders_q1["approval_duration_hours"].median()
upper_limit = orders_q1["approval_duration_hours"].quantile(0.99)

data = orders_q1[
    orders_q1["approval_duration_hours"] <= upper_limit
]

# Q2: menghitung pengiriman pada hari yang sama atau berbeda.
orders_q2 = orders2017.drop_duplicates(
    subset="order_id"
).copy()

orders_q2["approval_date"] = orders_q2["order_approved_at"].dt.date
orders_q2["carrier_date"] = orders_q2["order_delivered_carrier_date"].dt.date

orders_q2["same_day_shipping"] = (
    orders_q2["approval_date"] == orders_q2["carrier_date"]
)

same_day_count = (orders_q2["same_day_shipping"] == True).sum()
different_day_count = (orders_q2["same_day_shipping"] == False).sum()
total_orders = len(orders_q2)

same_day_percentage = (same_day_count / total_orders) * 100
different_day_percentage = (different_day_count / total_orders) * 100

# Q3: menghitung metode pembayaran dari kolom hitungan di main_data.csv.
# Satu order bisa muncul di beberapa baris setelah penggabungan data.
# Karena itu, ambil satu nilai per order terlebih dahulu agar tidak terhitung berulang.
# Q3: menghitung metode pembayaran.
payment_counts = orders2017["payment_type"].value_counts()

payment_percentage = (
    payment_counts / payment_counts.sum()
) * 100

payment_summary = pd.DataFrame({
    "Jumlah Transaksi": payment_counts,
    "Persentase (%)": payment_percentage.round(2)
})

# header dashboard
st.markdown("""
<div class="main-title">
    <h1>🛍️ E-Commerce Data Analysis Dashboard</h1>
    <p>Analisis data pesanan dan metode pembayaran selama Januari–Desember 2017</p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="section-description">'
    'Dashboard ini menyajikan hasil analisis waktu persetujuan pesanan, '
    'kecepatan penyerahan pesanan kepada pihak pengiriman, dan metode pembayaran.'
    '</div>',
    unsafe_allow_html=True
)

# ringkasan data 
st.markdown('<div class="section-heading">Ringkasan Analisis</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-description">Gambaran singkat hasil pengolahan data tahun 2017.</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Jumlah Pesanan Unik",
        value=f"{orders2017['order_id'].nunique():,}"
    )

with col2:
    st.metric(
        label="Rata-rata Approval Time",
        value=f"{mean_approval:.2f} jam"
    )

with col3:
    st.metric(
        label="Same Day Shipping",
        value=f"{same_day_percentage:.2f}%"
    )

with col4:
    credit_card_percentage = (
        payment_percentage.get("credit_card", 0)
    )
    st.metric(
        label="Credit Card",
        value=f"{credit_card_percentage:.2f}%"
    )

st.divider()

# pertanyaan 1 

st.markdown(
    '<div class="section-heading">Pertanyaan 1 — Waktu Persetujuan Pesanan</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Berapa rata-rata waktu yang dibutuhkan sejak customer melakukan pembelian '
    'hingga pesanan disetujui selama Januari–Desember 2017?'
    '</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Rata-rata (Mean)",
        value=f"{mean_approval:.2f} jam"
    )

with col2:
    st.metric(
        label="Median",
        value=f"{median_approval:.2f} jam"
    )

# Grafik Q1: dipertahankan sesuai kode visualisasi di notebook.
plt.figure(figsize=(14, 6))

ax = sns.histplot(
    data=data,
    x="approval_duration_hours",
    bins=30
)

# Empat tingkat warna cokelat.
brown_colors = [
    "#D8B99A",
    "#B88963",
    "#895431",
    "#4A2818"
]

# Mengambil jumlah pesanan pada setiap batang.
counts = [patch.get_height() for patch in ax.patches]

# Mengelompokkan jumlah pesanan menjadi empat tingkat.
nonzero_counts = [count for count in counts if count > 0]

q25, q50, q75 = np.quantile(
    nonzero_counts,
    [0.25, 0.50, 0.75]
)

color_levels = np.digitize(
    counts,
    [q25, q50, q75]
)

# Mengubah warna batang berdasarkan jumlah pesanan.
for patch, count, level in zip(
    ax.patches, counts, color_levels
):
    patch.set_facecolor(brown_colors[level])

    # Menampilkan angka di tengah batang.
    if count > 0:
        x_center = patch.get_x() + patch.get_width() / 2
        y_center = count / 2

        text_color = "white" if level >= 2 else "black"

        ax.text(
            x_center,
            y_center,
            f"{count:.0f}",
            ha="center",
            va="center",
            fontsize=8,
            color=text_color,
            fontweight="bold"
        )

# Menampilkan garis rata-rata.
plt.axvline(
    mean_approval,
    linestyle="--",
    color="#6B4226",
    label=f"Mean: {mean_approval:.2f} hours"
)

# Menampilkan garis median.
plt.axvline(
    median_approval,
    linestyle=":",
    color="#A66B3F",
    label=f"Median: {median_approval:.2f} hours"
)

# Judul dan label.
plt.title(
    "Distribution rata-rata waktu yang dibutuhkan sejak customer melakukan pembelian hingga pesanan disetujui selama Januari - Desember 2017"
)
plt.xlabel("Approval Time (Hours)")
plt.ylabel("Number of Orders")

plt.legend()
plt.tight_layout()

fig_q1 = plt.gcf()
st.pyplot(fig_q1, use_container_width=True)
plt.close(fig_q1)

st.markdown("""
<div class="insight-card">
    <b>Insight Q1</b><br>
    Berdasarkan analisis terhadap pesanan pada tahun 2017, rata-rata waktu
    persetujuan pesanan dapat dibandingkan dengan nilai median untuk melihat
    apakah terdapat sejumlah pesanan dengan waktu persetujuan yang jauh lebih lama.
    Perbedaan mean dan median yang besar menunjukkan distribusi waktu yang
    cenderung menceng ke kanan (right-skewed).
</div>
""", unsafe_allow_html=True)

st.divider()

# pertanyaan 2 
st.markdown(
    '<div class="section-heading">Pertanyaan 2 — Pengiriman Pesanan</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Berapa persentase barang yang dikirim di hari yang sama setelah pesanan '
    'disetujui selama Januari–Desember 2017?'
    '</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Pesanan",
        value=f"{total_orders:,}"
    )

with col2:
    st.metric(
        label="Same Day",
        value=f"{same_day_count:,}",
        delta=f"{same_day_percentage:.2f}%"
    )
with col3:
    st.metric(
        label="Different Day",
        value=f"{different_day_count:,}",
        delta=f"{different_day_percentage:.2f}%",
        delta_color="off"
    )

# Grafik Q2 (Pie Chart): dipertahankan sesuai notebook.
shipping_counts = [
    same_day_count,
    different_day_count
]

shipping_labels = [
    "Same Day",
    "Different Day"
]

shipping_colors = [
    "#D8B99A",
    "#4A2818"
]

def show_percentage_and_count(values):
    def format_label(pct):
        count = int(round(pct / 100 * sum(values)))
        return f"{pct:.2f}%\n({count:,} pesanan)"
    return format_label

plt.figure(figsize=(9, 7))

plt.pie(
    shipping_counts,
    labels=None,
    colors=shipping_colors,
    autopct=show_percentage_and_count(shipping_counts),
    startangle=90,
    pctdistance=0.65,
    textprops={
        "color": "white",
        "fontsize": 10,
        "fontweight": "bold"
    }
)

plt.legend(
    shipping_labels,
    title="Shipping Status",
    loc="upper center",
    bbox_to_anchor=(0.5, -0.05),
    ncol=2
)

plt.title("Persentase Pesanan Dikirim selama Januari - Desember 2017")

plt.tight_layout()

fig_q2_pie = plt.gcf()
st.pyplot(fig_q2_pie, use_container_width=True)
plt.close(fig_q2_pie)

# Grafik Q2 (Bar Chart): dipertahankan sesuai notebook.
shipping_data = pd.DataFrame({
    "Shipping Status": [
        "Same Day",
        "Different Day"
    ],
    "Number of Orders": [
        same_day_count,
        different_day_count
    ]
})

plt.figure(figsize=(9, 6))

ax = sns.barplot(
    data=shipping_data,
    x="Shipping Status",
    y="Number of Orders",
    hue="Shipping Status",
    palette={
        "Same Day": "#D8B99A",
        "Different Day": "#4A2818"
    },
    legend=False
)

# Menampilkan angka di tengah batang.
for i, bar in enumerate(ax.patches):

    height = bar.get_height()

    if i == 0:
        text_color = "black"
    else:
        text_color = "white"

    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height / 2,
        f"{height:.0f}",
        ha="center",
        va="center",
        fontsize=11,
        fontweight="bold",
        color=text_color
    )

plt.title("Order Shipping by Approval Date")
plt.xlabel("Shipping Status")
plt.ylabel("Number of Orders")

plt.tight_layout()

fig_q2_bar = plt.gcf()
st.pyplot(fig_q2_bar, use_container_width=True)
plt.close(fig_q2_bar)

st.markdown("""
<div class="insight-card">
    <b>Insight Q2</b><br>
    Sebagian besar pesanan diserahkan kepada pihak pengiriman pada tanggal
    yang berbeda dari tanggal persetujuannya. Hasil ini dapat menjadi bahan
    evaluasi terhadap proses persiapan dan penyerahan pesanan.
</div>
""", unsafe_allow_html=True)

st.divider()

# pertanyaan 3 
st.markdown(
    '<div class="section-heading">Pertanyaan 3 — Metode Pembayaran</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Berapa persentase transaksi yang menggunakan credit card dibandingkan '
    'metode pembayaran lainnya selama Januari–Desember 2017?'
    '</div>',
    unsafe_allow_html=True
)

if "credit_card" in payment_percentage.index:
    st.metric(
        label="Persentase Transaksi Credit Card",
        value=f"{payment_percentage['credit_card']:.2f}%"
    )

# Grafik Q3: donut chart dipertahankan sesuai kode visualisasi di notebook.
payment_colors = [
    "#4A2818",
    "#895431",
    "#B88963",
    "#D8B99A"
]

plt.figure(figsize=(9, 7))

wedges, texts, autotexts = plt.pie(
    payment_counts,
    labels=None,
    colors=payment_colors[:len(payment_counts)],
    autopct="%1.2f%%",
    startangle=90,
    pctdistance=0.65,
    textprops={
        "color": "white",
        "weight": "bold",
        "fontsize": 10
    }
)

# Membuat lubang di tengah agar persentase tetap mudah dibaca.
centre_circle = plt.Circle(
    (0, 0),
    0.40,
    fc="white"
)

fig = plt.gcf()
fig.gca().add_artist(centre_circle)

# Keterangan payment type beserta jumlah transaksi.
payment_labels = [
    f"{payment}: {count:,} transaksi"
    for payment, count in payment_counts.items()
]

plt.legend(
    wedges,
    payment_labels,
    title="Payment Type",
    loc="upper center",
    bbox_to_anchor=(0.5, -0.05),
    ncol=2
)

plt.title("Persentase metode pembayaran selama Januari – Desember 2017")

plt.tight_layout()

fig_q3 = plt.gcf()
st.pyplot(fig_q3, use_container_width=True)
plt.close(fig_q3)

st.markdown("**Ringkasan jumlah dan persentase transaksi berdasarkan metode pembayaran:**")
st.dataframe(
    payment_summary,
    use_container_width=True
)

st.markdown("""
<div class="insight-card">
    <b>Insight Q3</b><br>
    Credit card merupakan metode pembayaran yang paling banyak digunakan,
    diikuti oleh boleto, voucher, dan debit card. Perusahaan perlu memastikan
    metode pembayaran yang paling banyak digunakan tetap mudah diakses dan
    berjalan dengan baik, sekaligus mempertahankan alternatif pembayaran lainnya.
</div>
""", unsafe_allow_html=True)

st.divider()

# Kesimpulan 
st.markdown(
    '<div class="section-heading">Conclusion & Recommendation</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="content-card">
    <h4 style="color:#4A2818;">Conclusion</h4>
    <ol>
        <li>
            Rata-rata waktu yang dibutuhkan sejak customer melakukan pembelian
            hingga pesanan disetujui adalah <b>""" + f"{mean_approval:.2f} jam" + """</b>,
            sedangkan mediannya adalah <b>""" + f"{median_approval:.2f} jam" + """</b>.
        </li>
        <li>
            Sebanyak <b>""" + f"{same_day_count:,}" + """ pesanan
            (""" + f"{same_day_percentage:.2f}%" + """)</b> diserahkan kepada carrier
            pada hari yang sama dengan tanggal persetujuan, sedangkan
            <b>""" + f"{different_day_count:,}" + """ pesanan
            (""" + f"{different_day_percentage:.2f}%" + """)</b> diserahkan pada
            tanggal yang berbeda.
        </li>
        <li>
            Metode pembayaran yang paling banyak digunakan customer adalah
            <b>""" + f"{payment_counts.index[0]}" + """</b>
            (""" + f"{payment_percentage.iloc[0]:.2f}%" + """),
            diikuti oleh metode pembayaran lainnya.
        </li>
    </ol>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="recommendation-card">
    <b>1. Evaluasi waktu persetujuan pesanan</b><br>
    Perusahaan perlu mengevaluasi pesanan yang membutuhkan waktu persetujuan
    sangat lama dan mengidentifikasi penyebab keterlambatan tersebut.
</div>

<div class="recommendation-card">
    <b>2. Evaluasi proses penyerahan pesanan</b><br>
    Perusahaan dapat mengevaluasi proses persiapan dan penyerahan pesanan
    kepada pihak pengiriman, khususnya pesanan yang tidak diserahkan pada
    hari yang sama setelah persetujuan.
</div>

<div class="recommendation-card">
    <b>3. Pertahankan kualitas metode pembayaran</b><br>
    Credit card menjadi metode pembayaran yang paling banyak digunakan.
    Perusahaan perlu memastikan pembayaran melalui credit card tetap mudah
    digunakan dan berjalan dengan baik. Metode pembayaran lain juga perlu
    dipertahankan agar pelanggan memiliki alternatif pembayaran.
</div>
""", unsafe_allow_html=True)

# footer

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="
        text-align:center;
        color:#8A786C;
        padding:18px 0 8px 0;
        border-top:1px solid #E5D7CB;
        font-size:13px;">
        E-Commerce Data Analysis Dashboard | January–December 2017
    </div>
    """,
    unsafe_allow_html=True
)
