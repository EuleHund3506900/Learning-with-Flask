const ls = localStorage;

const favorites = ls.length > 0 ? Object.keys(ls).filter(key => key.endsWith('++favorite') && ls.getItem(key) === 'true') : [];
const completed = ls.length > 0 ? Object.keys(ls).filter(key => key.endsWith('++complete') && ls.getItem(key) === 'true') : [];

const files = document.querySelectorAll('a.file');

files.forEach(file => {
    const fileName = file.dataset.filepath;
    const isFavorite = favorites.includes(`${fileName}++favorite`);
    const favoriteIcon = file.querySelector('.lesson-status-icon[data-status-indicator="favorite"]');
    if(favoriteIcon === null) {
        return;
    }
    if(isFavorite) {
        favoriteIcon.classList.add('is-active');
        favoriteIcon.classList.remove('hidden');
    } else {
        favoriteIcon.classList.remove('is-active');
        favoriteIcon.classList.add('hidden');
    }

    const isCompleted = completed.includes(`${fileName}++complete`);
    const completedIcon = file.querySelector('.lesson-status-icon[data-status-indicator="complete"]');
    if(completedIcon === null) {
        return
    }
    if(isCompleted) {
        completedIcon.classList.add('is-active');
        completedIcon.classList.remove('hidden');
    } else {
        completedIcon.classList.remove('is-active');
        completedIcon.classList.add('hidden');
    }
});