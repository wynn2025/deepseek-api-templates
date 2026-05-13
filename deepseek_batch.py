"""
DeepSeek V4 API - 批量处理模板
==============================
功能：批量处理文本任务（翻译/摘要/分类/改写等）
使用：python deepseek_batch.py

环境要求：
  pip install openai

特色：
  - 从文件读取输入，批量输出结果
  - 支持并发请求（加速处理）
  - 自动保存结果到文件
  - 内置5种常用任务模板
  - 断点续传（跳过已处理项）
"""

import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI

# ============ 配置区域 ============
API_KEY = "sk-your-api-key-here"
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-chat"
MAX_CONCURRENT = 3  # 并发数（注意API限流）
# ==================================


# ---- 内置任务模板 ----
TASK_TEMPLATES = {
    "translate": {
        "system": "你是一个专业翻译，将文本翻译为{target_lang}，只输出翻译结果。",
        "user": "{text}"
    },
    "summarize": {
        "system": "你是一个文本摘要专家，请将文本压缩为{max_words}字以内的摘要。",
        "user": "{text}"
    },
    "classify": {
        "system": "你是一个文本分类器，请将文本分类到以下类别之一：{categories}。只输出类别名称。",
        "user": "{text}"
    },
    "rewrite": {
        "system": "你是一个文案改写专家，请改写文本使其更加{style}。只输出改写后的文本。",
        "user": "{text}"
    },
    "sentiment": {
        "system": "你是一个情感分析专家，请判断文本的情感倾向。只输出：正面/负面/中性",
        "user": "{text}"
    }
}


def create_client():
    return OpenAI(api_key=API_KEY, base_url=BASE_URL)


def process_single(client, text, task_type, **params):
    """处理单条文本"""
    template = TASK_TEMPLATES.get(task_type)
    if not template:
        raise ValueError(f"未知任务类型: {task_type}，可选: {list(TASK_TEMPLATES.keys())}")
    
    system_prompt = template["system"].format(**params)
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        temperature=0.3,
        max_tokens=1024
    )
    return response.choices[0].message.content


def process_batch(client, items, task_type, output_file="batch_results.json", **params):
    """
    批量处理文本列表
    参数：
        items: 文本列表 [{"id": 1, "text": "..."}, ...]
        task_type: 任务类型
        output_file: 结果输出文件
        params: 模板参数
    """
    # 断点续传：加载已处理的结果
    completed = {}
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    result = json.loads(line)
                    completed[result["id"]] = result
    
    # 过滤已完成的项
    pending = [item for item in items if item["id"] not in completed]
    
    if completed:
        print(f"  断点续传：已完成 {len(completed)} 项，剩余 {len(pending)} 项")
    
    results = list(completed.values())
    failed = []
    
    def _process(item):
        try:
            result = process_single(client, item["text"], task_type, **params)
            return {"id": item["id"], "input": item["text"][:100], "result": result, "status": "ok"}
        except Exception as e:
            return {"id": item["id"], "input": item["text"][:100], "error": str(e), "status": "error"}
    
    # 并发处理
    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT) as executor:
        futures = {executor.submit(_process, item): item for item in pending}
        
        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            results.append(result)
            
            # 实时写入文件（追加模式）
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(result, ensure_ascii=False) + "\n")
            
            if result["status"] == "ok":
                print(f"  [{i}/{len(pending)}] ID:{result['id']} ✓ {result['result'][:60]}")
            else:
                failed.append(result)
                print(f"  [{i}/{len(pending)}] ID:{result['id']} ✗ {result['error']}")
    
    print(f"\n完成！成功 {len(results) - len(failed)} 项，失败 {len(failed)} 项")
    print(f"结果已保存到: {output_file}")
    return results


def load_input_file(filepath):
    """加载输入文件（每行一条JSON或纯文本）"""
    items = []
    with open(filepath, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
                if "id" not in item:
                    item["id"] = i + 1
            except json.JSONDecodeError:
                # 纯文本模式
                item = {"id": i + 1, "text": line}
            items.append(item)
    return items


def quick_demo():
    """快速演示"""
    client = create_client()
    
    demo_items = [
        {"id": 1, "text": "今天天气真好，适合出去玩！"},
        {"id": 2, "text": "这个产品质量太差了，强烈不推荐。"},
        {"id": 3, "text": "明天下午三点开会，请注意准时参加。"},
        {"id": 4, "text": "Python is a great programming language for beginners."},
        {"id": 5, "text": "DeepSeek V4 is an amazing open source AI model."},
    ]
    
    print("=== 情感分析演示 ===\n")
    process_batch(client, demo_items, "sentiment", output_file="demo_sentiment.json")
    
    print("\n=== 翻译演示 ===\n")
    process_batch(client, demo_items[3:], "translate", 
                  output_file="demo_translate.json", target_lang="中文")


if __name__ == "__main__":
    client = create_client()
    
    print("=" * 50)
    print("  DeepSeek 批量处理工具")
    print("  1. 快速演示  2. 从文件处理")
    print("=" * 50)
    
    choice = input("选择模式 (1/2): ").strip()
    
    if choice == "1":
        quick_demo()
    elif choice == "2":
        input_file = input("输入文件路径: ").strip()
        items = load_input_file(input_file)
        print(f"加载了 {len(items)} 条数据")
        
        print(f"\n可用任务类型: {', '.join(TASK_TEMPLATES.keys())}")
        task_type = input("选择任务类型: ").strip()
        
        output_file = input("输出文件 (默认 batch_results.json): ").strip() or "batch_results.json"
        
        # 根据任务类型获取额外参数
        params = {}
        if task_type == "translate":
            params["target_lang"] = input("目标语言 (默认: 中文): ").strip() or "中文"
        elif task_type == "summarize":
            params["max_words"] = input("最大字数 (默认: 100): ").strip() or "100"
        elif task_type == "classify":
            params["categories"] = input("类别列表 (逗号分隔): ").strip()
        elif task_type == "rewrite":
            params["style"] = input("改写风格 (如: 专业/口语化/学术): ").strip() or "专业"
        
        process_batch(client, items, task_type, output_file, **params)
