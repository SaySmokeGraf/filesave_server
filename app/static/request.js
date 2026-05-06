async function apiRequest(url, options = {}, method = 'GET', contentType = 'application/json') {
    const token = getCookie('auth_token');
    if (!token) {
        return {
            error: 'No authentication token found. Please log in.',
            status: 401,
            body: null
        };
    } else {
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