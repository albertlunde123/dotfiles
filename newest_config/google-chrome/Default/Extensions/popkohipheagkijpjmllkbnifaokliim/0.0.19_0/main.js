const LS = {
    getAllItems: () => chrome.storage.local.get(),
    getItem: async key => (await chrome.storage.local.get(key))[key],
    setItem: (key, val) => chrome.storage.local.set({[key]: val}),
    removeItems: keys => chrome.storage.local.remove(keys),
};

const app = new Vue({
    el: "#app",
    data: {
        shift: 0,
        dark: 0,
        domain: 0,
        opacity: 30,
        color: "#fac563"
    },
    async created() {
        let self = this;

        this.shift = await LS.getItem('shift');
        this.dark = await LS.getItem('dark');
        this.opacity = await LS.getItem('opacityActive')?parseInt(await LS.getItem('opacityActive')):30;
        this.color = await LS.getItem('colorActive')?await LS.getItem('colorActive'):"#fac563";
        
        chrome.tabs.query({active: true, currentWindow: true}, async function(tabs) {

            let url = new URL(tabs[0].url);
            let domain = url.hostname;
            let domains = await LS.getItem('domains');

            if (domains) {
                domains = JSON.parse(domains);
            } else {
                domains = {};
            }
            
            if (domains[domain]) {
                self.domain = 1;
            } else {
                self.domain = 0;
            }


            chrome.tabs.sendMessage(tabs[0].id, {
                name: 'sentOption',
                opacity: self.opacity,
                color: self.color
            }, function(response){
            });
        });
    },
    methods: {

        async switchShift() {
            let dark = !!await LS.getItem('dark');
            let shift = !!await LS.getItem('shift');
            this.shift = !this.shift;
            await LS.setItem('shift', !shift);
            
            chrome.tabs.query({active: true, currentWindow: true}, 
                function(tabs) {

                    chrome.scripting.executeScript({
                        target: {tabId: tabs[0].id},
                        func: function (dark, shift) {
                            localStorage.activeDarkGoogle = dark;
                            localStorage.activeShift = !shift;
                        },
                        args: [dark, shift]
                    });
                
                    chrome.tabs.update(tabs[0].id, {url: tabs[0].url});
                }
            )
            
        },

        async switchDark() {
            let dark = !!await LS.getItem('dark');
            let shift = !!await LS.getItem('shift');
            this.dark = !this.dark;

            await LS.setItem('dark', !dark);

            chrome.tabs.query({active: true, currentWindow: true},
                function(tabs) {

                    if(dark) {
                        chrome.tabs.query({}, function(tabs) {
                            for (var i=0; i<tabs.length; ++i) {
    
                                chrome.scripting.executeScript({
                                    target: {tabId: tabs[i].id},
                                    func: function (dark) {
                                        localStorage.activeDarkGoogle = !dark;
                                    },
                                    args: [dark]
                                });
    
                            }
                        });
                    }
                    
                
                    chrome.scripting.executeScript({
                        target: {tabId: tabs[0].id},
                        func: function (dark, shift) {
                            localStorage.activeDarkGoogle = !dark;
                            localStorage.activeShift = shift;
                        },
                        args: [dark, shift]
                    });
                    
                    chrome.tabs.update(tabs[0].id, {url: tabs[0].url});
                }
            )
        },

        switchDarkDomain() {

            let self = this;

            chrome.tabs.query({active: true, currentWindow: true}, async function(tabs) {
                
                let url = new URL(tabs[0].url);
                let domain = url.hostname;
                let domains = await LS.getItem('domains');
                
                if (domains) {
                    domains = JSON.parse(domains);
                } else {
                    domains = {};
                }

                if (domains[domain]) {
                    delete domains[domain];
                    self.domain = 0;
                    domains = JSON.stringify(domains);
                    await LS.setItem('domains', domains);
                } else {
                    domains[domain] = {};
                    self.domain = 1;
                    domains = JSON.stringify(domains);
                    await LS.setItem('domains', domains);
                }

                chrome.tabs.query({active: true, currentWindow: true}, async function(tabs) {
                    chrome.scripting.executeScript({
                        target: {tabId: tabs[0].id},
                        func: function() {
                            localStorage.activeShift = false;
                            localStorage.activeDarkGoogle = false;
                            window.location.reload();
                        }
                    });
                });
                
            });
            
        },

        changeShift() {
            let self = this;

            chrome.tabs.query({active: true, currentWindow: true}, async function(tabs) {

                await LS.setItem('opacityActive', self.opacity);
                await LS.setItem('colorActive', self.color);

                chrome.tabs.sendMessage(tabs[0].id, {
                    name: 'sentOption',
                    opacity: self.opacity,
                    color: self.color
                }, function(response){
                });
            });
            
        }
        
    }
});