const dataToSend = { 0: "Hello World" };
chrome.runtime.sendMessage({ action: 'resume', data: dataToSend }, response => {
    if (chrome.runtime.lastError) {
        console.error(chrome.runtime.lastError.message);
    } else if (response) {
        console.log(`Received result: ${response.result}`);
        // Handle the result as needed
    }
});

