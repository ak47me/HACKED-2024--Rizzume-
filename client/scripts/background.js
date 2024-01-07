chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'resume') {
      fetch('http://127.0.0.1:5000/resume', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(message.data)
      })
      .then(response => {
        console.log(response);
        return response.json()
      })
      .then(data => {
          // Send the response back to the content script
          console.log(data);
          sendResponse({ "result": data.result });
      })
      .catch(error => {
          console.error('Error:', error);
      });
    }
    return true;  // Indicates the asynchronous sendResponse is used
  });
  