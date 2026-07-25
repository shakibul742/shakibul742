svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 350" width="850" height="350">
    <style>
        .title { font-family: monospace; font-size: 13px; fill: #8b949e; font-weight: bold; text-anchor: middle; }
        .text { font-family: 'Courier New', Courier, monospace; font-size: 15px; fill: #c9d1d9; }
        .prompt-user { fill: #27c93f; font-weight: bold; }
        .prompt-dir { fill: #3b8eea; font-weight: bold; }
        .command { fill: #f8e3a1; font-weight: bold; }
        .log { fill: #8b949e; }
        .success { fill: #27c93f; }
        .exe { fill: #ff5f56; font-weight: bold; }
        .value { fill: #58a6ff; font-weight: bold; }
        .blink { animation: blinker 1s linear infinite; fill: #c9d1d9; font-weight: bold; }
        @keyframes blinker { 50% { opacity: 0; } }
    </style>
    
    <!-- Background with shadow -->
    <rect x="0" y="0" width="850" height="350" rx="10" ry="10" fill="#0d1117" stroke="#30363d" stroke-width="2"/>
    
    <!-- Title Bar -->
    <rect x="0" y="0" width="850" height="30" rx="10" ry="10" fill="#161b22"/>
    <rect x="0" y="15" width="850" height="15" fill="#161b22"/>
    <line x1="0" y1="30" x2="850" y2="30" stroke="#30363d" stroke-width="2"/>

    <!-- Window Controls -->
    <circle cx="20" cy="15" r="6" fill="#ff5f56"/>
    <circle cx="40" cy="15" r="6" fill="#ffbd2e"/>
    <circle cx="60" cy="15" r="6" fill="#27c93f"/>

    <!-- Title -->
    <text x="425" y="20" class="title">shakibul742@security: ~</text>

    <!-- Content -->
    <g class="text">
        <!-- Execution command -->
        <text x="20" y="65">
            <tspan class="prompt-user">shakibul742@security</tspan><tspan>:</tspan><tspan class="prompt-dir">~</tspan><tspan>$ </tspan><tspan class="command">./about_me.exe</tspan>
        </text>
        
        <!-- Loading sequence -->
        <text x="20" y="95" class="log">[+] INITIATING SECURE CONNECTION...</text>
        <text x="20" y="115" class="success">[+] ACCESS GRANTED.</text>
        <text x="20" y="135" class="log">[+] LOADING MODULES...</text>
        
        <!-- LEFT COLUMN (x=20) -->
        <text x="20" y="175"><tspan class="exe">&gt; name.exe</tspan></text>
        <text x="40" y="195"><tspan class="value">SHAKIBUL ISLAM</tspan></text>

        <text x="20" y="225"><tspan class="exe">&gt; username.exe</tspan></text>
        <text x="40" y="245"><tspan class="value">shakibul742</tspan></text>

        <text x="20" y="275"><tspan class="exe">&gt; whoami.exe</tspan></text>
        <text x="40" y="295"><tspan class="value">CyberSecurity Learner</tspan></text>

        <!-- RIGHT COLUMN (x=400) -->
        <text x="400" y="175"><tspan class="exe">&gt; location.exe</tspan></text>
        <text x="420" y="195"><tspan class="value">Bangladesh</tspan></text>

        <text x="400" y="225"><tspan class="exe">&gt; university.exe</tspan></text>
        <text x="420" y="245"><tspan class="value">Pabna University of Science and Technology(PUST)</tspan></text>

        <text x="400" y="275"><tspan class="exe">&gt; degree.exe</tspan></text>
        <text x="420" y="295"><tspan class="value">B.Sc. in Computer Science &amp; Engineering</tspan></text>
        
        <text x="400" y="325"><tspan class="exe">&gt; focus.exe</tspan></text>
        <text x="420" y="345"><tspan class="value">Defensive Security, SOC Analyst</tspan></text>

    </g>
</svg>
"""

with open("assets/terminal.svg", "w") as f:
    f.write(svg_content)
