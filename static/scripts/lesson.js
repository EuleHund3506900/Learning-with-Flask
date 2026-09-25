const sidebar = document.querySelector(".lesson-sidebar");
const sidebarToggle = document.querySelector(".lesson-sidebar-toggle");
const sidebarClose = document.querySelector(".lesson-sidebar-close");
const sidebarBackdrop = document.querySelector(".lesson-sidebar-backdrop");

const setSidebarVisibility = (isVisible) => {
    sidebar.classList.toggle("is-open", isVisible);
    sidebarBackdrop.hidden = !isVisible;
    sidebarToggle.setAttribute("aria-expanded", String(isVisible));
};

sidebarToggle.addEventListener("click", () => setSidebarVisibility(true));
sidebarClose.addEventListener("click", () => setSidebarVisibility(false));
sidebarBackdrop.addEventListener("click", () => setSidebarVisibility(false));

document.querySelectorAll(".lesson-tree-folder details").forEach((folder) => {
    folder.addEventListener("toggle", () => {
        folder.closest(".lesson-tree-folder").classList.toggle("is-open", folder.open);
    });
});

const ls = localStorage;

ls.setItem("last-lesson", window.location.pathname);