
const ui_assest_dir  = '/home/lucas-vital/projects/AIRoutineAssistant/Assets/UI';
const userImage = `${ui_assest_dir}/lucasvittal.jpeg`;
const botImage = `${ui_assest_dir}/bot.png`;
const host = 'localhost';
port = 5050;


function createAndAppendMessageBox( imageSrc, messageText, messagesDiv) {
    // Create a new message box
    var messageBox = document.createElement('div');
    messageBox.className = 'message-box';

    // Create an image element for the user
    var image = document.createElement('img');
    image.src = imageSrc;
    image.className = 'user-image';

    // Create a new message element
    var message = document.createElement('p');
    message.innerHTML = messageText;
    message.className = 'user-message';

    // Add the user's name, image, and message to the message box
   
    messageBox.appendChild(image);
    messageBox.appendChild(message);

    // Add the message box to the messages div
    messagesDiv.appendChild(messageBox);
}
 



 
 sendApiRequest = (url, query) => {
    const request_options = {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                
                                body: JSON.stringify({ query: query }),
                            }
    fetch(url, request_options)
        .then(response => response.json())
        .then(data => {

            var messagesDiv = document.querySelector('#messages');
            createAndAppendMessageBox(botImage, data['answer'], messagesDiv);
        
        })
        .catch(error => console.error('Error:', error));
}



window.onload = () => {
    // Get the input box, send button, and messages div
    var inputBox = document.querySelector('#input-area input');
    var sendButton = document.querySelector('#input-area button');
    var messagesDiv = document.querySelector('#messages');

    
    sendButton.addEventListener('click', function() {
    
    var userText = inputBox.value;
    createAndAppendMessageBox(userImage, userText, messagesDiv);

    // Clear the input box
    const query = inputBox.value;
    
    // send api request
    sendApiRequest(`http://${host}:${port}/getAnswer`, query);


    inputBox.value = '';
    });

};