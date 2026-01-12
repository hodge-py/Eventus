document.getElementById('mainSender').addEventListener("submit", async event => {
    event.preventDefault();
    const emailValue = document.getElementById("email").value
    
    const data = {
        email: emailValue,
    };

    try {
        const response = await fetch('/emailSent', {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json' // Tell server you're sending JSON
            },
            body: JSON.stringify(data) // Convert JS object to JSON string
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log('Success:', result);
        document.getElementById('emailVisual').textContent = "The event page link has been sent to your email";

    } catch (error) {
        console.error('Error:', error);
    }

})