async function get_cameras_available() {
    const response = await fetch('http://localhost:9090/cameras_available');
    if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
    }
    const json = await response.json();
    let options = '';
    json.forEach(op => {
        options += `<option value="${op}" style="border-radius: 5px;"">Cámara ${op}</option>`
    })
    document.getElementById("cameraAvailableDropdown").innerHTML = options;
    return json;
}
