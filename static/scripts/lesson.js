const star_icon = document.querySelector(" .ti-star");

const favorite_button = document.querySelector(".ghost");

const complete_button = document.querySelector(".full");

const lesson_title = document.querySelector(".lesson-title");

const reset_button = document.querySelector(".reset-button");

const local_storage = window.localStorage;

if(local_storage.getItem(window.location.pathname.split("/file/")[1] + "++favorite") === "true") {
  star_icon.classList.remove("ti-star");
  star_icon.classList.add("ti-check");
}

if(local_storage.getItem(window.location.pathname.split("/file/")[1] + "++complete") === "true") {
  complete_button.disabled = true;
  lesson_title.innerHTML = lesson_title.innerHTML + "<p class='lesson-complete'><i class='ti ti-check'></i> Abgeschlossen</p>";
    reset_button.classList.remove("hidden");
}

favorite_button.addEventListener("click", () => {
  if (star_icon.classList.contains("ti-star")) {
    star_icon.classList.remove("ti-star");
    star_icon.classList.add("ti-check");
    local_storage.setItem(window.location.pathname.split("/file/")[1] + "++favorite", "true");
  } else {
    star_icon.classList.remove("ti-check");
    star_icon.classList.add("ti-star");
    local_storage.removeItem(window.location.pathname.split("/file/")[1] + "++favorite");
  }

});

complete_button.addEventListener("click", () => {
  if(complete_button.innerHTML.includes("Abschließen")) {
    complete_button.innerHTML = "<i class='ti ti-reload'></i> Status zurücksetzten ";
    local_storage.setItem(window.location.pathname.split("/file/")[1] + "++complete", "true");
    window.navigation.back();
  } else {
    complete_button.innerHTML = "<i class='ti ti-check'></i> Abschließen";
    local_storage.removeItem(window.location.pathname.split("/file/")[1] + "++complete");
    lesson_title.innerHTML = lesson_title.innerHTML.replace("<div class='lesson-complete'><i class='ti ti-check'></i> Abgeschlossen</div>", "");
  }
});

reset_button.addEventListener("click", () => {
  local_storage.removeItem(window.location.pathname.split("/file/")[1] + "++complete");
  complete_button.disabled = false;
  lesson_title.innerHTML = lesson_title.innerHTML.split("<p")[0];
  reset_button.classList.add("hidden");
}
)
