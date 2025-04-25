document.addEventListener("DOMContentLoaded", function () {
    var s = document.createElement('script');
    s.src = chrome.runtime.getURL('shift.js');
    (document.head || document.documentElement).appendChild(s);

    var ss = document.createElement('script');
    ss.src = chrome.runtime.getURL('dark.js');
    (document.head || document.documentElement).appendChild(ss);
});