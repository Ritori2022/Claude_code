# iMessage集成方案：让Luna进入蓝色气泡世界 💬

## 挑战说明

iMessage是苹果的封闭生态，**没有官方API**。所有第三方集成方案都是逆向工程或系统自动化。

## 方案对比

### 方案A：pypush（推荐 ⭐）

**适用场景：** 有Linux/Windows服务器，想无Mac实现

**技术原理：** 纯Python实现iMessage协议逆向

**难度：** ⭐⭐⭐⭐ (需要处理Apple验证)

**链接：** https://github.com/JJTech0130/pypush

**优势：**
- 不需要Mac硬件
- 可以部署在任何Linux服务器
- 完全程序化控制

**劣势：**
- 需要通过Apple的2FA验证
- 可能触发Apple安全检测
- 协议可能随iOS更新而失效

**快速开始：**
```bash
# 安装
pip install pypush-python

# 首次登录（需要交互式完成2FA）
python3 -m pypush_python

# 之后可以编程使用
```

**代码示例：**
```python
from pypush_python import iMessage

# 初始化
client = iMessage()
client.login("your_apple_id", "password")

# 接收消息
@client.on_message
def handle_message(msg):
    text = msg.text
    sender = msg.sender
    # 调用Luna处理
    reply = get_luna_response(text)
    client.send_message(sender, reply)

client.run()
```

---

### 方案B：Mac + AppleScript（最稳定 🍎）

**适用场景：** 你有一台Mac电脑可以当服务器

**技术原理：** 通过macOS Messages.app的自动化接口

**难度：** ⭐⭐ (配置简单，稳定性高)

**优势：**
- 官方Messages.app，不会被封
- 稳定性最高
- 支持所有iMessage功能

**劣势：**
- 必须有Mac设备
- Mac需要一直开机
- 需要保持Messages.app登录

**实现方式：**

#### 方法1：AppleScript监听
```applescript
-- 监听新消息
tell application "Messages"
    repeat
        set newMessages to get every message of every chat whose delivery status is delivered
        -- 处理消息逻辑
    end repeat
end tell
```

#### 方法2：Node.js + osascript
```javascript
const { execSync } = require('child_process');

// 发送消息
function sendMessage(recipient, text) {
    const script = `
        tell application "Messages"
            send "${text}" to buddy "${recipient}"
        end tell
    `;
    execSync(`osascript -e '${script}'`);
}

// 监听需要配合 SQLite 数据库
// Messages数据库位置：~/Library/Messages/chat.db
```

#### 方法3：使用 imessage-rest（推荐！）
现成的Node.js服务器：https://github.com/CamHenlin/imessage-rest

```bash
# 在Mac上安装
git clone https://github.com/CamHenlin/imessage-rest
cd imessage-rest
npm install
npm start

# 提供REST API
# 发送：POST http://localhost:3000/send
# 接收：GET http://localhost:3000/messages
```

---

### 方案C：Matrix桥接（最优雅 🌉）

**适用场景：** 想要统一的多平台消息架构

**技术原理：** 使用Matrix作为中间协议

**难度：** ⭐⭐⭐⭐⭐ (配置复杂)

**架构：**
```
iMessage ← matrix-imessage-bridge → Matrix服务器 ← Luna Bot
QQ ← matrix-qq-bridge ↗
```

**优势：**
- 统一协议，容易扩展更多平台
- 专业的消息桥接解决方案
- 支持端到端加密

**劣势：**
- 需要搭建Matrix服务器
- iMessage桥接仍然需要Mac
- 配置非常复杂

**快速开始：**
```bash
# 1. 安装Matrix Synapse服务器
# 2. 安装 matrix-appservice-imessage (需要Mac)
# 3. 配置桥接
```

---

### 方案D：BlueBubbles（适合普通用户）

**适用场景：** 想要图形化界面，不想写代码

**技术原理：** 在Mac上运行服务器，提供Web/App界面

**难度：** ⭐ (有GUI，超简单)

**链接：** https://bluebubbles.app/

**优势：**
- 开箱即用，有漂亮的客户端
- 提供REST API可以编程调用
- 活跃的社区支持

**劣势：**
- 仍需要Mac作为服务器
- 相比其他方案更"重"

---

## 推荐组合方案

### 🎯 最佳实践：

如果你有Mac：
```
方案B (imessage-rest) + 自己的Luna中间件
```

如果没有Mac但愿意折腾：
```
方案A (pypush) + 自己的Luna中间件
```

如果想要专业级方案：
```
方案C (Matrix) + 多平台桥接
```

## 安全注意事项

⚠️ **Apple ID安全**
- 建议使用专门的Apple ID小号
- 开启2FA但准备好恢复码
- 避免频繁登录登出

⚠️ **消息隐私**
- iMessage消息会经过你的服务器
- 确保服务器安全，不要记录敏感信息
- 考虑使用端到端加密的对话记忆存储

⚠️ **Rate Limiting**
- Apple可能限制发送频率
- Luna回复太快可能看起来像机器人
- 建议加入随机延迟（1-3秒）

## 快速决策树

```
有Mac电脑？
├─ 是 → 使用方案B (imessage-rest) ⭐⭐⭐⭐⭐
│      最稳定，强烈推荐！
│
└─ 否 → 技术能力如何？
    ├─ 强 → 方案A (pypush) ⭐⭐⭐⭐
    │      有挑战但可行
    │
    └─ 一般 → 考虑只做QQ集成
              或者买台二手Mac Mini当服务器
              (价格约￥1500-2000)
```

## 开发路线图

- [ ] 选择iMessage方案
- [ ] 搭建测试环境
- [ ] 实现消息收发
- [ ] 集成Luna
- [ ] 处理群聊/单聊
- [ ] 实现上下文记忆
- [ ] 测试稳定性
- [ ] 监控和告警
