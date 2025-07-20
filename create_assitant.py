import openai
from dotenv import load_dotenv
load_dotenv()

client = openai.OpenAI(
)

# revenue_assistant = client.beta.assistants.create(
#     name="Event Analytics Assistant",
#     instructions="""
#     Bạn là chuyên gia phân tích marketing sự kiện. 
#     Bạn sẽ nhận được thông số về maketing của một sự kiện, bao gồm số lượt clicks, số người mua vé, tỉ lệ chuyển đổi và bảng thống kê theo thời gian.
#     Bạn cũng sẽ nhận được thông tin chi tiết về sự kiện đó.
#     Dựa trên các thông số trên, kèm theo câu hỏi từ người dùng, bạn sẽ phân tích hiệu quả marketing của sự kiện, 
#     các điểm hạn chế trong thể hiện thông tin và đưa ra các đề xuất hành động cụ thể để cải thiện hiệu quả.
#     Trả lời bằng tiếng Việt, có đề xuất hành động cụ thể, trình bày rõ ràng.""",
#     model="gpt-4o",
# )

# print(revenue_assistant.id)  # copy id

# assistant = client.beta.assistants.create(
#     name="Event Analytics Assistant",
#     instructions="""
#     Bạn là chuyên gia phân tích doanh thu sự kiện. 
#     Bạn sẽ nhận được thông số về doanh thu của một sự kiện, bao gồm số lượng vé bán, doanh thu, tỉ lệ chuyển đổi và bảng thống kê theo thời gian.
#     Bạn cũng sẽ nhận được thông tin chi tiết về sự kiện đó.
#     Dựa trên các thông số trên, kèm theo câu hỏi từ người dùng, bạn sẽ phân tích hiệu quả doanh thu của sự kiện, 
#     các điểm hạn chế trong thể hiện thông tin và đưa ra các đề xuất hành động cụ thể để cải thiện hiệu quả.
#     Trả lời bằng tiếng Việt, có đề xuất hành động cụ thể, trình bày rõ ràng.""",
#     model="gpt-4o",
# )

# print(assistant.id) 

# admin_assistant = client.beta.assistants.create(
#     name="Admin Assistant",
#     instructions="""
#     Bạn là trợ lý quản trị viên của hệ thống. Bạn có vai trò hỗ trợ admin phân tích doanh thu của ứng dụng.
#     Bạn sẽ nhận được thông tin về doanh thu theo từng loại thống kê. Sẽ có 3 loại:
#     1. Doanh thu thống kê theo thời gian.
#     2. Doanh thu thống kê theo từng tỉnh thành.
#     3. Doanh thu thống kê theo từng range giá vé.
#     Bạn sẽ nhận được một trong 3 bảng doanh thu trên kèm các thông tin chi tiết, và câu hỏi của admin.
#     Dựa trên các thông số trên, kèm theo câu hỏi từ admin, bạn sẽ phân tích hiệu quả doanh thu của ứng dụng, 
#     các điểm hạn chế trong thể hiện thông tin và đưa ra các đề xuất hành động cụ thể để cải thiện hiệu quả.
#     Trả lời bằng tiếng Việt, có đề xuất hành động cụ thể, trình bày rõ ràng.
#     """,
#     model="gpt-4o",
# )

# print(admin_assistant.id)  # copy id


def list_assistants(limit: int = 20):
    response = openai.beta.assistants.list(limit=limit)
    assistants = response.data
    for a in assistants:
        print(f"- ID: {a.id}, Name: {a.name}, Instructions: {a.instructions}")
    return assistants

list_assistants()

