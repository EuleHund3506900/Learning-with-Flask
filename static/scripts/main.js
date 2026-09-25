const ls = window.localStorage;

const favorites = ls.length > 0 ? Object.keys(ls).filter(key => key.endsWith('++favorite') && ls.getItem(key) === 'true') : [];

favorites.forEach(favorite => {
    const fileName = favorite.split('++')[0];
    const displayName = getDisplayName(fileName);
    const fileLink = `/app/file/${fileName}`;
    const favoriteItem = document.createElement('a');
    const dropdownContent = document.querySelector('.dropdown-content');
    if (dropdownContent) {
        favoriteItem.classList.add('file');
        favoriteItem.setAttribute('href', fileLink);
        favoriteItem.innerHTML = `<div class="file-name"><span><i class="ti ti-file file"></i>${displayName}</span></div><i class="ti ti-chevron-right"></i>`;
        dropdownContent.appendChild(favoriteItem);
    }
});