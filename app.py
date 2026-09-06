from flask import Flask, render_template_string

app = Flask(__name__)

# Main shell HTML – only fetches and injects the UI
MAIN_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>JoyMix - Created by Muhammad Taqi</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background-color: #0f0f0f; margin: 0; }
    </style>
</head>
<body>
    <div id="joymix-app"></div>
    <script>
        fetch('/api/render-ui')
            .then(response => response.text())
            .then(html => {
                const appDiv = document.getElementById('joymix-app');
                appDiv.innerHTML = html;
                // Execute all script tags that were part of the injected UI
                const scripts = appDiv.querySelectorAll('script');
                scripts.forEach(script => {
                    const newScript = document.createElement('script');
                    newScript.textContent = script.textContent;
                    document.body.appendChild(newScript);
                    script.remove();
                });
            })
            .catch(err => console.error('Error loading UI:', err));
    </script>
</body>
</html>"""

# Full JoyMix UI (styles + markup + logic) returned by the API
BACKEND_UI_COMPONENT = r"""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Roboto', 'Segoe UI', Arial, sans-serif;
        -webkit-tap-highlight-color: transparent;
    }

    body {
        background-color: #0f0f0f;
        color: #f1f1f1;
        min-height: 100vh;
        overflow-x: hidden;
    }

    /* Mode Selection Screen */
    #selector-screen {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh;
        width: 100vw;
        background: radial-gradient(circle at center, #1f1f1f 0%, #0f0f0f 100%);
        text-align: center;
        padding: 20px;
    }

    .brand-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 8px;
        color: #ffffff;
        letter-spacing: -1px;
    }

    .brand-title span {
        color: #ff0000;
    }

    .creator-tag {
        font-size: 0.95rem;
        color: #aaa;
        margin-bottom: 40px;
        background: rgba(255, 255, 255, 0.05);
        padding: 6px 16px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .btn-container {
        display: flex;
        gap: 20px;
        flex-wrap: wrap;
        justify-content: center;
        width: 100%;
        max-width: 400px;
    }

    .mode-btn {
        background: #181818;
        color: #fff;
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 16px 30px;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 12px;
        width: 100%;
        justify-content: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    }

    .mode-btn:active {
        transform: scale(0.98);
    }

    .mode-btn.online-btn:hover {
        background: #ff0000;
    }

    .mode-btn.offline-btn:hover {
        background: #333333;
    }

    /* Fullscreen Containers */
    #online-frame-container, #offline-container {
        display: none;
        width: 100vw;
        height: 100vh;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 10;
    }

    iframe.full-page-frame {
        width: 100%;
        height: 100%;
        border: none;
    }

    /* Back to Menu Button */
    .back-to-menu {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: rgba(255, 0, 0, 0.9);
        color: #fff;
        border: none;
        padding: 12px 20px;
        border-radius: 30px;
        font-weight: bold;
        cursor: pointer;
        z-index: 9999;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        backdrop-filter: blur(5px);
    }

    /* Offline Template Custom Internal Styles */
    :root {
        --bg-color: #0f0f0f;
        --card-bg: #181818;
        --text-color: #f1f1f1;
        --subtext-color: #aaa;
        --border-color: rgba(255, 255, 255, 0.1);
        --chip-bg: rgba(255, 255, 255, 0.1);
        --chip-hover-bg: #f1f1f1;
        --chip-hover-text: #0f0f0f;
        --shadow-color: rgba(0, 0, 0, 0.6);
    }

    body.light-theme {
        --bg-color: #ffffff;
        --card-bg: #f9f9f9;
        --text-color: #0f0f0f;
        --subtext-color: #606060;
        --border-color: rgba(0, 0, 0, 0.1);
        --chip-bg: rgba(0, 0, 0, 0.05);
        --chip-hover-bg: #0f0f0f;
        --chip-hover-text: #ffffff;
        --shadow-color: rgba(0, 0, 0, 0.15);
    }

    #offline-container {
        background-color: var(--bg-color);
        color: var(--text-color);
        overflow-y: auto;
    }

    header {
        width: 100%;
        height: 60px;
        background: var(--bg-color);
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 15px;
        position: sticky;
        top: 0;
        z-index: 100;
        border-bottom: 1px solid var(--border-color);
    }

    .logo-box {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 20px;
        font-weight: 700;
        color: var(--text-color);
        text-decoration: none;
    }

    .logo-icon {
        color: #ff0000;
        font-size: 24px;
    }

    .header-actions {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .theme-toggle-btn {
        background: var(--chip-bg);
        color: var(--text-color);
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        border: 1px solid var(--border-color);
        font-size: 16px;
    }

    .creator-link {
        background: var(--chip-bg);
        color: var(--text-color);
        padding: 6px 12px;
        border-radius: 20px;
        text-decoration: none;
        font-size: 12px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
        border: 1px solid var(--border-color);
    }

    .category-bar {
        width: 100%;
        padding: 10px 15px;
        background: var(--bg-color);
        display: flex;
        gap: 10px;
        overflow-x: auto;
        position: sticky;
        top: 60px;
        z-index: 90;
        border-bottom: 1px solid var(--border-color);
    }

    .category-bar::-webkit-scrollbar {
        display: none;
    }

    .chip {
        background: var(--chip-bg);
        color: var(--text-color);
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        white-space: nowrap;
        cursor: pointer;
        border: none;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .chip.active {
        background: #ff0000;
        color: #ffffff;
    }

    main {
        padding: 15px;
        max-width: 1600px;
        margin: 0 auto;
        width: 100%;
    }

    .grid-feed {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(100%, 1fr));
        gap: 15px;
    }

    @media (min-width: 600px) {
        .grid-feed {
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        }
    }

    .card {
        background: var(--card-bg);
        border-radius: 12px;
        overflow: hidden;
        cursor: pointer;
        display: flex;
        flex-direction: column;
        border: 1px solid var(--border-color);
    }

    .card:active {
        transform: scale(0.98);
    }

    .thumbnail {
        width: 100%;
        height: 160px;
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: rgba(128, 128, 128, 0.1);
    }

    .thumbnail i.play-icon {
        font-size: 42px;
        color: #ff0000;
    }

    .badge {
        position: absolute;
        bottom: 8px;
        right: 8px;
        background: rgba(0, 0, 0, 0.85);
        color: #fff;
        padding: 3px 6px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
    }

    .card-details {
        padding: 12px;
        display: flex;
        gap: 10px;
    }

    .avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: var(--chip-bg);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        color: var(--text-color);
        flex-shrink: 0;
    }

    .info h3 {
        font-size: 14px;
        font-weight: 600;
        color: var(--text-color);
        line-height: 1.3;
        margin-bottom: 2px;
    }

    .info p {
        font-size: 12px;
        color: var(--subtext-color);
    }

    /* Mobile Full-Screen Player Modal */
    .player-modal {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: #000;
        z-index: 10000;
        flex-direction: column;
    }

    .player-container {
        width: 100%;
        height: 100%;
        position: relative;
    }

    #mainFrame {
        width: 100%;
        height: 100%;
        border: none;
        display: block;
    }

    .controls-overlay {
        position: fixed;
        top: 12px;
        right: 12px;
        z-index: 10001;
    }

    .action-btn {
        color: #fff;
        font-size: 18px;
        cursor: pointer;
        background: rgba(255, 0, 0, 0.85);
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    .action-btn:active {
        transform: scale(0.9);
    }
</style>

<div id="selector-screen">
    <h1 class="brand-title">Joy<span>Mix</span></h1>
    <div class="creator-tag"><i class="fa-solid fa-code"></i> Created by Muhammad Taqi</div>        
    <div class="btn-container">
        <button class="mode-btn online-btn" onclick="launchOnline()">
            <i class="fa-solid fa-globe"></i> Online
        </button>
        <button class="mode-btn offline-btn" onclick="launchOffline()">
            <i class="fa-solid fa-wifi-slash"></i> Offline
        </button>
    </div>
</div>

<div id="online-frame-container">
    <button class="back-to-menu" onclick="resetToMenu()"><i class="fa-solid fa-house"></i> Main Menu</button>
    <iframe id="online-iframe" class="full-page-frame" src="" allowfullscreen></iframe>
</div>

<div id="offline-container">
    <header>
        <a href="#" onclick="resetToMenu()" class="logo-box">
            <i class="fa-brands fa-youtube logo-icon"></i> JoyMix
        </a>
        <div class="header-actions">
            <div class="theme-toggle-btn" onclick="toggleTheme()" title="Toggle Dark/Light Mode">
                <i class="fa-solid fa-moon" id="themeIcon"></i>
            </div>
            <a href="#" onclick="resetToMenu()" class="creator-link">
                <i class="fa-solid fa-circle-user"></i> Muhammad Taqi
            </a>
        </div>
    </header>

    <div class="category-bar">
        <button class="chip active" onclick="filterCategory('all', this)"><i class="fa-solid fa-house"></i> All</button>
        <button class="chip" onclick="filterCategory('games', this)"><i class="fa-solid fa-gamepad"></i> Games</button>
        <button class="chip" onclick="filterCategory('images', this)"><i class="fa-solid fa-image"></i> Images</button>
        <button class="chip" onclick="filterCategory('poetry', this)"><i class="fa-solid fa-feather"></i> Poetry</button>
    </div>

    <main>
        <div class="grid-feed" id="feedGrid"></div>
    </main>

    <div class="player-modal" id="playerModal">
        <div class="controls-overlay">
            <div class="action-btn" onclick="closePlayer()" title="Close Fullscreen">
                <i class="fa-solid fa-xmark"></i>
            </div>
        </div>
        <div class="player-container">
            <iframe id="mainFrame" src="" allow="autoplay; encrypted-media; fullscreen" allowfullscreen></iframe>
        </div>
    </div>
</div>

<script>
    function launchOnline() {
        document.getElementById('selector-screen').style.display = 'none';
        document.getElementById('online-frame-container').style.display = 'block';
        document.getElementById('online-iframe').src = 'https://joymix1.oneapp.dev/';
    }

    function launchOffline() {
        document.getElementById('selector-screen').style.display = 'none';
        document.getElementById('offline-container').style.display = 'block';
        loadFeed();
    }

    function resetToMenu() {
        document.getElementById('online-iframe').src = '';
        document.getElementById('online-frame-container').style.display = 'none';
        document.getElementById('offline-container').style.display = 'none';
        document.getElementById('selector-screen').style.display = 'flex';
    }

    const staticItems = [
        { type: 'games', title: '50 Game Classic', path: '50.html', icon: 'fa-trophy', bg: 'fa-gamepad' },
        { type: 'games', title: 'Flappy Bird Arcade', path: 'Flappy-Bird.html', icon: 'fa-dove', bg: 'fa-crow' },
        { type: 'games', title: 'Hill Climb Racing', path: 'Hill-Climb.html', icon: 'fa-truck', bg: 'fa-car' },
        { type: 'games', title: 'Dino Runner v1', path: 'diano1.html', icon: 'fa-paw', bg: 'fa-dragon' },
        { type: 'games', title: 'Dino Runner v2', path: 'diano2.html', icon: 'fa-dragon', bg: 'fa-dragon' },
        { type: 'games', title: 'Ludo Star Online', path: 'ludo.html', icon: 'fa-dice-four', bg: 'fa-dice' },
        { type: 'games', title: 'Stickman Hero', path: 'stickman.html', icon: 'fa-user-ninja', bg: 'fa-person-running' },
        { type: 'games', title: 'Rock Paper Scissors', path: 'stone-paper-seasor.html', icon: 'fa-hand-back-fist', bg: 'fa-hand' },
        { type: 'games', title: 'Tic Tac Toe Pro v2', path: 'tic-cros-2.html', icon: 'fa-xmark', bg: 'fa-hashtag' },
        { type: 'games', title: 'Tic Tac Toe Classic', path: 'tic-cross.html', icon: 'fa-grip-lines', bg: 'fa-table-cells' },
        { type: 'poetry', title: 'Poetry Cards & Quotes', path: 'poetry.html', icon: 'fa-book-open', bg: 'fa-feather' },
        { type: 'images', title: 'Offline Image Storage', path: 'offline.html', icon: 'fa-box-archive', bg: 'fa-hard-drive' }
    ];

    function toggleTheme() {
        const body = document.body;
        const icon = document.getElementById('themeIcon');
        body.classList.toggle('light-theme');
        icon.className = body.classList.contains('light-theme') ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
    }

    function loadFeed() {
        const grid = document.getElementById('feedGrid');
        let allCards = [];
        staticItems.forEach(item => {
            allCards.push({
                category: item.type,
                html: `
                    <div class="card item-${item.type}" onclick="playDirectItem('${item.path}')">
                        <div class="thumbnail">
                            <i class="fa-solid ${item.bg} play-icon"></i>
                            <span class="badge">${item.type.toUpperCase()}</span>
                        </div>
                        <div class="card-details">
                            <div class="avatar"><i class="fa-solid ${item.icon}"></i></div>
                            <div class="info">
                                <h3>${item.title}</h3>
                                <p>JoyMix • Open Full Screen</p>
                            </div>
                        </div>
                    </div>`
            });
        });

        grid.innerHTML = allCards.map(c => c.html).join('');
    }

    function filterCategory(category, el) {
        document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
        el.classList.add('active');

        const cards = document.querySelectorAll('.card');
        cards.forEach(card => {
            card.style.display = (category === 'all' || card.classList.contains('item-' + category)) ? 'flex' : 'none';
        });
    }

    // Full Page View Logic for Mobile
    function playDirectItem(path) {
        const playerModal = document.getElementById('playerModal');
        const mainFrame = document.getElementById('mainFrame');
                
        mainFrame.src = path;
        playerModal.style.display = 'flex';
                
        // Mobile Browser Par Fullscreen API trigger karna (optional)
        if (playerModal.requestFullscreen) {
            playerModal.requestFullscreen().catch(err => console.log(err));
        } else if (playerModal.webkitRequestFullscreen) {
            playerModal.webkitRequestFullscreen();
        }
    }

    function closePlayer() {
        const playerModal = document.getElementById('playerModal');
        const mainFrame = document.getElementById('mainFrame');
                
        mainFrame.src = '';
        playerModal.style.display = 'none';

        // Exit full screen mode if active
        if (document.fullscreenElement || document.webkitFullscreenElement) {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.webkitExitFullscreen) {
                document.webkitExitFullscreen();
            }
        }
    }
</script>
"""

@app.route('/')
def home():
    return render_template_string(MAIN_HTML)

@app.route('/api/render-ui')
def render_ui():
    return BACKEND_UI_COMPONENT

if __name__ == '__main__':
    app.run(debug=True)
