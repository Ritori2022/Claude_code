# Luna多平台聊天桥接 🐱✨

让AI猫娘学者Luna加入你的QQ和iMessage聊天！

## 🌟 项目简介

这是一个多平台聊天集成框架，允许Claude AI（以Luna人格）同时在QQ和iMessage中与你聊天。

### 特性

- 🐧 **QQ集成**：基于NapCat/OneBot 11标准
- 💬 **iMessage集成**：支持多种方案（imessage-rest、pypush、Matrix）
- 🧠 **Luna人格系统**：完整的多重人格AI（Luna/Nyx/Chaos）
- 🔄 **上下文管理**：记住对话历史
- 📱 **统一接口**：一套代码，多平台适配
- 🎨 **格式转换**：自动将Markdown转换为各平台支持的格式

## 📁 项目结构

```
Claude_code/
├── src/
│   └── luna_chat_bridge.js      # 核心桥接服务
├── docs/
│   ├── QQ_INTEGRATION_GUIDE.md       # QQ集成详细指南
│   └── IMESSAGE_INTEGRATION_GUIDE.md # iMessage集成详细指南
├── QUICK_START.md               # 快速启动指南
├── CLAUDE.md                    # Luna人格系统提示词
├── .env.example                 # 配置文件示例
└── package.json                 # 项目依赖

ponytown/                        # Ponytown自动化（独立项目）
```

## 🚀 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 配置环境

```bash
cp .env.example .env
# 编辑 .env 填入你的配置
```

### 3. 部署QQ机器人

详见：[QQ集成指南](docs/QQ_INTEGRATION_GUIDE.md)

推荐使用Docker：
```bash
docker run -d --name napcat -p 3000:3000 mlikiowa/napcat-docker:latest
```

### 4. 启动Luna

```bash
npm start
```

详细步骤请查看：[QUICK_START.md](QUICK_START.md)

## 📚 文档

- **[快速启动指南](QUICK_START.md)** - 从零开始的完整部署教程
- **[QQ集成指南](docs/QQ_INTEGRATION_GUIDE.md)** - QQ Bot详细配置
- **[iMessage集成指南](docs/IMESSAGE_INTEGRATION_GUIDE.md)** - iMessage多方案对比
- **[Luna人格系统](CLAUDE.md)** - AI人格配置说明

## 🎯 使用场景

- ✅ 让AI参与你和朋友的群聊讨论
- ✅ 在多个平台保持对话连续性
- ✅ 构建个性化的AI助手
- ✅ 学习聊天机器人开发

## 🛠️ 技术栈

- **AI模型**: Claude 4.5 Sonnet (Anthropic)
- **QQ Bot**: NapCat (OneBot 11)
- **iMessage**: imessage-rest / pypush
- **运行环境**: Node.js 18+
- **自动化**: Puppeteer / Playwright

## ⚙️ 配置说明

关键配置项（在 `.env` 中设置）：

```bash
ANTHROPIC_API_KEY=your_api_key     # Claude API密钥
QQ_GROUPS=123456789                # 监听的QQ群
IMESSAGE_ENABLED=false             # 是否启用iMessage
LUNA_TRIGGER=luna|Luna             # Luna响应触发词
```

## 🔧 开发

```bash
# 开发模式（自动重启）
npm run dev

# 生产模式
npm start
```

## 🐛 常见问题

### QQ机器人无法登录？
- 使用老QQ账号
- 避免频繁登录登出
- 查看NapCat日志

### Luna没有响应？
- 检查触发词配置
- 确认API密钥正确
- 查看终端日志

### iMessage集成失败？
- Mac方案：确保Messages.app已登录
- pypush方案：需要完成Apple 2FA验证

更多问题请查看：[QUICK_START.md](QUICK_START.md)

## 📝 Todo

- [ ] WebSocket实时消息推送
- [ ] 数据库持久化上下文
- [ ] 管理员指令系统
- [ ] 多群隔离配置
- [ ] 消息统计面板
- [ ] Docker一键部署
- [ ] 更多平台支持（微信、Telegram等）

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 License

ISC

## 💖 致谢

- Claude AI by Anthropic
- NapCat QQ Bot框架
- imessage-rest项目
- 所有开源贡献者

---

**Made with ❤️ by 喵喵 & Luna**

喵～让我们一起聊天吧！ (๑•̀ㅂ•́)و✧
