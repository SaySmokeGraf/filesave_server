
function setSecureCookie(name, value, days, isSecure = false) {

    console.log(name);
    console.log(days);
    console.log(value);
    let cookieString = `${name}=${encodeURIComponent(value)}; path=/`;

    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        cookieString += `; expires=${date.toUTCString()}`;
    }

    if (isSecure && window.location.protocol === 'http:') {
        cookieString += '; Secure';
    }

    cookieString += '; SameSite=Strict'; // или Lax, в зависимости от требований

    document.cookie = cookieString;
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return decodeURIComponent(parts.pop().split(';').shift());
    // console.log(decodeURIComponent(parts.pop().split(';').shift()));
    return null;
}