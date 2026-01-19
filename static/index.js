document.getElementById('mainSender').addEventListener("submit", async event => {
    event.preventDefault();
    
    data = {
        "email": "test"
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
        document.getElementById('emailVisual').innerHTML = `<div>The event page links have been generated! Admin access link:
        <a href=${result.admin} target=_blank>${result.admin}</a> | Public access link: <a target=_blank href=${result.public}>${result.public}</a> | Please save the links somewhere 
        secure as they will disappear once the page is reloaded</div>`;

    } catch (error) {
        console.error('Error:', error);
    }

})