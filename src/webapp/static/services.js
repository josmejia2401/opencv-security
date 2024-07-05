const current_host = `${window.location.protocol}//${window.location.host}`


async function get_cameras_available() {
    const response = await fetch(current_host + '/cameras_available');
    if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
    }
    const json = await response.json();
    let options = '';
    json.forEach(op => {
        options += `<option value="${op}" style="border-radius: 5px;"">Cámara ${op}</option>`;
    })
    document.getElementById("cameraAvailableDropdown").innerHTML = options;
    return json;
}

async function selecte_cam(selectObject) {
    const value = selectObject.value;  
    console.log(value);
    const response = await fetch(current_host + '/selected_cam?selected='+value);
    if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
    }
    console.log("selecte_cam", response.text);
}


async function get_dimensions() {
    const response = await fetch(current_host + '/dimensions');
    if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
    }
    const json = await response.json();
    console.log(json)
    let options = '';
    json.forEach(op => {
        options += `<option value="${op}" style="border-radius: 5px;"">${op}</option>`;
    })
    document.getElementById("dimensionsDropdown").innerHTML = options;
    return json;
}

async function selecte_dimensions(selectObject) {
    const value = selectObject.value;  
    console.log(value);
    const response = await fetch(current_host + '/selected_dim?selected='+value);
    if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
    }
    console.log("selecte_cam", response.text);
}