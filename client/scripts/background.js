chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    console.log(message)
    if (message === "currTab") {
        console.log("inside loop")
        chrome.tabs.query({ currentWindow: true, active: true}, (tab)=>{
            console.log(tab[0].url);
            sendResponse(tab[0].url);
        });
    }
});
