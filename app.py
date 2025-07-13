import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from pulp import LpMaximize, LpProblem, LpVariable

st.title("Optimasi Produksi Tepung Ketan (Linear Programming)")

st.markdown("Aplikasi untuk memaksimalkan keuntungan dari produksi Tepung Ketan Hitam dan Tepung Ketan Putih dengan batasan sumber daya.")

# Input untuk produk
produk = ["Tepung Ketan Hitam", "Tepung Ketan Putih"]
keuntungan = [st.number_input(f"Keuntungan per kg {p} (Rp)", min_value=0.0, value=15000.0 if i==0 else 12000.0) for i, p in enumerate(produk)]
waktu = [st.number_input(f"Waktu produksi per kg {p} (jam)", min_value=0.0, value=2.0 if i==0 else 1.5) for i, p in enumerate(produk)]
bahan = [st.number_input(f"Bahan baku per kg {p} (kg)", min_value=0.0, value=3.0 if i==0 else 2.5) for i, p in enumerate(produk)]

# Batasan sumber daya
max_waktu = st.number_input("Total waktu tersedia (jam)", min_value=0.0, value=120.0)
max_bahan = st.number_input("Total bahan baku tersedia (kg)", min_value=0.0, value=200.0)

if st.button("Hitung Solusi Optimal"):
    # Model optimasi
    model = LpProblem("Optimasi_Tepung_Ketan", LpMaximize)

    x = LpVariable("Ketan_Hitam", lowBound=0, cat='Continuous')
    y = LpVariable("Ketan_Putih", lowBound=0, cat='Continuous')

    # Fungsi objektif
    model += keuntungan[0]*x + keuntungan[1]*y, "Total_Keuntungan"

    # Batasan
    model += waktu[0]*x + waktu[1]*y <= max_waktu, "Batasan_Waktu"
    model += bahan[0]*x + bahan[1]*y <= max_bahan, "Batasan_Bahan"

    # Solve
    model.solve()

    st.success("Solusi Optimal:")
    st.write(f"Tepung Ketan Hitam: {x.varValue:.2f} kg")
    st.write(f"Tepung Ketan Putih: {y.varValue:.2f} kg")
    st.write(f"Total Keuntungan: Rp {model.objective.value():,.2f}")

    # Visualisasi
    st.subheader("Visualisasi Area Feasible")

    fig, ax = plt.subplots()
    x_vals = np.linspace(0, max(max_waktu, max_bahan), 400)
    y1 = (max_waktu - waktu[0]*x_vals) / waktu[1]
    y2 = (max_bahan - bahan[0]*x_vals) / bahan[1]

    ax.plot(x_vals, y1, label="Batasan Waktu")
    ax.plot(x_vals, y2, label="Batasan Bahan")
    ax.fill_between(x_vals, 0, np.minimum(y1, y2), where=(np.minimum(y1, y2) > 0), alpha=0.3)

    ax.set_xlabel("Tepung Ketan Hitam (kg)")
    ax.set_ylabel("Tepung Ketan Putih (kg)")
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.legend()
    st.pyplot(fig)