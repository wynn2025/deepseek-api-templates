#!/usr/bin/env python3
"""DeepSeek API Templates - Interactive launcher"""
import sys, os

TEMPLATES = {
    "1": ("Chat (对话)", "deepseek_chat.py"),
    "2": ("Code Generation (代码生成)", "deepseek_code.py"),
    "3": ("Data Analysis (数据分析)", "deepseek_analyze.py"),
    "4": ("Batch Processing (批量处理)", "deepseek_batch.py"),
}

def main():
    print("DeepSeek V4 API Templates")
    print("=" * 40)
    if not os.environ.get("DEEPSEEK_API_KEY"):
        print("[!] Please set DEEPSEEK_API_KEY first")
        print("    export DEEPSEEK_API_KEY=your-key")
        sys.exit(1)

    print("\nSelect a template:")
    for k, (desc, _) in TEMPLATES.items():
        print("  {}. {}".format(k, desc))
    print()

    choice = input("Enter choice (1-4): ").strip()
    if choice in TEMPLATES:
        script = TEMPLATES[choice][1]
        print("\nRunning {}...\n".format(script))
        os.execvp(sys.executable, [sys.executable, script])
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
