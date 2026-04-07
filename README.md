# 小红书文案生成器

AI驱动的小红书爆款文案生成工具，包含文案生成、爆款基因分析、封面模板等功能。

**在线访问**: https://xhs-copywriter.onrender.com

## 功能特性

- ✨ 3版不同风格文案（真实测评型/清单种草型/反套路型）
- 🔥 爆款基因分析（4维度评分+优化建议）
- 🎨 6种封面模板+制作指南
- 📋 一键复制文案

## 技术栈

- 前端：HTML + Tailwind CSS + JavaScript
- 后端：Python Flask
- AI：Moonshot (Kimi) API
- 部署：Render

## 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py
```

访问 http://localhost:5000

## 部署到 Render

1. Fork 本项目到 GitHub
2. 登录 [render.com](https://render.com)
3. 点击 "New Web Service"
4. 连接 GitHub 仓库
5. 配置：
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. 点击 Deploy

## 环境变量

| 变量名 | 说明 | 必填 |
|--------|------|------|
| MOONSHOT_API_KEY | Kimi API Key | 否（有默认值） |

## License

MIT
