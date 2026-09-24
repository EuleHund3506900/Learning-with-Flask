(() => {
    const storage = window.localStorage;
    const statusNames = ["complete", "favorite"];

    const getElementsForFile = (filepath) => Array.from(document.querySelectorAll("[data-filepath]"))
        .filter((element) => element.dataset.filepath === filepath);

    const isActive = (filepath, status) => storage.getItem(`${filepath}++${status}`) === "true";

    const updateFileStatus = (filepath, status) => {
        const active = isActive(filepath, status);
        getElementsForFile(filepath).forEach((element) => {
            element.querySelectorAll(`[data-status-indicator="${status}"]`).forEach((indicator) => {
                indicator.classList.toggle("is-active", active);
            });
            element.querySelectorAll(`[data-status-action="${status}"]`).forEach((button) => {
                button.setAttribute("aria-pressed", String(active));
                const label = status === "complete"
                    ? (active ? "Lektion als offen markieren" : "Lektion als abgeschlossen markieren")
                    : (active ? "Aus Favoriten entfernen" : "Als Favorit markieren");
                button.setAttribute("aria-label", label);
                const text = button.querySelector("span");
                if (text && status === "complete") {
                    text.textContent = active ? "Abgeschlossen" : "Abschließen";
                }
            });
        });
    };

    const updateAllStatuses = () => {
        document.querySelectorAll("[data-filepath]").forEach((element) => {
            statusNames.forEach((status) => updateFileStatus(element.dataset.filepath, status));
        });
    };

    document.addEventListener("click", (event) => {
        const button = event.target.closest("[data-status-action]");
        if (!button) {
            return;
        }

        event.preventDefault();
        const filepath = button.dataset.filepath;
        const status = button.dataset.statusAction;
        const nextValue = !isActive(filepath, status);
        storage.setItem(`${filepath}++${status}`, String(nextValue));
        updateFileStatus(filepath, status);
    });

    updateAllStatuses();
})();
