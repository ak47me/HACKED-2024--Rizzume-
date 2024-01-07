// background.js

// Listen for messages from content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'sendData') {
      fetch('http://127.0.0.1:5000/process_data', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(message.data)
      })
      .then(response => response.json())
      .then(data => {
          // Send the response back to the content script
          sendResponse({ result: data.result });
      })
      .catch(error => {
          console.error('Error:', error);
      });
    }
    return true;  // Indicates the asynchronous sendResponse is used
  });
  