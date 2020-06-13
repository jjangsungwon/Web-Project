// 잠금 해제 저장을 위한 쿠키 생성
var setCookie = function (name, value, exp) {
    var date = new Date();
    date.setTime(date.getTime() + exp * 24 * 60 * 60 * 1000);
    document.cookie = name + '=' + value + ';expires=' + date.toUTCString() + ';';
};

// 지정된 쿠키값을 읽기 위한 함수
var getCookie = function (name) {
    var value = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return value ? value[2] : null;
};

// 지정된 쿠키값을 삭제하는 함수
var deleteCookie = function(name) {
    document.cookie = name + '=; expires=Thu, 01 Jan 1999 00:00:10 GMT;';
}

// 쿠키값을 전부 삭제하는 함수
function clearAllCookies() {  
    var cookies = document.cookie.split(';');  
    for(var i = cookies.length - 1; i>=0; i--){
        document.cookie = cookies[i].split('=')[0] + '=; expires=Thu, 01 Jan 1999 00:00:10 GMT;';
    }
 }
    