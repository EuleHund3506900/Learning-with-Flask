const courseLocalStorage = window.localStorage;
const courses = document.querySelectorAll("a.course-item");

const getCompletedLectures = (coursePath) => Object.keys(courseLocalStorage)
    .filter((key) => key.startsWith(`${coursePath}/`))
    .filter((key) => key.endsWith("++complete") && courseLocalStorage.getItem(key) === "true");

const updateCourseProgress = async (course) => {
    const coursePath = course.dataset.coursePath;
    const progressBar = course.querySelector(".course-progress");
    const progressFill = course.querySelector(".course-progress-fill");
    const progressLabel = course.querySelector(".course-progress-label");

    try {
        const response = await fetch(`/api/courses/lectures?course_path=${encodeURIComponent(coursePath)}`);
        if (!response.ok) {
            throw new Error("Unable to fetch lecture count");
        }

        const { total_lectures: totalLectures } = await response.json();
        const completedLectures = getCompletedLectures(coursePath).length;
        const progress = totalLectures > 0
            ? Math.min(100, Math.round((completedLectures / totalLectures) * 100))
            : 0;

        progressBar.setAttribute("aria-valuenow", String(progress));
        progressFill.style.width = `${progress}%`;
        progressLabel.textContent = `${progress}%`;
    } catch (error) {
        console.error(`Could not load progress for ${coursePath}`, error);
    }
};

courses.forEach((course) => updateCourseProgress(course));