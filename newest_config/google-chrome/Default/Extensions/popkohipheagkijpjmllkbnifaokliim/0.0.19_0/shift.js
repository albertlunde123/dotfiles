/******/ (() => { // webpackBootstrap
var __webpack_exports__ = {};
/*!******************!*\
  !*** ./shift.js ***!
  \******************/
chrome.storage.local.get().then(res => {
  let opacityActive = res['opacityActive'];
  let colorActive = res['colorActive'];
  let url = new URL(window.location.href);
  let domain = url.hostname;
  let domains = res['domains'];

  if (domains) {
    domains = JSON.parse(domains);
  } else {
    domains = {};
  }

  if (!domains[domain] && res['shift']) {
    activeShift();
  }

  function activeShift() {
    let nn = document.getElementById('night_shift_d');

    if (!nn) {
      let div = document.createElement('div');
      div.id = 'night_shift_d';
      div.style.transition = 'opacity 0.1s ease 0s';
      div.style.zIndex = '2147483647';
      div.style.margin = '0';
      div.style.borderRadius = '0';
      div.style.padding = '0';
      div.style.pointerEvents = 'none';
      div.style.position = 'fixed';
      div.style.top = '-10%';
      div.style.right = '-10%';
      div.style.width = '120%';
      div.style.height = '120%';
      div.style.mixBlendMode = 'multiply';
      div.style.display = 'block'; //div.style.setProperty("background", "#fab760", "important");

      if (opacityActive) {
        let opacity = opacityActive / 100;
        div.style.opacity = opacity;
      }

      if (colorActive) {
        let color = colorActive;
        div.style.setProperty("background", color, "important");
      }

      document.documentElement.appendChild(div);
      chrome.runtime.onMessage.addListener((msg, sender, response) => {
        if (msg.opacity || msg.opacity === 0) {
          if (msg.opacity == 0) {
            div.style.opacity = 0;
          } else {
            div.style.opacity = msg.opacity / 100;
          }
        }

        div.style.setProperty("background", msg.color, "important");
        response({});
      });
    }
  }
});
/******/ })()
;
//# sourceMappingURL=shift.js.map