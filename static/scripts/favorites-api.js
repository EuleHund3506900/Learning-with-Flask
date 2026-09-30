(() => {
    const storage = window.localStorage;
    let syncPromise;
    let completedSyncPromise;

    const getFavoriteStorageKeys = () => Object.keys(storage)
        .filter((key) => key.endsWith('++favorite'));

    const setLocalFavorite = (filepath, active) => {
        const key = `${filepath}++favorite`;
        if (active) {
            storage.setItem(key, 'true');
        } else {
            storage.removeItem(key);
        }
    };

    const isApiResponse = (response) => response.ok
        && !response.redirected
        && response.headers.get('content-type')?.includes('application/json');

    const requestFavorites = async (options = {}) => {
        const response = await fetch('/api/favorites', {
            credentials: 'same-origin',
            ...options,
        });
        if (!isApiResponse(response)) {
            throw new Error('Favorites API unavailable');
        }
        return response.json();
    };

    const syncFavorites = () => {
        if (!syncPromise) {
            syncPromise = requestFavorites().then((data) => {
                getFavoriteStorageKeys().forEach((key) => storage.removeItem(key));
                data.favorites.forEach((favorite) => setLocalFavorite(favorite.item_url, true));
                window.dispatchEvent(new Event('favorites-synced'));
                return data.favorites;
            });
        }
        return syncPromise;
    };

    const saveFavorite = async (filepath, active) => {
        await requestFavorites({
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ item_url: filepath, favorite: active }),
        });
    };

    const syncCompleted = () => {
        if (!completedSyncPromise) {
            completedSyncPromise = requestStatus('/api/completed', 'completed')
                .then((items) => {
                    getStorageKeys('complete').forEach((key) => storage.removeItem(key));
                    items.forEach((item) => setLocalStatus(item.item_url, 'complete', true));
                    return items;
                });
        }
        return completedSyncPromise;
    };

    const requestStatus = async (url, property) => {
        const response = await fetch(url, { credentials: 'same-origin' });
        if (!isApiResponse(response)) {
            throw new Error('Status API unavailable');
        }
        const data = await response.json();
        return data[property];
    };

    const getStorageKeys = (status) => Object.keys(storage)
        .filter((key) => key.endsWith(`++${status}`));

    const setLocalStatus = (filepath, status, active) => {
        const key = `${filepath}++${status}`;
        if (active) {
            storage.setItem(key, 'true');
        } else {
            storage.removeItem(key);
        }
    };

    const saveCompleted = async (filepath, active) => {
        const response = await fetch('/api/completed', {
            method: 'POST',
            credentials: 'same-origin',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ item_url: filepath, completed: active }),
        });
        if (!isApiResponse(response)) {
            throw new Error('Completed API unavailable');
        }
    };

    window.favoriteApi = {
        setLocalFavorite,
        syncFavorites,
        saveFavorite,
        syncCompleted,
        saveCompleted,
    };

    syncFavorites().catch(() => {});
})();
