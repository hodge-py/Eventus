document.getElementById("titleButton").addEventListener('click', async event => {
    console.log("test")
    
    let titleValue = document.getElementById('titleData').value;

    console.log(titleValue)

    const pathParts = window.location.pathname.split('/');
    const secretToken = pathParts[pathParts.length - 1];

    data = {
        "title": titleValue,
        "secret": secretToken
    }

    const response = await fetch(`/admin/titleSave`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    console.log(result)
    alert("Title Saved!")
})

document.getElementById("descriptionSave").addEventListener('click', async event => {
    console.log("test")
    
    let titleValue = document.getElementById('description-sub').value;

    const pathParts = window.location.pathname.split('/');
    const secretToken = pathParts[pathParts.length - 1];

    data = {
        "description": titleValue,
        "secret": secretToken
    }

    const response = await fetch(`/admin/titleSave`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    console.log(result)
    alert("Description Saved!")
})

document.getElementById("dateSaver").addEventListener('click', async event => {    
    let startValue = document.getElementById('startTimeVal').value;

    let endValue = document.getElementById('endTimeVal').value;

    const pathParts = window.location.pathname.split('/');
    const secretToken = pathParts[pathParts.length - 1];

    data = {
        "start": startValue,
        "end": endValue,
        "secret": secretToken
    }

    const response = await fetch(`/admin/titleSave`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    console.log(result)
    alert("Dates Saved!")
})

document.getElementById("savePic").addEventListener('click', async event => {   
    const fileGet = document.getElementById('picFile')
    const file = fileGet.files[0];
    if (!file) {
        alert("Please select a file.");
        return;
    }

    const pathParts = window.location.pathname.split('/');
    const secretToken = pathParts[pathParts.length - 1];

    const formData = new FormData();
    formData.append('file', file);
    formData.append('secret',secretToken)

    const response = await fetch(`/admin/titleSave`, {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    console.log(result)
    alert("Picture Saved!")
})