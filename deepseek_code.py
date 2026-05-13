"""
DeepSeek V4 API - 代码生成模板
==============================
功能：利用DeepSeek V4生成、解释、优化代码
使用：运行后选择模式，输入需求

环境要求：
  pip install openai

特色：
  - 三种模式：生成代码 / 解释代码 / 优化代码
  - 内置代码专用系统提示词
  - 流式输出，实时看到代码
"""

from openai import OpenAI
import json

# ============ 配置区域 ============
API_KEY = "sk-your-api-key-here"
BASE_URL = "https://api.deepseek.com"
# DeepSeek-Coder V2 专为代码优化（也可用 deepseek-chat）
MODEL = "deepseek-coder"  # 或 "deepseek-chat"
# ==================================


CODE_SYSTEM_PROMPT = """你是一个资深全栈工程师，精通Python/JavaScript/TypeScript/Go/Rust等主流语言。
请遵循以下规范：
1. 代码必须有完整的错误处理
2. 关键函数必须有中文注释
3. 优先使用标准库或主流第三方库
4. 代码风格遵循PEP8/ESLint等规范
5. 如果用户没有指定语言，默认使用Python
"""


def create_client():
    return OpenAI(api_key=API_KEY, base_url=BASE_URL)


def generate_code(client, prompt, language="Python"):
    """根据需求生成代码"""
    messages = [
        {"role": "system", "content": CODE_SYSTEM_PROMPT},
        {"role": "user", "content": f"请用{language}编写以下功能的代码：\n\n{prompt}"}
    ]
    return _stream_response(client, messages)


def explain_code(client, code):
    """解释一段代码的功能"""
    messages = [
        {"role": "system", "content": "你是一个代码解读专家，请用清晰易懂的中文解释代码。"},
        {"role": "user", "content": f"请逐行解释以下代码的功能和逻辑：\n\n```\n{code}\n```"}
    ]
    return _stream_response(client, messages)


def optimize_code(client, code, goal="性能和可读性"):
    """优化一段代码"""
    messages = [
        {"role": "system", "content": CODE_SYSTEM_PROMPT},
        {"role": "user", "content": f"""请优化以下代码，优化目标：{goal}
要求：
1. 输出优化后的完整代码
2. 在代码后说明做了哪些优化以及原因

原始代码：
```
{code}
```"""}
    ]
    return _stream_response(client, messages)


def _stream_response(client, messages):
    """流式输出响应"""
    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.3,  # 代码生成用较低temperature更稳定
        stream=True
    )
    full_text = ""
    for chunk in stream:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            full_text += content
    print()
    return full_text


def main():
    client = create_client()
    
    print("=" * 50)
    print("  DeepSeek 代码助手")
    print("  1. 生成代码  2. 解释代码  3. 优化代码")
    print("=" * 50)
    
    while True:
        choice = input("\n选择模式 (1/2/3, quit退出): ").strip()
        
        if choice == "quit":
            break
        elif choice == "1":
            lang = input("编程语言 (默认Python): ").strip() or "Python"
            prompt = input("描述你需要的功能: ").strip()
            if prompt:
                print(f"\n--- 生成 {lang} 代码 ---")
                generate_code(client, prompt, lang)
        elif choice == "2":
            print("粘贴代码（输入 END 结束）:")
            lines = []
            while True:
                line = input()
                if line.strip() == "END":
                    break
                lines.append(line)
            code = "\n".join(lines)
            if code:
                print("\n--- 代码解释 ---")
                explain_code(client, code)
        elif choice == "3":
            print("粘贴代码（输入 END 结束）:")
            lines = []
            while True:
                line = input()
                if line.strip() == "END":
                    break
                lines.append(line)
            code = "\n".join(lines)
            goal = input("优化目标 (默认: 性能和可读性): ").strip() or "性能和可读性"
            if code:
                print("\n--- 优化后代码 ---")
                optimize_code(client, code, goal)


if __name__ == "__main__":
    main()
