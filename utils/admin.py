import openai
import pandas as pd
from typing import Optional

# Load environment variables
ASSISTANT_ID = "asst_RERShkfyWERhLWBvg4N4O9fX"

def format_percentage(val: float) -> str:
    return f"{val * 100:.2f}%"


def generate_context(data: dict) -> str:
    visits_df = pd.DataFrame(data.get("chart", []))
    if not visits_df.empty:
        # visits_df = visits_df.rename(columns={'weekStart': 'Tuần bắt đầu', 'visits': 'Lượt truy cập'})
        visits_markdown = visits_df.to_markdown(index=False)
    else:
        visits_markdown = "Không có dữ liệu truy cập theo tuần."

    return f"""
### Thống kê theo tuần:
{visits_markdown}
"""


def get_event_analytics(
    query: str = "",
    data: Optional[dict] = None,
    previous_thread_id: Optional[str] = None
) -> tuple[str, str]:
    if previous_thread_id:
        # Tiếp tục thread cũ
        thread_id = previous_thread_id
    else:
        # Tạo thread mới
        thread = openai.beta.threads.create()
        thread_id = thread.id

        context = generate_context(data)
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

    return last_message, thread_id
