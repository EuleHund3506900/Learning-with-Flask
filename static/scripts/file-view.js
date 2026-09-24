const files = document.querySelectorAll(".file-container");

const badge_containers = document.querySelectorAll(".file-badge-container");

console.log(files);

const ls = window.localStorage;

files.forEach((file, index) => {
    const href = file.getAttribute("href").split("/file/")[1]
    if(ls.getItem(href + "++complete") === "true") {
        badge_containers[index].innerHTML = badge_containers[index].innerHTML + "<p class='lesson-complete badge'><i class='ti ti-check'></i> Abgeschlossen</p>";
    }
    if(ls.getItem(href + "++favorite") === "true") {
        badge_containers[index].innerHTML = badge_containers[index].innerHTML + "<p class='lesson-favorite badge'><i class='ti ti-star'></i> Favorit</p>";
    }
});