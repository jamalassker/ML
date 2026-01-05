
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>APEX SCALPER PRO | AI Trading Simulator</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --bg-primary: #0a0e17;
            --bg-secondary: #111827;
            --bg-tertiary: #1a2235;
            --accent-cyan: #00f0ff;
            --accent-magenta: #ff00aa;
            --accent-gold: #ffd700;
            --profit-green: #00ff88;
            --loss-red: #ff3366;
            --text-primary: #e8f0ff;
            --text-secondary: #8892a8;
            --border-glow: rgba(0, 240, 255, 0.3);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Rajdhani', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
        }

        /* Animated Background */
        .bg-grid {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(rgba(0, 240, 255, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 240, 255, 0.03) 1px, transparent 1px);
            background-size: 50px 50px;
            pointer-events: none;
            z-index: 0;
        }

        .bg-glow {
            position: fixed;
            width: 600px;
            height: 600px;
            border-radius: 50%;
            filter: blur(150px);
            opacity: 0.15;
            pointer-events: none;
            z-index: 0;
        }

        .glow-1 {
            top: -200px;
            right: -200px;
            background: var(--accent-cyan);
            animation: pulse 8s ease-in-out infinite;
        }

        .glow-2 {
            bottom: -200px;
            left: -200px;
            background: var(--accent-magenta);
            animation: pulse 8s ease-in-out infinite 4s;
        }

        @keyframes pulse {
            0%, 100% { opacity: 0.1; transform: scale(1); }
            50% { opacity: 0.2; transform: scale(1.1); }
        }

        /* Header */
        .header {
            position: relative;
            z-index: 10;
            padding: 15px 20px;
            background: linear-gradient(180deg, rgba(17, 24, 39, 0.95) 0%, transparent 100%);
            border-bottom: 1px solid var(--border-glow);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo-icon {
            width: 45px;
            height: 45px;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-magenta));
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            animation: logoGlow 3s ease-in-out infinite;
        }

        @keyframes logoGlow {
            0%, 100% { box-shadow: 0 0 20px rgba(0, 240, 255, 0.5); }
            50% { box-shadow: 0 0 40px rgba(255, 0, 170, 0.5); }
        }

        .logo-text {
            font-family: 'Orbitron', monospace;
            font-size: 1.4rem;
            font-weight: 900;
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-magenta));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .logo-sub {
            font-size: 0.65rem;
            color: var(--text-secondary);
            letter-spacing: 3px;
            text-transform: uppercase;
        }

        .balance-display {
            display: flex;
            align-items: center;
            gap: 20px;
            flex-wrap: wrap;
        }

        .balance-item {
            text-align: right;
        }

        .balance-label {
            font-size: 0.7rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .balance-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.3rem;
            font-weight: 700;
        }

        .balance-value.profit { color: var(--profit-green); }
        .balance-value.loss { color: var(--loss-red); }

        /* Main Container */
        .main-container {
            position: relative;
            z-index: 10;
            display: grid;
            grid-template-columns: 1fr 320px;
            gap: 15px;
            padding: 15px;
            max-width: 1600px;
            margin: 0 auto;
        }

        @media (max-width: 1024px) {
            .main-container {
                grid-template-columns: 1fr;
            }
        }

        /* Chart Container */
        .chart-container {
            background: var(--bg-secondary);
            border-radius: 16px;
            border: 1px solid var(--border-glow);
            overflow: hidden;
        }

        .chart-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 16px;
            background: var(--bg-tertiary);
            border-bottom: 1px solid rgba(255,255,255,0.05);
            flex-wrap: wrap;
            gap: 10px;
        }

        .pair-selector {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .pair-name {
            font-family: 'Orbitron', monospace;
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--accent-cyan);
        }

        .pair-price {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.2rem;
        }

        .price-change {
            font-size: 0.85rem;
            padding: 3px 8px;
            border-radius: 6px;
        }

        .price-change.up {
            background: rgba(0, 255, 136, 0.15);
            color: var(--profit-green);
        }

        .price-change.down {
            background: rgba(255, 51, 102, 0.15);
            color: var(--loss-red);
        }

        .timeframe-selector {
            display: flex;
            gap: 5px;
        }

        .tf-btn {
            padding: 6px 12px;
            background: transparent;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 6px;
            color: var(--text-secondary);
            font-family: 'Rajdhani', sans-serif;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }

        .tf-btn:hover, .tf-btn.active {
            background: var(--accent-cyan);
            color: var(--bg-primary);
            border-color: var(--accent-cyan);
        }

        .chart-canvas-container {
            position: relative;
            height: 400px;
        }

        #chartCanvas {
            width: 100%;
            height: 100%;
        }

        /* Indicators Panel */
        .indicators-bar {
            display: flex;
            gap: 15px;
            padding: 10px 16px;
            background: rgba(0,0,0,0.3);
            border-top: 1px solid rgba(255,255,255,0.05);
            overflow-x: auto;
            flex-wrap: wrap;
        }

        .indicator-chip {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 6px 12px;
            background: var(--bg-tertiary);
            border-radius: 20px;
            font-size: 0.75rem;
            white-space: nowrap;
        }

        .indicator-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
        }

        .indicator-value {
            font-family: 'JetBrains Mono', monospace;
            font-weight: 600;
        }

        /* Trading Panel */
        .trading-panel {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .panel-card {
            background: var(--bg-secondary);
            border-radius: 16px;
            border: 1px solid var(--border-glow);
            overflow: hidden;
        }

        .panel-header {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px 16px;
            background: var(--bg-tertiary);
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }

        .panel-icon {
            width: 32px;
            height: 32px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
        }

        .panel-title {
            font-family: 'Orbitron', monospace;
            font-size: 0.85rem;
            font-weight: 700;
            letter-spacing: 1px;
        }

        .panel-content {
            padding: 16px;
        }

        /* AI Signal Card */
        .ai-signal-card .panel-icon {
            background: linear-gradient(135deg, var(--accent-magenta), var(--accent-cyan));
        }

        .signal-main {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 15px;
        }

        .signal-direction {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .signal-arrow {
            width: 50px;
            height: 50px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }

        .signal-arrow.buy {
            background: linear-gradient(135deg, rgba(0, 255, 136, 0.2), rgba(0, 255, 136, 0.05));
            color: var(--profit-green);
         animation: signalPulse 2s ease-in-out infinite;
        }

        .signal-arrow.sell {
            background: linear-gradient(135deg, rgba(255, 51, 102, 0.2), rgba(255, 51, 102, 0.05));
            color: var(--loss-red);
            animation: signalPulse 2s ease-in-out infinite;
        }

        .signal-arrow.neutral {
            background: rgba(255, 215, 0, 0.15);
            color: var(--accent-gold);
        }

        @keyframes signalPulse {
            0%, 100% { box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.4); }
            50% { box-shadow: 0 0 20px 5px rgba(0, 255, 136, 0.1); }
        }

        .signal-text {
            font-family: 'Orbitron', monospace;
            font-size: 1.2rem;
            font-weight: 700;
        }

        .signal-confidence {
            text-align: right;
        }

        .confidence-label {
            font-size: 0.7rem;
            color: var(--text-secondary);
            text-transform: uppercase;
        }

        .confidence-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--accent-cyan);
        }

        .signal-reasons {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .reason-item {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            background: rgba(0,0,0,0.3);
            border-radius: 8px;
            font-size: 0.8rem;
        }

        .reason-icon {
            color: var(--accent-cyan);
        }

        /* Trade Execution */
        .trade-card .panel-icon {
            background: linear-gradient(135deg, var(--profit-green), #00aa55);
        }

        .trade-inputs {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .input-group {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        .input-label {
            font-size: 0.75rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .input-field {
            display: flex;
            align-items: center;
            background: var(--bg-tertiary);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 10px;
            overflow: hidden;
        }

        .input-field input {
            flex: 1;
            padding: 12px;
            background: transparent;
            border: none;
            color: var(--text-primary);
            font-family: 'JetBrains Mono', monospace;
            font-size: 1rem;
            outline: none;
        }

        .input-field input::placeholder {
            color: var(--text-secondary);
        }

        .input-suffix {
            padding: 12px;
            color: var(--text-secondary);
            font-size: 0.85rem;
            background: rgba(0,0,0,0.2);
        }

        .leverage-selector {
            display: flex;
            gap: 5px;
        }

        .lev-btn {
            flex: 1;
            padding: 10px;
            background: var(--bg-tertiary);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            color: var(--text-secondary);
            font-family: 'Rajdhani', sans-serif;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }

        .lev-btn:hover, .lev-btn.active {
            background: var(--accent-cyan);
            color: var(--bg-primary);
            border-color: var(--accent-cyan);
        }

        .trade-buttons {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 10px;
        }

        .trade-btn {
            padding: 14px;
            border: none;
            border-radius: 10px;
            font-family: 'Orbitron', monospace;
            font-size: 0.9rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .trade-btn.buy {
            background: linear-gradient(135deg, var(--profit-green), #00aa55);
            color: #000;
        }

        .trade-btn.sell {
            background: linear-gradient(135deg, var(--loss-red), #cc0033);
            color: #fff;
        }

        .trade-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }

        .trade-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }

        /* Active Trade */
        .active-trade {
            margin-top: 15px;
            padding: 15px;
            background: var(--bg-tertiary);
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.1);
            display: none;
        }

        .active-trade.visible {
            display: block;
            animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .trade-info {
            display: flex;
            justify-content: space-between;
            margin-bottom: 12px;
        }

        .trade-type {
            font-weight: 700;
            font-size: 0.9rem;
        }

        .trade-type.long { color: var(--profit-green); }
        .trade-type.short { color: var(--loss-red); }

        .trade-pnl {
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700;
        }

        .close-trade-btn {
            width: 100%;
            padding: 10px;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 8px;
            color: var(--text-primary);
            font-family: 'Rajdhani', sans-serif;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }

        .close-trade-btn:hover {
            background: var(--loss-red);
            border-color: var(--loss-red);
        }

        /* Strategy Guide */
        .strategy-card .panel-icon {
            background: linear-gradient(135deg, var(--accent-gold), #ff8800);
        }

        .strategy-list {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .strategy-item {
            padding: 12px;
            background: var(--bg-tertiary);
            border-radius: 10px;
            border-left: 3px solid var(--accent-cyan);
            cursor: pointer;
            transition: all 0.3s;
        }

        .strategy-item:hover {
            background: rgba(0, 240, 255, 0.1);
        }

        .strategy-item.active {
            border-left-color: var(--accent-gold);
            background: rgba(255, 215, 0, 0.1);
        }

        .strategy-name {
            font-weight: 600;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .strategy-badge {
            font-size: 0.65rem;
            padding: 2px 6px;
            background: var(--accent-magenta);
            border-radius: 4px;
            color: #fff;
        }

        .strategy-desc {
            font-size: 0.75rem;
            color: var(--text-secondary);
        }

        /* Stats Panel */
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }

        .stat-item {
            padding: 12px;
            background: var(--bg-tertiary);
            border-radius: 10px;
            text-align: center;
        }

        .stat-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.1rem;
            font-weight: 700;
        }

        .stat-label {
            font-size: 0.7rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            margin-top: 4px;
        }

        /* Trade History */
        .history-list {
            max-height: 200px;
            overflow-y: auto;
        }

        .history-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }

        .history-item:last-child {
            border-bottom: none;
        }

        .history-type {
            font-size: 0.75rem;
            font-weight: 600;
            padding: 3px 8px;
            border-radius: 4px;
        }

        .history-type.long {
            background: rgba(0, 255, 136, 0.15);
            color: var(--profit-green);
        }

        .history-type.short {
            background: rgba(255, 51, 102, 0.15);
            color: var(--loss-red);
        }

        .history-pnl {
            font-family: 'JetBrains Mono', monospace;
            font-weight: 600;
            font-size: 0.85rem;
        }

        /* Education Modal */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            backdrop-filter: blur(10px);
            z-index: 1000;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .modal-overlay.visible {
            display: flex;
        }

        .modal-content {
            background: var(--bg-secondary);
            border-radius: 20px;
            border: 1px solid var(--border-glow);
            max-width: 600px;
            width: 100%;
            max-height: 80vh;
            overflow-y: auto;
            animation: modalIn 0.3s ease;
        }

        @keyframes modalIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            background: var(--bg-tertiary);
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }

        .modal-title {
            font-family: 'Orbitron', monospace;
            font-size: 1.2rem;
            color: var(--accent-cyan);
        }

        .modal-close {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: rgba(255,255,255,0.1);
            border: none;
            color: var(--text-primary);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s;
        }

        .modal-close:hover {
            background: var(--loss-red);
        }

        .modal-body {
            padding: 20px;
        }

        .lesson-content h3 {
            color: var(--accent-gold);
            margin-bottom: 15px;
            font-family: 'Orbitron', monospace;
        }

        .lesson-content p {
            color: var(--text-secondary);
            line-height: 1.7;
            margin-bottom: 15px;
        }

        .lesson-content ul {
            margin-left: 20px;
            margin-bottom: 15px;
        }

        .lesson-content li {
            color: var(--text-secondary);
            margin-bottom: 8px;
            line-height: 1.6;
        }

        .lesson-content .highlight {
            color: var(--accent-cyan);
            font-weight: 600;
        }

        .lesson-content .warning {
            padding: 15px;
            background: rgba(255, 51, 102, 0.1);
            border-left: 3px solid var(--loss-red);
            border-radius: 8px;
            margin: 15px 0;
        }

        .lesson-content .pro-tip {
            padding: 15px;
            background: rgba(0, 240, 255, 0.1);
            border-left: 3px solid var(--accent-cyan);
            border-radius: 8px;
            margin: 15px 0;
        }

        /* Toast Notifications */
        .toast-container {
            position: fixed;
            top: 80px;
            right: 20px;
            z-index: 1001;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .toast {
            padding: 15px 20px;
            background: var(--bg-secondary);
            border-radius: 12px;
            border: 1px solid var(--border-glow);
            display: flex;
            align-items: center;
            gap: 12px;
            animation: toastIn 0.3s ease;
            max-width: 350px;
        }

        @keyframes toastIn {
            from { opacity: 0; transform: translateX(100px); }
            to { opacity: 1; transform: translateX(0); }
        }

        .toast.success { border-left: 4px solid var(--profit-green); }
        .toast.error { border-left: 4px solid var(--loss-red); }
        .toast.info { border-left: 4px solid var(--accent-cyan); }

        .toast-icon {
            font-size: 1.2rem;
        }

        .toast.success .toast-icon { color: var(--profit-green); }
        .toast.error .toast-icon { color: var(--loss-red); }
        .toast.info .toast-icon { color: var(--accent-cyan); }

        .toast-message {
            flex: 1;
            font-size: 0.9rem;
        }

        /* Disclaimer Banner */
        .disclaimer-banner {
            background: linear-gradient(90deg, rgba(255, 215, 0, 0.1), rgba(255, 0, 170, 0.1));
            padding: 10px 20px;
            text-align: center;
            font-size: 0.8rem;
            color: var(--accent-gold);
            border-bottom: 1px solid rgba(255, 215, 0, 0.2);
        }

        .disclaimer-banner i {
            margin-right: 8px;
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }

        ::-webkit-scrollbar-track {
            background: var(--bg-tertiary);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--accent-cyan);
            border-radius: 3px;
        }

        /* Mobile Responsive */
        @media (max-width: 768px) {
            .header {
                flex-direction: column;
                text-align: center;
            }

            .balance-display {
                justify-content: center;
            }

            .chart-canvas-container {
                height: 300px;
            }

            .main-container {
                padding: 10px;
            }

            .trade-buttons {
                grid-template-columns: 1fr;
            }

            .stats-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="bg-grid"></div>
    <div class="bg-glow glow-1"></div>
    <div class="bg-glow glow-2"></div>

    <div class="disclaimer-banner">
        <i class="fas fa-graduation-cap"></i>
        SIMULATION MODE — Practice with virtual funds. No real money involved. Learn before you trade!
    </div>

    <header class="header">
        <div class="logo">
            <div class="logo-icon">
                <i class="fas fa-bolt"></i>
            </div>
            <div>
                <div class="logo-text">APEX SCALPER</div>
                <div class="logo-sub">AI Trading Simulator</div>
            </div>
        </div>
        <div class="balance-display">
            <div class="balance-item">
                <div class="balance-label">Virtual Balance</div>
                <div class="balance-value" id="balance">$10.00</div>
            </div>
            <div class="balance-item">
                <div class="balance-label">Session P&L</div>
                <div class="balance-value profit" id="sessionPnl">+$0.00</div>
            </div>
            <div class="balance-item">
                <div class="balance-label">Win Rate</div>
                <div class="balance-value" id="winRate" style="color: var(--accent-cyan)">0%</div>
            </div>
        </div>
    </header>

    <main class="main-container">
        <div class="chart-section">
            <div class="chart-container">
                <div class="chart-header">
                    <div class="pair-selector">
                        <select id="pairSelect" style="background: var(--bg-tertiary); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 8px 12px; color: var(--text-primary); font-family: 'Orbitron', monospace; cursor: pointer;">
                            <option value="BTC/USDT">BTC/USDT</option>
                            <option value="ETH/USDT">ETH/USDT</option>
                            <option value="SOL/USDT">SOL/USDT</option>
                            <option value="XRP/USDT">XRP/USDT</option>
                        </select>
                        <span class="pair-price" id="currentPrice">$94,521.34</span>
                        <span class="price-change up" id="priceChange">+0.42%</span>
                    </div>
                    <div class="timeframe-selector">
                        <button class="tf-btn active" data-tf="1">1m</button>
                        <button class="tf-btn" data-tf="5">5m</button>
                        <button class="tf-btn" data-tf="15">15m</button>
                    </div>
                </div>
                <div class="chart-canvas-container">
                    <canvas id="chartCanvas"></canvas>
                </div>
                <div class="indicators-bar">
                    <div class="indicator-chip">
                        <div class="indicator-dot" style="background: #ff6384;"></div>
                        <span>RSI(14)</span>
                        <span class="indicator-value" id="rsiValue">52.4</span>
                    </div>
                    <div class="indicator-chip">
                        <div class="indicator-dot" style="background: #36a2eb;"></div>
                        <span>MACD</span>
                        <span class="indicator-value" id="macdValue">+12.5</span>
                    </div>
                    <div class="indicator-chip">
                        <div class="indicator-dot" style="background: #ffce56;"></div>
                        <span>BB Width</span>
                        <span class="indicator-value" id="bbValue">1.8%</span>
                    </div>
                    <div class="indicator-chip">
                        <div class="indicator-dot" style="background: #4bc0c0;"></div>
                        <span>EMA Cross</span>
                        <span class="indicator-value" id="emaValue">BULL</span>
                    </div>
                    <div class="indicator-chip">
                        <div class="indicator-dot" style="background: #9966ff;"></div>
                        <span>Volume</span>
                        <span class="indicator-value" id="volValue">HIGH</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="trading-panel">
            <!-- AI Signal Card -->
            <div class="panel-card ai-signal-card">
                <div class="panel-header">
                    <div class="panel-icon">
                        <i class="fas fa-brain"></i>
                    </div>
                    <div class="panel-title">AI SIGNAL ENGINE</div>
                </div>
                <div class="panel-content">
                    <div class="signal-main">
                        <div class="signal-direction">
                            <div class="signal-arrow neutral" id="signalArrow">
                                <i class="fas fa-minus"></i>
                            </div>
                            <div class="signal-text" id="signalText">ANALYZING...</div>
                        </div>
                        <div class="signal-confidence">
                            <div class="confidence-label">Confidence</div>
                            <div class="confidence-value" id="signalConfidence">--</div>
                        </div>
                    </div>
                    <div class="signal-reasons" id="signalReasons">
                        <div class="reason-item">
                            <i class="fas fa-spinner fa-spin reason-icon"></i>
                            <span>Analyzing market structure...</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Trade Execution -->
            <div class="panel-card trade-card">
                <div class="panel-header">
                    <div class="panel-icon">
                        <i class="fas fa-exchange-alt"></i>
                    </div>
                    <div class="panel-title">EXECUTE TRADE</div>
                </div>
                <div class="panel-content">
                    <div class="trade-inputs">
                        <div class="input-group">
                            <div class="input-label">Position Size</div>
                            <div class="input-field">
                                <input type="number" id="positionSize" value="1" min="0.1" max="10" step="0.1">
                                <span class="input-suffix">USD</span>
                            </div>
                        </div>
                        <div class="input-group">
                            <div class="input-label">Leverage</div>
                            <div class="leverage-selector">
                                <button class="lev-btn" data-lev="1">1x</button>
                                <button class="lev-btn" data-lev="5">5x</button>
                                <button class="lev-btn active" data-lev="10">10x</button>
                                <button class="lev-btn" data-lev="20">20x</button>
                            </div>
                        </div>
                        <div class="trade-buttons">
                            <button class="trade-btn buy" id="buyBtn">
                                <i class="fas fa-arrow-up"></i> LONG
                            </button>
                            <button class="trade-btn sell" id="sellBtn">
                                <i class="fas fa-arrow-down"></i> SHORT
                            </button>
                        </div>
                    </div>
                    <div class="active-trade" id="activeTrade">
                        <div class="trade-info">
                            <span class="trade-type" id="tradeType">LONG</span>
                            <span class="trade-pnl" id="tradePnl">+$0.00</span>
                        </div>
                        <div class="trade-info">
                            <span style="color: var(--text-secondary); font-size: 0.8rem;">Entry: <span id="entryPrice">$0</span></span>
                            <span style="color: var(--text-secondary); font-size: 0.8rem;">Size: <span id="tradeSize">$0</span></span>
                        </div>
                        <button class="close-trade-btn" id="closeTradeBtn">
                            <i class="fas fa-times"></i> Close Position
                        </button>
                    </div>
                </div>
            </div>

            <!-- Strategies -->
            <div class="panel-card strategy-card">
                <div class="panel-header">
                    <div class="panel-icon">
                        <i class="fas fa-lightbulb"></i>
                    </div>
                    <div class="panel-title">SCALPING STRATEGIES</div>
                </div>
                <div class="panel-content">
                    <div class="strategy-list">
                        <div class="strategy-item active" data-strategy="momentum">
                            <div class="strategy-name">
                                <i class="fas fa-rocket"></i>
                                Momentum Breakout
                                <span class="strategy-badge">HOT</span>
                            </div>
                            <div class="strategy-desc">RSI + Volume spike confirmation</div>
                        </div>
                        <div class="strategy-item" data-strategy="reversal">
                            <div class="strategy-name">
                                <i class="fas fa-sync-alt"></i>
                                Mean Reversion
                            </div>
                            <div class="strategy-desc">Bollinger Band bounce strategy</div>
                        </div>
                        <div class="strategy-item" data-strategy="ema">
                            <div class="strategy-name">
                                <i class="fas fa-chart-line"></i>
                                EMA Crossover
                            </div>
                            <div class="strategy-desc">9/21 EMA trend following</div>
                        </div>
                        <div class="strategy-item" data-strategy="orderflow">
                            <div class="strategy-name">
                                <i class="fas fa-stream"></i>
                                Order Flow Imbalance
                                <span class="strategy-badge">PRO</span>
                            </div>
                            <div class="strategy-desc">Volume delta analysis</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Stats -->
            <div class="panel-card">
                <div class="panel-header">
                    <div class="panel-icon" style="background: linear-gradient(135deg, #9966ff, #6633cc);">
                        <i class="fas fa-chart-pie"></i>
                    </div>
                    <div class="panel-title">SESSION STATS</div>
                </div>
                <div class="panel-content">
                    <div class="stats-grid">
                        <div class="stat-item">
                            <div class="stat-value" id="totalTrades">0</div>
                            <div class="stat-label">Total Trades</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value" style="color: var(--profit-green);" id="winTrades">0</div>
                            <div class="stat-label">Winning</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value" style="color: var(--loss-red);" id="lossTrades">0</div>
                            <div class="stat-label">Losing</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value" id="avgPnl">$0.00</div>
                            <div class="stat-label">Avg P&L</div>
                        </div>
                    </div>
                    <div class="history-list" id="historyList" style="margin-top: 15px;">
                        <!-- Trade history items will be added here -->
                    </div>
                </div>
            </div>
        </div>
    </main>

    <!-- Education Modal -->
    <div class="modal-overlay" id="eduModal">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title" id="modalTitle">Strategy Guide</div>
                <button class="modal-close" id="modalClose">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                <div class="lesson-content" id="lessonContent"></div>
            </div>
        </div>
    </div>

    <!-- Toast Container -->
    <div class="toast-container" id="toastContainer"></div>

    <script>
        // ============================================
        // APEX SCALPER PRO - AI Trading Simulator
        // ============================================

        // State Management
        const state = {
            balance: 10.00,
            sessionPnl: 0,
            currentPrice: 94521.34,
            currentPair: 'BTC/USDT',
            timeframe: 1,
            leverage: 10,
            positionSize: 1,
            activeTrade: null,
            trades: [],
            candles: [],
            indicators: {
                rsi: 50,
                macd: 0,
                bbWidth: 1.5,
                ema9: 0,
                ema21: 0,
                volumeProfile: 'MEDIUM'
            },
            strategy: 'momentum',
            priceHistory: []
        };

        // Pair base prices
        const pairPrices = {
            'BTC/USDT': 94521.34,
            'ETH/USDT': 3421.56,
            'SOL/USDT': 187.34,
            'XRP/USDT': 2.34
        };

        // Strategy definitions
        const strategies = {
            momentum: {
                title: 'Momentum Breakout Strategy',
                content: `
                    <h3>🚀 Momentum Breakout - The Scalper's Edge</h3>
                    <p>This strategy captures explosive moves when price breaks through key levels with volume confirmation.</p>
                    
                    <h3>Entry Signals</h3>
                    <ul>
                        <li><span class="highlight">RSI crosses above 55</span> from below (bullish momentum building)</li>
                        <li><span class="highlight">Volume spike > 150%</span> of 20-period average</li>
                        <li>Price breaks above recent swing high</li>
                        <li>MACD histogram turning positive</li>
                    </ul>
                    
                    <h3>Exit Rules</h3>
                    <ul>
                        <li>Take profit at <span class="highlight">0.3-0.5%</span> move (scalping targets)</li>
                        <li>Stop loss at <span class="highlight">0.2%</span> below entry</li>
                        <li>Exit if RSI reaches 75+ (overbought)</li>
                        <li>Trail stop after 0.2% profit</li>
                    </ul>
                    
                    <div class="pro-tip">
                        <strong>💡 Pro Tip:</strong> Best during high volatility sessions (US market open, major news). Avoid ranging markets!
                    </div>
                    
                    <div class="warning">
                        <strong>⚠️ Risk Warning:</strong> False breakouts are common. Always wait for volume confirmation before entering.
                    </div>
                `
            },
            reversal: {
                title: 'Mean Reversion Strategy',
                content: `
                    <h3>🔄 Mean Reversion - Fade the Extremes</h3>
                    <p>This strategy profits from price returning to its average after extreme moves. Perfect for ranging markets.</p>
                    
                    <h3>Entry Signals</h3>
                    <ul>
                        <li>Price touches <span class="highlight">lower Bollinger Band</span> (for longs)</li>
                        <li><span class="highlight">RSI below 30</span> (oversold territory)</li>
                        <li>Bullish candlestick pattern (hammer, engulfing)</li>
                        <li>Volume decreasing on the drop (exhaustion)</li>
                    </ul>
                    
                    <h3>Exit Rules</h3>
                    <ul>
                        <li>Take profit at <span class="highlight">middle Bollinger Band</span></li>
                        <li>Stop loss below recent low + buffer</li>
                        <li>Time-based exit: 5-10 candles max hold</li>
                    </ul>
                    
                    <div class="pro-tip">
                        <strong>💡 Pro Tip:</strong> Works best when BB Width is contracting. Avoid during strong trends!
                    </div>
                    
                    <div class="warning">
                        <strong>⚠️ Risk Warning:</strong> "Catching falling knives" is dangerous. Wait for confirmation candle!
                    </div>
                `
            },
            ema: {
                title: 'EMA Crossover Strategy',
                content: `
                    <h3>📈 EMA Crossover - Ride the Trend</h3>
                    <p>Classic trend-following strategy using fast and slow moving averages. Simple but effective.</p>
                    
                    <h3>Entry Signals</h3>
                    <ul>
                        <li><span class="highlight">9 EMA crosses above 21 EMA</span> (Golden cross = Long)</li>
                        <li><span class="highlight">9 EMA crosses below 21 EMA</span> (Death cross = Short)</li>
                        <li>Price above both EMAs for longs</li>
                        <li>Wait for pullback to 9 EMA for better entry</li>
                    </ul>
                    
                    <h3>Exit Rules</h3>
                    <ul>
                        <li>Exit when opposite crossover occurs</li>
                        <li>Take partial profits at <span class="highlight">1:2 risk-reward</span></li>
                        <li>Trail stop using the 9 EMA as dynamic support</li>
                    </ul>
                    
                    <div class="pro-tip">
                        <strong>💡 Pro Tip:</strong> Filter trades by higher timeframe trend. Only take longs if 15m is bullish!
                    </div>
                    
                    <div class="warning">
                        <strong>⚠️ Risk Warning:</strong> Whipsaws kill this strategy in ranging markets. Check ADX > 25 for trend strength.
                    </div>
                `
            },
            orderflow: {
                title: 'Order Flow Imbalance Strategy',
                content: `
                    <h3>🌊 Order Flow - The Institutional Edge</h3>
                    <p>Advanced strategy analyzing buying vs selling pressure. Used by prop traders and institutions.</p>
                    
                    <h3>Key Concepts</h3>
                    <ul>
                        <li><span class="highlight">Delta</span> = Buy volume - Sell volume</li>
                        <li><span class="highlight">CVD</span> = Cumulative Volume Delta (shows hidden demand/supply)</li>
                        <li><span class="highlight">Imbalance</span> = When one side overwhelms the other</li>
                    </ul>
                    
                    <h3>Entry Signals</h3>
                    <ul>
                       tive delta divergence (price drops but delta rises)</li>
                        <li><span class="highlight">Volume imbalance > 300%</span> buy vs sell</li>
               <li>Absorption: Large orders absorbed without price drop</li>
                      ed imbalances at price level (support forming)</li>
                    </ul>
                    
                    <h3>Exit Rules</h3>
                    <ul>
                  Exit when delta flips against position</li>
              <li>Take profit at previous high-volume nodes</li>
                        <li>Stop loss below absorption zone</li>
                    </ul>
                    
                    <div class="pro-tip">
                        ong>💡 Pro Tip:</strong> Combine with price action. Imbalance + break of structure = highty setup!
                    </div>
                 
                    <div class="warning">
                        <strong>⚠️ Risk Warning:</strong> Requires real order flow data. This simulation approximates the concept. Real trading needs proper tools.
                 iv>
                            };
 
        // DOM Elements
        const elements = {
            balance: document.getElementById('balance'),
            sessionPnl: document.getElementById('sessionPnl'),
            document.getElementById('winRate'),
            currentPrice: document.getElementById('currentPrice'),
            priceChange: document.getEle('priceChange'),
      hartCanvas:ocument.getElementById('chartCanvas'),
           siValue: document.getById('rsiValue'),
            macdValue: document.getElementById('macdValue'),
  Value: dment.getElementById('bbVa,
            emaValue: document.getElementById(alue        voalue: document.getElementBalue'),
            signalArrow: document.getElementById('signalArrow            signalText: document.getElemId('signalText'),
         signalConfidence: document.getElementById('signalConfidence'),
            s: document.getElementById('signalReasons')          buyBtn: document.getElementById('buyBtn'),
            selocument.gtById('sellBtn'),
  closeTradeBtn: document.getElementById('closeTradeBtn'),
           Trade: docuementById('activeTrade'),
       Type: docu.getElementById(pe'),
            tradePnl: documt.getElementById('tradePnl'),
            entryPrice: document.getElementById('),
            tradeSize: ent.getElemed('tradeSize'),
         totalTradest.getElementById('totalT         winTrades: documentElemenrades'),
            lossTrent.getElementById('ssTrades')         aPnl: dument.getElementById('a        yLisent.getElementById('historyList,
            positionSize: document.gementByISize'),
    pairSct: document.getElementById('pairSel),
       e documentlementById),
