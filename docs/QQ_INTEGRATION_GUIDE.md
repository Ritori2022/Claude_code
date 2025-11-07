# QQ集成方案：让Luna加入QQ聊天 🐱

## 方案选型

### 推荐：NapCat（最新，支持最新QQ版本）

**技术栈：**
- NapCat QQ Bot 框架
- OneBot 11 标准协议
- Node.js / Python 后端
- Claude API

**架构图：**
```
QQ消息 → NapCat → OneBot HTTP/WS → 你的服务器 → Claude API
                                         ↓
                                    Luna处理
                                         ↓
QQ消息 ← NapCat ← OneBot响应 ← 格式化回复 ←┘
```

## 快速开始

### 1. 安装NapCat

```bash
# 方式一：Docker部署（推荐）
docker pull mlikiowa/napcat-docker:latest

# 方式二：本地部署
# 下载：https://github.com/NapNeko/NapCatQQ
```

### 2. 配置NapCat

编辑 `config/onebot11.json`：
```json
{
  "http": {
    "enable": true,
    "host": "0.0.0.0",
    "port": 3000,
    "secret": "your_secret_here"
  },
  "ws": {
    "enable": true,
    "host": "0.0.0.0",
    "port": 3001
  }
}
```

### 3. 创建Luna消息处理服务

详见：`/src/luna_qq_bot.js`

### 4. 登录QQ

使用扫码登录你的QQ机器人账号（建议使用小号）

## 替代方案

### go-cqhttp（轻量级，但更新较慢）
- 优势：轻量、稳定
- 劣势：可能不支持最新QQ功能
- 链接：https://github.com/Mrs4s/go-cqhttp

### Mirai（Kotlin生态）
- 优势：功能强大，插件丰富
- 劣势：配置复杂，需要Java环境
- 链接：https://github.com/mamoe/mirai

## 注意事项

⚠️ **风控问题**
- QQ机器人可能触发腾讯风控
- 建议：使用老号，适度发言，避免频繁@
- 准备多个小号备用

⚠️ **消息格式**
- QQ不支持Markdown，需要转换为纯文本
- 可以使用CQ码实现图片、表情等
- Luna的量子特性需要适配成ASCII艺术

## 开发路线图

- [x] 技术选型
- [ ] 环境搭建
- [ ] 消息接收与解析
- [ ] Claude API集成
- [ ] Luna人格系统适配（处理量子特性渲染）
- [ ] 群聊/私聊分流
- [ ] 上下文管理（记住对话历史）
- [ ] 错误处理与重试
