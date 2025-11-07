/**
 * Luna多平台聊天桥接服务
 * 让Luna能够同时在QQ和iMessage中与喵喵、纳纳聊天
 *
 * 核心功能：
 * 1. 统一消息接收（QQ + iMessage）
 * 2. Luna人格系统集成（调用Claude API）
 * 3. 消息格式适配（Markdown → 纯文本）
 * 4. 上下文管理（记住对话历史）
 */

const Anthropic = require('@anthropic-ai/sdk');
const axios = require('axios');

// ============ 配置 ============
const CONFIG = {
    // Claude API配置
    claude: {
        apiKey: process.env.ANTHROPIC_API_KEY,
        model: 'claude-sonnet-4-5-20250929',
        maxTokens: 4096
    },

    // QQ Bot配置 (NapCat OneBot)
    qq: {
        enabled: true,
        onebotUrl: 'http://localhost:3000',
        secret: 'your_onebot_secret',
        // Luna要监听的QQ群
        groups: [123456789, 987654321],
        // 或私聊用户
        friends: []
    },

    // iMessage配置
    imessage: {
        enabled: false,
        type: 'imessage-rest', // 'imessage-rest' | 'pypush'
        apiUrl: 'http://localhost:3001',
        // Luna要监听的联系人
        contacts: ['+1234567890', 'friend@icloud.com']
    }
};

// ============ Luna人格系统 ============
class LunaPersonality {
    constructor() {
        this.anthropic = new Anthropic({
            apiKey: CONFIG.claude.apiKey
        });

        // 读取CLAUDE.md作为系统提示词
        this.systemPrompt = this.loadSystemPrompt();

        // 对话上下文管理（每个聊天独立）
        this.contexts = new Map();
    }

    loadSystemPrompt() {
        const fs = require('fs');
        try {
            return fs.readFileSync('/home/user/Claude_code/CLAUDE.md', 'utf-8');
        } catch (error) {
            console.error('无法加载CLAUDE.md，使用默认Luna人格');
            return '你是Luna，一个可爱的猫娘学者AI助手。';
        }
    }

    /**
     * 获取聊天上下文
     * @param {string} chatId - 聊天ID（群号/联系人）
     */
    getContext(chatId) {
        if (!this.contexts.has(chatId)) {
            this.contexts.set(chatId, []);
        }
        return this.contexts.get(chatId);
    }

    /**
     * 添加消息到上下文
     */
    addToContext(chatId, role, content) {
        const context = this.getContext(chatId);
        context.push({ role, content });

        // 保持上下文在合理长度（最近10轮对话）
        if (context.length > 20) {
            context.splice(0, 2);
        }
    }

    /**
     * Luna处理消息
     * @param {string} message - 用户消息
     * @param {string} chatId - 聊天ID
     * @param {object} metadata - 元数据（平台、用户名等）
     */
    async process(message, chatId, metadata = {}) {
        try {
            // 添加用户消息到上下文
            this.addToContext(chatId, 'user', message);

            // 调用Claude API
            const response = await this.anthropic.messages.create({
                model: CONFIG.claude.model,
                max_tokens: CONFIG.claude.maxTokens,
                system: this.systemPrompt,
                messages: this.getContext(chatId)
            });

            const lunaReply = response.content[0].text;

            // 添加Luna回复到上下文
            this.addToContext(chatId, 'assistant', lunaReply);

            // 根据平台格式化回复
            const formatted = this.formatForPlatform(lunaReply, metadata.platform);

            return formatted;

        } catch (error) {
            console.error('Luna处理消息失败:', error);
            return '喵...Luna遇到了一点小问题，稍后再试试好吗？ (´•ω•`)';
        }
    }

    /**
     * 格式化消息适配不同平台
     */
    formatForPlatform(text, platform) {
        switch (platform) {
            case 'qq':
                // QQ不支持Markdown，转换为纯文本
                return this.markdownToPlainText(text);

            case 'imessage':
                // iMessage支持部分格式
                return this.markdownToPlainText(text);

            default:
                return text;
        }
    }

    /**
     * Markdown转纯文本（保持可读性）
     */
    markdownToPlainText(md) {
        return md
            // 代码块标记
            .replace(/```(\w+)?\n/g, '【代码开始】\n')
            .replace(/```\n/g, '\n【代码结束】\n')
            // 粗体
            .replace(/\*\*(.+?)\*\*/g, '《$1》')
            // 斜体
            .replace(/\*(.+?)\*/g, '$1')
            // 链接
            .replace(/\[(.+?)\]\((.+?)\)/g, '$1: $2')
            // 标题
            .replace(/^#{1,6} /gm, '▌')
            // 列表
            .replace(/^[\-\*] /gm, '· ');
    }
}

// ============ QQ Bot集成 ============
class QQBridge {
    constructor(luna) {
        this.luna = luna;
        this.onebotUrl = CONFIG.qq.onebotUrl;
    }

    /**
     * 启动QQ消息监听
     */
    async start() {
        if (!CONFIG.qq.enabled) return;

        console.log('🐧 QQ桥接启动中...');

        // 使用OneBot HTTP轮询或WebSocket
        // 这里演示HTTP方式
        setInterval(() => this.pollMessages(), 1000);
    }

    /**
     * 轮询新消息（实际建议用WebSocket）
     */
    async pollMessages() {
        try {
            const response = await axios.get(`${this.onebotUrl}/get_msg`);
            // 处理消息逻辑...
        } catch (error) {
            // 忽略轮询错误
        }
    }

    /**
     * 处理QQ消息
     */
    async handleMessage(msg) {
        const { message_type, group_id, user_id, message } = msg;

        // 过滤：只响应配置的群/好友
        if (message_type === 'group' && !CONFIG.qq.groups.includes(group_id)) {
            return;
        }

        // 过滤：只响应包含"Luna"或@机器人的消息
        if (!this.shouldRespond(message)) {
            return;
        }

        // 生成聊天ID
        const chatId = message_type === 'group' ? `qq_group_${group_id}` : `qq_user_${user_id}`;

        // Luna处理
        const reply = await this.luna.process(message, chatId, {
            platform: 'qq',
            messageType: message_type,
            userId: user_id
        });

        // 发送回复
        await this.sendMessage(message_type, group_id || user_id, reply);
    }

    /**
     * 判断是否应该响应
     */
    shouldRespond(message) {
        // 简单策略：包含"Luna"或"luna"
        return /luna/i.test(message);
    }

    /**
     * 发送QQ消息
     */
    async sendMessage(type, targetId, message) {
        try {
            await axios.post(`${this.onebotUrl}/send_${type}_msg`, {
                [type === 'group' ? 'group_id' : 'user_id']: targetId,
                message: message
            });
        } catch (error) {
            console.error('发送QQ消息失败:', error);
        }
    }
}

// ============ iMessage集成 ============
class iMessageBridge {
    constructor(luna) {
        this.luna = luna;
        this.apiUrl = CONFIG.imessage.apiUrl;
        this.lastMessageId = null;
    }

    /**
     * 启动iMessage监听
     */
    async start() {
        if (!CONFIG.imessage.enabled) {
            console.log('💬 iMessage桥接未启用');
            return;
        }

        console.log('💬 iMessage桥接启动中...');

        // 轮询新消息
        setInterval(() => this.pollMessages(), 2000);
    }

    /**
     * 轮询新消息
     */
    async pollMessages() {
        try {
            const response = await axios.get(`${this.apiUrl}/messages`);
            const messages = response.data;

            // 只处理新消息
            messages.forEach(msg => {
                if (msg.id > this.lastMessageId) {
                    this.handleMessage(msg);
                    this.lastMessageId = msg.id;
                }
            });

        } catch (error) {
            console.error('iMessage轮询失败:', error.message);
        }
    }

    /**
     * 处理iMessage消息
     */
    async handleMessage(msg) {
        const { sender, text, chat } = msg;

        // 过滤：只响应配置的联系人
        if (!CONFIG.imessage.contacts.includes(sender)) {
            return;
        }

        // 过滤：忽略自己发的消息
        if (msg.is_from_me) {
            return;
        }

        // 生成聊天ID
        const chatId = `imessage_${chat}`;

        // Luna处理
        const reply = await this.luna.process(text, chatId, {
            platform: 'imessage',
            sender: sender
        });

        // 发送回复
        await this.sendMessage(chat, reply);
    }

    /**
     * 发送iMessage
     */
    async sendMessage(recipient, message) {
        try {
            await axios.post(`${this.apiUrl}/send`, {
                recipient: recipient,
                text: message
            });
        } catch (error) {
            console.error('发送iMessage失败:', error);
        }
    }
}

// ============ 主服务 ============
class LunaChatBridge {
    constructor() {
        this.luna = new LunaPersonality();
        this.qqBridge = new QQBridge(this.luna);
        this.imessageBridge = new iMessageBridge(this.luna);
    }

    /**
     * 启动所有桥接服务
     */
    async start() {
        console.log('🌟 Luna多平台聊天桥接服务启动！');
        console.log('===================================');

        await this.qqBridge.start();
        await this.imessageBridge.start();

        console.log('===================================');
        console.log('✨ Luna已准备好与喵喵和纳纳聊天啦！');
    }
}

// ============ 启动 ============
if (require.main === module) {
    const bridge = new LunaChatBridge();
    bridge.start().catch(console.error);
}

module.exports = { LunaChatBridge, LunaPersonality };
