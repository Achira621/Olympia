"""
OLYMPIA Ultra-Complex Kinetic & Shader Physics Engine.
Injects a parent-document JavaScript physics engine, HTML5 canvas ember/vortex particle system,
3D matrix card-tilt listener, magnetic gravity buttons, SVG turbulence flame shaders,
and mechanical typography decoders directly onto the Streamlit root DOM.
"""

import re
import streamlit as st
import streamlit.components.v1 as components


KINETIC_PARENT_SCRIPT = """
<script>
(function() {
    const parentDoc = window.parent.document;
    const parentWin = window.parent;

    if (!parentDoc || !parentWin) return;

    // ============================================================
    // 1. INJECT GLOBAL SVG SHADERS (feTurbulence Liquid Heat-Haze)
    // ============================================================
    if (!parentDoc.getElementById("olympia-svg-shaders")) {
        const svgContainer = parentDoc.createElement("div");
        svgContainer.id = "olympia-svg-shaders";
        svgContainer.style.cssText = "position: absolute; width: 0; height: 0; overflow: hidden; pointer-events: none;";
        svgContainer.innerHTML = `
        <svg style="position: absolute; width: 0; height: 0;" aria-hidden="true">
            <defs>
                <!-- Flame Fluid Heat-Haze Turbulence Shader -->
                <filter id="olympia-flame-shader" x="-25%" y="-25%" width="150%" height="150%">
                    <feTurbulence type="fractalNoise" baseFrequency="0.025 0.08" numOctaves="3" seed="3" result="noise">
                        <animate attributeName="baseFrequency" values="0.02 0.07; 0.035 0.13; 0.02 0.07" dur="3.2s" repeatCount="indefinite" />
                    </feTurbulence>
                    <feDisplacementMap in="SourceGraphic" in2="noise" scale="7" xChannelSelector="R" yChannelSelector="G" />
                </filter>

                <!-- High-Voltage Plasma Arc Shader for Matchup Clash -->
                <filter id="olympia-plasma-shader" x="-30%" y="-30%" width="160%" height="160%">
                    <feTurbulence type="turbulence" baseFrequency="0.08 0.15" numOctaves="2" seed="5" result="arcs">
                        <animate attributeName="seed" values="1;5;9;15;2" dur="0.8s" repeatCount="indefinite" />
                    </feTurbulence>
                    <feColorMatrix type="matrix" values="
                        1 0 0 0 0.83
                        0 1 0 0 0.69
                        0 0 1 0 0.22
                        0 0 0 18 -7" result="glowArcs" />
                    <feBlend in="SourceGraphic" in2="glowArcs" mode="screen" />
                </filter>

                <!-- Specular Holographic Lens Shader -->
                <filter id="olympia-hologram-shader" x="-10%" y="-10%" width="120%" height="120%">
                    <feGaussianBlur in="SourceGraphic" stdDeviation="1.5" result="blur" />
                    <feColorMatrix in="blur" type="matrix" values="
                        1 0 0 0 0.85
                        0 1 0 0 0.70
                        0 0 1 0 0.20
                        0 0 0 2 -0.1" result="colorShift" />
                    <feMerge>
                        <feMergeNode in="colorShift" />
                        <feMergeNode in="SourceGraphic" />
                    </feMerge>
                </filter>
            </defs>
        </svg>
        `;
        parentDoc.body.appendChild(svgContainer);
    }

    // ============================================================
    // 2. INJECT KINETIC CSS TOKENS & 3D HARDWARE-ACCELERATED STYLES
    // ============================================================
    if (!parentDoc.getElementById("olympia-kinetic-css")) {
        const styleSheet = parentDoc.createElement("style");
        styleSheet.id = "olympia-kinetic-css";
        styleSheet.textContent = `
        /* Procedural Flame Ripple Class */
        .olympia-flame-animated, [data-flame="true"], svg.olympia-torch-flame path.flame-core {
            filter: url(#olympia-flame-shader) !important;
            will-change: filter, transform;
        }

        /* 3D Bento Card Specular Foil & Matrix Tilt Container */
        .hero-onyx-card, .hero-legacy-card, .ag-glass-panel, .fifa-ovr-card,
        [data-testid="stMetric"], .stMetric, div[data-testid="column"] > div > div > div.olympia-card,
        .olympia-card, .ticker-card {
            transform-style: preserve-3d !important;
            transform: perspective(1000px) rotateX(var(--rx, 0deg)) rotateY(var(--ry, 0deg)) translate3d(0, 0, var(--tz, 0px));
            transition: transform 180ms cubic-bezier(0.16, 1, 0.3, 1), box-shadow 180ms ease-out !important;
            position: relative !important;
            will-change: transform, box-shadow;
        }

        /* Holographic Specular Glare Overlay */
        .hero-onyx-card::before, .ag-glass-panel::before, .olympia-card::before {
            content: '';
            position: absolute;
            inset: 0;
            border-radius: inherit;
            background: radial-gradient(550px circle at var(--glare-x, 50%) var(--glare-y, 50%), rgba(212, 175, 55, 0.16), transparent 60%);
            pointer-events: none;
            opacity: var(--glare-opacity, 0);
            transition: opacity 300ms ease;
            z-index: 2;
        }
        .hero-onyx-card:hover::before, .ag-glass-panel:hover::before, .olympia-card:hover::before {
            --glare-opacity: 1;
        }

        /* Dynamic Laser-Cut Gold Border Highlight */
        .hero-onyx-card::after, .ag-glass-panel::after, .olympia-card::after {
            content: '';
            position: absolute;
            inset: -1px;
            border-radius: inherit;
            padding: 1.5px;
            background: radial-gradient(280px circle at var(--glare-x, 50%) var(--glare-y, 50%), #D4AF37, transparent 70%);
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            pointer-events: none;
            opacity: var(--glare-opacity, 0);
            transition: opacity 250ms ease;
            z-index: 3;
        }
        .hero-onyx-card:hover::after, .ag-glass-panel:hover::after, .olympia-card:hover::after {
            --glare-opacity: 1;
        }

        /* Magnetic Pull Physical Elevation */
        .magnetic-btn, .stButton > button, a[href*="?role="] {
            transition: transform 160ms cubic-bezier(0.22, 1, 0.36, 1), box-shadow 160ms ease !important;
            will-change: transform;
            position: relative;
        }

        /* Mechanical 3D Glyph Cipher */
        .kinetic-glyph-char {
            display: inline-block;
            font-family: 'JetBrains Mono', monospace;
            font-variant-numeric: tabular-nums;
            transition: color 200ms ease;
        }

        /* Sonar Map Hub Pulses */
        @keyframes sonarRipple {
            0% { transform: scale(0.6); opacity: 1; }
            50% { opacity: 0.6; }
            100% { transform: scale(2.8); opacity: 0; }
        }
        .sonar-beacon {
            position: absolute;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: #D4AF37;
            box-shadow: 0 0 12px #D4AF37;
        }
        .sonar-beacon::before, .sonar-beacon::after {
            content: '';
            position: absolute;
            inset: -4px;
            border-radius: 50%;
            border: 1.5px solid #D4AF37;
            animation: sonarRipple 2.2s cubic-bezier(0.1, 0.8, 0.3, 1) infinite;
        }
        .sonar-beacon::after {
            animation-delay: 1.1s;
        }

        /* 3D Astrolabe Gyroscopic Rings */
        .astrolabe-viewport {
            perspective: 1200px;
            perspective-origin: 50% 50%;
        }
        .astrolabe-ring-mesh {
            transform-style: preserve-3d;
            transition: transform 600ms cubic-bezier(0.22, 1, 0.36, 1);
        }
        .astrolabe-viewport:hover .astrolabe-ring-mesh {
            transform: rotateX(0deg) rotateY(0deg) translateZ(35px) !important;
        }

        /* Wind-Tunnel Streamlines */
        @keyframes windStreamline {
            0% { stroke-dashoffset: 240; opacity: 0.2; }
            50% { opacity: 0.95; }
            100% { stroke-dashoffset: 0; opacity: 0.2; }
        }
        .wind-line-laminar {
            stroke: #D4AF37;
            stroke-dasharray: 60 180;
            animation: windStreamline var(--flow-speed, 1.4s) linear infinite;
        }
        .wind-line-turbulent {
            stroke: #C41E3A;
            stroke-dasharray: 40 140;
            animation: windStreamline var(--flow-speed-turb, 1.1s) linear infinite;
        }

        /* Radar Scanner Sweep */
        @keyframes radarSweepScan {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .radar-sweep-conduit {
            transform-origin: 50% 50%;
            animation: radarSweepScan 4s linear infinite;
        }

        /* Plasma Clash Fulcrum */
        @keyframes clashJitter {
            0% { transform: scaleY(1) translateY(0); filter: drop-shadow(0 0 6px #D4AF37); }
            50% { transform: scaleY(1.2) translateY(-1px); filter: drop-shadow(0 0 16px #C41E3A); }
            100% { transform: scaleY(1) translateY(0); filter: drop-shadow(0 0 6px #D4AF37); }
        }
        .clash-spark-fulcrum {
            animation: clashJitter 0.12s steps(2, start) infinite;
        }

        /* Kinetic Accordion Strip */
        .monument-accordion-strip {
            display: flex;
            gap: 0.75rem;
            width: 100%;
            height: 290px;
            margin: 1.4rem 0;
        }
        .monument-panel {
            flex: 1;
            background: linear-gradient(135deg, #1C1B19 0%, #292622 100%);
            border: 1px solid rgba(212, 175, 55, 0.35);
            border-radius: 14px;
            padding: 1.4rem;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            cursor: pointer;
            position: relative;
            box-shadow: 0 4px 18px rgba(0,0,0,0.25);
            transition: flex 600ms cubic-bezier(0.22, 1, 0.36, 1), 
                        border-color 300ms ease, 
                        box-shadow 300ms ease;
        }
        .monument-panel:hover {
            flex: 4.2;
            border-color: #D4AF37;
            box-shadow: 0 12px 35px rgba(212, 175, 55, 0.28);
        }
        .monument-title-rot {
            font-family: 'Cinzel', serif;
            font-weight: 800;
            font-size: 1.15rem;
            color: #FAF8F2;
            letter-spacing: 0.08em;
            writing-mode: vertical-rl;
            transform: rotate(180deg);
            transition: all 400ms ease;
            white-space: nowrap;
        }
        .monument-panel:hover .monument-title-rot {
            writing-mode: horizontal-tb;
            transform: rotate(0deg);
            color: #D4AF37;
            font-size: 1.35rem;
        }
        .monument-inner-content {
            opacity: 0;
            transform: translateY(18px);
            transition: opacity 400ms ease 150ms, transform 400ms cubic-bezier(0.22, 1, 0.36, 1) 150ms;
            color: #EBD9C3;
            font-size: 0.88rem;
            line-height: 1.5;
        }
        .monument-panel:hover .monument-inner-content {
            opacity: 1;
            transform: translateY(0);
        }
        `;
        parentDoc.head.appendChild(styleSheet);
    }

    // ============================================================
    // 3. HTML5 <canvas> OLYMPIC TORCH FLAME & CONVECTIVE FIRE TRAIL
    // ============================================================
    // Clean up any prior canvas to ensure hot updates take effect immediately
    const existingOldCanvas = parentDoc.getElementById("olympia-ember-canvas");
    if (existingOldCanvas) existingOldCanvas.remove();
    const existingFireCanvas = parentDoc.getElementById("olympia-fire-canvas");
    if (existingFireCanvas) existingFireCanvas.remove();
    if (parentWin.__olympiaFireAnimId) {
        parentWin.cancelAnimationFrame(parentWin.__olympiaFireAnimId);
    }

    const canvas = parentDoc.createElement("canvas");
    canvas.id = "olympia-fire-canvas";
    canvas.style.cssText = "position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 999998;";
    parentDoc.body.appendChild(canvas);

    const ctx = canvas.getContext("2d");
    let width = canvas.width = parentWin.innerWidth;
    let height = canvas.height = parentWin.innerHeight;

    const onResize = () => {
        width = canvas.width = parentWin.innerWidth;
        height = canvas.height = parentWin.innerHeight;
    };
    if (parentWin.__olympiaFireResizeHandler) {
        parentWin.removeEventListener("resize", parentWin.__olympiaFireResizeHandler);
    }
    parentWin.__olympiaFireResizeHandler = onResize;
    parentWin.addEventListener("resize", onResize);

    // Dynamic Olympic Fire Particle System
    const flameTongues = [];
    const flameSparks = [];
    const ambientSparks = [];
    const mouse = { x: -9999, y: -9999, vx: 0, vy: 0, lastX: -9999, lastY: -9999 };

    // 24 ambient rising golden embers in the atmosphere
    for (let i = 0; i < 24; i++) {
        ambientSparks.push({
            x: Math.random() * width,
            y: Math.random() * height,
            radius: 0.9 + Math.random() * 1.5,
            baseVy: -(0.3 + Math.random() * 0.6),
            vx: 0,
            vy: 0,
            seed: Math.random() * 100,
            phase: Math.random() * Math.PI * 2,
            color: Math.random() > 0.3 ? "#D4AF37" : "#FF5722",
            alpha: 0.2 + Math.random() * 0.5
        });
    }

    const onMouseMove = (e) => {
        mouse.vx = e.clientX - mouse.lastX;
        mouse.vy = e.clientY - mouse.lastY;
        mouse.x = e.clientX;
        mouse.y = e.clientY;
        mouse.lastX = e.clientX;
        mouse.lastY = e.clientY;

        const speed = Math.hypot(mouse.vx, mouse.vy);

        // Spawn licking flame tongues along cursor path
        const spawnCount = speed > 7 ? 3 : (speed > 1.8 ? 2 : 1);
        for (let k = 0; k < spawnCount; k++) {
            if (flameTongues.length < 55) {
                const spread = (Math.random() - 0.5) * 8;
                flameTongues.push({
                    x: e.clientX + spread,
                    y: e.clientY + spread,
                    vx: (Math.random() - 0.5) * 1.4 - mouse.vx * 0.08,
                    vy: -(1.8 + Math.random() * 2.8) - Math.abs(mouse.vy) * 0.06,
                    baseWidth: 10 + Math.random() * 14,
                    baseHeight: 20 + Math.random() * 28,
                    angle: -mouse.vx * 0.025 + (Math.random() - 0.5) * 0.2,
                    angularSpeed: (Math.random() - 0.5) * 0.04,
                    life: 1.0,
                    decay: 0.038 + Math.random() * 0.025,
                    seed: Math.random() * 100
                });
            }
        }

        // Spawn flying flame sparks / cinders on faster moves
        if (speed > 4 && flameSparks.length < 35) {
            flameSparks.push({
                x: e.clientX + (Math.random() - 0.5) * 10,
                y: e.clientY + (Math.random() - 0.5) * 10,
                vx: (Math.random() - 0.5) * 3.4 - mouse.vx * 0.1,
                vy: -(2.4 + Math.random() * 4.2),
                radius: 1.4 + Math.random() * 2.2,
                life: 1.0,
                decay: 0.04 + Math.random() * 0.03,
                seed: Math.random() * 100
            });
        }
    };

    if (parentWin.__olympiaFireMouseHandler) {
        parentWin.removeEventListener("mousemove", parentWin.__olympiaFireMouseHandler);
    }
    parentWin.__olympiaFireMouseHandler = onMouseMove;
    parentWin.addEventListener("mousemove", onMouseMove);

    let lastTime = performance.now();

    function renderFireSystem(now) {
        const dt = Math.min(32, now - lastTime);
        lastTime = now;

        ctx.clearRect(0, 0, width, height);

        // 1. Ambient Golden Atmosphere Embers
        ctx.globalCompositeOperation = "source-over";
        for (let i = 0; i < ambientSparks.length; i++) {
            const p = ambientSparks[i];
            p.y += (p.baseVy + p.vy) * (dt / 16);
            p.x += (Math.sin(now * 0.0018 + p.seed) * 0.45 + p.vx) * (dt / 16);
            p.vx *= 0.94;
            p.vy *= 0.94;

            // Wrap bounds
            if (p.y < -10) { p.y = height + 10; p.x = Math.random() * width; }
            if (p.x < -10) p.x = width + 10;
            if (p.x > width + 10) p.x = -10;

            const pulsatingAlpha = Math.max(0.1, Math.min(0.85, p.alpha + Math.sin(now * 0.003 + p.phase) * 0.2));
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.globalAlpha = pulsatingAlpha;
            ctx.shadowColor = p.color;
            ctx.shadowBlur = p.radius * 3;
            ctx.fill();
        }

        // 2. Idle Olympic Torch Flame Flickering at Cursor
        if (mouse.x > 0 && mouse.x < width && mouse.y > 0 && mouse.y < height) {
            if (Math.random() > 0.4 && flameTongues.length < 55) {
                flameTongues.push({
                    x: mouse.x + (Math.random() - 0.5) * 6,
                    y: mouse.y + (Math.random() - 0.5) * 6,
                    vx: (Math.random() - 0.5) * 0.8,
                    vy: -(1.6 + Math.random() * 2.2),
                    baseWidth: 9 + Math.random() * 11,
                    baseHeight: 18 + Math.random() * 22,
                    angle: (Math.random() - 0.5) * 0.15,
                    angularSpeed: (Math.random() - 0.5) * 0.04,
                    life: 1.0,
                    decay: 0.042 + Math.random() * 0.025,
                    seed: Math.random() * 100
                });
            }
        }

        // 3. Render Flame Tongues with Additive Blending (Real Combustion Core!)
        ctx.globalCompositeOperation = "lighter";
        ctx.shadowBlur = 0;

        for (let i = flameTongues.length - 1; i >= 0; i--) {
            const p = flameTongues[i];
            p.x += p.vx * (dt / 16);
            p.y += p.vy * (dt / 16);
            p.vy -= 0.11 * (dt / 16); // Upward convective thermal buoyancy
            p.vx += Math.sin(now * 0.014 + p.seed) * 0.25 * (dt / 16); // Thermal turbulent vortex
            p.angle += p.angularSpeed;
            p.life -= p.decay * (dt / 16);

            if (p.life <= 0) {
                flameTongues.splice(i, 1);
                continue;
            }

            const progress = 1 - p.life;
            const curW = Math.max(0.8, p.baseWidth * Math.pow(p.life, 0.65));
            const curH = Math.max(2, p.baseHeight * Math.pow(p.life, 0.45));

            ctx.save();
            ctx.translate(p.x, p.y);
            ctx.rotate(p.angle);

            // Thermal color decay: White incandescent core -> Imperial Gold -> Fire Orange -> Crimson -> Smoke
            const grad = ctx.createRadialGradient(0, curH * 0.2, 0, 0, 0, curH);
            if (progress < 0.22) {
                grad.addColorStop(0, "rgba(255, 255, 245, 0.95)");
                grad.addColorStop(0.25, "rgba(255, 215, 0, 0.9)");
                grad.addColorStop(0.65, "rgba(255, 69, 0, 0.75)");
                grad.addColorStop(1, "rgba(196, 30, 58, 0)");
            } else if (progress < 0.55) {
                grad.addColorStop(0, "rgba(255, 215, 0, 0.85)");
                grad.addColorStop(0.35, "rgba(255, 87, 34, 0.7)");
                grad.addColorStop(0.8, "rgba(196, 30, 58, 0.4)");
                grad.addColorStop(1, "rgba(46, 42, 37, 0)");
            } else {
                grad.addColorStop(0, "rgba(255, 69, 0, 0.55)");
                grad.addColorStop(0.5, "rgba(196, 30, 58, 0.3)");
                grad.addColorStop(0.9, "rgba(46, 42, 37, 0.12)");
                grad.addColorStop(1, "rgba(0, 0, 0, 0)");
            }

            ctx.fillStyle = grad;
            ctx.beginPath();
            ctx.moveTo(0, curH * 0.35);
            ctx.bezierCurveTo(-curW, curH * 0.15, -curW * 0.8, -curH * 0.45, 0, -curH);
            ctx.bezierCurveTo(curW * 0.8, -curH * 0.45, curW, curH * 0.15, 0, curH * 0.35);
            ctx.closePath();
            ctx.fill();

            ctx.restore();
        }

        // 4. Render Incendiary Flying Sparks / Cinders
        for (let i = flameSparks.length - 1; i >= 0; i--) {
            const s = flameSparks[i];
            s.x += s.vx * (dt / 16);
            s.y += s.vy * (dt / 16);
            s.vy -= 0.16 * (dt / 16);
            s.vx += Math.sin(now * 0.02 + s.seed) * 0.35 * (dt / 16);
            s.life -= s.decay * (dt / 16);

            if (s.life <= 0) {
                flameSparks.splice(i, 1);
                continue;
            }

            const progress = 1 - s.life;
            const r = Math.max(0.6, s.radius * s.life);
            ctx.beginPath();
            ctx.arc(s.x, s.y, r, 0, Math.PI * 2);
            ctx.fillStyle = progress < 0.25 ? "#FFFFF0" : (progress < 0.6 ? "#FFD700" : (progress < 0.85 ? "#FF4500" : "#C41E3A"));
            ctx.shadowColor = "#FF4500";
            ctx.shadowBlur = 10;
            ctx.globalAlpha = Math.max(0, s.life * 0.95);
            ctx.fill();
        }

        ctx.shadowBlur = 0;
        ctx.globalAlpha = 1.0;
        ctx.globalCompositeOperation = "source-over";
        parentWin.__olympiaFireAnimId = parentWin.requestAnimationFrame(renderFireSystem);
    }

    parentWin.__olympiaFireAnimId = parentWin.requestAnimationFrame(renderFireSystem);

    // ============================================================
    // 4. 3D MATRIX TILT CONTROLLER ON ALL BENTO CARDS
    // ============================================================
    function bindCard3DTilt() {
        const cardSelectors = [
            ".hero-onyx-card",
            ".hero-legacy-card",
            ".ag-glass-panel",
            ".fifa-ovr-card",
            ".olympia-card",
            ".ticker-card",
            "[data-testid='stMetric']"
        ];
        const cards = parentDoc.querySelectorAll(cardSelectors.join(", "));

        cards.forEach(card => {
            if (card.__olympiaTiltBound) return;
            card.__olympiaTiltBound = true;

            card.addEventListener("mousemove", (e) => {
                const rect = card.getBoundingClientRect();
                if (rect.width === 0 || rect.height === 0) return;

                const xRel = (e.clientX - rect.left) / rect.width - 0.5;
                const yRel = (e.clientY - rect.top) / rect.height - 0.5;

                const rx = (yRel * -13.5).toFixed(2);
                const ry = (xRel * 13.5).toFixed(2);
                const glareX = ((xRel + 0.5) * 100).toFixed(1);
                const glareY = ((yRel + 0.5) * 100).toFixed(1);

                card.style.setProperty("--rx", `${rx}deg`);
                card.style.setProperty("--ry", `${ry}deg`);
                card.style.setProperty("--tz", `6px`);
                card.style.setProperty("--glare-x", `${glareX}%`);
                card.style.setProperty("--glare-y", `${glareY}%`);
                card.style.setProperty("--glare-opacity", `1`);
            });

            card.addEventListener("mouseleave", () => {
                card.style.setProperty("--rx", "0deg");
                card.style.setProperty("--ry", "0deg");
                card.style.setProperty("--tz", "0px");
                card.style.setProperty("--glare-opacity", "0");
            });
        });
    }

    // ============================================================
    // 5. MAGNETIC GRAVITY BUTTON PHYSICS
    // ============================================================
    function bindMagneticGravityButtons() {
        const buttons = parentDoc.querySelectorAll(".magnetic-btn, .stButton > button");

        buttons.forEach(btn => {
            if (btn.__olympiaMagBound) return;
            btn.__olympiaMagBound = true;

            btn.addEventListener("mousemove", (e) => {
                const rect = btn.getBoundingClientRect();
                const centerX = rect.left + rect.width / 2;
                const centerY = rect.top + rect.height / 2;
                const dx = e.clientX - centerX;
                const dy = e.clientY - centerY;
                btn.style.transform = `translate3d(${dx * 0.22}px, ${dy * 0.22}px, 0)`;
            });

            btn.addEventListener("mouseleave", () => {
                btn.style.transform = "translate3d(0, 0, 0)";
            });
        });
    }

    // ============================================================
    // 6. DUAL-STAGE MECHANICAL CIPHER SCRAMBLE
    // ============================================================
    function triggerKineticOdometerScramble() {
        const cipherElements = parentDoc.querySelectorAll(".kinetic-odometer, [data-odometer='true']");
        const GREEK_GLYPHS = ["Δ", "Ω", "Σ", "Φ", "Λ", "Ξ", "Ψ", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];

        cipherElements.forEach(el => {
            if (el.__olympiaScrambleRunning) return;
            el.__olympiaScrambleRunning = true;

            const targetText = el.getAttribute("data-target-value") || el.innerText.trim();
            const originalChars = targetText.split("");
            const duration = 450;
            const startTime = performance.now();

            function scrambleStep(now) {
                const elapsed = now - startTime;
                const progress = Math.min(1, elapsed / duration);
                const lockedCount = Math.floor(progress * originalChars.length);

                let displayStr = "";
                for (let i = 0; i < originalChars.length; i++) {
                    const char = originalChars[i];
                    if (char === "," || char === "." || char === " " || char === "%" || char === "+" || char === "-") {
                        displayStr += char;
                    } else if (i < lockedCount) {
                        displayStr += char;
                    } else {
                        const randomGlyph = GREEK_GLYPHS[Math.floor(Math.random() * GREEK_GLYPHS.length)];
                        displayStr += `<span style="color: #D4AF37;">${randomGlyph}</span>`;
                    }
                }
                el.innerHTML = displayStr;

                if (progress < 1) {
                    parentWin.requestAnimationFrame(scrambleStep);
                } else {
                    el.innerHTML = targetText;
                    el.__olympiaScrambleRunning = false;
                }
            }
            parentWin.requestAnimationFrame(scrambleStep);
        });
    }

    // Run DOM binders & schedule periodic re-checks for dynamic Streamlit widgets
    bindCard3DTilt();
    bindMagneticGravityButtons();
    triggerKineticOdometerScramble();

    if (!parentWin.__olympiaKineticInterval) {
        parentWin.__olympiaKineticInterval = parentWin.setInterval(() => {
            bindCard3DTilt();
            bindMagneticGravityButtons();
        }, 1200);
    }
})();
</script>
"""


def inject_kinetic_engine():
    """
    Mounts the parent-window kinetic physics engine, particle canvas,
    3D matrix card-tilt listener, and SVG turbulence shaders.
    """
    components.html(KINETIC_PARENT_SCRIPT, height=0, width=0)


def render_monument_accordion(role_param: str = "fan"):
    """
    Renders the Monumental Expanding Accordion Strip (5 architectural pillars)
    with smooth cubic-bezier flex expansion, vertical-to-horizontal text rotation,
    and unveiling telemetry on hover.
    """
    accordion_html = f"""
    <div class="monument-accordion-strip">
        <!-- 1. ATHLETES -->
        <div class="monument-panel">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div class="monument-title-rot">ATHLETES</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #D4AF37; font-weight: 700;">01</div>
            </div>
            <div class="monument-inner-content">
                <div style="font-family: 'Cinzel', serif; font-size: 1.15rem; font-weight: 800; color: #FAF8F2; margin-bottom: 0.4rem;">
                    Living Legends & Archetypes
                </div>
                <div>
                    Deep career trajectories across 12,000+ individual medalists. Trace career longevity from Michael Phelps to Nadia Comăneci.
                </div>
                <div style="margin-top: 0.8rem;">
                    <a href="?role={role_param}&nav=athletes" target="_self" style="color: #D4AF37; font-weight: 700; text-decoration: none; font-size: 0.82rem;">Explore Athletes →</a>
                </div>
            </div>
        </div>

        <!-- 2. NATIONS -->
        <div class="monument-panel">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div class="monument-title-rot">NATIONS</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #D4AF37; font-weight: 700;">02</div>
            </div>
            <div class="monument-inner-content">
                <div style="font-family: 'Cinzel', serif; font-size: 1.15rem; font-weight: 800; color: #FAF8F2; margin-bottom: 0.4rem;">
                    Geopolitical Dynasties
                </div>
                <div>
                    Explore national rise, Cold-War rivalries, and modern Asian medal acceleration across 206 National Olympic Committees.
                </div>
                <div style="margin-top: 0.8rem;">
                    <a href="?role={role_param}&nav=country" target="_self" style="color: #D4AF37; font-weight: 700; text-decoration: none; font-size: 0.82rem;">Country Deep-Dive →</a>
                </div>
            </div>
        </div>

        <!-- 3. SPORTS -->
        <div class="monument-panel">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div class="monument-title-rot">SPORTS</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #D4AF37; font-weight: 700;">03</div>
            </div>
            <div class="monument-inner-content">
                <div style="font-family: 'Cinzel', serif; font-size: 1.15rem; font-weight: 800; color: #FAF8F2; margin-bottom: 0.4rem;">
                    Discipline Specialization
                </div>
                <div>
                    Analyze Shannon entropy diversification and event parity across 47 Olympic sports disciplines.
                </div>
                <div style="margin-top: 0.8rem;">
                    <a href="?role={role_param}&nav=sports" target="_self" style="color: #D4AF37; font-weight: 700; text-decoration: none; font-size: 0.82rem;">Analyze Disciplines →</a>
                </div>
            </div>
        </div>

        <!-- 4. HISTORY -->
        <div class="monument-panel">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div class="monument-title-rot">HISTORY</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #D4AF37; font-weight: 700;">04</div>
            </div>
            <div class="monument-inner-content">
                <div style="font-family: 'Cinzel', serif; font-size: 1.15rem; font-weight: 800; color: #FAF8F2; margin-bottom: 0.4rem;">
                    131-Year Star Schema
                </div>
                <div>
                    Immutable record of human achievement from Athens 1896 to Milano-Cortina 2026 loaded inside an offline Star Schema.
                </div>
                <div style="margin-top: 0.8rem;">
                    <a href="?role={role_param}&nav=medals" target="_self" style="color: #D4AF37; font-weight: 700; text-decoration: none; font-size: 0.82rem;">View Podiums →</a>
                </div>
            </div>
        </div>

        <!-- 5. TACTICS -->
        <div class="monument-panel">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div class="monument-title-rot">TACTICS</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #D4AF37; font-weight: 700;">05</div>
            </div>
            <div class="monument-inner-content">
                <div style="font-family: 'Cinzel', serif; font-size: 1.15rem; font-weight: 800; color: #FAF8F2; margin-bottom: 0.4rem;">
                    Coach Strategy Studio
                </div>
                <div>
                    Biometric slipstream aerodynamic physics, tactical radar profiles, and opponent head-to-head scouting.
                </div>
                <div style="margin-top: 0.8rem;">
                    <a href="?role={role_param}&nav=coach" target="_self" style="color: #D4AF37; font-weight: 700; text-decoration: none; font-size: 0.82rem;">Enter Studio →</a>
                </div>
            </div>
        </div>
    </div>
    """
    cleaned = re.sub(r'\n\s*', ' ', accordion_html).strip()
    if hasattr(st, "html"):
        st.html(cleaned)
    else:
        st.markdown(cleaned, unsafe_allow_html=True)



def get_3d_astrolabe_rings_html(width: int = 320, height: int = 140) -> str:
    """
    Returns the 3D Gyroscopic Astrolabe Olympic Rings with multi-axis rotation
    and dynamic gleam stop gradients.
    """
    return f"""
    <div class="astrolabe-viewport" style="display: flex; justify-content: center; align-items: center; padding: 0.6rem 0;">
        <div class="astrolabe-ring-mesh">
            <svg width="{width}" height="{height}" viewBox="0 0 340 150" fill="none" xmlns="http://www.w3.org/2000/svg" style="display: block; filter: drop-shadow(0 8px 24px rgba(46,42,37,0.18));">
                <defs>
                    <linearGradient id="astroGold1" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#E5DED2"><animate attributeName="stop-color" values="#E5DED2;#F3E7C5;#E5DED2" dur="4s" repeatCount="indefinite"/></stop>
                        <stop offset="40%" stop-color="#D4AF37"><animate attributeName="stop-color" values="#D4AF37;#AA820A;#D4AF37" dur="4s" repeatCount="indefinite"/></stop>
                        <stop offset="100%" stop-color="#AA820A"/>
                    </linearGradient>
                    <linearGradient id="astroBronze1" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#D4AF37"/>
                        <stop offset="60%" stop-color="#8C6D1F"/>
                        <stop offset="100%" stop-color="#5A4005"/>
                    </linearGradient>
                    <linearGradient id="astroSilver1" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#FFFFFF"/>
                        <stop offset="50%" stop-color="#C5BEB3"/>
                        <stop offset="100%" stop-color="#8B857C"/>
                    </linearGradient>
                </defs>
                <!-- Top Three Rings with Orbital 3D Tilt -->
                <circle cx="80" cy="55" r="46" stroke="url(#astroGold1)" stroke-width="8.5" stroke-linecap="round" style="transform-origin: 80px 55px; transform: rotateX(12deg) rotateY(-8deg);"/>
                <circle cx="170" cy="55" r="46" stroke="url(#astroBronze1)" stroke-width="9" stroke-linecap="round" style="transform-origin: 170px 55px; transform: rotateX(-8deg) rotateY(14deg);"/>
                <circle cx="260" cy="55" r="46" stroke="url(#astroSilver1)" stroke-width="8.5" stroke-linecap="round" style="transform-origin: 260px 55px; transform: rotateX(14deg) rotateY(6deg);"/>
                <!-- Bottom Two Rings -->
                <circle cx="125" cy="95" r="46" stroke="url(#astroBronze1)" stroke-width="8.5" stroke-linecap="round" style="transform-origin: 125px 95px; transform: rotateX(-12deg) rotateY(-10deg);"/>
                <circle cx="215" cy="95" r="46" stroke="url(#astroGold1)" stroke-width="8.5" stroke-linecap="round" style="transform-origin: 215px 95px; transform: rotateX(10deg) rotateY(12deg);"/>
            </svg>
        </div>
    </div>
    """


# ============================================================
# 10. ISOMETRIC 3D EXPLODING OLAP CUBE WIDGET
# ============================================================
def render_isometric_3d_olap_cube(active_op: str = "slice") -> str:
    """
    Renders an Interactive 3D CSS Isometric Data Cube (3x3x3 voxels)
    with live operation choreography:
    - Slice: horizontal layer slides out & glows in gold
    - Dice: 3x3x3 explodes outward isolating a glowing 2x2x2 core
    - Roll-Up: vertically compresses into a dense gold slab
    - Drill-Down: expands into 3 floating strata
    - Pivot: 90-degree 3D gimbal rotation
    """
    op = (active_op or "slice").lower()

    # Generate 27 voxels with CSS 3D transforms
    voxels_html = []
    size = 28  # pixel size of each sub-cube
    gap = 8   # resting gap between sub-cubes

    for x in range(3):
        for y in range(3):
            for z in range(3):
                # Base resting position centered at (0,0,0)
                bx = (x - 1) * (size + gap)
                by = (y - 1) * (size + gap)
                bz = (z - 1) * (size + gap)

                # Compute dynamic transform & styling based on active_op
                extra_cls = ""
                tx, ty, tz = bx, by, bz
                scale = 1.0
                opacity = 0.88

                if "slice" in op:
                    if y == 0:  # Top horizontal slice slides out & glows
                        tz += 45
                        ty -= 12
                        extra_cls = "voxel-slice-highlight"
                        opacity = 1.0
                    else:
                        opacity = 0.28
                elif "dice" in op:
                    # Explode outward radially
                    tx += (x - 1) * 22
                    ty += (y - 1) * 22
                    tz += (z - 1) * 22
                    if x <= 1 and y <= 1 and z <= 1:
                        extra_cls = "voxel-dice-highlight"
                        opacity = 1.0
                    else:
                        opacity = 0.3
                elif "roll" in op:
                    # Vertically compress into single dense slab
                    ty = (y - 1) * 4
                    scale = 0.95
                    extra_cls = "voxel-rollup-highlight"
                elif "drill" in op:
                    # Vertically expand into 3 floating strata
                    ty = (y - 1) * (size + gap + 24)
                    extra_cls = "voxel-drilldown-highlight"
                elif "pivot" in op:
                    extra_cls = "voxel-pivot-highlight"

                cube_html = f"""
                <div class="olap-voxel {extra_cls}" style="transform: translate3d({tx}px, {ty}px, {tz}px) scale({scale}); opacity: {opacity};">
                    <div class="voxel-face voxel-front"></div>
                    <div class="voxel-face voxel-back"></div>
                    <div class="voxel-face voxel-right"></div>
                    <div class="voxel-face voxel-left"></div>
                    <div class="voxel-face voxel-top"></div>
                    <div class="voxel-face voxel-bottom"></div>
                </div>
                """
                voxels_html.append(cube_html)

    joined_voxels = "\n".join(voxels_html)
    op_label = op.upper()
    if "slice" in op:
        desc = "Single 2D layer isolated along the Year dimension."
    elif "dice" in op:
        desc = "2×2×2 Sub-cube isolated across Country, Sport & Season."
    elif "roll" in op:
        desc = "Dimensions aggregated up the hierarchy into macro summaries."
    elif "drill" in op:
        desc = "Granular event-level hierarchy expanded into floating strata."
    elif "pivot" in op:
        desc = "Axes rotated 90° to cross-tabulate Sport vs Country."
    else:
        desc = "Multidimensional analytical data cube operational."

    return f"""
    <div class="olap-cube-container">
        <style>
        .olap-cube-container {{
            background: linear-gradient(135deg, #1C1B19 0%, #292622 100%);
            border: 1px solid rgba(212, 175, 55, 0.35);
            border-radius: 16px;
            padding: 1.4rem;
            color: #FAF8F2;
            position: relative;
            overflow: hidden;
            box-shadow: 0 12px 32px rgba(0,0,0,0.25);
            margin-bottom: 1.4rem;
        }}
        .olap-cube-stage {{
            width: 100%;
            height: 220px;
            perspective: 1000px;
            display: flex;
            align-items: center;
            justify-content: center;
            transform-style: preserve-3d;
        }}
        .olap-cube-gimbal {{
            width: 0;
            height: 0;
            transform-style: preserve-3d;
            transform: rotateX(-25deg) rotateY(38deg);
            transition: transform 700ms cubic-bezier(0.22, 1, 0.36, 1);
        }}
        .olap-cube-container:hover .olap-cube-gimbal {{
            transform: rotateX(-20deg) rotateY(55deg) scale(1.05);
        }}
        .olap-gimbal-pivot-active {{
            animation: cubePivotSpin 12s linear infinite !important;
        }}
        @keyframes cubePivotSpin {{
            0% {{ transform: rotateX(-25deg) rotateY(0deg); }}
            100% {{ transform: rotateX(-25deg) rotateY(360deg); }}
        }}
        .olap-voxel {{
            position: absolute;
            width: 28px;
            height: 28px;
            transform-style: preserve-3d;
            transition: transform 650ms cubic-bezier(0.22, 1, 0.36, 1), opacity 400ms ease;
        }}
        .voxel-face {{
            position: absolute;
            width: 28px;
            height: 28px;
            background: rgba(232, 217, 195, 0.18);
            border: 1px solid rgba(212, 175, 55, 0.45);
            box-sizing: border-box;
            backdrop-filter: blur(1px);
        }}
        .voxel-front  {{ transform: rotateY(  0deg) translateZ(14px); }}
        .voxel-back   {{ transform: rotateY(180deg) translateZ(14px); }}
        .voxel-right  {{ transform: rotateY( 90deg) translateZ(14px); }}
        .voxel-left   {{ transform: rotateY(-90deg) translateZ(14px); }}
        .voxel-top    {{ transform: rotateX( 90deg) translateZ(14px); background: rgba(250, 248, 242, 0.35); }}
        .voxel-bottom {{ transform: rotateX(-90deg) translateZ(14px); background: rgba(46, 42, 37, 0.5); }}

        /* Operation highlights */
        .voxel-slice-highlight .voxel-face {{
            background: rgba(212, 175, 55, 0.45) !important;
            border-color: #D4AF37 !important;
            box-shadow: 0 0 12px rgba(212, 175, 55, 0.6);
        }}
        .voxel-dice-highlight .voxel-face {{
            background: rgba(196, 30, 58, 0.4) !important;
            border-color: #C41E3A !important;
            box-shadow: 0 0 12px rgba(196, 30, 58, 0.6);
        }}
        .voxel-rollup-highlight .voxel-face {{
            background: linear-gradient(135deg, rgba(212, 175, 55, 0.6), rgba(170, 130, 10, 0.8)) !important;
            border-color: #F3E7C5 !important;
        }}
        .voxel-drilldown-highlight .voxel-face {{
            border-color: #E8D9C3 !important;
            box-shadow: 0 0 8px rgba(232, 217, 195, 0.4);
        }}
        </style>

        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.6rem;">
            <div>
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #D4AF37; background: rgba(212,175,55,0.15); border: 1px solid rgba(212,175,55,0.4); padding: 0.15rem 0.5rem; border-radius: 9999px; font-weight: 700;">
                        3D ISOMETRIC VOXEL CUBE
                    </span>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #E8D9C3;">
                        3×3×3 • 27 Granular Cells
                    </span>
                </div>
                <div style="font-family: 'Cinzel', serif; font-size: 1.15rem; font-weight: 800; color: #FAF8F2;">
                    Live Choreography: {op_label}
                </div>
                <div style="font-size: 0.78rem; color: #8B857C; margin-top: 0.2rem;">
                    {desc}
                </div>
            </div>
            <div style="text-align: right;">
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #D4AF37; font-weight: 700;">
                    3D PERSPECTIVE ACTIVE
                </span>
            </div>
        </div>

        <div class="olap-cube-stage">
            <div class="olap-cube-gimbal {'olap-gimbal-pivot-active' if 'pivot' in op else ''}">
                {joined_voxels}
            </div>
        </div>
    </div>
    """


# ============================================================
# 11. DATA MINING ARENA KINETIC SIGNATURE HEADERS
# ============================================================
def render_apriori_energy_conduits_html(top_rules_df=None) -> str:
    """
    Renders discovered Apriori association rules as Interactive Force-Directed
    Bezier energy conduits with golden particle stream velocity proportional to Lift.
    """
    rules_data = [
        {"ant": "Athletics", "con": "Swimming", "lift": 2.85, "conf": "68.4%"},
        {"ant": "Cross Country Skiing", "con": "Biathlon", "lift": 3.42, "conf": "81.2%"},
        {"ant": "Gymnastics", "con": "Diving", "lift": 2.15, "conf": "59.0%"},
        {"ant": "Cycling", "con": "Triathlon", "lift": 3.10, "conf": "74.8%"}
    ]

    conduits_svg = []
    y_start = 45
    for idx, r in enumerate(rules_data):
        y = y_start + idx * 52
        lift_val = float(r["lift"])
        speed_sec = round(max(0.8, 4.0 / lift_val), 2)
        conduits_svg.append(f"""
        <g class="apriori-conduit-pair" style="cursor: pointer;">
            <!-- Antecedent Node (Left) -->
            <rect x="25" y="{y - 16}" width="150" height="32" rx="8" fill="#1C1B19" stroke="#D4AF37" stroke-width="1.2"/>
            <text x="100" y="{y + 4}" fill="#FAF8F2" font-family="'Inter', sans-serif" font-size="11" font-weight="700" text-anchor="middle">{r['ant']}</text>

            <!-- Curved Bezier Conduit Arc -->
            <path d="M 175 {y} C 300 {y}, 340 {y}, 465 {y}" fill="none" stroke="rgba(212,175,55,0.25)" stroke-width="2.5" stroke-dasharray="4 4"/>
            <path d="M 175 {y} C 300 {y}, 340 {y}, 465 {y}" fill="none" stroke="#D4AF37" stroke-width="2" stroke-dasharray="14 120" style="animation: aprioriFlow {speed_sec}s linear infinite;"/>

            <!-- Moving Golden Spark along Path -->
            <circle r="4" fill="#D4AF37" filter="drop-shadow(0 0 6px #D4AF37)">
                <animateMotion path="M 175 {y} C 300 {y}, 340 {y}, 465 {y}" dur="{speed_sec}s" repeatCount="indefinite" />
            </circle>

            <!-- Consequent Node (Right) -->
            <rect x="465" y="{y - 16}" width="150" height="32" rx="8" fill="#2E2A25" stroke="#C41E3A" stroke-width="1.2"/>
            <text x="540" y="{y + 4}" fill="#FAF8F2" font-family="'Inter', sans-serif" font-size="11" font-weight="700" text-anchor="middle">{r['con']}</text>

            <!-- Lift Telemetry Badge (Center) -->
            <rect x="290" y="{y - 12}" width="65" height="24" rx="12" fill="#1F1F1F" stroke="#D4AF37" stroke-width="1"/>
            <text x="322" y="{y + 3}" fill="#D4AF37" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="800" text-anchor="middle">{r['lift']}x</text>
        </g>
        """)

    svg_content = "\n".join(conduits_svg)

    return f"""
    <div style="background: linear-gradient(135deg, #1A1917 0%, #262420 100%); border: 1px solid rgba(212,175,55,0.35); border-radius: 14px; padding: 1.2rem; margin-bottom: 1.2rem; color: #FAF8F2;">
        <style>
        @keyframes aprioriFlow {{
            from {{ stroke-dashoffset: 134; }}
            to {{ stroke-dashoffset: 0; }}
        }}
        </style>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
            <div>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #D4AF37; background: rgba(212,175,55,0.15); border: 1px solid rgba(212,175,55,0.4); padding: 0.15rem 0.5rem; border-radius: 9999px; font-weight: 700;">
                    FORCE-DIRECTED ENERGY CONDUITS
                </span>
                <div style="font-family: 'Cinzel', serif; font-size: 1.15rem; font-weight: 800; color: #FAF8F2; margin-top: 0.3rem;">
                    Apriori Multi-Sport Affinity Energy Conduits
                </div>
                <div style="font-size: 0.78rem; color: #8B857C;">
                    Particle velocity streams proportionally to Lift score. Antecedent ━━▶ Consequent.
                </div>
            </div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #D4AF37;">
                LIVE LIFT FLOW
            </div>
        </div>
        <div style="display: flex; justify-content: center; overflow-x: auto;">
            <svg width="640" height="240" viewBox="0 0 640 240" fill="none" xmlns="http://www.w3.org/2000/svg">
                {svg_content}
            </svg>
        </div>
    </div>
    """


def render_centroid_gravity_pulse_html() -> str:
    """
    Renders an animated Centroid Gravity Pulse header where data points visibly orbit
    and snap into their color-coded cluster centroids (#D4AF37, #C41E3A, #2E2A25, #8C6D1F).
    """
    return """
    <div style="background: linear-gradient(135deg, #1C1B19 0%, #292622 100%); border: 1px solid rgba(212,175,55,0.35); border-radius: 14px; padding: 1.2rem; margin-bottom: 1.2rem; color: #FAF8F2;">
        <style>
        @keyframes centroidShockwave {
            0% { r: 16px; opacity: 0.8; stroke-width: 2.5px; }
            100% { r: 52px; opacity: 0; stroke-width: 0.5px; }
        }
        @keyframes orbitCW {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        @keyframes orbitCCW {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(-360deg); }
        }
        </style>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
            <div>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #D4AF37; background: rgba(212,175,55,0.15); border: 1px solid rgba(212,175,55,0.4); padding: 0.15rem 0.5rem; border-radius: 9999px; font-weight: 700;">
                    UNSUPERVISED GRAVITATIONAL PHYSICS
                </span>
                <div style="font-family: 'Cinzel', serif; font-size: 1.15rem; font-weight: 800; color: #FAF8F2; margin-top: 0.3rem;">
                    K-Means & Hierarchical Centroid Gravity Field
                </div>
                <div style="font-size: 0.78rem; color: #8B857C;">
                    Nations snap to athletic DNA centroids: Superpowers (Gold), Powerhouses (Red), Contenders (Charcoal).
                </div>
            </div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #D4AF37;">
                K=3 GRAVITY HUBS
            </div>
        </div>

        <div style="display: flex; justify-content: center; overflow-x: auto;">
            <svg width="680" height="180" viewBox="0 0 680 180" fill="none" xmlns="http://www.w3.org/2000/svg">
                <!-- CENTROID 1: Global Superpowers (Gold) -->
                <g transform="translate(130, 90)">
                    <circle cx="0" cy="0" r="16" stroke="#D4AF37" fill="none" style="animation: centroidShockwave 2.8s ease-out infinite;"/>
                    <circle cx="0" cy="0" r="18" fill="rgba(212,175,55,0.25)" stroke="#D4AF37" stroke-width="2"/>
                    <circle cx="0" cy="0" r="7" fill="#D4AF37"/>
                    <text x="0" y="36" fill="#D4AF37" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="700" text-anchor="middle">μ1 Superpowers</text>
                    <!-- Orbiting Nodes -->
                    <g style="transform-origin: 0 0; animation: orbitCW 6s linear infinite;">
                        <circle cx="38" cy="0" r="3.5" fill="#FAF8F2"/>
                        <circle cx="-32" cy="18" r="4" fill="#FAF8F2"/>
                        <circle cx="8" cy="-35" r="3" fill="#D4AF37"/>
                    </g>
                </g>

                <!-- Gravitational Force Lines -->
                <path d="M 170 90 L 300 90" stroke="rgba(212,175,55,0.2)" stroke-dasharray="3 3"/>

                <!-- CENTROID 2: Specialist Powerhouses (Red) -->
                <g transform="translate(340, 90)">
                    <circle cx="0" cy="0" r="16" stroke="#C41E3A" fill="none" style="animation: centroidShockwave 2.8s ease-out infinite 0.9s;"/>
                    <circle cx="0" cy="0" r="18" fill="rgba(196,30,58,0.25)" stroke="#C41E3A" stroke-width="2"/>
                    <circle cx="0" cy="0" r="7" fill="#C41E3A"/>
                    <text x="0" y="36" fill="#C41E3A" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="700" text-anchor="middle">μ2 Specialists</text>
                    <!-- Orbiting Nodes -->
                    <g style="transform-origin: 0 0; animation: orbitCCW 8s linear infinite;">
                        <circle cx="34" cy="-14" r="3.5" fill="#FAF8F2"/>
                        <circle cx="-30" cy="-20" r="3" fill="#FAF8F2"/>
                        <circle cx="5" cy="35" r="4" fill="#C41E3A"/>
                    </g>
                </g>

                <!-- Gravitational Force Lines -->
                <path d="M 380 90 L 510 90" stroke="rgba(212,175,55,0.2)" stroke-dasharray="3 3"/>

                <!-- CENTROID 3: Emerging Contenders (Sandstone/Charcoal) -->
                <g transform="translate(550, 90)">
                    <circle cx="0" cy="0" r="16" stroke="#E8D9C3" fill="none" style="animation: centroidShockwave 2.8s ease-out infinite 1.8s;"/>
                    <circle cx="0" cy="0" r="18" fill="rgba(232,217,195,0.2)" stroke="#E8D9C3" stroke-width="2"/>
                    <circle cx="0" cy="0" r="7" fill="#E8D9C3"/>
                    <text x="0" y="36" fill="#E8D9C3" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="700" text-anchor="middle">μ3 Contenders</text>
                    <!-- Orbiting Nodes -->
                    <g style="transform-origin: 0 0; animation: orbitCW 10s linear infinite;">
                        <circle cx="36" cy="12" r="3" fill="#FAF8F2"/>
                        <circle cx="-28" cy="22" r="3.5" fill="#FAF8F2"/>
                        <circle cx="-12" cy="-32" r="3" fill="#E8D9C3"/>
                    </g>
                </g>
            </svg>
        </div>
    </div>
    """


def render_bifurcating_tree_svg_html() -> str:
    """
    Renders an animated Bifurcating Golden Tree SVG where a glowing pulse
    travels down the decision branches from Root to Leaf (Gold/Silver/Bronze outcome).
    """
    return """
    <div style="background: linear-gradient(135deg, #1C1B19 0%, #292622 100%); border: 1px solid rgba(212,175,55,0.35); border-radius: 14px; padding: 1.2rem; margin-bottom: 1.2rem; color: #FAF8F2;">
        <style>
        @keyframes treePulseFlow {
            0% { stroke-dashoffset: 180; }
            100% { stroke-dashoffset: 0; }
        }
        .tree-pulse-path {
            stroke-dasharray: 20 160;
            animation: treePulseFlow 2.8s cubic-bezier(0.4, 0, 0.2, 1) infinite;
        }
        </style>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
            <div>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #D4AF37; background: rgba(212,175,55,0.15); border: 1px solid rgba(212,175,55,0.4); padding: 0.15rem 0.5rem; border-radius: 9999px; font-weight: 700;">
                    SUPERVISED DECISION GRAPH
                </span>
                <div style="font-family: 'Cinzel', serif; font-size: 1.15rem; font-weight: 800; color: #FAF8F2; margin-top: 0.3rem;">
                    Bifurcating Decision Tree & Naive Bayes Branching
                </div>
                <div style="font-size: 0.78rem; color: #8B857C;">
                    Entropy-driven recursive binary splits from Context Root to Podium Leaves.
                </div>
            </div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #D4AF37;">
                DECISION FLOW
            </div>
        </div>

        <div style="display: flex; justify-content: center; overflow-x: auto;">
            <svg width="660" height="210" viewBox="0 0 660 210" fill="none" xmlns="http://www.w3.org/2000/svg">
                <!-- ROOT NODE -->
                <rect x="250" y="10" width="160" height="34" rx="8" fill="#1F1F1F" stroke="#D4AF37" stroke-width="1.8"/>
                <text x="330" y="32" fill="#FAF8F2" font-family="'Inter', sans-serif" font-size="11" font-weight="800" text-anchor="middle">Root: Event Gender & NOC</text>

                <!-- Branch lines to Level 1 -->
                <path d="M 330 44 L 180 85" stroke="rgba(212,175,55,0.3)" stroke-width="2"/>
                <path d="M 330 44 L 180 85" stroke="#D4AF37" stroke-width="2.5" class="tree-pulse-path"/>

                <path d="M 330 44 L 480 85" stroke="rgba(212,175,55,0.3)" stroke-width="2"/>
                <path d="M 330 44 L 480 85" stroke="#D4AF37" stroke-width="2.5" class="tree-pulse-path" style="animation-delay: 0.4s;"/>

                <!-- LEVEL 1 NODES -->
                <rect x="100" y="85" width="160" height="32" rx="8" fill="#2E2A25" stroke="#E8D9C3" stroke-width="1.2"/>
                <text x="180" y="105" fill="#FAF8F2" font-family="'Inter', sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">Discipline Dominance ≤ 0.45</text>

                <rect x="400" y="85" width="160" height="32" rx="8" fill="#2E2A25" stroke="#E8D9C3" stroke-width="1.2"/>
                <text x="480" y="105" fill="#FAF8F2" font-family="'Inter', sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">Discipline Dominance &gt; 0.45</text>

                <!-- Branch lines to Leaf Nodes -->
                <path d="M 180 117 L 90 155" stroke="rgba(212,175,55,0.3)" stroke-width="2"/>
                <path d="M 180 117 L 90 155" stroke="#AA820A" stroke-width="2.5" class="tree-pulse-path" style="animation-delay: 0.8s;"/>

                <path d="M 180 117 L 250 155" stroke="rgba(212,175,55,0.3)" stroke-width="2"/>
                <path d="M 180 117 L 250 155" stroke="#FFFFFF" stroke-width="2.5" class="tree-pulse-path" style="animation-delay: 1.0s;"/>

                <path d="M 480 117 L 410 155" stroke="rgba(212,175,55,0.3)" stroke-width="2"/>
                <path d="M 480 117 L 410 155" stroke="#FFFFFF" stroke-width="2.5" class="tree-pulse-path" style="animation-delay: 1.1s;"/>

                <path d="M 480 117 L 570 155" stroke="rgba(212,175,55,0.3)" stroke-width="2"/>
                <path d="M 480 117 L 570 155" stroke="#D4AF37" stroke-width="2.5" class="tree-pulse-path" style="animation-delay: 1.2s;"/>

                <!-- LEAF NODES (Podium Outcomes) -->
                <!-- Bronze -->
                <rect x="30" y="155" width="120" height="36" rx="8" fill="#2E2A25" stroke="#AA820A" stroke-width="1.5"/>
                <text x="90" y="177" fill="#D4AF37" font-family="'Cinzel', serif" font-size="11" font-weight="800" text-anchor="middle">🥉 BRONZE (62%)</text>

                <!-- Silver Left -->
                <rect x="190" y="155" width="120" height="36" rx="8" fill="#2E2A25" stroke="#FFFFFF" stroke-width="1.5"/>
                <text x="250" y="177" fill="#FFFFFF" font-family="'Cinzel', serif" font-size="11" font-weight="800" text-anchor="middle">🥈 SILVER (71%)</text>

                <!-- Silver Right -->
                <rect x="350" y="155" width="120" height="36" rx="8" fill="#2E2A25" stroke="#FFFFFF" stroke-width="1.5"/>
                <text x="410" y="177" fill="#FFFFFF" font-family="'Cinzel', serif" font-size="11" font-weight="800" text-anchor="middle">🥈 SILVER (75%)</text>

                <!-- Gold -->
                <rect x="510" y="155" width="120" height="36" rx="8" fill="#1F1F1F" stroke="#D4AF37" stroke-width="2" filter="drop-shadow(0 0 8px rgba(212,175,55,0.4))"/>
                <text x="570" y="177" fill="#D4AF37" font-family="'Cinzel', serif" font-size="11" font-weight="900" text-anchor="middle">🥇 GOLD (88.4%)</text>
            </svg>
        </div>
    </div>
    """


# ============================================================
# 12. STAR SCHEMA WAREHOUSE: INTERACTIVE BLUEPRINT & CONDUITS
# ============================================================
def render_star_schema_blueprint_html(counts: dict | None = None) -> str:
    """
    Renders the full-width Interactive SVG Star Schema Blueprint:
    fact_medal (20,582 rows) as a glowing 3D Octagonal Gold Core surrounded
    by 5 dimension nodes (dim_game, dim_country, dim_sport, dim_event, dim_medal).
    Triple-layered animated circuit conduits with moving gold data packets into center.
    Hovering any dimension node highlights its foreign-key conduit in Victory Red
    and previews its live schema columns.
    """
    if not counts:
        counts = {
            "fact_medal": 20582,
            "dim_game": 54,
            "dim_country": 206,
            "dim_sport": 47,
            "dim_event": 1017,
            "dim_medal": 3
        }

    fact_cnt = counts.get("fact_medal", 20582)
    game_cnt = counts.get("dim_game", 54)
    ctry_cnt = counts.get("dim_country", 206)
    sport_cnt = counts.get("dim_sport", 47)
    event_cnt = counts.get("dim_event", 1017)
    medal_cnt = counts.get("dim_medal", 3)

    return f"""
    <div class="star-schema-blueprint-card">
        <style>
        .star-schema-blueprint-card {{
            background: linear-gradient(135deg, #1C1B19 0%, #292622 100%);
            border: 1px solid rgba(212, 175, 55, 0.4);
            border-radius: 18px;
            padding: 1.8rem;
            color: #FAF8F2;
            position: relative;
            overflow: hidden;
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.35);
            margin-bottom: 2rem;
        }}
        @keyframes starPacketFlow {{
            0% {{ stroke-dashoffset: 160; }}
            100% {{ stroke-dashoffset: 0; }}
        }}
        @keyframes corePulseGlow {{
            0% {{ filter: drop-shadow(0 0 12px rgba(212, 175, 55, 0.4)); }}
            50% {{ filter: drop-shadow(0 0 28px rgba(212, 175, 55, 0.85)); }}
            100% {{ filter: drop-shadow(0 0 12px rgba(212, 175, 55, 0.4)); }}
        }}
        .star-circuit-base {{
            stroke: rgba(232, 217, 195, 0.2);
            stroke-width: 2.5;
            fill: none;
        }}
        .star-packet-stream {{
            stroke: #D4AF37;
            stroke-width: 2.5;
            stroke-dasharray: 16 120;
            fill: none;
            animation: starPacketFlow 2.4s linear infinite;
        }}
        .dim-node-card {{
            cursor: pointer;
            transition: transform 240ms cubic-bezier(0.22, 1, 0.36, 1);
        }}
        .dim-node-card:hover {{
            transform: scale(1.04);
        }}
        .dim-node-card:hover rect {{
            stroke: #C41E3A !important;
            stroke-width: 2.2 !important;
        }}
        </style>

        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.2rem; flex-wrap: wrap; gap: 0.8rem;">
            <div>
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.3rem;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #D4AF37; background: rgba(212,175,55,0.15); border: 1px solid rgba(212,175,55,0.4); padding: 0.2rem 0.6rem; border-radius: 9999px; font-weight: 700;">
                        STAR SCHEMA RELATIONAL TOPOLOGY
                    </span>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #E8D9C3;">
                        SQLite 3 • Normalized Dimensions (3NF) • Central Fact (20,582 Rows)
                    </span>
                </div>
                <h2 style="font-family: 'Cinzel', serif; font-size: 1.8rem; font-weight: 800; color: #FAF8F2; margin: 0;">
                    Interactive Star Schema Circuit Blueprint
                </h2>
                <div style="font-size: 0.84rem; color: #8B857C; margin-top: 0.3rem;">
                    Triple-layered circuit conduits stream normalized dimension keys into the central fact table.
                    Hover any dimension node to isolate its foreign-key linkage.
                </div>
            </div>
            <div style="background: rgba(212,175,55,0.12); border: 1px solid rgba(212,175,55,0.3); border-radius: 10px; padding: 0.6rem 1rem; text-align: right;">
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #8B857C; text-transform: uppercase;">Central Fact Table</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.3rem; font-weight: 900; color: #D4AF37;">{fact_cnt:,} Rows</div>
            </div>
        </div>

        <div style="display: flex; justify-content: center; overflow-x: auto; padding: 0.8rem 0;">
            <svg width="860" height="420" viewBox="0 0 860 420" fill="none" xmlns="http://www.w3.org/2000/svg">
                <!-- Circuit Lines to Central Fact (Center: 430, 210) -->
                <!-- 1. dim_game (Top: 430, 45) -->
                <path d="M 430 80 L 430 160" class="star-circuit-base"/>
                <path d="M 430 80 L 430 160" class="star-packet-stream" style="animation-delay: 0s;"/>

                <!-- 2. dim_country (Top Left: 150, 80) -->
                <path d="M 230 110 C 300 130, 340 180, 380 195" class="star-circuit-base"/>
                <path d="M 230 110 C 300 130, 340 180, 380 195" class="star-packet-stream" style="animation-delay: 0.4s;"/>

                <!-- 3. dim_sport (Top Right: 710, 80) -->
                <path d="M 630 110 C 560 130, 520 180, 480 195" class="star-circuit-base"/>
                <path d="M 630 110 C 560 130, 520 180, 480 195" class="star-packet-stream" style="animation-delay: 0.8s;"/>

                <!-- 4. dim_event (Bottom Right: 710, 340) -->
                <path d="M 630 310 C 560 290, 520 240, 480 225" class="star-circuit-base"/>
                <path d="M 630 310 C 560 290, 520 240, 480 225" class="star-packet-stream" style="animation-delay: 1.2s;"/>

                <!-- 5. dim_medal (Bottom Left: 150, 340) -->
                <path d="M 230 310 C 300 290, 340 240, 380 225" class="star-circuit-base"/>
                <path d="M 230 310 C 300 290, 340 240, 380 225" class="star-packet-stream" style="animation-delay: 1.6s;"/>

                <!-- CENTRAL FACT TABLE: fact_medal (Octagon) -->
                <g transform="translate(430, 210)" style="animation: corePulseGlow 3.5s ease-in-out infinite;">
                    <polygon points="0,-48 34,-34 48,0 34,34 0,48 -34,34 -48,0 -34,-34" fill="#1C1B19" stroke="#D4AF37" stroke-width="3"/>
                    <circle cx="0" cy="0" r="28" fill="rgba(212,175,55,0.22)" stroke="#AA820A" stroke-width="1.5"/>
                    <text x="0" y="-8" fill="#FFFFFF" font-family="'Cinzel', serif" font-size="12" font-weight="900" text-anchor="middle">fact_medal</text>
                    <text x="0" y="8" fill="#D4AF37" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="800" text-anchor="middle">{fact_cnt:,}</text>
                    <text x="0" y="21" fill="#8B857C" font-family="'Inter', sans-serif" font-size="7.5" text-anchor="middle">CENTRAL FACT</text>
                </g>

                <!-- 1. DIM_GAME (Top Center) -->
                <g class="dim-node-card" transform="translate(340, 15)">
                    <rect x="0" y="0" width="180" height="65" rx="10" fill="#2E2A25" stroke="#D4AF37" stroke-width="1.5"/>
                    <text x="12" y="20" fill="#FAF8F2" font-family="'Cinzel', serif" font-size="12" font-weight="800">dim_game</text>
                    <text x="168" y="20" fill="#D4AF37" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="700" text-anchor="end">{game_cnt} rows</text>
                    <line x1="12" y1="28" x2="168" y2="28" stroke="rgba(255,255,255,0.1)"/>
                    <text x="12" y="42" fill="#D4AF37" font-family="'JetBrains Mono', monospace" font-size="9">PK: game_id</text>
                    <text x="12" y="55" fill="#8B857C" font-family="'JetBrains Mono', monospace" font-size="8.5">year • season • games</text>
                </g>

                <!-- 2. DIM_COUNTRY (Top Left) -->
                <g class="dim-node-card" transform="translate(50, 75)">
                    <rect x="0" y="0" width="180" height="65" rx="10" fill="#2E2A25" stroke="#D4AF37" stroke-width="1.5"/>
                    <text x="12" y="20" fill="#FAF8F2" font-family="'Cinzel', serif" font-size="12" font-weight="800">dim_country</text>
                    <text x="168" y="20" fill="#D4AF37" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="700" text-anchor="end">{ctry_cnt} rows</text>
                    <line x1="12" y1="28" x2="168" y2="28" stroke="rgba(255,255,255,0.1)"/>
                    <text x="12" y="42" fill="#D4AF37" font-family="'JetBrains Mono', monospace" font-size="9">PK: country_id</text>
                    <text x="12" y="55" fill="#8B857C" font-family="'JetBrains Mono', monospace" font-size="8.5">country_code • country_name</text>
                </g>

                <!-- 3. DIM_SPORT (Top Right) -->
                <g class="dim-node-card" transform="translate(630, 75)">
                    <rect x="0" y="0" width="180" height="65" rx="10" fill="#2E2A25" stroke="#D4AF37" stroke-width="1.5"/>
                    <text x="12" y="20" fill="#FAF8F2" font-family="'Cinzel', serif" font-size="12" font-weight="800">dim_sport</text>
                    <text x="168" y="20" fill="#D4AF37" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="700" text-anchor="end">{sport_cnt} rows</text>
                    <line x1="12" y1="28" x2="168" y2="28" stroke="rgba(255,255,255,0.1)"/>
                    <text x="12" y="42" fill="#D4AF37" font-family="'JetBrains Mono', monospace" font-size="9">PK: sport_id</text>
                    <text x="12" y="55" fill="#8B857C" font-family="'JetBrains Mono', monospace" font-size="8.5">sport_name (UNIQUE)</text>
                </g>

                <!-- 4. DIM_EVENT (Bottom Right) -->
                <g class="dim-node-card" transform="translate(630, 275)">
                    <rect x="0" y="0" width="180" height="65" rx="10" fill="#2E2A25" stroke="#D4AF37" stroke-width="1.5"/>
                    <text x="12" y="20" fill="#FAF8F2" font-family="'Cinzel', serif" font-size="12" font-weight="800">dim_event</text>
                    <text x="168" y="20" fill="#D4AF37" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="700" text-anchor="end">{event_cnt:,} rows</text>
                    <line x1="12" y1="28" x2="168" y2="28" stroke="rgba(255,255,255,0.1)"/>
                    <text x="12" y="42" fill="#D4AF37" font-family="'JetBrains Mono', monospace" font-size="9">PK: event_id • FK: sport_id</text>
                    <text x="12" y="55" fill="#8B857C" font-family="'JetBrains Mono', monospace" font-size="8.5">event_name • event_gender</text>
                </g>

                <!-- 5. DIM_MEDAL (Bottom Left) -->
                <g class="dim-node-card" transform="translate(50, 275)">
                    <rect x="0" y="0" width="180" height="65" rx="10" fill="#2E2A25" stroke="#D4AF37" stroke-width="1.5"/>
                    <text x="12" y="20" fill="#FAF8F2" font-family="'Cinzel', serif" font-size="12" font-weight="800">dim_medal</text>
                    <text x="168" y="20" fill="#D4AF37" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="700" text-anchor="end">{medal_cnt} rows</text>
                    <line x1="12" y1="28" x2="168" y2="28" stroke="rgba(255,255,255,0.1)"/>
                    <text x="12" y="42" fill="#D4AF37" font-family="'JetBrains Mono', monospace" font-size="9">PK: medal_id</text>
                    <text x="12" y="55" fill="#8B857C" font-family="'JetBrains Mono', monospace" font-size="8.5">medal_name • medal_points (3,2,1)</text>
                </g>
            </svg>
        </div>
    </div>
    """

