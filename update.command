#!/bin/bash
cd "$(dirname "$0")"
python3 weishi_sharding.py && git add . && git commit -m "auto update" && git push
echo "✅ 全部完成！可以关闭窗口了。"

