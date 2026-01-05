+    1 <!DOCTYPE html>
+    2 <html lang="en">
+    3 <head>
+    4     <meta charset="UTF-8">
+    5     <meta name="viewport" content="width=device-width, initial-scale=1.0">
+    6     <title>APEX SCALPER PRO | AI Trading Simulator</title>
+    7     <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
+    8     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
+    9     <style>
+   10         :root {
+   11             --bg-primary: #0a0e17;
+   12             --bg-secondary: #111827;
+   13             --bg-tertiary: #1a2235;
+   14             --accent-cyan: #00f0ff;
+   15             --accent-magenta: #ff00aa;
+   16             --accent-gold: #ffd700;
+   17             --profit-green: #00ff88;
+   18             --loss-red: #ff3366;
+   19             --text-primary: #e8f0ff;
+   20             --text-secondary: #8892a8;
+   21             --border-glow: rgba(0, 240, 255, 0.3);
+   22         }
+   23 
+   24         * {
+   25             margin: 0;
+   26             padding: 0;
+   27             box-sizing: border-box;
+   28         }
+   29 
+   30         body {
+   31             font-family: 'Rajdhani', sans-serif;
+   32             background: var(--bg-primary);
+   33             color: var(--text-primary);
+   34             min-height: 100vh;
+   35             overflow-x: hidden;
+   36         }
+   37 
+   38         /* Animated Background */
+   39         .bg-grid {
+   40             position: fixed;
+   41             top: 0;
+   42             left: 0;
+   43             width: 100%;
+   44             height: 100%;
+   45             background-image: 
+   46                 linear-gradient(rgba(0, 240, 255, 0.03) 1px, transparent 1px),
+   47                 linear-gradient(90deg, rgba(0, 240, 255, 0.03) 1px, transparent 1px);
+   48             background-size: 50px 50px;
+   49             pointer-events: none;
+   50             z-index: 0;
+   51         }
+   52 
+   53         .bg-glow {
+   54             position: fixed;
+   55             width: 600px;
+   56             height: 600px;
+   57             border-radius: 50%;
+   58             filter: blur(150px);
+   59             opacity: 0.15;
+   60             pointer-events: none;
+   61             z-index: 0;
+   62         }
+   63 
+   64         .glow-1 {
+   65             top: -200px;
+   66             right: -200px;
+   67             background: var(--accent-cyan);
+   68             animation: pulse 8s ease-in-out infinite;
+   69         }
+   70 
+   71         .glow-2 {
+   72             bottom: -200px;
+   73             left: -200px;
+   74             background: var(--accent-magenta);
+   75             animation: pulse 8s ease-in-out infinite 4s;
+   76         }
+   77 
+   78         @keyframes pulse {
+   79             0%, 100% { opacity: 0.1; transform: scale(1); }
+   80             50% { opacity: 0.2; transform: scale(1.1); }
+   81         }
+   82 
+   83         /* Header */
+   84         .header {
+   85             position: relative;
+   86             z-index: 10;
+   87             padding: 15px 20px;
+   88             background: linear-gradient(180deg, rgba(17, 24, 39, 0.95) 0%, transparent 100%);
+   89             border-bottom: 1px solid var(--border-glow);
+   90             display: flex;
+   91             justify-content: space-between;
+   92             align-items: center;
+   93             flex-wrap: wrap;
+   94             gap: 10px;
+   95         }
+   96 
+   97         .logo {
+   98             display: flex;
+   99             align-items: center;
+  100             gap: 12px;
+  101         }
+  102 
+  103         .logo-icon {
+  104             width: 45px;
+  105             height: 45px;
+  106             background: linear-gradient(135deg, var(--accent-cyan), var(--accent-magenta));
+  107             border-radius: 12px;
+  108             display: flex;
+  109             align-items: center;
+  110             justify-content: center;
+  111             font-size: 20px;
+  112             animation: logoGlow 3s ease-in-out infinite;
+  113         }
+  114 
+  115         @keyframes logoGlow {
+  116             0%, 100% { box-shadow: 0 0 20px rgba(0, 240, 255, 0.5); }
+  117             50% { box-shadow: 0 0 40px rgba(255, 0, 170, 0.5); }
+  118         }
+  119 
+  120         .logo-text {
+  121             font-family: 'Orbitron', monospace;
+  122             font-size: 1.4rem;
+  123             font-weight: 900;
+  124             background: linear-gradient(90deg, var(--accent-cyan), var(--accent-magenta));
+  125             -webkit-background-clip: text;
+  126             -webkit-text-fill-color: transparent;
+  127             background-clip: text;
+  128         }
+  129 
+  130         .logo-sub {
+  131             font-size: 0.65rem;
+  132             color: var(--text-secondary);
+  133             letter-spacing: 3px;
+  134             text-transform: uppercase;
+  135         }
+  136 
+  137         .balance-display {
+  138             display: flex;
+  139             align-items: center;
+  140             gap: 20px;
+  141             flex-wrap: wrap;
+  142         }
+  143 
+  144         .balance-item {
+  145             text-align: right;
+  146         }
+  147 
+  148         .balance-label {
+  149             font-size: 0.7rem;
+  150             color: var(--text-secondary);
+  151             text-transform: uppercase;
+  152             letter-spacing: 1px;
+  153         }
+  154 
+  155         .balance-value {
+  156             font-family: 'JetBrains Mono', monospace;
+  157             font-size: 1.3rem;
+  158             font-weight: 700;
+  159         }
+  160 
+  161         .balance-value.profit { color: var(--profit-green); }
+  162         .balance-value.loss { color: var(--loss-red); }
+  163 
+  164         /* Main Container */
+  165         .main-container {
+  166             position: relative;
+  167             z-index: 10;
+  168             display: grid;
+  169             grid-template-columns: 1fr 320px;
+  170             gap: 15px;
+  171             padding: 15px;
+  172             max-width: 1600px;
+  173             margin: 0 auto;
+  174         }
+  175 
+  176         @media (max-width: 1024px) {
+  177             .main-container {
+  178                 grid-template-columns: 1fr;
+  179             }
+  180         }
+  181 
+  182         /* Chart Container */
+  183         .chart-container {
+  184             background: var(--bg-secondary);
+  185             border-radius: 16px;
+  186             border: 1px solid var(--border-glow);
+  187             overflow: hidden;
+  188         }
+  189 
+  190         .chart-header {
+  191             display: flex;
+  192             justify-content: space-between;
+  193             align-items: center;
+  194             padding: 12px 16px;
+  195             background: var(--bg-tertiary);
+  196             border-bottom: 1px solid rgba(255,255,255,0.05);
+  197             flex-wrap: wrap;
+  198             gap: 10px;
+  199         }
+  200 
+  201         .pair-selector {
+  202             display: flex;
+  203             align-items: center;
+  204             gap: 10px;
+  205         }
+  206 
+  207         .pair-name {
+  208             font-family: 'Orbitron', monospace;
+  209             font-size: 1.1rem;
+  210             font-weight: 700;
+  211             color: var(--accent-cyan);
+  212         }
+  213 
+  214         .pair-price {
+  215             font-family: 'JetBrains Mono', monospace;
+  216             font-size: 1.2rem;
+  217         }
+  218 
+  219         .price-change {
+  220             font-size: 0.85rem;
+  221             padding: 3px 8px;
+  222             border-radius: 6px;
+  223         }
+  224 
+  225         .price-change.up {
+  226             background: rgba(0, 255, 136, 0.15);
+  227             color: var(--profit-green);
+  228         }
+  229 
+  230         .price-change.down {
+  231             background: rgba(255, 51, 102, 0.15);
+  232             color: var(--loss-red);
+  233         }
+  234 
+  235         .timeframe-selector {
+  236             display: flex;
+  237             gap: 5px;
+  238         }
+  239 
+  240         .tf-btn {
+  241             padding: 6px 12px;
+  242             background: transparent;
+  243             border: 1px solid rgba(255,255,255,0.1);
+  244             border-radius: 6px;
+  245             color: var(--text-secondary);
+  246             font-family: 'Rajdhani', sans-serif;
+  247             font-size: 0.85rem;
+  248             font-weight: 600;
+  249             cursor: pointer;
+  250             transition: all 0.3s;
+  251         }
+  252 
+  253         .tf-btn:hover, .tf-btn.active {
+  254             background: var(--accent-cyan);
+  255             color: var(--bg-primary);
+  256             border-color: var(--accent-cyan);
+  257         }
+  258 
+  259         .chart-canvas-container {
+  260             position: relative;
+  261             height: 400px;
+  262         }
+  263 
+  264         #chartCanvas {
+  265             width: 100%;
+  266             height: 100%;
+  267         }
+  268 
+  269         /* Indicators Panel */
+  270         .indicators-bar {
+  271             display: flex;
+  272             gap: 15px;
+  273             padding: 10px 16px;
+  274             background: rgba(0,0,0,0.3);
+  275             border-top: 1px solid rgba(255,255,255,0.05);
+  276             overflow-x: auto;
+  277             flex-wrap: wrap;
+  278         }
+  279 
+  280         .indicator-chip {
+  281             display: flex;
+  282             align-items: center;
+  283             gap: 8px;
+  284             padding: 6px 12px;
+  285             background: var(--bg-tertiary);
+  286             border-radius: 20px;
+  287             font-size: 0.75rem;
+  288             white-space: nowrap;
+  289         }
+  290 
+  291         .indicator-dot {
+  292             width: 8px;
+  293             height: 8px;
+  294             border-radius: 50%;
+  295         }
+  296 
+  297         .indicator-value {
+  298             font-family: 'JetBrains Mono', monospace;
+  299             font-weight: 600;
+  300         }
+  301 
+  302         /* Trading Panel */
+  303         .trading-panel {
+  304             display: flex;
+  305             flex-direction: column;
+  306             gap: 15px;
+  307         }
+  308 
+  309         .panel-card {
+  310             background: var(--bg-secondary);
+  311             border-radius: 16px;
+  312             border: 1px solid var(--border-glow);
+  313             overflow: hidden;
+  314         }
+  315 
+  316         .panel-header {
+  317             display: flex;
+  318             align-items: center;
+  319             gap: 10px;
+  320             padding: 12px 16px;
+  321             background: var(--bg-tertiary);
+  322             border-bottom: 1px solid rgba(255,255,255,0.05);
+  323         }
+  324 
+  325         .panel-icon {
+  326             width: 32px;
+  327             height: 32px;
+  328             border-radius: 8px;
+  329             display: flex;
+  330             align-items: center;
+  331             justify-content: center;
+  332             font-size: 14px;
+  333         }
+  334 
+  335         .panel-title {
+  336             font-family: 'Orbitron', monospace;
+  337             font-size: 0.85rem;
+  338             font-weight: 700;
+  339             letter-spacing: 1px;
+  340         }
+  341 
+  342         .panel-content {
+  343             padding: 16px;
+  344         }
+  345 
+  346         /* AI Signal Card */
+  347         .ai-signal-card .panel-icon {
+  348             background: linear-gradient(135deg, var(--accent-magenta), var(--accent-cyan));
+  349         }
+  350 
+  351         .signal-main {
+  352             display: flex;
+  353             align-items: center;
+  354             justify-content: space-between;
+  355             margin-bottom: 15px;
+  356         }
+  357 
+  358         .signal-direction {
+  359             display: flex;
+  360             align-items: center;
+  361             gap: 10px;
+  362         }
+  363 
+  364         .signal-arrow {
+  365             width: 50px;
+  366             height: 50px;
+  367             border-radius: 12px;
+  368             display: flex;
+  369             align-items: center;
+  370             justify-content: center;
+  371             font-size: 24px;
+  372         }
+  373 
+  374         .signal-arrow.buy {
+  375             background: linear-gradient(135deg, rgba(0, 255, 136, 0.2), rgba(0, 255, 136, 0.05));
+  376             color: var(--profit-green);
+  377          animation: signalPulse 2s ease-in-out infinite;
+  378         }
+  379 
+  380         .signal-arrow.sell {
+  381             background: linear-gradient(135deg, rgba(255, 51, 102, 0.2), rgba(255, 51, 102, 0.05));
+  382             color: var(--loss-red);
+  383             animation: signalPulse 2s ease-in-out infinite;
+  384         }
+  385 
+  386         .signal-arrow.neutral {
+  387             background: rgba(255, 215, 0, 0.15);
+  388             color: var(--accent-gold);
+  389         }
+  390 
+  391         @keyframes signalPulse {
+  392             0%, 100% { box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.4); }
+  393             50% { box-shadow: 0 0 20px 5px rgba(0, 255, 136, 0.1); }
+  394         }
+  395 
+  396         .signal-text {
+  397             font-family: 'Orbitron', monospace;
+  398             font-size: 1.2rem;
+  399             font-weight: 700;
+  400         }
+  401 
+  402         .signal-confidence {
+  403             text-align: right;
+  404         }
+  405 
+  406         .confidence-label {
+  407             font-size: 0.7rem;
+  408             color: var(--text-secondary);
+  409             text-transform: uppercase;
+  410         }
+  411 
+  412         .confidence-value {
+  413             font-family: 'JetBrains Mono', monospace;
+  414             font-size: 1.4rem;
+  415             font-weight: 700;
+  416             color: var(--accent-cyan);
+  417         }
+  418 
+  419         .signal-reasons {
+  420             display: flex;
+  421             flex-direction: column;
+  422             gap: 8px;
+  423         }
+  424 
+  425         .reason-item {
+  426             display: flex;
+  427             align-items: center;
+  428             gap: 8px;
+  429             padding: 8px 12px;
+  430             background: rgba(0,0,0,0.3);
+  431             border-radius: 8px;
+  432             font-size: 0.8rem;
+  433         }
+  434 
+  435         .reason-icon {
+  436             color: var(--accent-cyan);
+  437         }
+  438 
+  439         /* Trade Execution */
+  440         .trade-card .panel-icon {
+  441             background: linear-gradient(135deg, var(--profit-green), #00aa55);
+  442         }
+  443 
+  444         .trade-inputs {
+  445             display: flex;
+  446             flex-direction: column;
+  447             gap: 12px;
+  448         }
+  449 
+  450         .input-group {
+  451             display: flex;
+  452             flex-direction: column;
+  453             gap: 5px;
+  454         }
+  455 
+  456         .input-label {
+  457             font-size: 0.75rem;
+  458             color: var(--text-secondary);
+  459             text-transform: uppercase;
+  460             letter-spacing: 1px;
+  461         }
+  462 
+  463         .input-field {
+  464             display: flex;
+  465             align-items: center;
+  466             background: var(--bg-tertiary);
+  467             border: 1px solid rgba(255,255,255,0.1);
+  468             border-radius: 10px;
+  469             overflow: hidden;
+  470         }
+  471 
+  472         .input-field input {
+  473             flex: 1;
+  474             padding: 12px;
+  475             background: transparent;
+  476             border: none;
+  477             color: var(--text-primary);
+  478             font-family: 'JetBrains Mono', monospace;
+  479             font-size: 1rem;
+  480             outline: none;
+  481         }
+  482 
+  483         .input-field input::placeholder {
+  484             color: var(--text-secondary);
+  485         }
+  486 
+  487         .input-suffix {
+  488             padding: 12px;
+  489             color: var(--text-secondary);
+  490             font-size: 0.85rem;
+  491             background: rgba(0,0,0,0.2);
+  492         }
+  493 
+  494         .leverage-selector {
+  495             display: flex;
+  496             gap: 5px;
+  497         }
+  498 
+  499         .lev-btn {
+  500             flex: 1;
+  501             padding: 10px;
+  502             background: var(--bg-tertiary);
+  503             border: 1px solid rgba(255,255,255,0.1);
+  504             border-radius: 8px;
+  505             color: var(--text-secondary);
+  506             font-family: 'Rajdhani', sans-serif;
+  507             font-weight: 600;
+  508             cursor: pointer;
+  509             transition: all 0.3s;
+  510         }
+  511 
+  512         .lev-btn:hover, .lev-btn.active {
+  513             background: var(--accent-cyan);
+  514             color: var(--bg-primary);
+  515             border-color: var(--accent-cyan);
+  516         }
+  517 
+  518         .trade-buttons {
+  519             display: grid;
+  520             grid-template-columns: 1fr 1fr;
+  521             gap: 10px;
+  522             margin-top: 10px;
+  523         }
+  524 
+  525         .trade-btn {
+  526             padding: 14px;
+  527             border: none;
+  528             border-radius: 10px;
+  529             font-family: 'Orbitron', monospace;
+  530             font-size: 0.9rem;
+  531             font-weight: 700;
+  532             cursor: pointer;
+  533             transition: all 0.3s;
+  534             display: flex;
+  535             align-items: center;
+  536             justify-content: center;
+  537             gap: 8px;
+  538         }
+  539 
+  540         .trade-btn.buy {
+  541             background: linear-gradient(135deg, var(--profit-green), #00aa55);
+  542             color: #000;
+  543         }
+  544 
+  545         .trade-btn.sell {
+  546             background: linear-gradient(135deg, var(--loss-red), #cc0033);
+  547             color: #fff;
+  548         }
+  549 
+  550         .trade-btn:hover {
+  551             transform: translateY(-2px);
+  552             box-shadow: 0 10px 30px rgba(0,0,0,0.3);
+  553         }
+  554 
+  555         .trade-btn:disabled {
+  556             opacity: 0.5;
+  557             cursor: not-allowed;
+  558             transform: none;
+  559         }
+  560 
+  561         /* Active Trade */
+  562         .active-trade {
+  563             margin-top: 15px;
+  564             padding: 15px;
+  565             background: var(--bg-tertiary);
+  566             border-radius: 12px;
+  567             border: 1px solid rgba(255,255,255,0.1);
+  568             display: none;
+  569         }
+  570 
+  571         .active-trade.visible {
+  572             display: block;
+  573             animation: slideIn 0.3s ease;
+  574         }
+  575 
+  576         @keyframes slideIn {
+  577             from { opacity: 0; transform: translateY(-10px); }
+  578             to { opacity: 1; transform: translateY(0); }
+  579         }
+  580 
+  581         .trade-info {
+  582             display: flex;
+  583             justify-content: space-between;
+  584             margin-bottom: 12px;
+  585         }
+  586 
+  587         .trade-type {
+  588             font-weight: 700;
+  589             font-size: 0.9rem;
+  590         }
+  591 
+  592         .trade-type.long { color: var(--profit-green); }
+  593         .trade-type.short { color: var(--loss-red); }
+  594 
+  595         .trade-pnl {
+  596             font-family: 'JetBrains Mono', monospace;
+  597             font-weight: 700;
+  598         }
+  599 
+  600         .close-trade-btn {
+  601             width: 100%;
+  602             padding: 10px;
+  603             background: rgba(255,255,255,0.1);
+  604             border: 1px solid rgba(255,255,255,0.2);
+  605             border-radius: 8px;
+  606             color: var(--text-primary);
+  607             font-family: 'Rajdhani', sans-serif;
+  608             font-weight: 600;
+  609             cursor: pointer;
+  610             transition: all 0.3s;
+  611         }
+  612 
+  613         .close-trade-btn:hover {
+  614             background: var(--loss-red);
+  615             border-color: var(--loss-red);
+  616         }
+  617 
+  618         /* Strategy Guide */
+  619         .strategy-card .panel-icon {
+  620             background: linear-gradient(135deg, var(--accent-gold), #ff8800);
+  621         }
+  622 
+  623         .strategy-list {
+  624             display: flex;
+  625             flex-direction: column;
+  626             gap: 10px;
+  627         }
+  628 
+  629         .strategy-item {
+  630             padding: 12px;
+  631             background: var(--bg-tertiary);
+  632             border-radius: 10px;
+  633             border-left: 3px solid var(--accent-cyan);
+  634             cursor: pointer;
+  635             transition: all 0.3s;
+  636         }
+  637 
+  638         .strategy-item:hover {
+  639             background: rgba(0, 240, 255, 0.1);
+  640         }
+  641 
+  642         .strategy-item.active {
+  643             border-left-color: var(--accent-gold);
+  644             background: rgba(255, 215, 0, 0.1);
+  645         }
+  646 
+  647         .strategy-name {
+  648             font-weight: 600;
+  649             margin-bottom: 4px;
+  650             display: flex;
+  651             align-items: center;
+  652             gap: 8px;
+  653         }
+  654 
+  655         .strategy-badge {
+  656             font-size: 0.65rem;
+  657             padding: 2px 6px;
+  658             background: var(--accent-magenta);
+  659             border-radius: 4px;
+  660             color: #fff;
+  661         }
+  662 
+  663         .strategy-desc {
+  664             font-size: 0.75rem;
+  665             color: var(--text-secondary);
+  666         }
+  667 
+  668         /* Stats Panel */
+  669         .stats-grid {
+  670             display: grid;
+  671             grid-template-columns: 1fr 1fr;
+  672             gap: 10px;
+  673         }
+  674 
+  675         .stat-item {
+  676             padding: 12px;
+  677             background: var(--bg-tertiary);
+  678             border-radius: 10px;
+  679             text-align: center;
+  680         }
+  681 
+  682         .stat-value {
+  683             font-family: 'JetBrains Mono', monospace;
+  684             font-size: 1.1rem;
+  685             font-weight: 700;
+  686         }
+  687 
+  688         .stat-label {
+  689             font-size: 0.7rem;
+  690             color: var(--text-secondary);
+  691             text-transform: uppercase;
+  692             margin-top: 4px;
+  693         }
+  694 
+  695         /* Trade History */
+  696         .history-list {
+  697             max-height: 200px;
+  698             overflow-y: auto;
+  699         }
+  700 
+  701         .history-item {
+  702             display: flex;
+  703             justify-content: space-between;
+  704             align-items: center;
+  705             padding: 10px;
+  706             border-bottom: 1px solid rgba(255,255,255,0.05);
+  707         }
+  708 
+  709         .history-item:last-child {
+  710             border-bottom: none;
+  711         }
+  712 
+  713         .history-type {
+  714             font-size: 0.75rem;
+  715             font-weight: 600;
+  716             padding: 3px 8px;
+  717             border-radius: 4px;
+  718         }
+  719 
+  720         .history-type.long {
+  721             background: rgba(0, 255, 136, 0.15);
+  722             color: var(--profit-green);
+  723         }
+  724 
+  725         .history-type.short {
+  726             background: rgba(255, 51, 102, 0.15);
+  727             color: var(--loss-red);
+  728         }
+  729 
+  730         .history-pnl {
+  731             font-family: 'JetBrains Mono', monospace;
+  732             font-weight: 600;
+  733             font-size: 0.85rem;
+  734         }
+  735 
+  736         /* Education Modal */
+  737         .modal-overlay {
+  738             position: fixed;
+  739             top: 0;
+  740             left: 0;
+  741             width: 100%;
+  742             height: 100%;
+  743             background: rgba(0,0,0,0.8);
+  744             backdrop-filter: blur(10px);
+  745             z-index: 1000;
+  746             display: none;
+  747             align-items: center;
+  748             justify-content: center;
+  749             padding: 20px;
+  750         }
+  751 
+  752         .modal-overlay.visible {
+  753             display: flex;
+  754         }
+  755 
+  756         .modal-content {
+  757             background: var(--bg-secondary);
+  758             border-radius: 20px;
+  759             border: 1px solid var(--border-glow);
+  760             max-width: 600px;
+  761             width: 100%;
+  762             max-height: 80vh;
+  763             overflow-y: auto;
+  764             animation: modalIn 0.3s ease;
+  765         }
+  766 
+  767         @keyframes modalIn {
+  768             from { opacity: 0; transform: scale(0.9); }
+  769             to { opacity: 1; transform: scale(1); }
+  770         }
+  771 
+  772         .modal-header {
+  773             display: flex;
+  774             justify-content: space-between;
+  775             align-items: center;
+  776             padding: 20px;
+  777             background: var(--bg-tertiary);
+  778             border-bottom: 1px solid rgba(255,255,255,0.1);
+  779         }
+  780 
+  781         .modal-title {
+  782             font-family: 'Orbitron', monospace;
+  783             font-size: 1.2rem;
+  784             color: var(--accent-cyan);
+  785         }
+  786 
+  787         .modal-close {
+  788             width: 36px;
+  789             height: 36px;
+  790             border-radius: 50%;
+  791             background: rgba(255,255,255,0.1);
+  792             border: none;
+  793             color: var(--text-primary);
+  794             cursor: pointer;
+  795             display: flex;
+  796             align-items: center;
+  797             justify-content: center;
+  798             transition: all 0.3s;
+  799         }
+  800 
+  801         .modal-close:hover {
+  802             background: var(--loss-red);
+  803         }
+  804 
+  805         .modal-body {
+  806             padding: 20px;
+  807         }
+  808 
+  809         .lesson-content h3 {
+  810             color: var(--accent-gold);
+  811             margin-bottom: 15px;
+  812             font-family: 'Orbitron', monospace;
+  813         }
+  814 
+  815         .lesson-content p {
+  816             color: var(--text-secondary);
+  817             line-height: 1.7;
+  818             margin-bottom: 15px;
+  819         }
+  820 
+  821         .lesson-content ul {
+  822             margin-left: 20px;
+  823             margin-bottom: 15px;
+  824         }
+  825 
+  826         .lesson-content li {
+  827             color: var(--text-secondary);
+  828             margin-bottom: 8px;
+  829             line-height: 1.6;
+  830         }
+  831 
+  832         .lesson-content .highlight {
+  833             color: var(--accent-cyan);
+  834             font-weight: 600;
+  835         }
+  836 
+  837         .lesson-content .warning {
+  838             padding: 15px;
+  839             background: rgba(255, 51, 102, 0.1);
+  840             border-left: 3px solid var(--loss-red);
+  841             border-radius: 8px;
+  842             margin: 15px 0;
+  843         }
+  844 
+  845         .lesson-content .pro-tip {
+  846             padding: 15px;
+  847             background: rgba(0, 240, 255, 0.1);
+  848             border-left: 3px solid var(--accent-cyan);
+  849             border-radius: 8px;
+  850             margin: 15px 0;
+  851         }
+  852 
+  853         /* Toast Notifications */
+  854         .toast-container {
+  855             position: fixed;
+  856             top: 80px;
+  857             right: 20px;
+  858             z-index: 1001;
+  859             display: flex;
+  860             flex-direction: column;
+  861             gap: 10px;
+  862         }
+  863 
+  864         .toast {
+  865             padding: 15px 20px;
+  866             background: var(--bg-secondary);
+  867             border-radius: 12px;
+  868             border: 1px solid var(--border-glow);
+  869             display: flex;
+  870             align-items: center;
+  871             gap: 12px;
+  872             animation: toastIn 0.3s ease;
+  873             max-width: 350px;
+  874         }
+  875 
+  876         @keyframes toastIn {
+  877             from { opacity: 0; transform: translateX(100px); }
+  878             to { opacity: 1; transform: translateX(0); }
+  879         }
+  880 
+  881         .toast.success { border-left: 4px solid var(--profit-green); }
+  882         .toast.error { border-left: 4px solid var(--loss-red); }
+  883         .toast.info { border-left: 4px solid var(--accent-cyan); }
+  884 
+  885         .toast-icon {
+  886             font-size: 1.2rem;
+  887         }
+  888 
+  889         .toast.success .toast-icon { color: var(--profit-green); }
+  890         .toast.error .toast-icon { color: var(--loss-red); }
+  891         .toast.info .toast-icon { color: var(--accent-cyan); }
+  892 
+  893         .toast-message {
+  894             flex: 1;
+  895             font-size: 0.9rem;
+  896         }
+  897 
+  898         /* Disclaimer Banner */
+  899         .disclaimer-banner {
+  900             background: linear-gradient(90deg, rgba(255, 215, 0, 0.1), rgba(255, 0, 170, 0.1));
+  901             padding: 10px 20px;
+  902             text-align: center;
+  903             font-size: 0.8rem;
+  904             color: var(--accent-gold);
+  905             border-bottom: 1px solid rgba(255, 215, 0, 0.2);
+  906         }
+  907 
+  908         .disclaimer-banner i {
+  909             margin-right: 8px;
+  910         }
+  911 
+  912         /* Scrollbar */
+  913         ::-webkit-scrollbar {
+  914             width: 6px;
+  915             height: 6px;
+  916         }
+  917 
+  918         ::-webkit-scrollbar-track {
+  919             background: var(--bg-tertiary);
+  920         }
+  921 
+  922         ::-webkit-scrollbar-thumb {
+  923             background: var(--accent-cyan);
+  924             border-radius: 3px;
+  925         }
+  926 
+  927         /* Mobile Responsive */
+  928         @media (max-width: 768px) {
+  929             .header {
+  930                 flex-direction: column;
+  931                 text-align: center;
+  932             }
+  933 
+  934             .balance-display {
+  935                 justify-content: center;
+  936             }
+  937 
+  938             .chart-canvas-container {
+  939                 height: 300px;
+  940             }
+  941 
+  942             .main-container {
+  943                 padding: 10px;
+  944             }
+  945 
+  946             .trade-buttons {
+  947                 grid-template-columns: 1fr;
+  948             }
+  949 
+  950             .stats-grid {
+  951                 grid-template-columns: 1fr;
+  952             }
+  953         }
+  954     </style>
+  955 </head>
+  956 <body>
+  957     <div class="bg-grid"></div>
+  958     <div class="bg-glow glow-1"></div>
+  959     <div class="bg-glow glow-2"></div>
+  960 
+  961     <div class="disclaimer-banner">
+  962         <i class="fas fa-graduation-cap"></i>
+  963         SIMULATION MODE — Practice with virtual funds. No real money involved. Learn before you trade!
+  964     </div>
+  965 
+  966     <header class="header">
+  967         <div class="logo">
+  968             <div class="logo-icon">
+  969                 <i class="fas fa-bolt"></i>
+  970             </div>
+  971             <div>
+  972                 <div class="logo-text">APEX SCALPER</div>
+  973                 <div class="logo-sub">AI Trading Simulator</div>
+  974             </div>
+  975         </div>
+  976         <div class="balance-display">
+  977             <div class="balance-item">
+  978                 <div class="balance-label">Virtual Balance</div>
+  979                 <div class="balance-value" id="balance">$10.00</div>
+  980             </div>
+  981             <div class="balance-item">
+  982                 <div class="balance-label">Session P&L</div>
+  983                 <div class="balance-value profit" id="sessionPnl">+$0.00</div>
+  984             </div>
+  985             <div class="balance-item">
+  986                 <div class="balance-label">Win Rate</div>
+  987                 <div class="balance-value" id="winRate" style="color: var(--accent-cyan)">0%</div>
+  988             </div>
+  989         </div>
+  990     </header>
+  991 
+  992     <main class="main-container">
+  993         <div class="chart-section">
+  994             <div class="chart-container">
+  995                 <div class="chart-header">
+  996                     <div class="pair-selector">
+  997                         <select id="pairSelect" style="background: var(--bg-tertiary); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 8px 12px; color: var(--text-primary); font-family: 'Orbitron', monospace; cursor: pointer;">
+  998                             <option value="BTC/USDT">BTC/USDT</option>
+  999                             <option value="ETH/USDT">ETH/USDT</option>
+ 1000                             <option value="SOL/USDT">SOL/USDT</option>
+ 1001                             <option value="XRP/USDT">XRP/USDT</option>
+ 1002                         </select>
+ 1003                         <span class="pair-price" id="currentPrice">$94,521.34</span>
+ 1004                         <span class="price-change up" id="priceChange">+0.42%</span>
+ 1005                     </div>
+ 1006                     <div class="timeframe-selector">
+ 1007                         <button class="tf-btn active" data-tf="1">1m</button>
+ 1008                         <button class="tf-btn" data-tf="5">5m</button>
+ 1009                         <button class="tf-btn" data-tf="15">15m</button>
+ 1010                     </div>
+ 1011                 </div>
+ 1012                 <div class="chart-canvas-container">
+ 1013                     <canvas id="chartCanvas"></canvas>
+ 1014                 </div>
+ 1015                 <div class="indicators-bar">
+ 1016                     <div class="indicator-chip">
+ 1017                         <div class="indicator-dot" style="background: #ff6384;"></div>
+ 1018                         <span>RSI(14)</span>
+ 1019                         <span class="indicator-value" id="rsiValue">52.4</span>
+ 1020                     </div>
+ 1021                     <div class="indicator-chip">
+ 1022                         <div class="indicator-dot" style="background: #36a2eb;"></div>
+ 1023                         <span>MACD</span>
+ 1024                         <span class="indicator-value" id="macdValue">+12.5</span>
+ 1025                     </div>
+ 1026                     <div class="indicator-chip">
+ 1027                         <div class="indicator-dot" style="background: #ffce56;"></div>
+ 1028                         <span>BB Width</span>
+ 1029                         <span class="indicator-value" id="bbValue">1.8%</span>
+ 1030                     </div>
+ 1031                     <div class="indicator-chip">
+ 1032                         <div class="indicator-dot" style="background: #4bc0c0;"></div>
+ 1033                         <span>EMA Cross</span>
+ 1034                         <span class="indicator-value" id="emaValue">BULL</span>
+ 1035                     </div>
+ 1036                     <div class="indicator-chip">
+ 1037                         <div class="indicator-dot" style="background: #9966ff;"></div>
+ 1038                         <span>Volume</span>
+ 1039                         <span class="indicator-value" id="volValue">HIGH</span>
+ 1040                     </div>
+ 1041                 </div>
+ 1042             </div>
+ 1043         </div>
+ 1044 
+ 1045         <div class="trading-panel">
+ 1046             <!-- AI Signal Card -->
+ 1047             <div class="panel-card ai-signal-card">
+ 1048                 <div class="panel-header">
+ 1049                     <div class="panel-icon">
+ 1050                         <i class="fas fa-brain"></i>
+ 1051                     </div>
+ 1052                     <div class="panel-title">AI SIGNAL ENGINE</div>
+ 1053                 </div>
+ 1054                 <div class="panel-content">
+ 1055                     <div class="signal-main">
+ 1056                         <div class="signal-direction">
+ 1057                             <div class="signal-arrow neutral" id="signalArrow">
+ 1058                                 <i class="fas fa-minus"></i>
+ 1059                             </div>
+ 1060                             <div class="signal-text" id="signalText">ANALYZING...</div>
+ 1061                         </div>
+ 1062                         <div class="signal-confidence">
+ 1063                             <div class="confidence-label">Confidence</div>
+ 1064                             <div class="confidence-value" id="signalConfidence">--</div>
+ 1065                         </div>
+ 1066                     </div>
+ 1067                     <div class="signal-reasons" id="signalReasons">
+ 1068                         <div class="reason-item">
+ 1069                             <i class="fas fa-spinner fa-spin reason-icon"></i>
+ 1070                             <span>Analyzing market structure...</span>
+ 1071                         </div>
+ 1072                     </div>
+ 1073                 </div>
+ 1074             </div>
+ 1075 
+ 1076             <!-- Trade Execution -->
+ 1077             <div class="panel-card trade-card">
+ 1078                 <div class="panel-header">
+ 1079                     <div class="panel-icon">
+ 1080                         <i class="fas fa-exchange-alt"></i>
+ 1081                     </div>
+ 1082                     <div class="panel-title">EXECUTE TRADE</div>
+ 1083                 </div>
+ 1084                 <div class="panel-content">
+ 1085                     <div class="trade-inputs">
+ 1086                         <div class="input-group">
+ 1087                             <div class="input-label">Position Size</div>
+ 1088                             <div class="input-field">
+ 1089                                 <input type="number" id="positionSize" value="1" min="0.1" max="10" step="0.1">
+ 1090                                 <span class="input-suffix">USD</span>
+ 1091                             </div>
+ 1092                         </div>
+ 1093                         <div class="input-group">
+ 1094                             <div class="input-label">Leverage</div>
+ 1095                             <div class="leverage-selector">
+ 1096                                 <button class="lev-btn" data-lev="1">1x</button>
+ 1097                                 <button class="lev-btn" data-lev="5">5x</button>
+ 1098                                 <button class="lev-btn active" data-lev="10">10x</button>
+ 1099                                 <button class="lev-btn" data-lev="20">20x</button>
+ 1100                             </div>
+ 1101                         </div>
+ 1102                         <div class="trade-buttons">
+ 1103                             <button class="trade-btn buy" id="buyBtn">
+ 1104                                 <i class="fas fa-arrow-up"></i> LONG
+ 1105                             </button>
+ 1106                             <button class="trade-btn sell" id="sellBtn">
+ 1107                                 <i class="fas fa-arrow-down"></i> SHORT
+ 1108                             </button>
+ 1109                         </div>
+ 1110                     </div>
+ 1111                     <div class="active-trade" id="activeTrade">
+ 1112                         <div class="trade-info">
+ 1113                             <span class="trade-type" id="tradeType">LONG</span>
+ 1114                             <span class="trade-pnl" id="tradePnl">+$0.00</span>
+ 1115                         </div>
+ 1116                         <div class="trade-info">
+ 1117                             <span style="color: var(--text-secondary); font-size: 0.8rem;">Entry: <span id="entryPrice">$0</span></span>
+ 1118                             <span style="color: var(--text-secondary); font-size: 0.8rem;">Size: <span id="tradeSize">$0</span></span>
+ 1119                         </div>
+ 1120                         <button class="close-trade-btn" id="closeTradeBtn">
+ 1121                             <i class="fas fa-times"></i> Close Position
+ 1122                         </button>
+ 1123                     </div>
+ 1124                 </div>
+ 1125             </div>
+ 1126 
+ 1127             <!-- Strategies -->
+ 1128             <div class="panel-card strategy-card">
+ 1129                 <div class="panel-header">
+ 1130                     <div class="panel-icon">
+ 1131                         <i class="fas fa-lightbulb"></i>
+ 1132                     </div>
+ 1133                     <div class="panel-title">SCALPING STRATEGIES</div>
+ 1134                 </div>
+ 1135                 <div class="panel-content">
+ 1136                     <div class="strategy-list">
+ 1137                         <div class="strategy-item active" data-strategy="momentum">
+ 1138                             <div class="strategy-name">
+ 1139                                 <i class="fas fa-rocket"></i>
+ 1140                                 Momentum Breakout
+ 1141                                 <span class="strategy-badge">HOT</span>
+ 1142                             </div>
+ 1143                             <div class="strategy-desc">RSI + Volume spike confirmation</div>
+ 1144                         </div>
+ 1145                         <div class="strategy-item" data-strategy="reversal">
+ 1146                             <div class="strategy-name">
+ 1147                                 <i class="fas fa-sync-alt"></i>
+ 1148                                 Mean Reversion
+ 1149                             </div>
+ 1150                             <div class="strategy-desc">Bollinger Band bounce strategy</div>
+ 1151                         </div>
+ 1152                         <div class="strategy-item" data-strategy="ema">
+ 1153                             <div class="strategy-name">
+ 1154                                 <i class="fas fa-chart-line"></i>
+ 1155                                 EMA Crossover
+ 1156                             </div>
+ 1157                             <div class="strategy-desc">9/21 EMA trend following</div>
+ 1158                         </div>
+ 1159                         <div class="strategy-item" data-strategy="orderflow">
+ 1160                             <div class="strategy-name">
+ 1161                                 <i class="fas fa-stream"></i>
+ 1162                                 Order Flow Imbalance
+ 1163                                 <span class="strategy-badge">PRO</span>
+ 1164                             </div>
+ 1165                             <div class="strategy-desc">Volume delta analysis</div>
+ 1166                         </div>
+ 1167                     </div>
+ 1168                 </div>
+ 1169             </div>
+ 1170 
+ 1171             <!-- Stats -->
+ 1172             <div class="panel-card">
+ 1173                 <div class="panel-header">
+ 1174                     <div class="panel-icon" style="background: linear-gradient(135deg, #9966ff, #6633cc);">
+ 1175                         <i class="fas fa-chart-pie"></i>
+ 1176                     </div>
+ 1177                     <div class="panel-title">SESSION STATS</div>
+ 1178                 </div>
+ 1179                 <div class="panel-content">
+ 1180                     <div class="stats-grid">
+ 1181                         <div class="stat-item">
+ 1182                             <div class="stat-value" id="totalTrades">0</div>
+ 1183                             <div class="stat-label">Total Trades</div>
+ 1184                         </div>
+ 1185                         <div class="stat-item">
+ 1186                             <div class="stat-value" style="color: var(--profit-green);" id="winTrades">0</div>
+ 1187                             <div class="stat-label">Winning</div>
+ 1188                         </div>
+ 1189                         <div class="stat-item">
+ 1190                             <div class="stat-value" style="color: var(--loss-red);" id="lossTrades">0</div>
+ 1191                             <div class="stat-label">Losing</div>
+ 1192                         </div>
+ 1193                         <div class="stat-item">
+ 1194                             <div class="stat-value" id="avgPnl">$0.00</div>
+ 1195                             <div class="stat-label">Avg P&L</div>
+ 1196                         </div>
+ 1197                     </div>
+ 1198                     <div class="history-list" id="historyList" style="margin-top: 15px;">
+ 1199                         <!-- Trade history items will be added here -->
+ 1200                     </div>
+ 1201                 </div>
+ 1202             </div>
+ 1203         </div>
+ 1204     </main>
+ 1205 
+ 1206     <!-- Education Modal -->
+ 1207     <div class="modal-overlay" id="eduModal">
+ 1208         <div class="modal-content">
+ 1209             <div class="modal-header">
+ 1210                 <div class="modal-title" id="modalTitle">Strategy Guide</div>
+ 1211                 <button class="modal-close" id="modalClose">
+ 1212                     <i class="fas fa-times"></i>
+ 1213                 </button>
+ 1214             </div>
+ 1215             <div class="modal-body">
+ 1216                 <div class="lesson-content" id="lessonContent"></div>
+ 1217             </div>
+ 1218         </div>
+ 1219     </div>
+ 1220 
+ 1221     <!-- Toast Container -->
+ 1222     <div class="toast-container" id="toastContainer"></div>
+ 1223 
+ 1224     <script>
+ 1225         // ============================================
+ 1226         // APEX SCALPER PRO - AI Trading Simulator
+ 1227         // ============================================
+ 1228 
+ 1229         // State Management
+ 1230         const state = {
+ 1231             balance: 10.00,
+ 1232             sessionPnl: 0,
+ 1233             currentPrice: 94521.34,
+ 1234             currentPair: 'BTC/USDT',
+ 1235             timeframe: 1,
+ 1236             leverage: 10,
+ 1237             positionSize: 1,
+ 1238             activeTrade: null,
+ 1239             trades: [],
+ 1240             candles: [],
+ 1241             indicators: {
+ 1242                 rsi: 50,
+ 1243                 macd: 0,
+ 1244                 bbWidth: 1.5,
+ 1245                 ema9: 0,
+ 1246                 ema21: 0,
+ 1247                 volumeProfile: 'MEDIUM'
+ 1248             },
+ 1249             strategy: 'momentum',
+ 1250             priceHistory: []
+ 1251         };
+ 1252 
+ 1253         // Pair base prices
+ 1254         const pairPrices = {
+ 1255             'BTC/USDT': 94521.34,
+ 1256             'ETH/USDT': 3421.56,
+ 1257             'SOL/USDT': 187.34,
+ 1258             'XRP/USDT': 2.34
+ 1259         };
+ 1260 
+ 1261         // Strategy definitions
+ 1262         const strategies = {
+ 1263             momentum: {
+ 1264                 title: 'Momentum Breakout Strategy',
+ 1265                 content: `
+ 1266                     <h3>🚀 Momentum Breakout - The Scalper's Edge</h3>
+ 1267                     <p>This strategy captures explosive moves when price breaks through key levels with volume confirmation.</p>
+ 1268                     
+ 1269                     <h3>Entry Signals</h3>
+ 1270                     <ul>
+ 1271                         <li><span class="highlight">RSI crosses above 55</span> from below (bullish momentum building)</li>
+ 1272                         <li><span class="highlight">Volume spike > 150%</span> of 20-period average</li>
+ 1273                         <li>Price breaks above recent swing high</li>
+ 1274                         <li>MACD histogram turning positive</li>
+ 1275                     </ul>
+ 1276                     
+ 1277                     <h3>Exit Rules</h3>
+ 1278                     <ul>
+ 1279                         <li>Take profit at <span class="highlight">0.3-0.5%</span> move (scalping targets)</li>
+ 1280                         <li>Stop loss at <span class="highlight">0.2%</span> below entry</li>
+ 1281                         <li>Exit if RSI reaches 75+ (overbought)</li>
+ 1282                         <li>Trail stop after 0.2% profit</li>
+ 1283                     </ul>
+ 1284                     
+ 1285                     <div class="pro-tip">
+ 1286                         <strong>💡 Pro Tip:</strong> Best during high volatility sessions (US market open, major news). Avoid ranging markets!
+ 1287                     </div>
+ 1288                     
+ 1289                     <div class="warning">
+ 1290                         <strong>⚠️ Risk Warning:</strong> False breakouts are common. Always wait for volume confirmation before entering.
+ 1291                     </div>
+ 1292                 `
+ 1293             },
+ 1294             reversal: {
+ 1295                 title: 'Mean Reversion Strategy',
+ 1296                 content: `
+ 1297                     <h3>🔄 Mean Reversion - Fade the Extremes</h3>
+ 1298                     <p>This strategy profits from price returning to its average after extreme moves. Perfect for ranging markets.</p>
+ 1299                     
+ 1300                     <h3>Entry Signals</h3>
+ 1301                     <ul>
+ 1302                         <li>Price touches <span class="highlight">lower Bollinger Band</span> (for longs)</li>
+ 1303                         <li><span class="highlight">RSI below 30</span> (oversold territory)</li>
+ 1304                         <li>Bullish candlestick pattern (hammer, engulfing)</li>
+ 1305                         <li>Volume decreasing on the drop (exhaustion)</li>
+ 1306                     </ul>
+ 1307                     
+ 1308                     <h3>Exit Rules</h3>
+ 1309                     <ul>
+ 1310                         <li>Take profit at <span class="highlight">middle Bollinger Band</span></li>
+ 1311                         <li>Stop loss below recent low + buffer</li>
+ 1312                         <li>Time-based exit: 5-10 candles max hold</li>
+ 1313                     </ul>
+ 1314                     
+ 1315                     <div class="pro-tip">
+ 1316                         <strong>💡 Pro Tip:</strong> Works best when BB Width is contracting. Avoid during strong trends!
+ 1317                     </div>
+ 1318                     
+ 1319                     <div class="warning">
+ 1320                         <strong>⚠️ Risk Warning:</strong> "Catching falling knives" is dangerous. Wait for confirmation candle!
+ 1321                     </div>
+ 1322                 `
+ 1323             },
+ 1324             ema: {
+ 1325                 title: 'EMA Crossover Strategy',
+ 1326                 content: `
+ 1327                     <h3>📈 EMA Crossover - Ride the Trend</h3>
+ 1328                     <p>Classic trend-following strategy using fast and slow moving averages. Simple but effective.</p>
+ 1329                     
+ 1330                     <h3>Entry Signals</h3>
+ 1331                     <ul>
+ 1332                         <li><span class="highlight">9 EMA crosses above 21 EMA</span> (Golden cross = Long)</li>
+ 1333                         <li><span class="highlight">9 EMA crosses below 21 EMA</span> (Death cross = Short)</li>
+ 1334                         <li>Price above both EMAs for longs</li>
+ 1335                         <li>Wait for pullback to 9 EMA for better entry</li>
+ 1336                     </ul>
+ 1337                     
+ 1338                     <h3>Exit Rules</h3>
+ 1339                     <ul>
+ 1340                         <li>Exit when opposite crossover occurs</li>
+ 1341                         <li>Take partial profits at <span class="highlight">1:2 risk-reward</span></li>
+ 1342                         <li>Trail stop using the 9 EMA as dynamic support</li>
+ 1343                     </ul>
+ 1344                     
+ 1345                     <div class="pro-tip">
+ 1346                         <strong>💡 Pro Tip:</strong> Filter trades by higher timeframe trend. Only take longs if 15m is bullish!
+ 1347                     </div>
+ 1348                     
+ 1349                     <div class="warning">
+ 1350                         <strong>⚠️ Risk Warning:</strong> Whipsaws kill this strategy in ranging markets. Check ADX > 25 for trend strength.
+ 1351                     </div>
+ 1352                 `
+ 1353             },
+ 1354             orderflow: {
+ 1355                 title: 'Order Flow Imbalance Strategy',
+ 1356                 content: `
+ 1357                     <h3>🌊 Order Flow - The Institutional Edge</h3>
+ 1358                     <p>Advanced strategy analyzing buying vs selling pressure. Used by prop traders and institutions.</p>
+ 1359                     
+ 1360                     <h3>Key Concepts</h3>
+ 1361                     <ul>
+ 1362                         <li><span class="highlight">Delta</span> = Buy volume - Sell volume</li>
+ 1363                         <li><span class="highlight">CVD</span> = Cumulative Volume Delta (shows hidden demand/supply)</li>
+ 1364                         <li><span class="highlight">Imbalance</span> = When one side overwhelms the other</li>
+ 1365                     </ul>
+ 1366                     
+ 1367                     <h3>Entry Signals</h3>
+ 1368                     <ul>
+ 1369                        tive delta divergence (price drops but delta rises)</li>
+ 1370                         <li><span class="highlight">Volume imbalance > 300%</span> buy vs sell</li>
+ 1371                <li>Absorption: Large orders absorbed without price drop</li>
+ 1372                       ed imbalances at price level (support forming)</li>
+ 1373                     </ul>
+ 1374                     
+ 1375                     <h3>Exit Rules</h3>
+ 1376                     <ul>
+ 1377                   Exit when delta flips against position</li>
+ 1378               <li>Take profit at previous high-volume nodes</li>
+ 1379                         <li>Stop loss below absorption zone</li>
+ 1380                     </ul>
+ 1381                     
+ 1382                     <div class="pro-tip">
+ 1383                         ong>💡 Pro Tip:</strong> Combine with price action. Imbalance + break of structure = highty setup!
+ 1384                     </div>
+ 1385                  
+ 1386                     <div class="warning">
+ 1387                         <strong>⚠️ Risk Warning:</strong> Requires real order flow data. This simulation approximates the concept. Real trading needs proper tools.
+ 1388                  iv>
+ 1389                             };
+ 1390 
+ 1391         // DOM Elements
+ 1392         const elements = {
+ 1393             balance: document.getElementById('balance'),
+ 1394             sessionPnl: document.getElementById('sessionPnl'),
+ 1395             document.getElementById('winRate'),
+ 1396             currentPrice: document.getElementById('currentPrice'),
+ 1397             priceChange: document.getEle('priceChange'),
+ 1398       hartCanvas:ocument.getElementById('chartCanvas'),
+ 1399            siValue: document.getById('rsiValue'),
+ 1400             macdValue: document.getElementById('macdValue'),
+ 1401   Value: dment.getElementById('bbVa,
+ 1402             emaValue: document.getElementById(alue        voalue: document.getElementBalue'),
+ 1403             signalArrow: document.getElementById('signalArrow            signalText: document.getElemId('signalText'),
+ 1404          signalConfidence: document.getElementById('signalConfidence'),
+ 1405             s: document.getElementById('signalReasons')          buyBtn: document.getElementById('buyBtn'),
+ 1406             selocument.gtById('sellBtn'),
+ 1407   closeTradeBtn: document.getElementById('closeTradeBtn'),
+ 1408            Trade: docuementById('activeTrade'),
+ 1409        Type: docu.getElementById(pe'),
+ 1410             tradePnl: documt.getElementById('tradePnl'),
+ 1411             entryPrice: document.getElementById('),
+ 1412             tradeSize: ent.getElemed('tradeSize'),
+ 1413          totalTradest.getElementById('totalT         winTrades: documentElemenrades'),
+ 1414             lossTrent.getElementById('ssTrades')         aPnl: dument.getElementById('a        yLisent.getElementById('historyList,
+ 1415             positionSize: document.gementByISize'),
+ 1416     pairSct: document.getElementById('pairSel),
+ 1417        e documentlementById),

