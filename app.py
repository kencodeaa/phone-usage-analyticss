"""Mini App Nhóm B: L2 Dev – Màn hình thông minh, giấc ngủ an lành.

Bố cục hiện đại lấy cảm hứng từ giao diện Landing/Dashboard:
- Thanh Top Navigation (Logo + Chuyển trang nhanh)
- Trang Chủ (Hero Banner + Tổng quan khảo sát + Truy cập nhanh)
- Tự Kiểm Tra Thói Quen
- Phân Tích Khảo Sát (Dashboard biểu đồ, 3 nhóm sử dụng, bảng dữ liệu & lọc)
- Công Thức & Tiêu Chí (Quy ước Tin học 9 + Khu vực công thức Excel)
- Báo Cáo & Kiến Thức An Toàn
"""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from logic import (
    REQUIRED_COLUMNS,
    calculate_sleep_hours,
    create_message,
    get_default_survey_data,
    prepare_dataframe,
    summarize_dataframe,
    validate_dataframe,
)

# [1] CẤU HÌNH TRANG & CSS TÙY CHỈNH
st.set_page_config(
    page_title="Mini app nhóm B | Màn hình thông minh – Giấc ngủ an lành",
    page_icon="📱",
    layout="wide",
)

st.markdown(
    """
    <style>
    /* Ẩn thanh header mặc định của Streamlit */
    header[data-testid="stHeader"] {
        display: none;
    }

    .stApp {
        background-color: #0B0F19;
        color: #F3F4F6;
    }
    .block-container {
        padding-top: 1.1rem;
        padding-bottom: 2.5rem;
        max-width: 1360px;
    }

    /* LOGO & BRANDING */
    .brand-wrap {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .brand-icon {
        width: 42px;
        height: 42px;
        background: linear-gradient(135deg, #3B82F6, #2563EB);
        border-radius: 11px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.4);
        transition: all 0.25s ease;
    }
    .brand-icon:hover {
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 6px 24px rgba(59, 130, 246, 0.7);
    }
    .brand-name {
        font-size: 1.15rem;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: 0.04em;
        line-height: 1.15;
    }
    .brand-sub {
        font-size: 0.7rem;
        font-weight: 600;
        color: #9CA3AF;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    /* HIỆU ỨNG NỔI & PHÁT SÁNG CHO TẤT CẢ CÁC NÚT */
    div.stButton > button {
        transition: all 0.25s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    /* Nút thường / Nút điều hướng */
    div.stButton > button[kind="secondary"] {
        background-color: #131A2A !important;
        border: 1px solid #1F2937 !important;
        color: #E5E7EB !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        transform: translateY(-3px) !important;
        border-color: #60A5FA !important;
        color: #FFFFFF !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4), 0 0 12px rgba(96, 165, 250, 0.28) !important;
    }

    /* Nút chính (Primary - Xanh dương) */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #3B82F6, #2563EB) !important;
        border: 1px solid #60A5FA !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 14px rgba(59, 130, 246, 0.35) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.65), 0 0 16px rgba(96, 165, 250, 0.45) !important;
    }

    div.stButton > button:active {
        transform: translateY(0px) scale(0.98) !important;
    }

    /* HERO BANNER (PHONG CÁCH THẺ LỚN HIỆN ĐẠI) */
    .hero-card {
        background: radial-gradient(circle at 82% 45%, rgba(59, 130, 246, 0.16) 0%, rgba(19, 26, 42, 0.96) 55%, #111827 100%);
        border: 1px solid #1F2937;
        border-radius: 20px;
        padding: 34px 38px;
        margin: 14px 0 26px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 28px;
        box-shadow: 0 14px 36px rgba(0, 0, 0, 0.45);
        transition: all 0.3s ease;
    }
    .hero-card:hover {
        border-color: #2D3B55;
        box-shadow: 0 18px 42px rgba(37, 99, 235, 0.14);
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(59, 130, 246, 0.12);
        border: 1px solid rgba(96, 165, 250, 0.3);
        color: #93C5FD;
        padding: 5px 14px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-bottom: 16px;
    }
    .hero-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #60A5FA;
        box-shadow: 0 0 8px #60A5FA;
    }
    .hero-heading {
        font-size: 2.35rem;
        font-weight: 900;
        line-height: 1.12;
        letter-spacing: -0.01em;
        margin: 0 0 16px 0;
        color: #FFFFFF;
    }
    .hero-heading span {
        background: linear-gradient(90deg, #60A5FA, #818CF8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-desc {
        font-size: 0.96rem;
        color: #CBD5E1;
        line-height: 1.6;
        max-width: 560px;
        margin-bottom: 8px;
    }
    .hero-visual {
        position: relative;
        min-width: 310px;
        height: 230px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .float-pill {
        position: absolute;
        background: rgba(15, 23, 42, 0.88);
        backdrop-filter: blur(8px);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 8px 13px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
        transition: all 0.25s ease;
    }
    .float-pill:hover {
        transform: translateY(-3px);
        border-color: #60A5FA;
        box-shadow: 0 10px 24px rgba(59, 130, 246, 0.35);
    }

    /* TIÊU ĐỀ SECTION & PILL NGUỒN DỮ LIỆU */
    .sec-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 8px 0 4px 0;
    }
    .sec-sub {
        font-size: 0.86rem;
        color: #9CA3AF;
        margin-bottom: 10px;
    }
    .source-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background-color: #131A2A;
        border: 1px solid #1F2937;
        border-radius: 999px;
        padding: 4px 14px;
        font-size: 0.78rem;
        color: #9CA3AF;
        margin-bottom: 16px;
    }

    /* THẺ KPI (4 THẺ TỔNG QUAN) + HOVER PHÁT SÁNG */
    .kpi-card {
        background-color: #131A2A;
        border: 1px solid #1F2937;
        border-radius: 14px;
        padding: 18px 20px;
        height: 100%;
        transition: all 0.28s cubic-bezier(0.25, 0.8, 0.25, 1);
        cursor: default;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: #3B82F6;
        box-shadow: 0 12px 26px -4px rgba(59, 130, 246, 0.35), 0 0 15px rgba(59, 130, 246, 0.22);
    }
    .kpi-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    .kpi-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: #9CA3AF;
    }
    .kpi-value {
        font-size: 1.95rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.1;
    }
    .kpi-sub {
        font-size: 0.78rem;
        margin-top: 8px;
        color: #9CA3AF;
    }
    .kpi-icon {
        width: 34px;
        height: 34px;
        border-radius: 9px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
    }

    /* 3 THẺ PHÂN NHÓM (NHÓM 1, NHÓM 2, NHÓM 3) + HOVER PHÁT SÁNG THEO MÀU */
    .group-card {
        border-radius: 14px;
        padding: 18px 20px;
        height: 100%;
        transition: all 0.28s cubic-bezier(0.25, 0.8, 0.25, 1);
        cursor: default;
    }
    .group-1 {
        background: linear-gradient(145deg, #10253E 0%, #111927 100%);
        border: 1px solid #1D4ED8;
    }
    .group-1:hover {
        transform: translateY(-5px);
        border-color: #60A5FA;
        box-shadow: 0 12px 28px -4px rgba(59, 130, 246, 0.48), 0 0 18px rgba(96, 165, 250, 0.32);
    }
    .group-2 {
        background: linear-gradient(145deg, #1E1B3A 0%, #111927 100%);
        border: 1px solid #4F46E5;
    }
    .group-2:hover {
        transform: translateY(-5px);
        border-color: #A5B4FC;
        box-shadow: 0 12px 28px -4px rgba(99, 102, 241, 0.48), 0 0 18px rgba(165, 180, 252, 0.32);
    }
    .group-3 {
        background: linear-gradient(145deg, #2D1520 0%, #111927 100%);
        border: 1px solid #DC2626;
    }
    .group-3:hover {
        transform: translateY(-5px);
        border-color: #F87171;
        box-shadow: 0 12px 28px -4px rgba(239, 68, 68, 0.48), 0 0 18px rgba(248, 113, 113, 0.32);
    }
    .group-title {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .group-val {
        font-size: 1.85rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 6px 0 2px 0;
    }
    .group-total {
        font-size: 0.85rem;
        color: #D1D5DB;
        margin-bottom: 10px;
    }
    .group-desc {
        font-size: 0.78rem;
        padding-top: 8px;
        border-top: 1px solid rgba(255,255,255,0.08);
    }

    /* THẺ TRUY CẬP NHANH (QUICK ACCESS CARDS) */
    .quick-card {
        background-color: #131A2A;
        border: 1px solid #1F2937;
        border-radius: 16px;
        padding: 20px 22px;
        margin-bottom: 10px;
        min-height: 158px;
        transition: all 0.28s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    .quick-card:hover {
        transform: translateY(-5px);
        border-color: #60A5FA;
        box-shadow: 0 12px 28px rgba(59, 130, 246, 0.3), 0 0 14px rgba(96, 165, 250, 0.22);
    }
    .quick-icon {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        margin-bottom: 14px;
    }
    .quick-title {
        font-size: 1.02rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 6px;
    }
    .quick-desc {
        font-size: 0.83rem;
        color: #9CA3AF;
        line-height: 1.5;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# [2] KHỞI TẠO DỮ LIỆU & TRẠNG THÁI TRANG (NAVIGATION)
if "survey_df" not in st.session_state:
    st.session_state.survey_df = get_default_survey_data()
if "data_source_label" not in st.session_state:
    st.session_state.data_source_label = "Dữ liệu mô phỏng mặc định – Lớp 9B (30 HS)"
if "active_page" not in st.session_state:
    st.session_state.active_page = "Trang chủ"


def go_to(page_name: str):
    st.session_state.active_page = page_name


def read_uploaded_file(uploaded_file) -> pd.DataFrame:
    name = uploaded_file.name.lower()
    if name.endswith((".xlsx", ".xls")):
        xl = pd.ExcelFile(uploaded_file)
        sheet = "Du_lieu_khao_sat" if "Du_lieu_khao_sat" in xl.sheet_names else xl.sheet_names[0]
        df_try = pd.read_excel(uploaded_file, sheet_name=sheet, skiprows=2)
        if not set(REQUIRED_COLUMNS).issubset(set(str(c).strip() for c in df_try.columns)):
            df_try = pd.read_excel(uploaded_file, sheet_name=sheet)
        return df_try
    if name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    raise ValueError("Định dạng chưa hỗ trợ. Vui lòng tải file .xlsx, .xls hoặc .csv.")


df = st.session_state.survey_df
summary = summarize_dataframe(df)

# [3] THANH ĐIỀU HƯỚNG TRÊN CÙNG (TOP NAVBAR)
nav_logo, nav_p1, nav_p2, nav_p3, nav_p4, nav_p5 = st.columns([2.8, 1.25, 1.45, 1.65, 1.5, 1.55])

with nav_logo:
    st.markdown(
        """
        <div class="brand-wrap">
            <div class="brand-icon">📱</div>
            <div>
                <div class="brand-name">L<sup>2</sup> Dev</div>
                <div class="brand-sub">SCREEN &amp; SLEEP ANALYTICS • BY LONG LE</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

pages = [
    ("Trang chủ", "🏠 Trang chủ", nav_p1),
    ("Tự kiểm tra", "🧭 Tự kiểm tra", nav_p2),
    ("Phân tích khảo sát", "📊 Phân tích khảo sát", nav_p3),
    ("Công thức & Tiêu chí", "🖩 Công thức Excel", nav_p4),
    ("Kiến thức & An toàn", "📘 Kiến thức & An toàn", nav_p5),
]

for page_key, page_label, col in pages:
    with col:
        btn_type = "primary" if st.session_state.active_page == page_key else "secondary"
        if st.button(page_label, key=f"nav_{page_key}", use_container_width=True, type=btn_type):
            go_to(page_key)
            st.rerun()

st.write("")

# ==============================================================================
# TRANG 1: TRANG CHỦ
# ==============================================================================
if st.session_state.active_page == "Trang chủ":
    # 1. HERO BANNER 2 CỘT
    st.markdown(
        """
        <div class="hero-card">
            <div style="flex: 1.2;">
                <div class="hero-badge">
                    <span class="hero-dot"></span>
                    <span>Sản phẩm STEM Tin học 9 • Nhóm B (Long Le)</span>
                </div>
                <h1 class="hero-heading">LÀM CHỦ MÀN HÌNH.<br><span>CHĂM SÓC GIẤC NGỦ.</span></h1>
                <p class="hero-desc">
                    <b>Mini app này</b> giúp học sinh phân tích dữ liệu khảo sát ẩn danh về thời gian sử dụng
                    điện thoại và giấc ngủ. Giảm màn hình trước ngủ – nâng cao chất lượng nghỉ ngơi mỗi ngày.
                </p>
            </div>
            <div class="hero-visual">
                <svg width="230" height="230" viewBox="0 0 220 220" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="110" cy="110" r="92" stroke="#1E293B" stroke-width="10"/>
                    <circle cx="110" cy="110" r="72" stroke="#1E293B" stroke-width="10"/>
                    <path d="M110 18 A92 92 0 1 1 26 148" stroke="#3B82F6" stroke-width="10" stroke-linecap="round"/>
                    <path d="M110 38 A72 72 0 1 1 56 156" stroke="#818CF8" stroke-width="10" stroke-linecap="round"/>
                    <circle cx="110" cy="110" r="46" fill="#0F172A" stroke="#334155" stroke-width="2"/>
                    <rect x="96" y="84" width="28" height="48" rx="6" fill="#1E293B" stroke="#60A5FA" stroke-width="2.5"/>
                    <circle cx="110" cy="124" r="2" fill="#60A5FA"/>
                    <path d="M128 84C133 84 137 88 137 93C132 93 128 89 128 84Z" fill="#FBBF24"/>
                    <text x="129" y="79" fill="#FBBF24" font-size="11" font-weight="bold">zZ</text>
                </svg>
                <div class="float-pill" style="top: 12px; right: -8px;">
                    <div style="font-size: 0.78rem; font-weight: 700; color: #60A5FA;">Khuyến nghị ngủ ≥ 8h</div>
                    <div style="font-size: 0.68rem; color: #9CA3AF;">mốc tham khảo tuổi 13–18</div>
                </div>
                <div class="float-pill" style="bottom: 16px; left: -12px;">
                    <div style="font-size: 0.78rem; font-weight: 700; color: #F87171;">Dùng ĐT &gt; 4 giờ/ngày</div>
                    <div style="font-size: 0.68rem; color: #9CA3AF;">ngưỡng cảnh báo thói quen</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Hai nút hành động chính ngay dưới Hero Banner
    cta1, cta2, _ = st.columns([1.9, 2.0, 6.1])
    with cta1:
        if st.button("🧭 Bắt đầu tự kiểm tra", type="primary", use_container_width=True):
            go_to("Tự kiểm tra")
            st.rerun()
    with cta2:
        if st.button("📊 Xem phân tích khảo sát", type="secondary", use_container_width=True):
            go_to("Phân tích khảo sát")
            st.rerun()

    st.write("")

    # 2. TỔNG QUAN KHẢO SÁT (4 THẺ KPI NỔI BẬT)
    st.markdown('<div class="sec-title">Tổng quan khảo sát</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sec-sub">Các chỉ số được tính trực tiếp từ dữ liệu khảo sát đang nạp trong ứng dụng.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="source-pill"><span class="hero-dot"></span><span>Nguồn: {st.session_state.data_source_label}</span></div>',
        unsafe_allow_html=True,
    )

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-top">
                    <span class="kpi-label">Số học sinh trong dữ liệu</span>
                    <div class="kpi-icon" style="background:rgba(59,130,246,0.15); color:#60A5FA;">👥</div>
                </div>
                <div class="kpi-value">{summary['total']}</div>
                <div class="kpi-sub">Lớp 9B khảo sát • Dùng ĐT TB: <b style="color:#E5E7EB;">{summary['avg_screen']}h</b></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-top">
                    <span class="kpi-label">Dùng điện thoại &lt; 2 giờ/ngày</span>
                    <div class="kpi-icon" style="background:rgba(56,189,248,0.15); color:#38BDF8;">🛡️</div>
                </div>
                <div class="kpi-value" style="color:#60A5FA;">{summary['g1_count']} HS</div>
                <div class="kpi-sub">Nhóm 1 an toàn • Tổng {summary['g1_sum']}h sử dụng</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-top">
                    <span class="kpi-label">Dùng màn hình trước khi ngủ</span>
                    <div class="kpi-icon" style="background:rgba(251,191,36,0.15); color:#FBBF24;">🌙</div>
                </div>
                <div class="kpi-value" style="color:#FBBF24;">{summary['before_bed_yes']} HS</div>
                <div class="kpi-sub">{summary['before_pct']}% tổng số học sinh • Ngủ TB: {summary['avg_sleep']}h</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-top">
                    <span class="kpi-label">Cần lưu ý cảnh báo</span>
                    <div class="kpi-icon" style="background:rgba(248,113,113,0.15); color:#F87171;">⚠️</div>
                </div>
                <div class="kpi-value" style="color:#F87171;">{summary['warning_count']} HS</div>
                <div class="kpi-sub" style="color:#FCA5A5;">Nhóm &gt;4h: {summary['g3_count']} HS • Ngủ &lt;8h: {summary['sleep_under']} HS</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    # 3. TRUY CẬP NHANH (3 THẺ CHỨC NĂNG)
    st.markdown('<div class="sec-title">Truy cập nhanh</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Chọn một mục để bắt đầu khám phá dữ liệu.</div>', unsafe_allow_html=True)

    q1, q2, q3 = st.columns(3)
    with q1:
        st.markdown(
            """
            <div class="quick-card">
                <div class="quick-icon" style="background:rgba(59,130,246,0.16); color:#60A5FA;">🧭</div>
                <div class="quick-title">Tự kiểm tra thói quen</div>
                <div class="quick-desc">Nhập thời gian dùng màn hình và giờ đi ngủ/thức dậy để nhận thông điệp gợi ý phù hợp.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Mở Tự kiểm tra →", key="q_btn_1", use_container_width=True):
            go_to("Tự kiểm tra")
            st.rerun()

    with q2:
        st.markdown(
            """
            <div class="quick-card">
                <div class="quick-icon" style="background:rgba(129,140,248,0.16); color:#818CF8;">📊</div>
                <div class="quick-title">Phân tích khảo sát</div>
                <div class="quick-desc">Nạp tệp Excel/CSV, xem 3 nhóm phân loại, biểu đồ trực quan và tra cứu dữ liệu lớp.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Mở Phân tích khảo sát →", key="q_btn_2", use_container_width=True):
            go_to("Phân tích khảo sát")
            st.rerun()

    with q3:
        st.markdown(
            """
            <div class="quick-card">
                <div class="quick-icon" style="background:rgba(251,191,36,0.16); color:#FBBF24;">📘</div>
                <div class="quick-title">Kiến thức &amp; an toàn</div>
                <div class="quick-desc">Mốc tham khảo giấc ngủ, quy ước của dự án và các nguyên tắc bảo vệ thông tin học đường.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Mở Kiến thức & An toàn →", key="q_btn_3", use_container_width=True):
            go_to("Kiến thức & An toàn")
            st.rerun()


# ==============================================================================
# TRANG 2: TỰ KIỂM TRA THÓI QUEN
# ==============================================================================
elif st.session_state.active_page == "Tự kiểm tra":
    st.markdown('<div class="sec-title">🧭 Tự xem lại một số thói quen cá nhân</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sec-sub">Nhập thông tin để xem cách ứng dụng phân tích. Không cần nhập họ tên hay thông tin định danh.</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        screen_hours = st.number_input(
            "Thời gian sử dụng màn hình (giờ/ngày)",
            min_value=0.0,
            max_value=24.0,
            value=3.0,
            step=0.5,
        )
        before_sleep = st.radio(
            "Có sử dụng màn hình trong 1 giờ trước khi ngủ?",
            ["Không", "Có"],
            horizontal=True,
        )
    with c2:
        bedtime = st.time_input("Giờ đi ngủ", value=pd.Timestamp("2026-01-01 22:00").time())
        wake_time = st.time_input("Giờ thức dậy", value=pd.Timestamp("2026-01-02 06:30").time())

    sleep_hours = calculate_sleep_hours(bedtime, wake_time)
    if sleep_hours is None:
        st.warning("Không tính được thời lượng ngủ. Hãy kiểm tra lại giờ đi ngủ và giờ thức dậy.")
    else:
        m1, m2, m3 = st.columns(3)
        m1.metric("Thời lượng ngủ tính được", f"{sleep_hours:.1f} giờ")
        m2.metric(
            "Nhóm thời lượng ngủ",
            "Dưới 8 giờ" if sleep_hours < 8 else ("8–10 giờ" if sleep_hours <= 10 else "Trên 10 giờ"),
        )
        m3.metric(
            "Phân nhóm dùng điện thoại",
            "Nhóm 1 (< 2h)" if screen_hours < 2 else ("Nhóm 2 (2h – 4h)" if screen_hours <= 4 else "Nhóm 3 (> 4h)"),
        )

        msg = create_message(screen_hours, before_sleep, sleep_hours)
        if msg.startswith("Cần"):
            st.warning(f"⚠️ {msg}")
        else:
            st.success(f"✅ {msg}")

    st.caption("Ngưỡng >4 giờ/ngày là quy ước học tập của dự án; mốc 8–10 giờ là khuyến nghị tham khảo phổ biến cho thanh thiếu niên 13–18 tuổi.")
    
# ==============================================================================
# TRANG 3: PHÂN TÍCH KHẢO SÁT (3 NHÓM, BIỂU ĐỒ & BẢNG DỮ LIỆU)
# ==============================================================================
elif st.session_state.active_page == "Phân tích khảo sát":
    st.markdown('<div class="sec-title">📊 Phân tích chi tiết khảo sát lớp 9B</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="source-pill"><span class="hero-dot"></span><span>Nguồn hiện tại: {st.session_state.data_source_label}</span></div>',
        unsafe_allow_html=True,
    )

    # Hàng 1: 3 thẻ phân nhóm sử dụng điện thoại (Nổi & phát sáng theo màu)
    g1, g2, g3 = st.columns(3)
    with g1:
        st.markdown(
            f"""
            <div class="group-card group-1">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="group-title" style="color:#60A5FA;">NHÓM 1 (&lt; 2H)</span>
                    <span style="font-size:20px;">🛡️</span>
                </div>
                <div class="group-val">{summary['g1_count']} HS</div>
                <div class="group-total">Tổng: <b>{summary['g1_sum']}h</b></div>
                <div class="group-desc" style="color:#60A5FA;">Mức độ an toàn - Duy trì thói quen tốt</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with g2:
        st.markdown(
            f"""
            <div class="group-card group-2">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="group-title" style="color:#A5B4FC;">NHÓM 2 (2H - 4H)</span>
                    <span style="font-size:20px;">⚖️</span>
                </div>
                <div class="group-val">{summary['g2_count']} HS</div>
                <div class="group-total">Tổng: <b>{summary['g2_sum']}h</b></div>
                <div class="group-desc" style="color:#A5B4FC;">Mức độ trung bình - Cần quản lý thời gian</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with g3:
        st.markdown(
            f"""
            <div class="group-card group-3">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="group-title" style="color:#F87171;">NHÓM 3 (&gt; 4H)</span>
                    <span style="font-size:20px;">🚨</span>
                </div>
                <div class="group-val">{summary['g3_count']} HS</div>
                <div class="group-total">Tổng: <b>{summary['g3_sum']}h</b></div>
                <div class="group-desc" style="color:#F87171;">Nguy cơ cao - Cần nhắc nhở và điều chỉnh</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    # Hàng 2: 2 Biểu đồ Plotly
    c_left, c_right = st.columns(2)
    with c_left:
        st.markdown("##### 📊 Phân Phối Học Sinh Theo Nhóm Sử Dụng Điện Thoại")
        fig_bar = go.Figure(
            data=[
                go.Bar(
                    x=["Nhóm 1 (< 2h)", "Nhóm 2 (2h – 4h)", "Nhóm 3 (> 4h)"],
                    y=[summary["g1_count"], summary["g2_count"], summary["g3_count"]],
                    marker_color=["#3B82F6", "#60A5FA", "#EF4444"],
                    text=[f"{summary['g1_count']} HS", f"{summary['g2_count']} HS", f"{summary['g3_count']} HS"],
                    textposition="outside",
                )
            ]
        )
        fig_bar.update_layout(
            paper_bgcolor="#131A2A",
            plot_bgcolor="#131A2A",
            font=dict(color="#E5E7EB"),
            margin=dict(l=20, r=20, t=25, b=20),
            height=320,
            yaxis=dict(gridcolor="#1F2937", title="Số học sinh", dtick=1),
            xaxis=dict(gridcolor="#1F2937"),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with c_right:
        st.markdown("##### 🌙 Thói Quen Dùng Điện Thoại 1 Giờ Trước Khi Ngủ")
        fig_donut = go.Figure(
            data=[
                go.Pie(
                    labels=["Có dùng trước ngủ", "Không dùng trước ngủ"],
                    values=[summary["before_bed_yes"], summary["before_bed_no"]],
                    hole=0.58,
                    marker=dict(colors=["#F59E0B", "#3B82F6"], line=dict(color="#131A2A", width=3)),
                    textinfo="label+percent",
                    textfont=dict(color="#F3F4F6"),
                )
            ]
        )
        fig_donut.update_layout(
            paper_bgcolor="#131A2A",
            plot_bgcolor="#131A2A",
            font=dict(color="#E5E7EB"),
            margin=dict(l=20, r=20, t=25, b=20),
            height=320,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.12, xanchor="center", x=0.5),
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    st.divider()

    # Hàng 3: Tải file & Bảng dữ liệu khảo sát
    st.markdown("#### ⊞ Quản lý & Tra cứu Dữ liệu Khảo sát")
    uploaded = st.file_uploader(
        "Tải file Excel Nhóm B (.xlsx, .xls) hoặc CSV ẩn danh để thay thế dữ liệu phân tích",
        type=["xlsx", "xls", "csv"],
        key="survey_upload",
    )
    if uploaded is not None:
        try:
            raw = read_uploaded_file(uploaded)
            prepared = prepare_dataframe(raw)
            st.session_state.survey_df = prepared
            st.session_state.data_source_label = f"File tải lên: {uploaded.name}"
            df = prepared
            issues = validate_dataframe(df)
            if issues:
                st.warning("Cần rà soát dữ liệu trước khi sử dụng kết quả:")
                for issue in issues:
                    st.write(f"- {issue}")
            else:
                st.success(f"Đã nạp thành công {len(df)} bản ghi hợp lệ từ {uploaded.name}.")
        except Exception as exc:
            st.error(f"Không thể xử lý file: {exc}")

    f1, f2 = st.columns([2, 1])
    with f1:
        search_id = st.text_input("🔍 Tìm kiếm theo Mã HS (ví dụ: HS05)", "")
    with f2:
        group_filter = st.selectbox(
            "Lọc theo nhóm",
            ["Tất cả", "Nhóm 1 (< 2h)", "Nhóm 2 (2h – 4h)", "Nhóm 3 (> 4h)", "Cần lưu ý cảnh báo"],
        )

    view_df = df.copy()
    if search_id.strip():
        view_df = view_df[view_df["Mã HS"].str.contains(search_id.strip(), case=False, na=False)]
    if group_filter == "Cần lưu ý cảnh báo":
        view_df = view_df[view_df["Thông điệp gợi ý"] == "Cần xem lại thói quen màn hình và giấc ngủ"]
    elif group_filter != "Tất cả":
        view_df = view_df[view_df["Phân nhóm ĐT"] == group_filter]

    st.dataframe(view_df, use_container_width=True, hide_index=True)


# ==============================================================================
# TRANG 4: CÔNG THỨC EXCEL & TIÊU CHÍ
# ==============================================================================
elif st.session_state.active_page == "Công thức & Tiêu chí":
    st.markdown('<div class="sec-title">⚖️ Quy ước đánh giá & Khu vực công thức Excel (Tin học 9)</div>', unsafe_allow_html=True)
    c_a, c_b = st.columns(2)
    with c_a:
        st.info(
            "**1. Phân loại thời gian sử dụng điện thoại/màn hình**\n"
            "- **Nhóm 1 (< 2 giờ/ngày):** Mức độ an toàn – Duy trì thói quen tốt.\n"
            "- **Nhóm 2 (2 – 4 giờ/ngày):** Mức độ trung bình – Cần quản lý thời gian hợp lý.\n"
            "- **Nhóm 3 (> 4 giờ/ngày):** Ngưỡng cảnh báo theo quy ước học tập của dự án."
        )
    with c_b:
        st.info(
            "**2. Phân loại thời lượng ngủ & thói quen trước ngủ**\n"
            "- **Dưới 8 giờ:** Nhóm dưới mốc khuyến nghị tham khảo cho tuổi 13–18.\n"
            "- **8 – 10 giờ:** Mốc khuyến nghị tham khảo phổ biến cho thanh thiếu niên.\n"
            "- **Dùng màn hình 1 giờ trước ngủ = Có:** Gắn nhãn cần nhắc nhở điều chỉnh thói quen."
        )

    st.markdown("#### Đối chiếu công thức bảng tính Excel (dữ liệu dòng 4 đến dòng 33)")
    formulas = [
        ("1. Tính thời lượng ngủ qua nửa đêm (cột F)", '=ROUND(MOD(E4 - D4, 1) * 24, 1)', "Hàm MOD xử lý trường hợp đi ngủ trước 24:00 (VD 22:30) và thức dậy sau 00:00 (VD 06:30)."),
        ("2. Phân loại 3 nhóm sử dụng điện thoại", '=IF(B4<2, "Nhóm 1 (< 2h)", IF(B4<=4, "Nhóm 2 (2h - 4h)", "Nhóm 3 (> 4h)"))', "Hàm IF lồng nhau phân loại mức độ sử dụng màn hình theo ngày."),
        ("3. Thông điệp cảnh báo tổng hợp (IF + OR)", '=IF(OR(B4>4, C4="Có", F4<8), "Cần xem lại thói quen màn hình và giấc ngủ", "Thói quen tương đối phù hợp")', "Hàm OR kết hợp 3 điều kiện: màn hình > 4h HOẶC dùng trước ngủ HOẶC ngủ < 8h."),
        ("4. Đếm số học sinh Nhóm 3 (> 4h) – COUNTIF", '=COUNTIF(B4:B33, ">4")', "Đếm có điều kiện các học sinh vượt ngưỡng 4 giờ/ngày."),
        ("5. Tính tổng giờ màn hình Nhóm 3 – SUMIF", '=SUMIF(B4:B33, ">4", B4:B33)', "Tính tổng có điều kiện số giờ sử dụng của nhóm > 4 giờ/ngày."),
        ("6. Đếm số học sinh ngủ dưới 8 giờ – COUNTIF", '=COUNTIF(F4:F33, "<8")', "Đếm số học sinh có thời lượng ngủ chưa đạt khuyến nghị 8 giờ."),
    ]
    for title, formula, desc in formulas:
        with st.container(border=True):
            st.markdown(f"**{title}**")
            st.code(formula, language="excel")
            st.caption(desc)


# ==============================================================================
# TRANG 5: KIẾN THỨC & AN TOÀN
# ==============================================================================
elif st.session_state.active_page == "Kiến thức & An toàn":
    st.markdown('<div class="sec-title">📘 Kiến thức nền, Đạo đức dữ liệu & Báo cáo lớp 9B</div>', unsafe_allow_html=True)
    st.markdown(
        "**Một số điểm cần nhớ**\n"
        "- Thanh thiếu niên 13–18 tuổi thường được khuyến nghị ngủ khoảng 8–10 giờ mỗi ngày.\n"
        "- Sử dụng màn hình sát giờ ngủ có thể làm giảm thời gian dành cho nghỉ ngơi hoặc gây khó thư giãn.\n"
        "- Khảo sát tự báo cáo có thể có sai số; dữ liệu lớp học nhỏ không đại diện cho tất cả học sinh."
    )
    st.warning(
        "Không dùng ứng dụng để chẩn đoán, xếp loại sức khỏe hoặc so sánh công khai từng học sinh. "
        "Nếu khó ngủ/mệt mỏi kéo dài, hãy trao đổi với cha mẹ/người chăm sóc hoặc nhân viên y tế."
    )
    st.markdown("**Vai trò của AI trong dự án**")
    st.write(
        "AI chỉ hỗ trợ học sinh và giáo viên trong giai đoạn thiết kế cấu trúc, tạo bản nháp code và giải thích lỗi. "
        "Khi ứng dụng đang chạy, mọi phép tính do Python thực hiện theo quy tắc lập trình sẵn; không có kết nối API AI trả phí."
    )
    st.markdown("#### Tóm tắt báo cáo nhanh (Sẵn sàng sao chép / in ấn)")
    report_text = (
        f"BÁO CÁO KHẢO SÁT THỜI GIAN SỬ DỤNG ĐIỆN THOẠI & GIẤC NGỦ – LỚP 9B\n"
        f"- Tổng số học sinh tham gia (ẩn danh): {summary['total']} học sinh\n"
        f"- Thời gian dùng điện thoại trung bình: {summary['avg_screen']} giờ/ngày\n"
        f"- Thời lượng ngủ trung bình: {summary['avg_sleep']} giờ/đêm (Khuyến nghị: 8–10 giờ)\n"
        f"- Phân bố nhóm sử dụng ĐT: Nhóm 1 (<2h): {summary['g1_count']} HS | Nhóm 2 (2-4h): {summary['g2_count']} HS | Nhóm 3 (>4h): {summary['g3_count']} HS\n"
        f"- Tỷ lệ dùng màn hình trong 1 giờ trước khi ngủ: {summary['before_bed_yes']}/{summary['total']} HS ({summary['before_pct']}%)\n"
        f"- Số trường hợp cần nhắc nhở điều chỉnh thói quen: {summary['warning_count']} HS\n"
        f"Ghi chú: Số liệu phục vụ học tập STEM Tin học 9, không mang tính chẩn đoán y tế."
    )
    st.text_area("Nội dung báo cáo tổng hợp", value=report_text, height=200)

st.divider()
st.caption("Sản phẩm học tập STEM – Tin học 9 | Made by LongLe VC | Dữ liệu vì sức khỏe học đường")
