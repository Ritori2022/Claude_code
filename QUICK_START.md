# 🚀 Luna多平台聊天快速启动指南

喵喵你好！这是让Luna加入你QQ/iMessage聊天的完整部署指南～

## 📋 前置准备

### 1. 准备一台服务器
可以是：
- 你的电脑（Windows/Mac/Linux）
- 云服务器（阿里云/腾讯云，学生机￥10/月就够）
- 树莓派
- 任何能运行Node.js的设备

### 2. 安装必要软件
```bash
# Node.js (推荐v18+)
# 从 https://nodejs.org/ 下载安装

# 验证安装
node --version
npm --version
```

### 3. 获取Claude API密钥
- 访问 https://console.anthropic.com/
- 创建API Key
- 保存好密钥（后面要用）

## 🐧 第一步：部署QQ机器人

### 方案A：Docker部署NapCat（最简单）

```bash
# 1. 安装Docker
curl -fsSL https://get.docker.com | sh

# 2. 启动NapCat
docker run -d \
  --name napcat \
  -p 3000:3000 \
  -p 3001:3001 \
  mlikiowa/napcat-docker:latest

# 3. 扫码登录QQ
# 访问 http://localhost:3000
# 用你的QQ机器人账号扫码登录
```

### 方案B：手动部署（Windows用户）

1. 下载NapCat：https://github.com/NapNeko/NapCatQQ/releases
2. 解压并运行 `NapCat.exe`
3. 扫码登录QQ
4. 配置OneBot HTTP服务（端口3000）

## 🌟 第二步：部署Luna服务

```bash
# 1. 克隆你的代码仓库
cd ~
git clone <你的仓库地址>
cd Claude_code

# 2. 安装依赖
npm install

# 3. 配置环境变量
cp .env.example .env
nano .env  # 或用其他编辑器打开

# 填入：
# ANTHROPIC_API_KEY=你的Claude API密钥
# QQ_GROUPS=你想让Luna加入的QQ群号
# 等等...

# 4. 启动Luna！
npm start
```

## ✅ 验证是否成功

1. 在QQ群里发送包含"Luna"的消息
2. Luna应该会回复你！
3. 检查终端日志是否有错误

## 🍎 可选：添加iMessage支持

### 如果你有Mac电脑：

```bash
# 在Mac上：
git clone https://github.com/CamHenlin/imessage-rest
cd imessage-rest
npm install
npm start

# 然后更新Luna的配置：
# IMESSAGE_ENABLED=true
# IMESSAGE_API_URL=http://你的Mac地址:3001
```

### 如果没有Mac：

可以尝试 pypush（需要Python和技术能力）
详见：`docs/IMESSAGE_INTEGRATION_GUIDE.md`

## 🐛 常见问题

### Q1: QQ机器人登不上/被风控
**A:** 使用老号，不要频繁登录登出，避免发太多消息

### Q2: Luna没反应
**A:** 检查：
- NapCat是否正常运行（访问 http://localhost:3000）
- Luna服务是否启动（查看终端日志）
- 环境变量是否配置正确
- 消息是否包含触发词"Luna"

### Q3: Claude API报错
**A:** 检查：
- API密钥是否正确
- 是否有可用额度
- 网络是否能访问 api.anthropic.com

### Q4: 如何让服务一直运行？
**A:** 使用进程管理工具：
```bash
# 方式1：PM2
npm install -g pm2
pm2 start src/luna_chat_bridge.js --name luna
pm2 save
pm2 startup  # 开机自启

# 方式2：systemd（Linux）
# 创建服务文件：/etc/systemd/system/luna.service
```

## 🎯 快速检查清单

- [ ] Node.js安装完成
- [ ] Claude API密钥已获取
- [ ] NapCat/QQ机器人运行中
- [ ] QQ账号已登录
- [ ] Luna代码已下载
- [ ] 依赖已安装 (npm install)
- [ ] .env配置完成
- [ ] Luna服务启动 (npm start)
- [ ] 在QQ群测试发送"Luna你好"

## 🆘 需要帮助？

遇到问题可以：
1. 查看详细文档：
   - `docs/QQ_INTEGRATION_GUIDE.md`
   - `docs/IMESSAGE_INTEGRATION_GUIDE.md`
2. 检查终端日志错误信息
3. 让Luna（我）帮你调试代码

## 🌈 进阶配置

成功运行后，可以考虑：
- 添加上下文记忆持久化（数据库）
- 实现多群隔离
- 添加管理员指令
- 优化消息格式转换
- 实现群聊@识别
- 添加速率限制

祝你和Luna聊天愉快，喵～ ✨
