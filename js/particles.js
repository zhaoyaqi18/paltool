/* ===== Particle System - Floating Fireflies ===== */
(function() {
  const canvas = document.createElement('canvas');
  canvas.style.cssText = 'position:fixed;inset:0;width:100%;height:100%;z-index:1;pointer-events:none';
  canvas.id = 'particle-canvas';
  document.body.prepend(canvas);

  const ctx = canvas.getContext('2d');
  let particles = [];
  let animId = null;

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  window.addEventListener('resize', resize);
  resize();

  const COUNT = 35;
  for (let i = 0; i < COUNT; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      r: 1 + Math.random() * 2,
      speed: 0.15 + Math.random() * 0.3,
      drift: (Math.random() - 0.5) * 0.4,
      phase: Math.random() * Math.PI * 2,
      phaseSpeed: 0.01 + Math.random() * 0.02,
      alpha: 0.3 + Math.random() * 0.5,
      hue: 200 + Math.random() * 40  // blue-ish range
    });
  }

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    for (const p of particles) {
      // Move upward with horizontal drift
      p.y -= p.speed;
      p.x += p.drift + Math.sin(p.phase * 0.5) * 0.3;
      p.phase += p.phaseSpeed;
      
      // Wrap around
      if (p.y < -10) { p.y = canvas.height + 10; p.x = Math.random() * canvas.width; }
      if (p.x < -10) p.x = canvas.width + 10;
      if (p.x > canvas.width + 10) p.x = -10;
      
      // Twinkle
      const twinkle = 0.5 + 0.5 * Math.sin(p.phase);
      const alpha = p.alpha * (0.4 + 0.6 * twinkle);
      const radius = p.r * (0.8 + 0.4 * twinkle);
      
      // Glow
      const grad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, radius * 4);
      grad.addColorStop(0, `rgba(180,220,255,${alpha})`);
      grad.addColorStop(0.3, `rgba(100,180,255,${alpha * 0.4})`);
      grad.addColorStop(1, `rgba(100,180,255,0)`);
      
      ctx.beginPath();
      ctx.arc(p.x, p.y, radius * 4, 0, Math.PI * 2);
      ctx.fillStyle = grad;
      ctx.fill();
      
      // Core
      ctx.beginPath();
      ctx.arc(p.x, p.y, radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(220,240,255,${alpha * 0.9})`;
      ctx.fill();
    }
    
    animId = requestAnimationFrame(draw);
  }

  draw();

  // Stop when page becomes hidden (save resources)
  document.addEventListener('visibilitychange', () => {
    if (document.hidden && animId) {
      cancelAnimationFrame(animId);
      animId = null;
    } else if (!document.hidden && !animId) {
      draw();
    }
  });
})();
