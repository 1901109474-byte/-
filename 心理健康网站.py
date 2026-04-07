from flask import Flask, render_template_string, request, jsonify
import requests
import json

# 初始化Flask应用
app = Flask(__name__)

# 千问AI配置
QIANWEN_API_KEY = "sk-373484df3143411a8f0ec309a5466978"
QIANWEN_API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

# 首页HTML模板
HOME_PAGE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>心灵驿站 - 专业心理健康服务平台</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Microsoft YaHei', sans-serif;
        }

        body {
            background: linear-gradient(135deg, #f5f7fa 0%, #e4eaf5 100%);
            color: #333;
        }

        /* 导航栏 */
        .navbar {
            background: rgba(255, 255, 255, 0.95);
            padding: 15px 50px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .logo {
            font-size: 24px;
            font-weight: bold;
            color: #6c8cbf;
        }

        .nav-links a {
            margin: 0 20px;
            text-decoration: none;
            color: #555;
            font-size: 16px;
            transition: color 0.3s;
        }

        .nav-links a:hover {
            color: #6c8cbf;
        }

        /* 首页横幅 */
        .banner {
            height: 400px;
            background: linear-gradient(rgba(108,140,191,0.8), rgba(108,140,191,0.6)), url('https://images.unsplash.com/photo-1506126613408-eca07ce68773?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80');
            background-size: cover;
            background-position: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: white;
            text-align: center;
        }

        .banner h1 {
            font-size: 42px;
            margin-bottom: 15px;
        }

        .banner p {
            font-size: 18px;
            margin-bottom: 30px;
        }

        /* 服务模块 */
        .services {
            max-width: 1200px;
            margin: 60px auto;
            padding: 0 20px;
        }

        .section-title {
            text-align: center;
            font-size: 32px;
            color: #444;
            margin-bottom: 50px;
            position: relative;
        }

        .section-title::after {
            content: '';
            width: 80px;
            height: 3px;
            background: #6c8cbf;
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
        }

        .service-cards {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 30px;
        }

        .card {
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            transition: transform 0.3s;
        }

        .card:hover {
            transform: translateY(-10px);
        }

        .card-img {
            height: 200px;
            overflow: hidden;
        }

        .card-img img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.5s;
        }

        .card:hover .card-img img {
            transform: scale(1.1);
        }

        .card-content {
            padding: 25px;
        }

        .card-title {
            font-size: 22px;
            color: #333;
            margin-bottom: 15px;
        }

        .card-desc {
            color: #666;
            line-height: 1.6;
            margin-bottom: 20px;
        }

        .card-btn {
            display: inline-block;
            padding: 10px 25px;
            background: #6c8cbf;
            color: white;
            text-decoration: none;
            border-radius: 25px;
            transition: background 0.3s;
        }

        .card-btn:hover {
            background: #5a7aa8;
        }

        /* 页脚 */
        .footer {
            background: #333;
            color: white;
            text-align: center;
            padding: 30px;
            margin-top: 80px;
        }
    </style>
</head>
<body>
    <!-- 导航栏 -->
    <div class="navbar">
        <div class="logo">心灵驿站</div>
        <div class="nav-links">
            <a href="/">首页</a>
            <a href="/courses">心理放松课程</a>
            <a href="/chat">AI深夜畅聊</a>
            <a href="/counseling">1对1心理辅导</a>
        </div>
    </div>

    <!-- 首页横幅 -->
    <div class="banner">
        <h1>守护心灵，温暖同行</h1>
        <p>专业心理健康服务，陪伴你度过每一个情绪时刻</p>
    </div>

    <!-- 服务模块 -->
    <div class="services">
        <h2 class="section-title">我们的服务</h2>
        <div class="service-cards">
            <!-- 心理放松课程 -->
            <div class="card">
                <div class="card-img">
                    <img src="https://images.unsplash.com/photo-1545389336-cf090694435e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80" alt="心理放松课程">
                </div>
                <div class="card-content">
                    <h3 class="card-title">心理放松课程</h3>
                    <p class="card-desc">冥想、呼吸训练、正念引导等专业放松课程，缓解压力与焦虑</p>
                    <a href="/courses" class="card-btn">进入学习</a>
                </div>
            </div>

            <!-- AI深夜畅聊 -->
            <div class="card">
                <div class="card-img">
                    <img src="https://images.unsplash.com/photo-1529156069898-49953e39b3ac?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80" alt="AI深夜畅聊">
                </div>
                <div class="card-content">
                    <h3 class="card-title">AI深夜畅聊</h3>
                    <p class="card-desc">24小时在线AI陪伴，倾听你的心声，温柔回应你的情绪</p>
                    <a href="/chat" class="card-btn">开始聊天</a>
                </div>
            </div>

            <!-- 1对1心理辅导 -->
            <div class="card">
                <div class="card-img">
                    <img src="https://images.unsplash.com/photo-1521737604893-d14cc237f11d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80" alt="1对1心理辅导">
                </div>
                <div class="card-content">
                    <h3 class="card-title">1对1心理辅导</h3>
                    <p class="card-desc">专业心理咨询师在线直播辅导，定制化解决心理困扰</p>
                    <a href="/counseling" class="card-btn">预约咨询</a>
                </div>
            </div>
        </div>
    </div>

    <!-- 页脚 -->
    <div class="footer">
        <p>心灵驿站 © 2026 版权所有 | 专业心理健康服务平台</p>
    </div>
</body>
</html>
"""

# 心理放松课程页面
COURSES_PAGE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>心理放松课程 - 心灵驿站</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Microsoft YaHei', sans-serif;
        }

        body {
            background: #f4f4f5;
        }

        /* 导航栏 */
        .navbar {
            background: #fb7299;
            padding: 15px 50px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .logo {
            font-size: 24px;
            font-weight: bold;
            color: white;
        }

        .nav-links a {
            margin: 0 20px;
            text-decoration: none;
            color: white;
            font-size: 16px;
        }

        /* 返回按钮 */
        .back-btn {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 50px;
            height: 50px;
            background: #fb7299;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            font-size: 20px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.2);
            z-index: 999;
        }

        /* 分类栏 */
        .category-bar {
            background: white;
            padding: 15px 50px;
            display: flex;
            gap: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }

        .category-item {
            padding: 5px 15px;
            border-radius: 20px;
            cursor: pointer;
        }

        .category-item.active {
            background: #fb7299;
            color: white;
        }

        /* 课程列表 */
        .courses-container {
            max-width: 1200px;
            margin: 30px auto;
            padding: 0 20px;
        }

        .courses-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 25px;
        }

        .course-card {
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }

        /* B站视频嵌入样式 */
        .video-frame {
            width: 100%;
            height: 280px;
            border: none;
        }

        .course-info {
            padding: 15px;
        }

        .course-title {
            font-size: 16px;
            color: #333;
            margin-bottom: 8px;
            font-weight: bold;
        }

        .course-meta {
            font-size: 13px;
            color: #999;
        }
    </style>
</head>
<body>
    <!-- 导航栏 -->
    <div class="navbar">
        <div class="logo">心灵驿站</div>
        <div class="nav-links">
            <a href="/">首页</a>
            <a href="/courses">心理放松课程</a>
            <a href="/chat">AI深夜畅聊</a>
            <a href="/counseling">1对1心理辅导</a>
        </div>
    </div>

    <!-- 分类栏 -->
    <div class="category-bar">
        <div class="category-item active">全部课程</div>
        <div class="category-item">冥想放松</div>
        <div class="category-item">呼吸训练</div>
        <div class="category-item">正念引导</div>
        <div class="category-item">睡眠改善</div>
        <div class="category-item">压力缓解</div>
    </div>

    <!-- 课程列表（全部替换为可播放视频） -->
    <div class="courses-container">
        <div class="courses-grid">
            <!-- 课程1：4分钟正念静心冥想（可直接播放） -->
            <div class="course-card">
                <iframe src="//player.bilibili.com/player.html?bvid=BV1JuNgzREiU&autoplay=0" class="video-frame" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
                <div class="course-info">
                    <div class="course-title">4分钟正念静心冥想｜放下焦虑，回归平静</div>
                    <div class="course-meta">12.5万观看 · 心理导师</div>
                </div>
            </div>

            <!-- 课程2：自我宽恕引导冥想（可直接播放） -->
            <div class="course-card">
                <iframe src="//player.bilibili.com/player.html?bvid=BV1DPNuzgEuK&autoplay=0" class="video-frame" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
                <div class="course-info">
                    <div class="course-title">自我宽恕冥想｜减压助眠，缓解抑郁焦虑</div>
                    <div class="course-meta">8.7万观看 · 正念导师</div>
                </div>
            </div>

            <!-- 课程3：深度睡眠引导（可直接播放） -->
            <div class="course-card">
                <iframe src="//player.bilibili.com/player.html?bvid=BV1HZD5BqEK1&autoplay=0" class="video-frame" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
                <div class="course-info">
                    <div class="course-title">深度睡眠引导｜停止内耗，告别失眠</div>
                    <div class="course-meta">20.1万观看 · 睡眠专家</div>
                </div>
            </div>

            <!-- 课程4：温柔疗愈冥想（可直接播放） -->
            <div class="course-card">
                <iframe src="//player.bilibili.com/player.html?bvid=BV16bPNzkEd5&autoplay=0" class="video-frame" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
                <div class="course-info">
                    <div class="course-title">4分钟温柔疗愈｜安抚身心，缓解紧绷</div>
                    <div class="course-meta">15.3万观看 · 心理导师</div>
                </div>
            </div>
        </div>
    </div>

    <!-- 返回首页按钮 -->
    <a href="/" class="back-btn">←</a>
</body>
</html>
"""

# AI深夜畅聊页面
CHAT_PAGE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI深夜畅聊 - 心灵驿站</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Microsoft YaHei', sans-serif;
        }

        body {
            background: linear-gradient(135deg, #2c3e50 0%, #4ca1af 100%);
            height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* 导航栏 */
        .navbar {
            background: rgba(255,255,255,0.1);
            padding: 15px 50px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            font-size: 24px;
            font-weight: bold;
            color: white;
        }

        .nav-links a {
            margin: 0 20px;
            text-decoration: none;
            color: white;
            font-size: 16px;
        }

        /* 返回按钮 */
        .back-btn {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 50px;
            height: 50px;
            background: #6c8cbf;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            font-size: 20px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.2);
            z-index: 999;
        }

        /* 聊天容器 */
        .chat-container {
            flex: 1;
            max-width: 800px;
            margin: 20px auto;
            width: 90%;
            background: rgba(255,255,255,0.9);
            border-radius: 15px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        /* 聊天头部 */
        .chat-header {
            padding: 15px;
            background: #6c8cbf;
            color: white;
            text-align: center;
        }

        /* 消息区域 */
        .messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .message {
            max-width: 70%;
            padding: 12px 18px;
            border-radius: 20px;
        }

        .user-message {
            align-self: flex-end;
            background: #6c8cbf;
            color: white;
        }

        .ai-message {
            align-self: flex-start;
            background: #e4eaf5;
            color: #333;
        }

        /* 输入区域 */
        .input-area {
            padding: 15px;
            display: flex;
            gap: 10px;
            border-top: 1px solid #eee;
        }

        #chat-input {
            flex: 1;
            padding: 12px 15px;
            border: 1px solid #ddd;
            border-radius: 25px;
            outline: none;
            font-size: 16px;
        }

        #send-btn {
            padding: 12px 25px;
            background: #6c8cbf;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: background 0.3s;
        }

        #send-btn:hover {
            background: #5a7aa8;
        }
    </style>
</head>
<body>
    <!-- 导航栏 -->
    <div class="navbar">
        <div class="logo">心灵驿站</div>
        <div class="nav-links">
            <a href="/">首页</a>
            <a href="/courses">心理放松课程</a>
            <a href="/chat">AI深夜畅聊</a>
            <a href="/counseling">1对1心理辅导</a>
        </div>
    </div>

    <!-- 聊天容器 -->
    <div class="chat-container">
        <div class="chat-header">
            <h3>AI深夜畅聊 - 温柔倾听你的心声</h3>
        </div>

        <div class="messages" id="messages">
            <div class="message ai-message">
                你好呀～ 我在这里陪着你，有什么想聊的都可以告诉我😊
            </div>
        </div>

        <div class="input-area">
            <input type="text" id="chat-input" placeholder="说点什么吧...">
            <button id="send-btn">发送</button>
        </div>
    </div>

    <!-- 返回首页按钮 -->
    <a href="/" class="back-btn">←</a>

    <script>
        // 聊天功能实现
        const messages = document.getElementById('messages');
        const chatInput = document.getElementById('chat-input');
        const sendBtn = document.getElementById('send-btn');

        // 发送消息
        function sendMessage() {
            const text = chatInput.value.trim();
            if (!text) return;

            // 添加用户消息
            const userMsg = document.createElement('div');
            userMsg.className = 'message user-message';
            userMsg.textContent = text;
            messages.appendChild(userMsg);

            // 清空输入框
            chatInput.value = '';

            // 滚动到底部
            messages.scrollTop = messages.scrollHeight;

            // 发送请求到后端
            fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: text })
            })
            .then(res => res.json())
            .then(data => {
                // 添加AI回复
                const aiMsg = document.createElement('div');
                aiMsg.className = 'message ai-message';
                aiMsg.textContent = data.reply;
                messages.appendChild(aiMsg);
                messages.scrollTop = messages.scrollHeight;
            });
        }

        // 绑定事件
        sendBtn.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
"""

# 1对1心理辅导页面
COUNSELING_PAGE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>1对1心理辅导 - 心灵驿站</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Microsoft YaHei', sans-serif;
        }

        body {
            background: #1a1a1a;
            color: white;
        }

        /* 导航栏 */
        .navbar {
            background: #262626;
            padding: 15px 50px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #f39c12;
        }

        .logo {
            font-size: 24px;
            font-weight: bold;
            color: #f39c12;
        }

        .nav-links a {
            margin: 0 20px;
            text-decoration: none;
            color: white;
            font-size: 16px;
        }

        /* 返回按钮 */
        .back-btn {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 50px;
            height: 50px;
            background: #f39c12;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            font-size: 20px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.2);
            z-index: 999;
        }

        /* 辅导师列表（双排布局） */
        .counselors-container {
            max-width: 1200px;
            margin: 30px auto;
            padding: 0 20px;
        }

        .counselors-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 25px;
        }

        .counselor-card {
            background: #262626;
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid #333;
            transition: border 0.3s;
        }

        .counselor-card:hover {
            border: 1px solid #f39c12;
        }

        .counselor-header {
            display: flex;
            padding: 15px;
            align-items: center;
            gap: 15px;
        }

        .avatar {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            overflow: hidden;
        }

        .avatar img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .counselor-info {
            flex: 1;
        }

        .counselor-name {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .counselor-title {
            color: #999;
            font-size: 14px;
        }

        .live-status {
            background: #e74c3c;
            color: white;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 12px;
        }

        .counselor-content {
            padding: 15px;
        }

        .counselor-desc {
            color: #ccc;
            line-height: 1.6;
            margin-bottom: 15px;
        }

        .counselor-btn {
            display: inline-block;
            padding: 8px 20px;
            background: #f39c12;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background 0.3s;
        }

        .counselor-btn:hover {
            background: #e67e22;
        }
    </style>
</head>
<body>
    <!-- 导航栏 -->
    <div class="navbar">
        <div class="logo">心灵驿站</div>
        <div class="nav-links">
            <a href="/">首页</a>
            <a href="/courses">心理放松课程</a>
            <a href="/chat">AI深夜畅聊</a>
            <a href="/counseling">1对1心理辅导</a>
        </div>
    </div>

    <!-- 辅导师列表 -->
    <div class="counselors-container">
        <div class="counselors-grid">
            <!-- 辅导师1 -->
            <div class="counselor-card">
                <div class="counselor-header">
                    <div class="avatar">
                        <img src="https://images.unsplash.com/photo-1566753323558-f4e0952af11?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&q=80" alt="李导师">
                    </div>
                    <div class="counselor-info">
                        <div class="counselor-name">甘涛 · 资深心理咨询师</div>
                        <div class="counselor-title">18年做人经验 | 情绪疏导专家</div>
                    </div>
                    <div class="live-status">正在直播</div>
                </div>
                <div class="counselor-content">
                    <p class="counselor-desc">专注焦虑、抑郁、人际关系问题，擅长认知行为疗法，温柔耐心陪伴每一位来访者</p>
                    <a href="/live?id=1" class="counselor-btn">进入直播间</a>
                </div>
            </div>

            <!-- 辅导师2 -->
            <div class="counselor-card">
                <div class="counselor-header">
                    <div class="avatar">
                        <img src="https://images.unsplash.com/photo-1563226021-f719043f7021?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&q=80" alt="王导师">
                    </div>
                    <div class="counselor-info">
                        <div class="counselor-name">王导师 · 心理督导师</div>
                        <div class="counselor-title">心理专家 | 压力管理专家</div>
                    </div>
                    <div class="live-status">正在直播</div>
                </div>
                <div class="counselor-content">
                    <p class="counselor-desc">专注职场压力、情感困扰、亲子关系，运用正念疗法帮助来访者找回内心力量</p>
                    <a href="/live?id=2" class="counselor-btn">进入直播间</a>
                </div>
            </div>

            <!-- 辅导师3 -->
            <div class="counselor-card">
                <div class="counselor-header">
                    <div class="avatar">
                        <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&q=80" alt="张导师">
                    </div>
                    <div class="counselor-info">
                        <div class="counselor-name">李永权 · 青少年心理专家</div>
                        <div class="counselor-title">资深二次元专家 | 家庭治疗师</div>
                    </div>
                    <div class="live-status">正在直播</div>
                </div>
                <div class="counselor-content">
                    <p class="counselor-desc">专注青少年厌学、叛逆、早恋问题，擅长家庭系统治疗，构建和谐亲子关系</p>
                    <a href="/live?id=3" class="counselor-btn">进入直播间</a>
                </div>
            </div>

            <!-- 辅导师4 -->
            <div class="counselor-card">
                <div class="counselor-header">
                    <div class="avatar">
                        <img src="https://images.unsplash.com/photo-1544005313-94ddf0286df2?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&q=80" alt="陈导师">
                    </div>
                    <div class="counselor-info">
                        <div class="counselor-name">陈导师 · 情感心理咨询师</div>
                        <div class="counselor-title">婚恋情感专家 | 创伤修复导师</div>
                    </div>
                    <div class="live-status">正在直播</div>
                </div>
                <div class="counselor-content">
                    <p class="counselor-desc">专注情感挽回、婚姻危机、失恋创伤，用专业陪伴走出情感困境</p>
                    <a href="/live?id=4" class="counselor-btn">进入直播间</a>
                </div>
            </div>
        </div>
    </div>

    <!-- 返回首页按钮 -->
    <a href="/" class="back-btn">←</a>
</body>
</html>
"""

# 新增：直播间页面
LIVE_PAGE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>心理咨询直播间 - 心灵驿站</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Microsoft YaHei', sans-serif;
        }

        body {
            background: #1e1e2e;
            color: white;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* 顶部栏 */
        .top-bar {
            background: #2b2b3d;
            padding: 12px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .room-title {
            font-size: 18px;
            font-weight: bold;
        }

        .counselor-name {
            color: #f39c12;
            margin-left: 10px;
        }

        .back-btn {
            color: white;
            text-decoration: none;
            background: #444;
            padding: 6px 15px;
            border-radius: 5px;
        }

        /* 主内容区（仿腾讯会议布局） */
        .main-content {
            flex: 1;
            display: flex;
            padding: 20px;
            gap: 20px;
        }

        /* 视频区域（左侧大窗口） */
        .video-area {
            flex: 3;
            background: #2b2b3d;
            border-radius: 10px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
        }

        .video-placeholder {
            width: 80%;
            height: 80%;
            background: #3b3b4f;
            border-radius: 10px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 15px;
        }

        .avatar-large {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            overflow: hidden;
            border: 3px solid #f39c12;
        }

        .avatar-large img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .live-label {
            background: #e74c3c;
            padding: 3px 10px;
            border-radius: 3px;
            font-size: 12px;
        }

        /* 聊天区域（右侧） */
        .chat-area {
            flex: 1;
            background: #2b2b3d;
            border-radius: 10px;
            display: flex;
            flex-direction: column;
        }

        .chat-header {
            padding: 15px;
            border-bottom: 1px solid #444;
            text-align: center;
        }

        .chat-messages {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
        }

        .chat-message {
            margin-bottom: 12px;
            max-width: 90%;
        }

        .msg-name {
            font-size: 12px;
            color: #f39c12;
            margin-bottom: 3px;
        }

        .msg-content {
            background: #3b3b4f;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 14px;
        }

        .chat-input {
            padding: 15px;
            border-top: 1px solid #444;
            display: flex;
            gap: 10px;
        }

        .chat-input input {
            flex: 1;
            background: #3b3b4f;
            border: none;
            padding: 10px;
            border-radius: 5px;
            color: white;
            outline: none;
        }

        .chat-input button {
            background: #f39c12;
            border: none;
            padding: 0 15px;
            border-radius: 5px;
            color: white;
            cursor: pointer;
        }

        /* 底部控制栏 */
        .control-bar {
            background: #2b2b3d;
            padding: 15px;
            display: flex;
            justify-content: center;
            gap: 20px;
        }

        .control-btn {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: #3b3b4f;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        }

        .control-btn.end {
            background: #e74c3c;
        }
    </style>
</head>
<body>
    <!-- 顶部栏 -->
    <div class="top-bar">
        <div>
            <span class="room-title">心理咨询直播间</span>
            <span class="counselor-name">{{ counselor_name }}</span>
        </div>
        <a href="/counseling" class="back-btn">返回辅导列表</a>
    </div>

    <!-- 主内容区 -->
    <div class="main-content">
        <!-- 视频区域 -->
        <div class="video-area">
            <div class="video-placeholder">
                <div class="avatar-large">
                    <img src="{{ avatar_url }}" alt="咨询师头像">
                </div>
                <div class="live-label">正在直播</div>
                <div style="color:#aaa;">视频通话中 · 1对1私密咨询</div>
            </div>
        </div>

        <!-- 聊天区域 -->
        <div class="chat-area">
            <div class="chat-header">
                <h3>咨询聊天</h3>
            </div>
            <div class="chat-messages" id="chatMessages">
                <div class="chat-message">
                    <div class="msg-name">咨询师 {{ counselor_name }}</div>
                    <div class="msg-content">你好，我在这里，有什么困扰都可以慢慢说。</div>
                </div>
            </div>
            <div class="chat-input">
                <input type="text" placeholder="输入消息..." id="msgInput">
                <button onclick="sendMessage()">发送</button>
            </div>
        </div>
    </div>

    <!-- 底部控制栏（仿腾讯会议） -->
    <div class="control-bar">
        <div class="control-btn">🎤</div>
        <div class="control-btn">📷</div>
        <div class="control-btn">💬</div>
        <div class="control-btn end">📞 结束</div>
    </div>

    <script>
        function sendMessage() {
            const input = document.getElementById('msgInput');
            const text = input.value.trim();
            if (!text) return;

            const chat = document.getElementById('chatMessages');
            const msg = document.createElement('div');
            msg.className = 'chat-message';
            msg.innerHTML = `
                <div class="msg-name">我</div>
                <div class="msg-content">${text}</div>
            `;
            chat.appendChild(msg);
            input.value = '';
            chat.scrollTop = chat.scrollHeight;
        }
    </script>
</body>
</html>
"""


# 路由定义
@app.route('/')
def home():
    return render_template_string(HOME_PAGE)


@app.route('/courses')
def courses():
    return render_template_string(COURSES_PAGE)


@app.route('/chat')
def chat():
    return render_template_string(CHAT_PAGE)


@app.route('/counseling')
def counseling():
    return render_template_string(COUNSELING_PAGE)


# 新增：直播间路由（根据ID显示不同咨询师）
@app.route('/live')
def live():
    counselor_id = request.args.get('id', '1')

    # 咨询师数据
    counselors = {
        '1': {
            'name': '李静 · 资深心理咨询师',
            'avatar': 'https://images.unsplash.com/photo-1566753323558-f4e0952af11?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&q=80'
        },
        '2': {
            'name': '王浩 · 心理督导师',
            'avatar': 'https://images.unsplash.com/photo-1563226021-f719043f7021?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&q=80'
        },
        '3': {
            'name': '张敏 · 青少年心理专家',
            'avatar': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&q=80'
        },
        '4': {
            'name': '陈明 · 情感心理咨询师',
            'avatar': 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&q=80'
        }
    }

    data = counselors.get(counselor_id, counselors['1'])
    return render_template_string(LIVE_PAGE,
                                  counselor_name=data['name'],
                                  avatar_url=data['avatar'])


# AI聊天接口（接入千问）
@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json()
    user_message = data.get('message', '')

    # 调用千问AI
    headers = {
        "Authorization": f"Bearer {QIANWEN_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "qwen-turbo",
        "input": {
            "messages": [
                {"role": "system",
                 "content": "你是一个温柔的心理陪伴AI，专注倾听和安慰，语气亲切温暖，不使用专业术语，像朋友一样陪伴用户"},
                {"role": "user", "content": user_message}
            ]
        },
        "parameters": {
            "result_format": "message"
        }
    }

    try:
        response = requests.post(QIANWEN_API_URL, headers=headers, json=payload)
        response_data = response.json()
        ai_reply = response_data['output']['choices'][0]['message']['content']
        return jsonify({"reply": ai_reply})
    except:
        # 备用回复（API不可用时）
        return jsonify({"reply": "我在这里陪着你呢，慢慢说，我都听着😊"})


# 运行应用
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
