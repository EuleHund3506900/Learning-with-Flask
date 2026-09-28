const main_local_storage = window.localStorage;

const main_favorites = main_local_storage.length > 0 ? Object.keys(main_local_storage).filter(key => key.endsWith('++favorite') && main_local_storage.getItem(key) === 'true') : [];

const dropdownContent = document.querySelector('.dropdown-content');

function decodePathPart(value) {
    try {
        return decodeURIComponent(value);
    } catch {
        return value;
    }
};

function getDisplayName(path) {
    const fileName = decodePathPart(path.split('/').pop() || '');
    return fileName.replace('.md', '').replace(fileName.replace('.md', '').split('_')[0] + '_', '');
};

if (main_favorites.length === 0) {
    if (dropdownContent) {
        dropdownContent.innerHTML = '';
        const noFavoritesItem = document.createElement('a');
        noFavoritesItem.innerHTML = '<span>Keine Favoriten</span>';
        dropdownContent.appendChild(noFavoritesItem);
    }
} else {
    dropdownContent.innerHTML = ''; // Clear existing content before adding favorites
    main_favorites.forEach(favorite => {
        const fileName = favorite.split('++')[0];
        const displayName = getDisplayName(fileName);
        const fileLink = `/app/file/${fileName}`;
        const favoriteItem = document.createElement('a');

        if (dropdownContent) {
            favoriteItem.setAttribute('href', fileLink);
            favoriteItem.innerHTML = `<span><i class="ti ti-file file"></i>  ${displayName}</span>`;
            dropdownContent.appendChild(favoriteItem);
        }
    });
}
