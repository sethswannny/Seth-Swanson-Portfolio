const glow = document.querySelector(".cursor-glow");

window.addEventListener("pointermove", (event) => {
  if (!glow) return;
  glow.style.left = `${event.clientX}px`;
  glow.style.top = `${event.clientY}px`;
});

for (const card of document.querySelectorAll("[data-tilt]")) {
  card.addEventListener("pointermove", (event) => {
    const rect = card.getBoundingClientRect();
    const x = (event.clientX - rect.left) / rect.width - 0.5;
    const y = (event.clientY - rect.top) / rect.height - 0.5;
    card.style.transform = `rotateX(${y * -5}deg) rotateY(${x * 5}deg) translateY(-3px)`;
  });

  card.addEventListener("pointerleave", () => {
    card.style.transform = "";
  });
}

const systemSection = document.querySelector(".system-strip");

if (systemSection) {
  systemSection.addEventListener("pointermove", (event) => {
    const rect = systemSection.getBoundingClientRect();
    const x = ((event.clientX - rect.left) / rect.width - 0.5) * 28;
    const y = ((event.clientY - rect.top) / rect.height - 0.5) * 28;
    systemSection.style.setProperty("--system-x", `${x}px`);
    systemSection.style.setProperty("--system-y", `${y}px`);
  });
}
