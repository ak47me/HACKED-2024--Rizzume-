const dataToSend = { some_key: 'some_value' };
chrome.runtime.sendMessage({ action: 'sendData', data: dataToSend }, response => {
    if (chrome.runtime.lastError) {
        console.error(chrome.runtime.lastError.message);
    } else if (response) {
        console.log(`Received result: ${response.result}`);
        // Handle the result as needed
    }
});