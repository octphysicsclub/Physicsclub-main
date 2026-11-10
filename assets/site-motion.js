(() => {
  const gsap = window.gsap;
  if (!gsap) return;

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const main = document.querySelector("main");
  if (main && !main.querySelector(":scope > .site-motion-atmosphere")) {
    const atmosphere = document.createElement("div");
    atmosphere.className = "site-motion-atmosphere";
    atmosphere.setAttribute("aria-hidden", "true");
    main.prepend(atmosphere);
  }

  if (reduced) return;
  if (window.ScrollTrigger) gsap.registerPlugin(window.ScrollTrigger);

  const intro = gsap.timeline({ defaults: { ease: "power3.out" } });
  const topBar = document.querySelector("body > header");
  if (topBar) intro.fromTo(topBar, { autoAlpha: 0, y: -14 }, { autoAlpha: 1, y: 0, duration: 0.55 });
  const navItems = gsap.utils.toArray("header nav:not(.hidden) > ul > li");
  if (navItems.length) intro.fromTo(navItems, { autoAlpha: 0, y: -8 }, { autoAlpha: 1, y: 0, duration: 0.36, stagger: 0.045 }, "-=0.24");

  const hero = document.querySelector(".hero-animated");
  if (hero) {
    const heroIntro = gsap.timeline({ defaults: { ease: "power3.out" } });
    heroIntro.fromTo(hero.querySelector("h1"), { autoAlpha: 0, y: 26 }, { autoAlpha: 1, y: 0, duration: 0.9, delay: 0.08 });
    heroIntro.fromTo(hero.querySelectorAll(":scope > .relative > p, :scope > .relative > .pt-2 > a"), { autoAlpha: 0, y: 16 }, { autoAlpha: 1, y: 0, duration: 0.62, stagger: 0.12 }, "-=0.48");
    const stats = hero.querySelector(":scope > .relative > .pt-12");
    if (stats) heroIntro.fromTo(stats, { autoAlpha: 0, y: 18 }, { autoAlpha: 1, y: 0, duration: 0.7 }, "-=0.24");
    const aurora = hero.querySelector(".hero-aurora");
    const orbit = hero.querySelector(".hero-orbit");
    const backdrop = hero.querySelector(".hero-backdrop-image");
    if (aurora) gsap.to(aurora, { xPercent: 4, yPercent: -3, scale: 1.1, opacity: 0.96, duration: 12, ease: "sine.inOut", yoyo: true, repeat: -1 });
    if (orbit) gsap.to(orbit, { rotation: 360, duration: 42, ease: "none", repeat: -1 });
    if (backdrop) gsap.to(backdrop, { scale: 1.13, duration: 26, ease: "sine.inOut", yoyo: true, repeat: -1 });
  }

  const atmosphere = document.querySelector(".site-motion-atmosphere");
  if (atmosphere) gsap.to(atmosphere, { xPercent: 3, yPercent: -2, scale: 1.035, opacity: 0.78, duration: 22, ease: "sine.inOut", yoyo: true, repeat: -1 });

  if (window.ScrollTrigger) {
    const revealItems = gsap.utils.toArray("main > section:not(.hero-animated), main .program-card, main .journal-story, main .ypwc-rail, main .article-body figure, main .publication-card");
    revealItems.forEach((item) => {
      gsap.fromTo(item, { autoAlpha: 0, y: 22 }, {
        autoAlpha: 1, y: 0, duration: 0.68, ease: "power2.out",
        scrollTrigger: { trigger: item, start: "top 91%", once: true }
      });
    });
  }

  const menuToggle = document.getElementById("mobile-menu-toggle");
  const drawer = document.getElementById("mobile-nav-drawer");
  if (menuToggle && drawer) {
    menuToggle.addEventListener("click", () => {
      requestAnimationFrame(() => {
        const links = drawer.querySelectorAll("li");
        const hidden = drawer.classList.contains("hidden");
        menuToggle.setAttribute("aria-expanded", String(!hidden));
        if (!hidden) gsap.fromTo(links, { autoAlpha: 0, x: -10 }, { autoAlpha: 1, x: 0, duration: 0.3, stagger: 0.035, clearProps: "all" });
        else if (links.length) {
          drawer.classList.remove("hidden");
          gsap.to(links, { autoAlpha: 0, x: -8, duration: 0.16, stagger: 0.018, onComplete: () => drawer.classList.add("hidden") });
        }
      });
    });
  }

  const hoverTilt = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  if (hoverTilt) {
    document.querySelectorAll(".program-card").forEach((card) => {
      const turnX = gsap.quickTo(card, "rotationX", { duration: 0.34, ease: "power3.out" });
      const turnY = gsap.quickTo(card, "rotationY", { duration: 0.34, ease: "power3.out" });
      card.addEventListener("pointerenter", () => gsap.to(card, { y: -4, scale: 1.006, transformPerspective: 1000, duration: 0.28, ease: "power2.out" }));
      card.addEventListener("pointermove", (event) => {
        const rect = card.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        card.style.setProperty("--pointer-x", `${x}px`);
        card.style.setProperty("--pointer-y", `${y}px`);
        turnX(((0.5 - y / rect.height) * 2.2));
        turnY(((x / rect.width - 0.5) * 3));
      });
      card.addEventListener("pointerleave", () => {
        gsap.to(card, { y: 0, scale: 1, rotationX: 0, rotationY: 0, duration: 0.48, ease: "elastic.out(1, 0.65)", clearProps: "transformPerspective" });
        card.style.setProperty("--pointer-x", "50%");
        card.style.setProperty("--pointer-y", "50%");
      });
    });
  }

  document.querySelectorAll("header nav a, main a[class*='bg-gradient-to-r'], main button").forEach((control) => {
    control.addEventListener("mouseenter", () => gsap.to(control, { y: -2, duration: 0.18, ease: "power2.out" }));
    control.addEventListener("mouseleave", () => gsap.to(control, { y: 0, duration: 0.22, ease: "power2.out" }));
  });


})();
