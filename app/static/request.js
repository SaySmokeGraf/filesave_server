async function apiRequest(url, options = {}, method = 'GET', contentType = 'application/json') {
    const token = getCookie('auth_token');
    if (!token) {
        return {
            error: 'No authentication token found. Please log in.',
            status: 401,
            body: null
        };
    } else {
        // Если body — обычный объект, преобразуем в JSON
        if (options.body && typeof options.body === 'object' && !(options.body instanceof FormData) && !(options.body instanceof File)) {
            options.body = JSON.stringify(options.body);
        }

        const config = {
            method: method,
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': contentType,
                ...options.headers
            },
            ...options
        };

        const response = await fetch(url, config);
        // if (response.status === 401) {
        //     window.location.href = '/site/registration.html';
        //     // Важно: дальше код не должен выполняться
        //     return; // или throw, если хочешь явно показать, что запрос не завершился
        // }

        if (!response.ok) {
            return {
                error: `HTTP error! status: ${response.status}`,
                status: response.status,
                body: await response.text()
            };
        }

        return response;
    }
}
