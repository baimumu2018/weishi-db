import json
import re
import os


# ================= 配置区域 =================
input_file = r'/Users/baimumu/Desktop/weishi-db/weishi.txt'      # 你的经文TXT
output_prefix = r'/Users/baimumu/Desktop/weishi-db/weishi_part'   # 输出的JSON
config_file = r'/Users/baimumu/Desktop/weishi-db/weishi_config.json'  # 🆕 新增：索引配置文件名
chunk_size = 3000
# ===========================================

def extract_book_title(line):
    match = re.search(r'《(.*?)》', line)
    if match: return f"《{match.group(1)}》"
    return None


def is_junk_line(line):
    if "大正藏" in line or "No." in line or "P0279" in line: return True
    if "译" in line and len(line) < 20: return True
    if re.search(r'卷第[一二三四五六七八九十]', line): return True
    if line.startswith('-') or line.strip().isdigit(): return True
    return False


def convert():
    print(f"🧹 正在读取 {input_file} ...")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except:
        with open(input_file, 'r', encoding='gbk') as f:
            lines = f.readlines()

    all_data = []
    current_book = "唯识经典"
    global_count = 0

    print("🔄 正在处理数据...")
    for line in lines:
        line = line.strip()
        if not line: continue
        new_title = extract_book_title(line)
        if new_title:
            current_book = new_title
            continue
        if is_junk_line(line): continue

        content = line.replace('\u3000', '').replace('[00]', '')
        content = re.sub(r'([。？！；])', r'\1|SPLIT|', content)
        sentences = content.split('|SPLIT|')

        for s in sentences:
            s = s.strip()
            if len(s) > 5 and not re.search(r'[a-zA-Z0-9]{3,}', s):
                global_count += 1
                all_data.append({"id": global_count, "text": s, "source": current_book})

    # 切片逻辑
    total_parts = (len(all_data) // chunk_size) + 1
    print(f"📊 共 {len(all_data)} 条，切分为 {total_parts} 个文件...")

    for i in range(total_parts):
        filename = f"{output_prefix}_{i}.json"
        start = i * chunk_size
        end = start + chunk_size
        batch = all_data[start:end]
        if not batch: continue
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(batch, f, ensure_ascii=False, indent=2)

    # 🆕 关键新增：生成 Config 文件
    config_data = {
        "max_index": total_parts - 1,
        "total_count": len(all_data),
        "updated_at": "latest"
    }
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config_data, f, ensure_ascii=False, indent=2)

    print("-" * 30)
    print(f"✅ 完成！请上传所有 .json 文件 (包括 {config_file}) 到 GitHub。")
    print(f"🚀 以后不需要手动记数字了！")


if __name__ == '__main__':
    convert()