const favorite_Container = document.querySelector('.favorite-container');

const ls = window.localStorage;

const favorites = ls.length > 0 ? Object.keys(ls).filter(key => key.endsWith('++favorite') && ls.getItem(key) === 'true') : [];

if (favorites.length > 0) {
    favorite_Container.innerHTML = '<h3>Favoriten</h3>';
    favorites.forEach(favorite => {
        const fileName = favorite.split('++')[0];
        const displayName = fileName.split('/').pop().replace('.md', '').replace(fileName.split('/').pop().replace('.md', '').split('_')[0] + '_', '');
        const fileLink = `/app/file/${fileName}`;
        const favoriteItem = document.createElement('a');
        favoriteItem.classList.add('file');
        favoriteItem.setAttribute('href', fileLink);
        favoriteItem.innerHTML = `<div class="file-name"><i class="ti ti-file file"></i><p>${displayName}</p></div><i class="ti ti-chevron-right"></i>`;
        favorite_Container.appendChild(favoriteItem);

    });
} else {
    favorite_Container.innerHTML = '<h3>Favoriten</h3><br /><p>Du hast noch keine Favoriten hinzugefügt.</p>';
}