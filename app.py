"""Mini App Nhóm B: L2 Dev – Màn hình thông minh, giấc ngủ an lành.

Tích hợp sẵn:
1. Màn hình chọn thiết bị ban đầu (Điện thoại / Máy tính) ngay trong app.py.
2. Giao diện Mobile Portrait chuyên biệt (Menu chọn nhanh 1 dòng, Hero 1 cột không bóp chữ).
3. Giao diện Desktop Dashboard đa cột đầy đủ.
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

# [1] CẤU HÌNH TRANG
st.set_page_config(
    page_title="Mini app nhóm B | Màn hình thông minh – Giấc ngủ an lành",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# [2] KHỞI TẠO SESSION STATE
if "device_mode" not in st.session_state:
    st.session_state.device_mode = None  # None = Màn hình chọn thiết bị | "mobile" | "desktop"
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


# [3] CSS CHUNG + SỬA TRIỆT ĐỂ LỖI BÓP CHỮ TRÊN ĐIỆN THOẠI
st.markdown(
    """
    <style>
    header[data-testid="stHeader"], footer, div[data-testid="stToolbar"] {
        display: none !important;
    }
    .stApp {
        background-color: #0B0F19;
        color: #F3F4F6;
        overflow-x: hidden;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 1360px;
    }

    /* LOGO */
    .brand-wrap {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 6px;
    }
    .brand-icon {
        width: 40px;
        height: 40px;
        min-width: 40px;
        background: linear-gradient(135deg, #3B82F6, #2563EB);
        border-radius: 11px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 19px;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.4);
    }
    .brand-name {
        font-size: 1.12rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.15;
    }
    .brand-sub {
        font-size: 0.68rem;
        font-weight: 600;
        color: #9CA3AF;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }

    /* NÚT BẤM */
    div.stButton > button {
        border-radius: 11px !important;
        font-weight: 600 !important;
        min-height: 44px !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button[kind="secondary"] {
        background-color: #131A2A !important;
        border: 1px solid #1F2937 !important;
        color: #E5E7EB !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        border-color: #60A5FA !important;
        color: #FFFFFF !important;
    }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #3B82F6, #2563EB) !important;
        border: 1px solid #60A5FA !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 14px rgba(59, 130, 246, 0.35) !important;
    }

    /* MÀN HÌNH CHỌN THIẾT BỊ (PORTAL) */
    .portal-box {
        background: linear-gradient(160deg, #131A2A 0%, #0D1322 100%);
        border: 1px solid #1F2937;
        border-radius: 18px;
        padding: 24px 20px;
        margin-bottom: 10px;
        height: 100%;
    }
    .portal-title {
        font-size: 1.2rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 12px 0 6px 0;
    }
    .portal-desc {
        font-size: 0.86rem;
        color: #9CA3AF;
        line-height: 1.5;
        margin-bottom: 12px;
    }

    /* HERO BANNER (DESKTOP & MOBILE) */
    .hero-card {
        background: radial-gradient(circle at 82% 45%, rgba(59, 130, 246, 0.16) 0%, rgba(19, 26, 42, 0.96) 55%, #111827 100%);
        border: 1px solid #1F2937;
        border-radius: 18px;
        padding: 30px 32px;
        margin: 10px 0 20px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 24px;
        width: 100%;
    }
    .hero-text-col {
        flex: 1;
        width: 100%;
        min-width: 0;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(59, 130, 246, 0.14);
        border: 1px solid rgba(96, 165, 250, 0.32);
        color: #93C5FD;
        padding: 5px 13px;
        border-radius: 999px;
        font-size: 0.76rem;
        font-weight: 600;
        margin-bottom: 12px;
        max-width: 100%;
        white-space: normal;
        line-height: 1.35;
    }
    .hero-dot {
        width: 7px;
        height: 7px;
        min-width: 7px;
        border-radius: 50%;
        background-color: #60A5FA;
        box-shadow: 0 0 8px #60A5FA;
    }
    .hero-heading {
        font-size: 2.2rem;
        font-weight: 900;
        line-height: 1.15;
        margin: 0 0 12px 0;
        color: #FFFFFF;
        word-break: normal;
    }
    .hero-heading span {
        background: linear-gradient(90deg, #60A5FA, #818CF8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-desc {
        font-size: 0.94rem;
        color: #CBD5E1;
        line-height: 1.55;
        margin: 0;
    }
    .hero-visual {
        position: relative;
        min-width: 280px;
        height: 210px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .float-pill {
        position: absolute;
        background: rgba(15, 23, 42, 0.92);
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 7px 11px;
    }

    /* CLASS RIÊNG CHO CHẾ ĐỘ ĐIỆN THOẠI (KHÔNG PHỤ THUỘC MEDIA QUERY) */
    .hero-card.mobile-layout {
        flex-direction: column;
        align-items: flex-start;
        padding: 20px 18px;
        gap: 14px;
    }
    .hero-card.mobile-layout .hero-heading {
        font-size: 1.55rem;
        line-height: 1.22;
    }
    .hero-card.mobile-layout .hero-desc {
        font-size: 0.88rem;
    }
    .hero-card.mobile-layout .hero-visual {
        width: 100%;
        min-width: 100%;
        height: 170px;
    }

    /* THẺ KPI & PHÂN NHÓM */
    .sec-title {
        font-size: 1.18rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 8px 0 4px 0;
    }
    .sec-sub {
        font-size: 0.85rem;
        color: #9CA3AF;
        margin-bottom: 10px;
    }
    .source-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background-color: #131A2A;
        border: 1px solid #1F2937;
        border-radius: 12px;
        padding: 6px 12px;
        font-size: 0.76rem;
        color: #9CA3AF;
        margin-bottom: 14px;
    }
    .kpi-card {
        background-color: #131A2A;
        border: 1px solid #1F2937;
        border-radius: 14px;
        padding: 16px 18px;
        margin-bottom: 10px;
        height: 100%;
    }
    .kpi-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    .kpi-label {
        font-size: 0.82rem;
        font-weight: 600;
        color: #9CA3AF;
    }
    .kpi-value {
        font-size: 1.75rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.1;
    }
    .kpi-sub {
        font-size: 0.78rem;
        margin-top: 6px;
        color: #9CA3AF;
    }
    .kpi-icon {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 15px;
    }
    .group-card {
        border-radius: 14px;
        padding: 16px 18px;
        margin-bottom: 10px;
        height: 100%;
    }
    .group-1 {
        background: linear-gradient(145deg, #10253E 0%, #111927 100%);
        border: 1px solid #1D4ED8;
    }
    .group-2 {
        background: linear-gradient(145deg, #1E1B3A 0%, #111927 100%);
        border: 1px solid #4F46E5;
    }
    .group-3 {
        background: linear-gradient(145deg, #2D1520 0%, #111927 100%);
        border: 1px solid #DC2626;
    }
    .group-title {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
    }
    .group-val {
        font-size: 1.7rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 6px 0 2px 0;
    }
    .group-total {
        font-size: 0.84rem;
        color: #D1D5DB;
        margin-bottom: 8px;
    }
    .group-desc {
        font-size: 0.78rem;
        padding-top: 8px;
        border-top: 1px solid rgba(255,255,255,0.08);
    }
    .quick-card {
        background-color: #131A2A;
        border: 1px solid #1F2937;
        border-radius: 14px;
        padding: 16px 18px;
        margin-bottom: 8px;
    }
    .quick-title {
        font-size: 1rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 4px;
    }
    .quick-desc {
        font-size: 0.83rem;
        color: #9CA3AF;
        line-height: 1.45;
    }

    @media (max-width: 768px) {
        .hero-card {
            flex-direction: column;
            align-items: flex-start;
            padding: 20px 18px;
        }
        .hero-heading {
            font-size: 1.55rem;
        }
        .hero-visual {
            width: 100%;
            min-width: 100%;
            height: 170px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# BƯỚC 1: MÀN HÌNH CHỌN THIẾT BỊ BAN ĐẦU (ĐIỆN THOẠI / MÁY TÍNH)
# ==============================================================================
if st.session_state.device_mode is None:
    st.markdown(
        """
        <div class="brand-wrap" style="margin-bottom: 14px;">
            <div class="brand-icon">📱</div>
            <div>
                <div class="brand-name">L<sup>2</sup> Dev</div>
                <div class="brand-sub">SCREEN &amp; SLEEP ANALYTICS • STEM TIN HỌC 9</div>
            </div>
        </div>
        <div class="hero-card mobile-layout" style="margin-top: 4px;">
            <div class="hero-text-col">
                <div class="hero-badge"><span class="hero-dot"></span><span>Bước 1: Chọn giao diện hiển thị</span></div>
                <h1 class="hero-heading">MÀN HÌNH THÔNG MINH.<br><span>GIẤC NGỦ AN LÀNH.</span></h1>
                <p class="hero-desc">Chọn thiết bị bạn đang sử dụng để tối ưu bố cục hiển thị dữ liệu khảo sát lớp 9B.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_m, col_d = st.columns(2)
    with col_m:
        st.markdown(
            """
            <div class="portal-box" style="border-color: #3B82F6;">
                <div style="font-size: 28px;">📱</div>
                <div class="portal-title">Giao diện Điện thoại (Chế độ dọc)</div>
                <div class="portal-desc">Bố cục 1 cột gọn gàng, thanh menu chọn nhanh 1 dòng, biểu đồ khóa cuộn nhầm cho iPhone &amp; Android.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("📱 Vào bản Điện thoại", type="primary", use_container_width=True):
            st.session_state.device_mode = "mobile"
            st.rerun()

    with col_d:
        st.markdown(
            """
            <div class="portal-box">
                <div style="font-size: 28px;">💻</div>
                <div class="portal-title">Giao diện Máy tính (Màn hình rộng)</div>
                <div class="portal-desc">Dashboard đa cột đầy đủ, thanh điều hướng ngang, phù hợp Laptop, PC và trình chiếu máy chiếu trên lớp.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("💻 Vào bản Máy tính", type="secondary", use_container_width=True):
            st.session_state.device_mode = "desktop"
            st.rerun()

    st.stop()


# ==============================================================================
# BƯỚC 2: GIAO DIỆN CHÍNH (TỰ ĐỘNG ĐIỀU CHỈNH THEO CHẾ ĐỘ ĐÃ CHỌN)
# ==============================================================================
is_mobile = st.session_state.device_mode == "mobile"
df = st.session_state.survey_df
summary = summarize_dataframe(df)
PLOTLY_CONFIG = {"displayModeBar": False, "responsive": True}

PAGE_OPTIONS = [
    "Trang chủ",
    "Tự kiểm tra",
    "Phân tích khảo sát",
    "Công thức & Tiêu chí",
    "Kiến thức & An toàn",
]

# HEADER + THANH ĐIỀU HƯỚNG
if is_mobile:
    # Trên điện thoại: Logo + nút đổi chế độ nằm trên 1 hàng gọn, Menu là 1 ô Selectbox duy nhất
    h_left, h_right = st.columns([2.2, 1.3])
    with h_left:
        st.markdown(
            """
            <div class="brand-wrap">
                <div class="brand-icon">📱</div>
                <div>
                    <div class="brand-name">L<sup>2</sup> Dev</div>
                    <div class="brand-sub">BẢN ĐIỆN THOẠI</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with h_right:
        if st.button("💻 Đổi sang PC", key="switch_to_pc", use_container_width=True):
            st.session_state.device_mode = "desktop"
            st.rerun()

    page_labels = {
        "Trang chủ": "🏠 Trang chủ",
        "Tự kiểm tra": "🧭 Tự kiểm tra thói quen",
        "Phân tích khảo sát": "📊 Phân tích khảo sát lớp 9B",
        "Công thức & Tiêu chí": "🖩 Công thức Excel & Tiêu chí",
        "Kiến thức & An toàn": "📘 Kiến thức & An toàn",
    }
    selected_page = st.selectbox(
        "Chuyển mục chức năng:",
        options=PAGE_OPTIONS,
        index=PAGE_OPTIONS.index(st.session_state.active_page),
        format_func=lambda k: page_labels[k],
        label_visibility="collapsed",
    )
    if selected_page != st.session_state.active_page:
        go_to(selected_page)
        st.rerun()
else:
    # Trên máy tính: Thanh điều hướng ngang đầy đủ + nút chuyển về bản Mobile
    nav_logo, nav_p1, nav_p2, nav_p3, nav_p4, nav_p5, nav_sw = st.columns([2.4, 1.15, 1.3, 1.5, 1.35, 1.4, 1.0])
    with nav_logo:
        st.markdown(
            """
            <div class="brand-wrap">
                <div class="brand-icon">📱</div>
                <div>
                    <div class="brand-name">L<sup>2</sup> Dev</div>
                    <div class="brand-sub">SCREEN &amp; SLEEP ANALYTICS</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    desktop_navs = [
        ("Trang chủ", "🏠 Trang chủ", nav_p1),
        ("Tự kiểm tra", "🧭 Tự kiểm tra", nav_p2),
        ("Phân tích khảo sát", "📊 Phân tích", nav_p3),
        ("Công thức & Tiêu chí", "🖩 Công thức", nav_p4),
        ("Kiến thức & An toàn", "📘 Kiến thức", nav_p5),
    ]
    for p_key, p_label, col in desktop_navs:
        with col:
            b_type = "primary" if st.session_state.active_page == p_key else "secondary"
            if st.button(p_label, key=f"nav_{p_key}", use_container_width=True, type=b_type):
                go_to(p_key)
                st.rerun()
    with nav_sw:
        if st.button("📱 Mobile", key="switch_to_mb", use_container_width=True):
            st.session_state.device_mode = "mobile"
            st.rerun()


# ==============================================================================
# TRANG 1: TRANG CHỦ
# ==============================================================================
if st.session_state.active_page == "Trang chủ":
    hero_cls = "hero-card mobile-layout" if is_mobile else "hero-card"
    svg_size = "155" if is_mobile else "215"
    st.markdown(
        f"""
        <div class="{hero_cls}">
            <div class="hero-text-col">
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
                <svg width="{svg_size}" height="{svg_size}" viewBox="0 0 220 220" fill="none" xmlns="http://www.w3.org/2000/svg">
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
                <div class="float-pill" style="top: 4px; right: 4px;">
                    <div style="font-size: 0.72rem; font-weight: 700; color: #60A5FA;">Khuyến nghị ngủ ≥ 8h</div>
                    <div style="font-size: 0.64rem; color: #9CA3AF;">mốc tham khảo tuổi 13–18</div>
                </div>
                <div class="float-pill" style="bottom: 4px; left: 4px;">
                    <div style="font-size: 0.72rem; font-weight: 700; color: #F87171;">Dùng ĐT &gt; 4 giờ/ngày</div>
                    <div style="font-size: 0.64rem; color: #9CA3AF;">ngưỡng cảnh báo thói quen</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if is_mobile:
        if st.button("🧭 Bắt đầu tự kiểm tra", type="primary", use_container_width=True):
            go_to("Tự kiểm tra")
            st.rerun()
        if st.button("📊 Xem phân tích khảo sát", type="secondary", use_container_width=True):
            go_to("Phân tích khảo sát")
            st.rerun()
    else:
        cta1, cta2, _ = st.columns([2.0, 2.1, 5.9])
        with cta1:
            if st.button("🧭 Bắt đầu tự kiểm tra", type="primary", use_container_width=True):
                go_to("Tự kiểm tra")
                st.rerun()
        with cta2:
            if st.button("📊 Xem phân tích khảo sát", type="secondary", use_container_width=True):
                go_to("Phân tích khảo sát")
                st.rerun()

    st.markdown('<div class="sec-title">Tổng quan khảo sát</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="source-pill"><span class="hero-dot"></span><span>Nguồn: {st.session_state.data_source_label}</span></div>',
        unsafe_allow_html=True,
    )

    kpi_cards_html = [
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
    ]

    if is_mobile:
        for card_html in kpi_cards_html:
            st.markdown(card_html, unsafe_allow_html=True)
    else:
        cols = st.columns(4)
        for col, card_html in zip(cols, kpi_cards_html):
            with col:
                st.markdown(card_html, unsafe_allow_html=True)

    st.markdown('<div class="sec-title">Truy cập nhanh</div>', unsafe_allow_html=True)
    quick_items = [
        ("🧭 Tự kiểm tra thói quen", "Nhập thời gian dùng màn hình và giờ đi ngủ/thức dậy để nhận gợi ý.", "Mở Tự kiểm tra →", "Tự kiểm tra"),
        ("📊 Phân tích khảo sát", "Nạp tệp Excel/CSV, xem 3 nhóm phân loại và biểu đồ trực quan.", "Mở Phân tích khảo sát →", "Phân tích khảo sát"),
        ("📘 Kiến thức & an toàn", "Mốc tham khảo giấc ngủ và nguyên tắc bảo vệ dữ liệu học đường.", "Mở Kiến thức & An toàn →", "Kiến thức & An toàn"),
    ]
    if is_mobile:
        for idx, (q_title, q_desc, q_btn, target) in enumerate(quick_items):
            st.markdown(
                f'<div class="quick-card"><div class="quick-title">{q_title}</div><div class="quick-desc">{q_desc}</div></div>',
                unsafe_allow_html=True,
            )
            if st.button(q_btn, key=f"q_mb_{idx}", use_container_width=True):
                go_to(target)
                st.rerun()
    else:
        q_cols = st.columns(3)
        for idx, (col, (q_title, q_desc, q_btn, target)) in enumerate(zip(q_cols, quick_items)):
            with col:
                st.markdown(
                    f'<div class="quick-card"><div class="quick-title">{q_title}</div><div class="quick-desc">{q_desc}</div></div>',
                    unsafe_allow_html=True,
                )
                if st.button(q_btn, key=f"q_pc_{idx}", use_container_width=True):
                    go_to(target)
                    st.rerun()


# ==============================================================================
# TRANG 2: TỰ KIỂM TRA THÓI QUEN
# ==============================================================================
elif st.session_state.active_page == "Tự kiểm tra":
    st.markdown('<div class="sec-title">🧭 Tự xem lại một số thói quen cá nhân</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sec-sub">Nhập thông tin để xem cách ứng dụng phân tích. Không cần nhập họ tên.</div>',
        unsafe_allow_html=True,
    )

    if is_mobile:
        screen_hours = st.number_input("Thời gian sử dụng màn hình (giờ/ngày)", 0.0, 24.0, 3.0, 0.5)
        before_sleep = st.radio("Có dùng màn hình trong 1 giờ trước ngủ?", ["Không", "Có"], horizontal=True)
        bedtime = st.time_input("Giờ đi ngủ", value=pd.Timestamp("2026-01-01 22:00").time())
        wake_time = st.time_input("Giờ thức dậy", value=pd.Timestamp("2026-01-02 06:30").time())
    else:
        c1, c2 = st.columns(2)
        with c1:
            screen_hours = st.number_input("Thời gian sử dụng màn hình (giờ/ngày)", 0.0, 24.0, 3.0, 0.5)
            before_sleep = st.radio("Có sử dụng màn hình trong 1 giờ trước khi ngủ?", ["Không", "Có"], horizontal=True)
        with c2:
            bedtime = st.time_input("Giờ đi ngủ", value=pd.Timestamp("2026-01-01 22:00").time())
            wake_time = st.time_input("Giờ thức dậy", value=pd.Timestamp("2026-01-02 06:30").time())

    sleep_hours = calculate_sleep_hours(bedtime, wake_time)
    if sleep_hours is None:
        st.warning("Không tính được thời lượng ngủ. Hãy kiểm tra lại giờ đi ngủ và giờ thức dậy.")
    else:
        sleep_grp = "Dưới 8 giờ" if sleep_hours < 8 else ("8–10 giờ" if sleep_hours <= 10 else "Trên 10 giờ")
        phone_grp = "Nhóm 1 (< 2h)" if screen_hours < 2 else ("Nhóm 2 (2h – 4h)" if screen_hours <= 4 else "Nhóm 3 (> 4h)")
        if is_mobile:
            st.metric("Thời lượng ngủ tính được", f"{sleep_hours:.1f} giờ")
            st.metric("Nhóm thời lượng ngủ", sleep_grp)
            st.metric("Phân nhóm dùng điện thoại", phone_grp)
        else:
            m1, m2, m3 = st.columns(3)
            m1.metric("Thời lượng ngủ tính được", f"{sleep_hours:.1f} giờ")
            m2.metric("Nhóm thời lượng ngủ", sleep_grp)
            m3.metric("Phân nhóm dùng điện thoại", phone_grp)

        msg = create_message(screen_hours, before_sleep, sleep_hours)
        if msg.startswith("Cần"):
            st.warning(f"⚠️ {msg}")
        else:
            st.success(f"✅ {msg}")


# ==============================================================================
# TRANG 3: PHÂN TÍCH KHẢO SÁT
# ==============================================================================
elif st.session_state.active_page == "Phân tích khảo sát":
    st.markdown('<div class="sec-title">📊 Phân tích chi tiết khảo sát lớp 9B</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="source-pill"><span class="hero-dot"></span><span>Nguồn: {st.session_state.data_source_label}</span></div>',
        unsafe_allow_html=True,
    )

    group_cards_html = [
        f"""
        <div class="group-card group-1">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="group-title" style="color:#60A5FA;">NHÓM 1 (&lt; 2H)</span><span>🛡️</span>
            </div>
            <div class="group-val">{summary['g1_count']} HS</div>
            <div class="group-total">Tổng: <b>{summary['g1_sum']}h</b></div>
            <div class="group-desc" style="color:#60A5FA;">Mức độ an toàn - Duy trì thói quen tốt</div>
        </div>
        """,
        f"""
        <div class="group-card group-2">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="group-title" style="color:#A5B4FC;">NHÓM 2 (2H - 4H)</span><span>⚖️</span>
            </div>
            <div class="group-val">{summary['g2_count']} HS</div>
            <div class="group-total">Tổng: <b>{summary['g2_sum']}h</b></div>
            <div class="group-desc" style="color:#A5B4FC;">Mức độ trung bình - Cần quản lý thời gian</div>
        </div>
        """,
        f"""
        <div class="group-card group-3">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="group-title" style="color:#F87171;">NHÓM 3 (&gt; 4H)</span><span>🚨</span>
            </div>
            <div class="group-val">{summary['g3_count']} HS</div>
            <div class="group-total">Tổng: <b>{summary['g3_sum']}h</b></div>
            <div class="group-desc" style="color:#F87171;">Nguy cơ cao - Cần nhắc nhở và điều chỉnh</div>
        </div>
        """,
    ]

    if is_mobile:
        for g_html in group_cards_html:
            st.markdown(g_html, unsafe_allow_html=True)
    else:
        g_cols = st.columns(3)
        for col, g_html in zip(g_cols, group_cards_html):
            with col:
                st.markdown(g_html, unsafe_allow_html=True)

    fig_bar = go.Figure(
        data=[
            go.Bar(
                x=["Nhóm 1 (<2h)", "Nhóm 2 (2–4h)", "Nhóm 3 (>4h)"],
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
        font=dict(color="#E5E7EB", size=12),
        margin=dict(l=14, r=14, t=28, b=20),
        height=280,
        dragmode=False,
        yaxis=dict(gridcolor="#1F2937", title="Số HS", dtick=2, fixedrange=True),
        xaxis=dict(gridcolor="#1F2937", fixedrange=True),
    )

    fig_donut = go.Figure(
        data=[
            go.Pie(
                labels=["Có dùng", "Không dùng"],
                values=[summary["before_bed_yes"], summary["before_bed_no"]],
                hole=0.58,
                marker=dict(colors=["#F59E0B", "#3B82F6"], line=dict(color="#131A2A", width=3)),
                textinfo="label+percent",
                textfont=dict(color="#F3F4F6", size=12),
            )
        ]
    )
    fig_donut.update_layout(
        paper_bgcolor="#131A2A",
        plot_bgcolor="#131A2A",
        font=dict(color="#E5E7EB", size=12),
        margin=dict(l=14, r=14, t=24, b=24),
        height=280,
        dragmode=False,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
    )

    if is_mobile:
        st.markdown("##### 📊 Phân Phối Học Sinh Theo Nhóm")
        st.plotly_chart(fig_bar, use_container_width=True, config=PLOTLY_CONFIG)
        st.markdown("##### 🌙 Dùng Điện Thoại 1 Giờ Trước Ngủ")
        st.plotly_chart(fig_donut, use_container_width=True, config=PLOTLY_CONFIG)
    else:
        c_left, c_right = st.columns(2)
        with c_left:
            st.markdown("##### 📊 Phân Phối Học Sinh Theo Nhóm")
            st.plotly_chart(fig_bar, use_container_width=True, config=PLOTLY_CONFIG)
        with c_right:
            st.markdown("##### 🌙 Dùng Điện Thoại 1 Giờ Trước Ngủ")
            st.plotly_chart(fig_donut, use_container_width=True, config=PLOTLY_CONFIG)

    st.divider()
    st.markdown("#### ⊞ Quản lý & Tra cứu Dữ liệu Khảo sát")
    uploaded = st.file_uploader(
        "Tải file Excel Nhóm B (.xlsx, .xls) hoặc CSV ẩn danh",
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

    search_id = st.text_input("🔍 Tìm kiếm theo Mã HS (ví dụ: HS05)", "")
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
    st.markdown('<div class="sec-title">⚖️ Quy ước đánh giá & Công thức Excel (Tin học 9)</div>', unsafe_allow_html=True)
    st.info(
        "**1. Phân loại thời gian sử dụng điện thoại/màn hình**\n"
        "- **Nhóm 1 (< 2 giờ/ngày):** Mức độ an toàn – Duy trì thói quen tốt.\n"
        "- **Nhóm 2 (2 – 4 giờ/ngày):** Mức độ trung bình – Cần quản lý thời gian hợp lý.\n"
        "- **Nhóm 3 (> 4 giờ/ngày):** Ngưỡng cảnh báo theo quy ước học tập của dự án."
    )
    st.info(
        "**2. Phân loại thời lượng ngủ & thói quen trước ngủ**\n"
        "- **Dưới 8 giờ:** Nhóm dưới mốc khuyến nghị tham khảo cho tuổi 13–18.\n"
        "- **8 – 10 giờ:** Mốc khuyến nghị tham khảo phổ biến cho thanh thiếu niên.\n"
        "- **Dùng màn hình 1 giờ trước ngủ = Có:** Gắn nhãn cần nhắc nhở điều chỉnh thói quen."
    )

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
