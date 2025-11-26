import streamlit as st
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import platform

# ---- 한글 폰트 설정 (그래프 한글 깨짐 방지) ----
def set_korean_font():
    system = platform.system()

    # OS별로 기본 한글 폰트 설정
    if system == "Windows":
        font_name = "Malgun Gothic"      # 맑은 고딕
    elif system == "Darwin":
        font_name = "AppleGothic"        # 맥 기본 한글 폰트
    else:
        # 리눅스/서버 환경: 있으면 나눔고딕, 없으면 기본 폰트
        font_name = "NanumGothic"

    try:
        mpl.rc('font', family=font_name)
    except Exception as e:
        # 폰트 설정 실패해도 앱이 죽지 않도록만 처리
        st.warning(f"⚠️ 한글 폰트 설정 실패: {e}")

    mpl.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

set_korean_font()

# ---- 페이지 설정 ----
st.set_page_config(page_title="양자 터널링 이항분포 그래프", layout="centered")

# ---- 제목 ----
st.markdown("<h1 style='text-align:center;'>양자 터널링 이항분포 그래프</h1>", unsafe_allow_html=True)

# ---- 부제 설명 ----
st.markdown("""
**양자 터널링이란?**  
양자 터널링은 입자가 고전역학적으로 넘을 수 없는 에너지 장벽을 **확률적으로 통과하는 현상**입니다.  
비유하자면, 벽에 공을 튕겼는데 **일정 확률로 공이 벽을 관통하는 것**이라고 볼 수 있습니다.
""")

st.write("---")

# ---- 터널링 확률 p(L) ----
K_CONST = 0.5   # nm^-1 (지수 감쇠 상수)

def tunneling_prob(L_nm: float) -> float:
    """장벽 두께 L_nm에서 터널링 확률 p(L) 계산"""
    p = math.exp(-K_CONST * L_nm)
    return max(min(p, 0.999999), 1e-10)

# ---- 입력 UI ----
st.subheader("1️⃣ 입력값 설정")

st.markdown("**✔ 입자 수 n** — 한 번에 장벽을 향해 이동하는 총 입자 수입니다.")

n = st.number_input(
    "입자 수 n 입력",
    min_value=1,
    max_value=20000,
    value=1000,
    step=1
)

st.markdown("""
**✔ 장벽 두께 L (nm)** — nm(나노미터) 단위의 장벽 두께이며,  
두꺼울수록 터널링 확률 p(L)이 지수적으로 급격히 감소합니다.
""")

L = st.number_input(
    "장벽 두께 L (nm) 입력",
    min_value=0.0,
    max_value=20.0,
    value=2.0,
    step=0.1
)

p = tunneling_prob(L)

st.markdown(f"### 👉 계산된 터널링 확률 p(L) = **{p:.6f}**")

# ---- 이항분포 그래프 ----
st.subheader("2️⃣ 이항분포 그래프 (X ~ Binomial(n, p))")

ks = np.arange(0, n+1)
pmf = np.array([math.comb(n, k)*(p**k)*((1-p)**(n-k)) for k in ks])

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(ks, pmf, width=1.0)
ax.set_title(f"이항분포: n={n}, p={p:.4f}")
ax.set_xlabel("터널링 성공한 입자 수 k")
ax.set_ylabel("P(X = k)")
ax.grid(axis='y', alpha=0.3)

st.pyplot(fig)

# ---- 특정 k개의 확률 계산 ----
st.subheader("3️⃣ 특정 개수 k개가 터널링할 확률 계산")

st.markdown("**✔ k 값** — n개 중 정확히 k개가 터널링할 확률을 계산합니다.")

k_user = st.number_input(
    f"k 값 입력 (0 ~ {n})",
    min_value=0,
    max_value=n,
    value=5,
    step=1
)

prob_k = math.comb(n, k_user)*(p**k_user)*((1-p)**(n-k_user))

# 🔥 확률을 ‘소수 8자리 + 퍼센트’로 표시
st.markdown(
    f"### 🔍 P(X = {k_user}) = **{prob_k:.8f}**  ( {prob_k*100:.2f}% )"
)

st.info("한글 폰트 설정(맑은 고딕/AppleGothic/NanumGothic)과 k 확률 소수점 8자리 표시가 적용된 버전입니다.")
