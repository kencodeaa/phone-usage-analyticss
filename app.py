"""Mini App Nhóm B: L2 Dev – Màn hình thông minh, giấc ngủ an lành.

Phiên bản tối ưu chuẩn giao diện dọc điện thoại (Mobile Portrait First).
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
    page_title="L2 Dev | Màn hình thông minh – Giấc ngủ an lành",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# [2] CSS TỐI ƯU GIAO DIỆN DỌC ĐIỆN THOẠI (MOBILE PORTRAIT)
st.markdown(
    """
    <style>
    /* Ẩn header, toolbar, footer mặc định của Streamlit */
    header[data-testid="stHeader"],
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"],
    footer {
        display: none !important;
    }

    .stApp {
        background-color: #0B0F19;
        color: #F3F4F6;
        overflow-x: hidden;
    }

    .block-container {
        padding-top: 0.85rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 0.9rem !important;
        padding-right: 0.9rem !important;
        max-width: 680px !important;
    }

    /* LOGO & BRANDING */
    .brand-wrap {
        display: flex;
        align-items: center;
        gap: 11px;
        margin-bottom: 10px;
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
        box-shadow: 0 4px 14px rgba(59, 130, 246, 0.4);
    }
    .brand-name {
        font-size: 1.15rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.15;
    }
    .brand-sub {
        font-size: 0.68rem;
        font-weight: 600;
        color: #9CA3AF;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    /* TÙY CHỈNH Ô CHỌN MENU (SELECTBOX) CHO GỌN TRÊN ĐIỆN THOẠI */
    div[data-baseweb="select"] > div {
        background-color: #131A2A !important;
        border: 1px solid #2563EB !important;
        border-radius: 12px !important;
        color: #FFFFFF !important;
        min-height: 44px !important;
    }

    /* NÚT BẤM CẢM ỨNG LỚN */
    div.stButton > button {
        border-radius: 12px !important;
        font-weight: 700 !important;
        min-height: 46px !important;
        font-size: 0.92rem !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #3B82F6, #2563EB) !important;
        border: 1px solid #60A5FA !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 14px rgba(59, 130, 246, 0.35) !important;
    }
    div.stButton > button[kind="secondary"] {
        background-color: #131A2A !important;
        border: 1px solid #1F2937 !important;
        color: #E5E7EB !important;
    }

    /* HERO BANNER CHUẨN DỌC (KHÔNG BỊ BÓP CHỮ) */
    .hero-card {
        background: radial-gradient(circle at 80% 20%, rgba(59, 130, 246, 0.18) 0%, rgba(19, 26, 42, 0.98) 60%, #111827 100%);
        border: 1px solid #1F2937;
        border-radius: 18px;
        padding: 20px 18px;
        margin: 10px 0 14px 0;
        width: 100%;
        box-sizing: border-box;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.45);
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        background: rgba(59, 130, 246, 0.15);
        border: 1px solid rgba(96, 165, 250, 0.35);
        color: #93C5FD;
        padding: 5px 12px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 12px;
        line-height: 1.3;
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
        font-size: 1.62rem;
        font-weight: 900;
        line-height: 1.2;
        margin: 0 0 10px 0;
        color: #FFFFFF;
    }
    .hero-heading span {
        background: linear-gradient(90deg, #60A5FA, #818CF8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-desc {
        font-size: 0.88rem;
        color: #CBD5E1;
        line-height: 1.55;
        margin: 0 0 14px 0;
    }
    .hero-pills-row {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }
    .mini-pill {
        flex: 1 1 135px;
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 8px 10px;
    }

    /* TIÊU ĐỀ SECTION & NGUỒN */
    .sec-title {
        font-size: 1.15rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 14px 0 4px 0;
    }
    .sec-sub {
        font-size: 0.83rem;
        color: #9CA3AF;
        margin-bottom: 8px;
    }
    .source-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background-color: #131A2A;
        border: 1px solid #1F2937;
        border-radius: 10px;
        padding: 6px 12px;
        font-size: 0.75rem;
        color: #9CA3AF;
        margin-bottom: 12px;
    }

    /* THẺ KPI 1 CỘT DỌC */
    .kpi-card {
        background-color: #131A2A;
        border: 1px solid #1F2937;
        border-radius: 14px;
        padding: 15px 16px;
        margin-bottom: 10px;
    }
    .kpi-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }
    .kpi-label {
        font-size: 0.82rem;
        font-weight: 600;
        color: #9CA3AF;
    }
    .kpi-value {
        font-size: 1.7rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.15;
    }
    .kpi-sub {
        font-size: 0.78rem;
        margin-top: 5px;
        color: #9CA3AF;
    }
    .kpi-icon {
        width: 30px;
        height: 30px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
    }

    /* 3 THẺ PHÂN NHÓM */
    .group-card {
        border-radius: 14px;
        padding: 15px 16px;
        margin-bottom: 10px;
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
        font-size: 1.65rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 4px 0 2px 0;
    }
    .group-total {
        font-size: 0.84rem;
        color: #D1D5DB;
        margin-bottom: 8px;
    }
    .group-desc {
        font-size: 0.78rem;
        padding-top: 7px;
        border-top: 1px solid rgba(255,255,255,0.08);
    }

    /* THẺ TRUY CẬP NHANH */
    .quick-card {
        background-color: #131A2A;
        border: 1px solid #1F2937;
        border-radius: 14px;
        padding: 15px 16px;
        margin-bottom: 8px;
    }
    .quick-title {
        font-size: 0.98rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 4px;
    }
    .quick-desc {
        font-size: 0.82rem;
        color: #9CA3AF;
        line-height: 1.45;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# [3] KHỞI TẠO DỮ LIỆU & TRẠNG THÁI TRANG
if "survey_df" not in st.session_state:
    st.session_state.survey_df = get_default_survey_data()
if "data_source_label" not in st.session_state:
    st.session_state.data_source_label = "Dữ liệu mô phỏng – Lớp 9B (30 HS)"
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
PLOTLY_CONFIG = {"displayModeBar": False, "responsive": True}

# [4] HEADER + MENU CHỌN MỤC GỌN 1 DÒNG CHO ĐIỆN THOẠI
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

PAGE_OPTIONS = [
    "Trang chủ",
    "Tự kiểm tra",
    "Phân tích khảo sát",
    "Công thức & Tiêu chí",
    "Kiến thức & An toàn",
]
PAGE_LABELS = {
    "Trang chủ": "🏠 Trang chủ",
    "Tự kiểm tra": "🧭 Tự kiểm tra thói quen",
    "Phân tích khảo sát": "📊 Phân tích khảo sát lớp 9B",
    "Công thức & Tiêu chí": "🖩 Công thức Excel & Tiêu chí",
    "Kiến thức & An toàn": "📘 Kiến thức & An toàn",
}

selected = st.selectbox(
    "Chọn trang:",
    options=PAGE_OPTIONS,
    index=PAGE_OPTIONS.index(st.session_state.active_page),
    format_func=lambda k: PAGE_LABELS[k],
    label_visibility="collapsed",
)
if selected != st.session_state.active_page:
    go_to(selected)
    st.rerun()

# ==============================================================================
# TRANG 1: TRANG CHỦ
# ==============================================================================
if st.session_state.active_page == "Trang chủ":
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-badge">
                <span class="hero-dot"></span>
                <span>STEM Tin học 9 • Nhóm B (Long Le)</span>
            </div>
            <h1 class="hero-heading">LÀM CHỦ MÀN HÌNH.<br><span>CHĂM SÓC GIẤC NGỦ.</span></h1>
            <p class="hero-desc">
                Phân tích dữ liệu khảo sát ẩn danh về thời gian sử dụng điện thoại và giấc ngủ.
                Giảm màn hình trước ngủ – nâng cao chất lượng nghỉ ngơi mỗi ngày.
            </p>
            <div class="hero-pills-row">
                <div class="mini-pill">
                    <div style="font-size: 0.76rem; font-weight: 700; color: #60A5FA;">Khuyến nghị ngủ ≥ 8h</div>
                    <div style="font-size: 0.68rem; color: #9CA3AF;">mốc tham khảo tuổi 13–18</div>
                </div>
                <div class="mini-pill">
                    <div style="font-size: 0.76rem; font-weight: 700; color: #F87171;">Dùng ĐT &gt; 4h/ngày</div>
                    <div style="font-size: 0.68rem; color: #9CA3AF;">ngưỡng cảnh báo thói quen</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🧭 Bắt đầu tự kiểm tra", type="primary", use_container_width=True):
        go_to("Tự kiểm tra")
        st.rerun()
    if st.button("📊 Xem phân tích khảo sát", type="secondary", use_container_width=True):
        go_to("Phân tích khảo sát")
        st.rerun()

    st.markdown('<div class="sec-title">Tổng quan khảo sát</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="source-pill"><span class="hero-dot"></span><span>Nguồn: {st.session_state.data_source_label}</span></div>',
        unsafe_allow_html=True,
    )

    kpi_cards = [
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
    for card in kpi_cards:
        st.markdown(card, unsafe_allow_html=True)

    st.markdown('<div class="sec-title">Truy cập nhanh</div>', unsafe_allow_html=True)
    quick_items = [
        ("🧭 Tự kiểm tra thói quen", "Nhập thời gian dùng màn hình và giờ đi ngủ/thức dậy để nhận gợi ý.", "Mở Tự kiểm tra →", "Tự kiểm tra"),
        ("📊 Phân tích khảo sát", "Nạp tệp Excel/CSV, xem 3 nhóm phân loại và biểu đồ trực quan.", "Mở Phân tích khảo sát →", "Phân tích khảo sát"),
        ("📘 Kiến thức & an toàn", "Mốc tham khảo giấc ngủ và nguyên tắc bảo vệ dữ liệu học đường.", "Mở Kiến thức & An toàn →", "Kiến thức & An toàn"),
    ]
    for idx, (q_title, q_desc, q_btn, target) in enumerate(quick_items):
        st.markdown(
            f'<div class="quick-card"><div class="quick-title">{q_title}</div><div class="quick-desc">{q_desc}</div></div>',
            unsafe_allow_html=True,
        )
        if st.button(q_btn, key=f"q_btn_{idx}", use_container_width=True):
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

    screen_hours = st.number_input("Thời gian sử dụng màn hình (giờ/ngày)", 0.0, 24.0, 3.0, 0.5)
    before_sleep = st.radio("Có dùng màn hình trong 1 giờ trước ngủ?", ["Không", "Có"], horizontal=True)
    bedtime = st.time_input("Giờ đi ngủ", value=pd.Timestamp("2026-01-01 22:00").time())
    wake_time = st.time_input("Giờ thức dậy", value=pd.Timestamp("2026-01-02 06:30").time())

    sleep_hours = calculate_sleep_hours(bedtime, wake_time)
    if sleep_hours is None:
        st.warning("Không tính được thời lượng ngủ. Hãy kiểm tra lại giờ đi ngủ và giờ thức dậy.")
    else:
        st.metric("Thời lượng ngủ tính được", f"{sleep_hours:.1f} giờ")
        st.metric(
            "Nhóm thời lượng ngủ",
            "Dưới 8 giờ" if sleep_hours < 8 else ("8–10 giờ" if sleep_hours <= 10 else "Trên 10 giờ"),
        )
        st.metric(
            "Phân nhóm dùng điện thoại",
            "Nhóm 1 (< 2h)" if screen_hours < 2 else ("Nhóm 2 (2h – 4h)" if screen_hours <= 4 else "Nhóm 3 (> 4h)"),
        )

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

    group_cards = [
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
    for g_card in group_cards:
        st.markdown(g_card, unsafe_allow_html=True)

    st.markdown("##### 📊 Phân Phối Học Sinh Theo Nhóm")
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
        margin=dict(l=12, r=12, t=28, b=20),
        height=270,
        dragmode=False,
        yaxis=dict(gridcolor="#1F2937", title="Số HS", dtick=2, fixedrange=True),
        xaxis=dict(gridcolor="#1F2937", fixedrange=True),
    )
    st.plotly_chart(fig_bar, use_container_width=True, config=PLOTLY_CONFIG)

    st.markdown("##### 🌙 Dùng Điện Thoại 1 Giờ Trước Ngủ")
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
        margin=dict(l=12, r=12, t=20, b=24),
        height=270,
        dragmode=False,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
    )
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
