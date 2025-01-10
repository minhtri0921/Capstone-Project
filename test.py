from graph import app

from langchain_core.messages import HumanMessage, AIMessage

message = "Lương của developer hiện tại tầm khoảng bao nhiêu ?"
config = {
    "configurable": {
        # "user_id": "6702982d6c93b0c530984c25",
        # "session_id": "6702982d6c93b0c530984c25",
    }
}
# HumanMessage(content="Chào bạn"),
# AIMessage(content="Bạn muốn tìm job gì?"),
# HumanMessage(content="Tôi muốn tìm job dạy học cho trung cấp"),
# AIMessage(content=)
history = []
initial_input = {
    "user_query": HumanMessage(content=message),
    "messages_history": [],
    "language": "vi",
}
output_stream = app.stream(initial_input, config, stream_mode="values")
for output in output_stream:
    print("===============================")
