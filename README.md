# DeepSeek V4 API 调用模板集

> 一套开箱即用的 DeepSeek V4 API Python 模板，覆盖对话、代码生成、数据分析、批量处理四大场景。  
> 零配置、带注释、可直接运行。

## 快速开始（30秒上手）

```bash
# 1. 安装依赖
pip install openai pandas

# 2. 填入你的API密钥（每个脚本顶部）
API_KEY = "sk-xxxxxxxxxxxxxxxx"

# 3. 运行任意模板
python deepseek_chat.py       # 开始聊天
python deepseek_code.py       # 代码助手
python deepseek_analyze.py sales.csv  # 分析数据
python deepseek_batch.py      # 批量处理
```

**API 密钥获取：** 注册 [DeepSeek 开放平台](https://platform.deepseek.com/) → API Keys → 创建密钥  
**费用：** DeepSeek V4 约 1-2 元/百万 token，日常使用一天不到 1 元

---

## 模板一览

| 模板 | 文件 | 功能 | 适用场景 |
|------|------|------|----------|
| 基础对话 | `deepseek_chat.py` | 多轮对话+流式输出 | 聊天机器人、客服 |
| 代码助手 | `deepseek_code.py` | 生成/解释/优化代码 | 编程辅助 |
| 数据分析 | `deepseek_analyze.py` | CSV/JSON 智能分析 | 数据报告 |
| 批量处理 | `deepseek_batch.py` | 翻译/摘要/分类等 | 文本批处理 |

---

## 详细使用示例

### 示例1：基础对话（deepseek_chat.py）

```bash
python deepseek_chat.py
```

**运行效果：**
```
==================================================
  DeepSeek V4 对话助手
  输入 'quit' 退出，输入 'clear' 清空对话历史
==================================================

你: 用Python写一个快速排序

AI: def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

# 测试
print(quicksort([3, 6, 8, 10, 1, 2, 1]))
# 输出: [1, 1, 2, 3, 6, 8, 10]

你: 再加一个参数控制升序还是降序

AI: def quicksort(arr, reverse=False):
    ...
```

**特色功能：**
- 流式逐字输出，体验丝滑
- 自动维护对话上下文
- `clear` 清空历史重新开始
- 可自定义系统提示词改变AI角色

> 截图说明：终端界面，上方显示欢迎信息，下方为交互对话，AI回复带颜色高亮

---

### 示例2：代码助手（deepseek_code.py）

```bash
python deepseek_code.py
```

**三种模式演示：**

**模式1 - 生成代码：**
```
选择模式: 1
编程语言: Python
描述功能: 读取Excel文件，统计每个部门的平均工资，生成柱状图

--- 生成 Python 代码 ---
import pandas as pd
import matplotlib.pyplot as plt

def analyze_salary(excel_path):
    """读取Excel并统计部门平均工资"""
    df = pd.read_excel(excel_path)
    dept_salary = df.groupby('部门')['工资'].mean()
    
    plt.figure(figsize=(10, 6))
    dept_salary.plot(kind='bar', color='steelblue')
    plt.title('各部门平均工资')
    plt.ylabel('工资（元）')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('salary_report.png')
    print(f"报告已生成: salary_report.png")
    return dept_salary

if __name__ == '__main__':
    result = analyze_salary('employees.xlsx')
    print(result)
```

**模式2 - 解释代码：** 粘贴任意代码，AI逐行解读逻辑  
**模式3 - 优化代码：** 粘贴代码+优化目标，输出优化版本+改动说明

> 截图说明：三栏对比（原始需求 → 生成代码 → 运行效果）

---

### 示例3：数据分析（deepseek_analyze.py）

```bash
# 分析CSV文件
python deepseek_analyze.py sales_data.csv

# 分析JSON文件
python deepseek_analyze.py users.json
```

**运行效果：**
```
加载数据文件: sales_data.csv
  数据概览：1000行 x 8列
  列名：日期, 产品, 销量, 单价, 总额, 地区, 渠道, 客户等级

==================================================
  数据分析助手
  输入 'auto' 自动生成完整报告
==================================================

分析问题: auto

[1/3] 哪些产品的销量增长最快？
→ 2026年Q1销量增长Top3：智能手表(+47%)、蓝牙耳机(+32%)、机械键盘(+28%)

[2/3] 不同地区的销售表现？
→ 华东地区占总销售额38%领跑，华南(22%)第二，华北(18%)第三...

[3/3] 有什么业务建议？
→ 建议加大华东智能手表库存，华南可主推蓝牙耳机...
```

**支持格式：** CSV、JSON  
**大文件处理：** 自动采样避免超token限制  
**auto模式：** 一键生成完整分析报告

> 截图说明：上方显示数据加载信息，下方为问答交互，AI回复包含数据表格

---

### 示例4：批量处理（deepseek_batch.py）

```bash
python deepseek_batch.py
```

**5种内置任务：**

| 模板 | 说明 | 输入 | 输出 |
|------|------|------|------|
| translate | 多语言翻译 | 英文产品描述 | 中文翻译 |
| summarize | 文本摘要 | 长篇文章 | 100字摘要 |
| classify | 文本分类 | 用户反馈 | 问题类型 |
| rewrite | 文案改写 | 口语文案 | 专业版本 |
| sentiment | 情感分析 | 商品评价 | 正面/负面/中性 |

**并发处理效果：**
```
=== 情感分析演示 ===

  [1/5] ID:1 ✓ 正面
  [2/5] ID:2 ✓ 负面
  [3/5] ID:3 ✓ 中性
  [4/5] ID:4 ✓ 正面
  [5/5] ID:5 ✓ 正面

完成！成功 5 项，失败 0 项
结果已保存到: demo_sentiment.json
```

**高级功能：**
- 并发请求（可配置并发数，默认3）
- 断点续传（中断后自动跳过已完成项）
- JSON Lines 格式实时写入
- 自定义任务模板

> 截图说明：左侧为输入文件预览，右侧为处理进度和结果

---

## 文件说明

```
deepseek-api-templates/
├── deepseek_chat.py      # 对话模板（95行）
├── deepseek_code.py      # 代码模板（130行）
├── deepseek_analyze.py   # 数据分析模板（170行）
├── deepseek_batch.py     # 批量处理模板（220行）
└── README.md             # 说明文档
```

**代码特点：**
- 每个文件独立运行，无需互相依赖
- 关键函数都有中文注释
- 配置区域集中在文件顶部，修改方便
- 适合初学者学习和二次开发

---

## 常见问题

**Q：API 调用费用多少？**  
A：DeepSeek V4 定价约 1-2 元/百万 token。日常使用一天不到 1 元，非常经济。

**Q：需要什么Python版本？**  
A：Python 3.7+，推荐 3.11。

**Q：如何修改模型？**  
A：编辑脚本中的 `MODEL` 变量。可选：`deepseek-chat`（对话）、`deepseek-coder`（代码）。

**Q：出现 Rate Limit 错误怎么办？**  
A：降低 `MAX_CONCURRENT` 并发数，或在循环中添加 `time.sleep(1)` 延迟。

**Q：可以用在其他兼容OpenAI API的平台吗？**  
A：可以！修改 `BASE_URL` 即可。支持：硅基流动、DeepSeek、OpenAI 等。

---

## 技术支持

购买后如遇问题，请在购买平台留言，会尽快回复。

---

## License

MIT License - 购买后可自由修改和用于商业项目。

---

## 获取完整版

本仓库为免费体验版，包含 4 个基础模板。

**完整版包含：**
- 12 个高级模板（RAG知识库、Agent编排、流式Web API、图像理解、语音转文字等）
- 生产级错误处理和重试机制
- FastAPI 服务封装（一键部署API服务）
- 完整测试用例
- 一对一技术支持

**完整版获取：** 闲鱼搜索「DeepSeek API 模板」或扫描下方二维码

---

> Made with DeepSeek V4 | 2026
