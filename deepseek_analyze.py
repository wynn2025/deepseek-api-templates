"""
DeepSeek V4 API - 数据分析模板
==============================
功能：用AI分析CSV/JSON数据，生成洞察报告
使用：python deepseek_analyze.py <数据文件路径>

环境要求：
  pip install openai pandas

特色：
  - 自动检测文件格式（CSV/JSON）
  - 支持自定义分析问题
  - 输出结构化分析报告
  - 大文件自动采样（避免超出token限制）
"""

import json
import csv
import sys
import os
from openai import OpenAI

# ============ 配置区域 ============
API_KEY = "sk-your-api-key-here"
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-chat"
MAX_DATA_TOKENS = 30000  # 数据部分最大token估算值
# ==================================


def create_client():
    return OpenAI(api_key=API_KEY, base_url=BASE_URL)


def load_csv(filepath, max_rows=500):
    """加载CSV文件，返回格式化的文本"""
    import pandas as pd
    df = pd.read_csv(filepath)
    
    # 如果数据量太大，采样
    if len(df) > max_rows:
        print(f"  注意：数据{len(df)}行，采样{max_rows}行以适应API限制")
        df = df.sample(n=max_rows, random_state=42)
    
    # 基本信息
    info = f"数据概览：{len(df)}行 x {len(df.columns)}列\n"
    info += f"列名：{', '.join(df.columns.tolist())}\n"
    info += f"数据类型：\n{df.dtypes.to_string()}\n\n"
    info += f"统计摘要：\n{df.describe(include='all').to_string()}\n\n"
    info += f"前10行数据：\n{df.head(10).to_string()}\n"
    
    return info


def load_json(filepath, max_items=200):
    """加载JSON文件"""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if isinstance(data, list):
        if len(data) > max_items:
            print(f"  注意：数据{len(data)}条，采样{max_items}条")
            import random
            data = random.sample(data, max_items)
        return json.dumps(data[:max_items], ensure_ascii=False, indent=2)
    else:
        return json.dumps(data, ensure_ascii=False, indent=2)


def analyze_data(client, data_text, question, file_info=""):
    """分析数据"""
    system_prompt = """你是一个数据分析专家。请基于提供的数据回答用户问题。
要求：
1. 使用清晰的数据支撑你的结论
2. 如果数据不足以回答，请说明
3. 给出具体的数字和百分比
4. 如有趋势，请指出
5. 回答用中文"""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"""文件信息：{file_info}

数据内容：
{data_text}

分析问题：{question}"""}
    ]
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.3,  # 数据分析用低temperature更准确
        max_tokens=4096
    )
    return response.choices[0].message.content


def batch_analyze(client, data_text, questions, file_info=""):
    """批量分析 - 对同一数据集回答多个问题"""
    results = []
    for i, question in enumerate(questions, 1):
        print(f"\n[{i}/{len(questions)}] 分析中: {question[:50]}...")
        result = analyze_data(client, data_text, question, file_info)
        results.append({"question": question, "answer": result})
        print(result)
        print("-" * 40)
    return results


def main():
    if len(sys.argv) < 2:
        print("用法: python deepseek_analyze.py <数据文件.csv/.json>")
        print("示例: python deepseek_analyze.py sales_data.csv")
        sys.exit(1)
    
    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"错误：文件不存在 {filepath}")
        sys.exit(1)
    
    client = create_client()
    
    # 自动检测格式并加载
    ext = os.path.splitext(filepath)[1].lower()
    print(f"加载数据文件: {filepath}")
    
    if ext == ".csv":
        data_text = load_csv(filepath)
        file_info = f"CSV文件: {filepath}"
    elif ext == ".json":
        data_text = load_json(filepath)
        file_info = f"JSON文件: {filepath}"
    else:
        print(f"不支持的格式: {ext}，仅支持 .csv 和 .json")
        sys.exit(1)
    
    print(f"数据加载完成，开始分析...\n")
    print("=" * 50)
    print("  数据分析助手")
    print("  输入问题进行分析，输入 'quit' 退出")
    print("  输入 'auto' 自动生成分析报告")
    print("=" * 50)
    
    while True:
        question = input("\n分析问题: ").strip()
        if not question:
            continue
        if question.lower() == "quit":
            break
        if question.lower() == "auto":
            # 自动生成分析报告
            auto_questions = [
                "请概括这份数据的整体情况",
                "数据中有哪些值得关注的异常或模式？",
                "基于数据，你能给出什么业务建议？"
            ]
            batch_analyze(client, data_text, auto_questions, file_info)
        else:
            result = analyze_data(client, data_text, question, file_info)
            print(f"\n{result}")


if __name__ == "__main__":
    main()
