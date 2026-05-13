"""
DeepSeek V4 API - 基础对话模板
==============================
功能：与DeepSeek V4进行多轮对话
使用：直接运行，在终端中与AI对话

环境要求：
  pip install openai

配置：
  将下方 API_KEY 替换为你的DeepSeek API密钥
  获取地址：https://platform.deepseek.com/
"""

from openai import OpenAI

# ============ 配置区域 ============
API_KEY = "sk-your-api-key-here"  # 替换为你的API密钥
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-chat"  # DeepSeek V4 对话模型
# ==================================


def create_client():
    """创建OpenAI兼容客户端"""
    return OpenAI(api_key=API_KEY, base_url=BASE_URL)


def chat_completion(client, messages, temperature=0.7, max_tokens=2048):
    """
    发送对话请求
    参数：
        messages: 消息列表 [{"role": "user/assistant/system", "content": "..."}]
        temperature: 创造性 0-2，越高越随机
        max_tokens: 最大回复长度
    """
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=False  # 设为True可开启流式输出
    )
    return response.choices[0].message.content


def chat_stream(client, messages, temperature=0.7):
    """流式对话 - 逐字输出，体验更好"""
    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
        stream=True
    )
    full_text = ""
    for chunk in stream:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            full_text += content
    print()  # 换行
    return full_text


def main():
    """交互式多轮对话"""
    client = create_client()
    
    # 系统提示词 - 定义AI的角色
    system_prompt = "你是DeepSeek AI助手，一个 helpful、准确、友好的AI。"
    messages = [{"role": "system", "content": system_prompt}]
    
    print("=" * 50)
    print("  DeepSeek V4 对话助手")
    print("  输入 'quit' 退出，输入 'clear' 清空对话历史")
    print("=" * 50)
    
    while True:
        user_input = input("\n你: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("再见！")
            break
        if user_input.lower() == "clear":
            messages = [{"role": "system", "content": system_prompt}]
            print("对话历史已清空")
            continue
        
        messages.append({"role": "user", "content": user_input})
        
        print("AI: ", end="")
        reply = chat_stream(client, messages)
        
        messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
