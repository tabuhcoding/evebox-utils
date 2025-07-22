import uuid
import openai
import pandas as pd
from typing import Optional
import os

# Load environment variables
ASSISTANT_ID = "asst_b93mV8M2dvLRvyh7fKgaI7Du"

def format_percentage(val: float) -> str:
    return f"{val * 100:.2f}%"


def generate_context(data: dict, event: str) -> str:
    event_title = data.get("eventTitle", "Sự kiện không tên")
    start_time = data.get("startTime")
    end_time = data.get("endTime")
    total_clicks = data.get("totalClicks", 0)
    week_clicks = data.get("weekClicks", 0)
    total_users = data.get("totalUsers", 0)
    total_buyers = data.get("totalBuyers", 0)
    total_orders = data.get("totalOrders", 0)
    time_range = f"{start_time} đến {end_time}" if start_time and end_time else "Không rõ"
    conversion_rate = (total_buyers / total_users) if total_users > 0 else 0.0

    visits_df = pd.DataFrame(data.get("statistic", []))
    if not visits_df.empty:
        visits_df = visits_df.rename(columns={'weekStart': 'Tuần bắt đầu', 'visits': 'Lượt truy cập'})
        visits_markdown = visits_df.to_markdown(index=False)
    else:
        visits_markdown = "Không có dữ liệu truy cập theo tuần."

    return f"""
### Dữ liệu tổng quan về hiệu quả sự kiện:
- **Tên sự kiện:** {event_title}
- **Thời gian:** {time_range}
- **Tổng lượt click:** {total_clicks:,}
- **Click trong tuần qua:** {week_clicks:,}
- **Số người dùng:** {total_users:,}
- **Số người mua:** {total_buyers:,}
- **Đơn hàng:** {total_orders:,}
- **Tỷ lệ chuyển đổi:** {format_percentage(conversion_rate)}

### Thống kê theo tuần:
{visits_markdown}

### Sự kiện: {event}
"""


def get_event_analytics(
    query: str = "",
    data: Optional[dict] = None,
    event: Optional[str] = None,
    previous_thread_id: Optional[str] = None
) -> tuple[str, str, dict]:
    if previous_thread_id:
        # Tiếp tục thread cũ
        thread_id = previous_thread_id
    else:
        # Tạo thread mới
        thread = openai.beta.threads.create()
        thread_id = thread.id

        context = generate_context(data, event)
        full_prompt = f"{context}\n\n### Yêu cầu phân tích:\n1. Đánh giá tổng quan.\n2. Phân tích chuyển đổi.\n3. Nhận xét xu hướng.\n4. Đề xuất hành động."
        openai.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=full_prompt
        )

    # Tiếp tục hoặc bắt đầu: gửi câu hỏi
    if query.strip():
        openai.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=query
        )

    # Gọi assistant để xử lý
    run = openai.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID
    )

    # Chờ assistant xử lý xong (polling)
    while True:
        run_status = openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run_status.status in ["completed", "failed"]:
            break

    if run_status.status != "completed":
        return {"error": "Assistant run failed", "previousId": thread_id}

    # Lấy message cuối cùng
    messages = openai.beta.threads.messages.list(thread_id=thread_id, order="desc")
    last_message = messages.data[0].content[0].text.value

    # Get usage
    usage = run_status.usage if run_status.usage else {}

    return last_message, thread_id, dict(usage)
