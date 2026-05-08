
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


function cleanCookie(name) {
    // Устанавливаем куку с тем же именем, но пустую и с датой в прошлом
    // path=/ важен, так как кука могла быть установлена для всего сайта
    document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";

    console.log(`Кука ${name} была очищена`);
}