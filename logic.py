"""Các hàm xử lý dữ liệu độc lập với giao diện Streamlit.

Học sinh có thể đọc module này trước để hiểu các phép tính cốt lõi.
Ứng dụng không gọi dịch vụ AI hoặc API trả phí khi đang chạy.
"""
from __future__ import annotations
import io
import pandas as pd

REQUIRED_COLUMNS = [
    "Mã HS",
    "Thời gian sử dụng màn hình (giờ/ngày)",
    "Có sử dụng màn hình trong 1 giờ trước khi ngủ? (Có/Không)",
    "Giờ đi ngủ",
    "Giờ thức dậy",
    "Thời lượng ngủ (giờ)",
    "Tự đánh giá ngủ đủ? (Có/Không)",
]

SCREEN_LOW_HOURS = 2.0
SCREEN_LIMIT_HOURS = 4.0  # Ngưỡng minh họa của dự án, không phải chuẩn y tế.
SLEEP_MIN_HOURS = 8.0
SLEEP_MAX_HOURS = 10.0


def get_default_survey_data() -> pd.DataFrame:
    """Tạo bộ dữ liệu mô phỏng 30 học sinh lớp 9B làm dữ liệu khởi tạo mặc định."""
    records = [
        ("HS01", 1.0, "Không", "22:00", "06:30", "Có"),
        ("HS02", 1.2, "Không", "22:15", "06:30", "Có"),
        ("HS03", 1.5, "Không", "22:00", "06:15", "Có"),
        ("HS04", 0.8, "Không", "21:45", "06:15", "Có"),
        ("HS05", 1.8, "Có", "22:30", "06:15", "Có"),
        ("HS06", 1.0, "Không", "22:00", "06:00", "Có"),
        ("HS07", 1.3, "Không", "22:15", "06:30", "Có"),
        ("HS08", 1.1, "Không", "22:00", "06:30", "Có"),
        ("HS09", 0.9, "Không", "21:30", "06:00", "Có"),
        ("HS10", 1.0, "Không", "22:00", "06:15", "Có"),
        ("HS11", 1.2, "Có", "22:30", "06:30", "Có"),
        ("HS12", 2.5, "Không", "22:45", "06:15", "Có"),
        ("HS13", 3.0, "Có", "23:15", "06:15", "Không"),
        ("HS14", 2.8, "Không", "22:30", "06:30", "Có"),
        ("HS15", 3.5, "Có", "23:30", "06:30", "Không"),
        ("HS16", 2.2, "Không", "22:30", "06:15", "Có"),
        ("HS17", 3.2, "Có", "23:15", "06:00", "Không"),
        ("HS18", 2.9, "Không", "23:00", "06:15", "Không"),
        ("HS19", 3.8, "Có", "23:45", "06:15", "Không"),
        ("HS20", 2.4, "Có", "23:00", "06:30", "Có"),
        ("HS21", 3.0, "Không", "22:45", "06:15", "Có"),
        ("HS22", 4.5, "Có", "00:00", "06:15", "Không"),
        ("HS23", 5.0, "Có", "00:30", "06:15", "Không"),
        ("HS24", 4.2, "Có", "23:45", "06:15", "Không"),
        ("HS25", 4.8, "Có", "00:15", "06:15", "Không"),
        ("HS26", 5.2, "Có", "00:30", "06:00", "Không"),
        ("HS27", 4.4, "Có", "23:30", "06:00", "Không"),
        ("HS28", 4.6, "Có", "00:00", "06:15", "Không"),
        ("HS29", 5.3, "Có", "00:45", "06:15", "Không"),
        ("HS30", 4.5, "Có", "23:45", "06:00", "Không"),
    ]
    rows = []
    for code, screen, before, bed, wake, self_eval in records:
        sleep_h = calculate_sleep_hours(bed, wake)
        rows.append({
            "Mã HS": code,
            "Thời gian sử dụng màn hình (giờ/ngày)": screen,
            "Có sử dụng màn hình trong 1 giờ trước khi ngủ? (Có/Không)": before,
            "Giờ đi ngủ": bed,
            "Giờ thức dậy": wake,
            "Thời lượng ngủ (giờ)": sleep_h,
            "Tự đánh giá ngủ đủ? (Có/Không)": self_eval,
        })
    return prepare_dataframe(pd.DataFrame(rows))


def _to_hour(value):
    """Đổi giá trị thời gian Excel/pandas hoặc chuỗi HH:MM thành số phút trong ngày."""
    if pd.isna(value):
        return None
    if hasattr(value, "hour") and hasattr(value, "minute"):
        return value.hour * 60 + value.minute
    text = str(value).strip()
    if not text:
        return None
    try:
        parts = text.split(":")
        hour, minute = int(parts[0]), int(parts[1])
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            return None
        return hour * 60 + minute
    except (ValueError, IndexError):
        return None


def calculate_sleep_hours(bedtime, wake_time):
    """Tính số giờ ngủ từ giờ đi ngủ đến giờ thức dậy, kể cả qua nửa đêm."""
    start, end = _to_hour(bedtime), _to_hour(wake_time)
    if start is None or end is None or start == end:
        return None
    minutes = (end - start) % (24 * 60)
    if minutes <= 0:
        return None
    return round(minutes / 60, 2)


def classify_screen_group_3(hours):
    """Phân 3 nhóm sử dụng điện thoại cho Dashboard (<2h, 2h-4h, >4h)."""
    if pd.isna(hours):
        return "Chưa đủ dữ liệu"
    val = float(hours)
    if val < SCREEN_LOW_HOURS:
        return "Nhóm 1 (< 2h)"
    if val <= SCREEN_LIMIT_HOURS:
        return "Nhóm 2 (2h – 4h)"
    return "Nhóm 3 (> 4h)"


def classify_screen_time(hours):
    """Phân nhóm thời gian màn hình theo ngưỡng học tập > 4 giờ/ngày."""
    if pd.isna(hours):
        return "Chưa đủ dữ liệu"
    return "Trên 4 giờ/ngày" if float(hours) > SCREEN_LIMIT_HOURS else "Không quá 4 giờ/ngày"


def classify_sleep(hours):
    """Phân nhóm thời lượng ngủ theo mốc tham khảo 8–10 giờ cho tuổi 13–18."""
    if pd.isna(hours):
        return "Chưa đủ dữ liệu"
    value = float(hours)
    if value < SLEEP_MIN_HOURS:
        return "Dưới 8 giờ"
    if value <= SLEEP_MAX_HOURS:
        return "8–10 giờ"
    return "Trên 10 giờ"


def create_message(screen_hours, before_sleep, sleep_hours):
    """Tạo thông điệp giáo dục theo quy tắc IF/OR; không phải chẩn đoán."""
    if pd.isna(screen_hours) or before_sleep not in ("Có", "Không") or pd.isna(sleep_hours):
        return "Chưa đủ dữ liệu để tạo thông điệp"
    if float(screen_hours) > SCREEN_LIMIT_HOURS or before_sleep == "Có" or float(sleep_hours) < SLEEP_MIN_HOURS:
        return "Cần xem lại thói quen màn hình và giấc ngủ"
    return "Thói quen tương đối phù hợp theo quy ước dự án"


def prepare_dataframe(raw_df):
    """Chuẩn hóa dữ liệu đầu vào, tính lại cột suy ra và kiểm tra lỗi cơ bản."""
    df = raw_df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError("Thiếu cột bắt buộc: " + ", ".join(missing))

    df = df[REQUIRED_COLUMNS].copy()
    df["Mã HS"] = df["Mã HS"].astype("string").str.strip()
    df["Thời gian sử dụng màn hình (giờ/ngày)"] = pd.to_numeric(
        df["Thời gian sử dụng màn hình (giờ/ngày)"], errors="coerce"
    )
    yes_no_cols = [
        "Có sử dụng màn hình trong 1 giờ trước khi ngủ? (Có/Không)",
        "Tự đánh giá ngủ đủ? (Có/Không)",
    ]
    for col in yes_no_cols:
        df[col] = df[col].astype("string").str.strip().str.capitalize()

    sleep_values = [
        calculate_sleep_hours(bed, wake)
        for bed, wake in zip(df["Giờ đi ngủ"], df["Giờ thức dậy"])
    ]
    df["Thời lượng ngủ (giờ)"] = sleep_values
    screen_col = "Thời gian sử dụng màn hình (giờ/ngày)"
    before_col = yes_no_cols[0]

    df["Phân nhóm ĐT"] = df[screen_col].apply(classify_screen_group_3)
    df["Nhóm thời gian màn hình"] = df[screen_col].apply(classify_screen_time)
    df["Nhóm thời lượng ngủ"] = df["Thời lượng ngủ (giờ)"].apply(classify_sleep)
    df["Thông điệp gợi ý"] = [
        create_message(s, b, h)
        for s, b, h in zip(df[screen_col], df[before_col], df["Thời lượng ngủ (giờ)"])
    ]
    return df


def validate_dataframe(df):
    """Trả về danh sách cảnh báo dữ liệu, không tự sửa/đoán câu trả lời."""
    issues = []
    id_col = "Mã HS"
    if df[id_col].isna().any() or (df[id_col].astype("string").str.len() == 0).any():
        issues.append("Có dòng chưa có mã học sinh.")
    duplicates = df.loc[df[id_col].notna(), id_col].duplicated()
    if duplicates.any():
        issues.append("Có mã học sinh bị trùng.")
    screen_col = "Thời gian sử dụng màn hình (giờ/ngày)"
    invalid_screen = df[screen_col].notna() & ~df[screen_col].between(0, 24)
    if invalid_screen.any():
        issues.append(f"Có {int(invalid_screen.sum())} giá trị thời gian màn hình ngoài khoảng 0–24 giờ.")
    for col in [
        "Có sử dụng màn hình trong 1 giờ trước khi ngủ? (Có/Không)",
        "Tự đánh giá ngủ đủ? (Có/Không)",
    ]:
        bad = df[col].notna() & ~df[col].isin(["Có", "Không"])
        if bad.any():
            issues.append(f"Cột “{col}” có giá trị khác Có/Không.")
    if df["Thời lượng ngủ (giờ)"].isna().any():
        issues.append(f"Có {int(df['Thời lượng ngủ (giờ)'].isna().sum())} dòng chưa tính được thời lượng ngủ.")
    if df["Thời lượng ngủ (giờ)"].notna().any() and (df["Thời lượng ngủ (giờ)"] > 16).any():
        issues.append("Có thời lượng ngủ trên 16 giờ; cần xác minh lại giờ đi ngủ/thức dậy.")
    return issues


def summarize_dataframe(df):
    """Tạo bộ chỉ số KPI & thống kê tổng hợp cho Dashboard và Excel."""
    screen_col = "Thời gian sử dụng màn hình (giờ/ngày)"
    sleep_col = "Thời lượng ngủ (giờ)"
    before_col = "Có sử dụng màn hình trong 1 giờ trước khi ngủ? (Có/Không)"

    total = int(df["Mã HS"].notna().sum())
    avg_screen = round(float(df[screen_col].mean()), 1) if total > 0 else 0.0
    avg_sleep = round(float(df[sleep_col].mean()), 1) if total > 0 else 0.0

    before_yes = int((df[before_col] == "Có").sum())
    before_no = int((df[before_col] == "Không").sum())
    before_pct = round((before_yes / total) * 100) if total > 0 else 0

    warning_count = int((df["Thông điệp gợi ý"] == "Cần xem lại thói quen màn hình và giấc ngủ").sum())

    g1_mask = df["Phân nhóm ĐT"] == "Nhóm 1 (< 2h)"
    g2_mask = df["Phân nhóm ĐT"] == "Nhóm 2 (2h – 4h)"
    g3_mask = df["Phân nhóm ĐT"] == "Nhóm 3 (> 4h)"

    return {
        "total": total,
        "avg_screen": avg_screen,
        "avg_sleep": avg_sleep,
        "before_bed_yes": before_yes,
        "before_bed_no": before_no,
        "before_pct": before_pct,
        "warning_count": warning_count,
        "g1_count": int(g1_mask.sum()),
        "g1_sum": round(float(df.loc[g1_mask, screen_col].sum()), 1),
        "g2_count": int(g2_mask.sum()),
        "g2_sum": round(float(df.loc[g2_mask, screen_col].sum()), 1),
        "g3_count": int(g3_mask.sum()),
        "g3_sum": round(float(df.loc[g3_mask, screen_col].sum()), 1),
        "screen_over": int((df["Nhóm thời gian màn hình"] == "Trên 4 giờ/ngày").sum()),
        "sleep_under": int((df["Nhóm thời lượng ngủ"] == "Dưới 8 giờ").sum()),
        "sum_screen_over": round(float(df.loc[df["Nhóm thời gian màn hình"] == "Trên 4 giờ/ngày", screen_col].sum()), 1),
        "sum_sleep_under": round(float(df.loc[df["Nhóm thời lượng ngủ"] == "Dưới 8 giờ", sleep_col].sum()), 1),
    }


def export_excel_workbook(df: pd.DataFrame) -> bytes:
    """Xuất file Excel gồm 2 sheet: Du_lieu_khao_sat (đúng định dạng dòng 3) và Thong_ke_tong_hop."""
    output = io.BytesIO()
    summary = summarize_dataframe(df)
    stat_df = pd.DataFrame([
        ["Tổng số học sinh khảo sát", summary["total"], "COUNTA(A4:A33)"],
        ["Thời gian dùng ĐT trung bình (giờ/ngày)", summary["avg_screen"], "AVERAGE(B4:B33)"],
        ["Thời lượng ngủ trung bình (giờ/ngày)", summary["avg_sleep"], "AVERAGE(F4:F33)"],
        ["Số HS Nhóm 1 (< 2h)", summary["g1_count"], 'COUNTIF(B4:B33, "<2")'],
        ["Tổng giờ Nhóm 1 (< 2h)", summary["g1_sum"], 'SUMIF(B4:B33, "<2", B4:B33)'],
        ["Số HS Nhóm 2 (2h – 4h)", summary["g2_count"], 'COUNTIFS(B4:B33, ">=2", B4:B33, "<=4")'],
        ["Tổng giờ Nhóm 2 (2h – 4h)", summary["g2_sum"], 'SUMIFS(B4:B33, B4:B33, ">=2", B4:B33, "<=4")'],
        ["Số HS Nhóm 3 (> 4h)", summary["g3_count"], 'COUNTIF(B4:B33, ">4")'],
        ["Tổng giờ Nhóm 3 (> 4h)", summary["g3_sum"], 'SUMIF(B4:B33, ">4", B4:B33)'],
        ["Số HS ngủ dưới 8 giờ", summary["sleep_under"], 'COUNTIF(F4:F33, "<8")'],
        ["Số HS dùng màn hình trước ngủ 1h", summary["before_bed_yes"], 'COUNTIF(C4:C33, "Có")'],
    ], columns=["Chỉ tiêu thống kê", "Kết quả", "Công thức Excel minh họa"])

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Du_lieu_khao_sat", index=False, startrow=2)
        ws = writer.sheets["Du_lieu_khao_sat"]
        ws["A1"] = "DỰ ÁN STEM TIN HỌC 9 – DỮ LIỆU VÌ SỨC KHỎE HỌC ĐƯỜNG (NHÓM B)"
        ws["A2"] = "Lưu ý: Dữ liệu ẩn danh phục vụ mục đích giáo dục, không dùng để chẩn đoán y tế."
        stat_df.to_excel(writer, sheet_name="Thong_ke_tong_hop", index=False)

    return output.getvalue()
