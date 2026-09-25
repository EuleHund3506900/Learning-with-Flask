const favorite_Content = document.querySelector('.favorite-content');

const ls = window.localStorage;

const decodePathPart = (value) => {
    try {
        return decodeURIComponent(value);
    } catch {
        return value;
    }
};

const getDisplayName = (path) => {
    const fileName = decodePathPart(path.split('/').pop() || '');
    return fileName.replace('.md', '').replace(fileName.replace('.md', '').split('_')[0] + '_', '');
};

const favorites = ls.length > 0 ? Object.keys(ls).filter(key => key.endsWith('++favorite') && ls.getItem(key) === 'true') : [];

if (favorite_Content && favorites.length > 0) {
    favorites.forEach(favorite => {
        const fileName = favorite.split('++')[0];
        const displayName = getDisplayName(fileName);
        const fileLink = `/app/file/${fileName}`;
        const favoriteItem = document.createElement('a');
        favoriteItem.classList.add('file');
        favoriteItem.setAttribute('href', fileLink);
        favoriteItem.innerHTML = `<div class="file-name"><span><i class="ti ti-file file"></i>${displayName}</span></div><i class="ti ti-chevron-right"></i>`;
        favorite_Content.appendChild(favoriteItem);

    });
} else if (favorite_Content) {
    favorite_Content.innerHTML = '<p>Du hast noch keine Favoriten hinzugefügt.</p>';
}

const lastLessonButton = document.querySelector('.last-lesson');
const lastLessonPath = ls.getItem('last-lesson');
const lastLessonName = lastLessonPath ? getDisplayName(lastLessonPath) : null;
const lastLessonCourse = lastLessonPath ? decodePathPart(lastLessonPath.split('Learning/')[1].split('/')[0]) : null;
if (lastLessonButton && lastLessonPath) {
    lastLessonButton.setAttribute('href', lastLessonPath);
    lastLessonButton.innerHTML = `${lastLessonCourse} - ${lastLessonName} <i class="ti ti-arrow-up-right" aria-hidden="true"></i>`;
} else if (lastLessonButton) {
    lastLessonButton.setAttribute('href', '/app/home');
    lastLessonButton.innerHTML = 'Du hast noch keine Lektionen begonnen <i class="ti ti-arrow-up-right" aria-hidden="true"></i>';
}