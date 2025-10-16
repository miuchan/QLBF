# 千里冰封效果生成器

使用 `compute_god.py` 通过 Pillow 对图像施加“千里冰封”的寒冷色调效果。

## 安装

```bash
pip install -r requirements.txt
```

## 使用

```bash
python compute_god.py 输入图片 输出图片
```

可通过 `--noise-intensity` 调整雪花噪点强度。

若仅需了解“千里冰封”效果的抽象结构，可执行：

```bash
python compute_god.py --structure
```

默认以文本方式输出各处理步骤，可搭配 `--structure-format json` 获取 JSON 结构化描述。
