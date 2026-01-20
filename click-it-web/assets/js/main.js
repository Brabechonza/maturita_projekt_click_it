(function () {
  const path = (location.pathname.split("/").pop() || "index.html").toLowerCase();
  document.querySelectorAll("[data-nav]").forEach(a => {
    const href = (a.getAttribute("href") || "").toLowerCase();
    if ((path === "" && href.includes("index.html")) || href.endsWith(path)) {
      a.classList.add("active");
    }
  });
})();