import uuid
import openai
import pandas as pd
from typing import Optional
import os

ASSISTANT_ID = "asst_FiOLqLcownWJRtGRY8jp3S0O"

def format_percentage(val: float) -> str:
  return f"{val * 100:.2f}%"

def generate_context(data: dict, event: str) -> str:
  event_title = data.get("eventTitle", "Sự kiện không tên")
  start_time = data.get("startTime")
  end_time = data.get("endTime")
  tickets_sold = data.get("ticketsSold", 0)
  total_tickets = data.get("totalTickets", 0)
  percentage_sold = data.get("percentageSold", 0.0)
  total_revenue = data.get("totalRevenue", 0)

  time_range = f"{start_time} đến {end_time}" if start_time and end_time else "Không rõ"
  # Format revenueChart
  revenue_df = pd.DataFrame(data.get("revenueChart", []))
  revenue_markdown = revenue_df.to_markdown(index=False) if not revenue_df.empty else "Không có dữ liệu doanh thu theo ngày."

  # Format ticket type
  ticket_type_df = pd.DataFrame(data.get("byTicketType", []))
  ticket_type_markdown = ticket_type_df.to_markdown(index=False) if not ticket_type_df.empty else "Không có dữ liệu theo loại vé."

  return f"""
  ### Dữ liệu tổng quan về doanh thu sự kiện:

  Thông tin sự kiện:
  - Tên sự kiện: {event_title}
  - Thời gian diễn ra: {time_range}
  - Tổng vé đã bán: {tickets_sold} / {total_tickets} vé
  - Tỉ lệ bán ra: {format_percentage(percentage_sold)}
  - Tổng doanh thu: {total_revenue:,} VND

  ### Doanh thu theo tuần:
  {revenue_markdown}

  ### Thống kê loại vé:
  {ticket_type_markdown}

  ### Sự kiện: {event}
  """

def analyze_revenue_event(
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

  # Gửi yêu cầu phân tích
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

  usage = run_status.usage if run_status.usage else {}

  return last_message, thread_id, dict(usage)
