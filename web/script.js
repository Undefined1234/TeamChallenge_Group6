
/**
*@author Constantijn Bok 
*/

/**
 * This function will return for each view (transversal, longitudinal, sagittal) the compressed image from the 3D array. 
 * The images are parsed to HTML by use of the base64 conversion. 
 * 
 * input: -
 * output: -
 */
async function show_view(){
    
    let dra_path = document.getElementById('dra_path').innerHTML;
    let mask_path = document.getElementById('mask_path').innerHTML;

    if (dra_path == "" || mask_path == ""){
        append_log("Either one of the paths was not given, please make sure botht the 3DRA and MASK path are given", 'red')
        return 
    }

    append_log("Generating image x")
    let image_x = await eel.show_view(dra_path, mask_path, "z")()
    document.getElementById('imagex').src = image_x
    append_log("Finished generating image x")
    append_log("Generating image y")
    let image_y = await eel.show_view(dra_path, mask_path, "z")()
    document.getElementById('imagey').src = image_y
    append_log("Finished generating image y")
    append_log("Generating image z")
    let image_z = await eel.show_view(dra_path, mask_path, "z")()
    document.getElementById('imagez').src = image_z
    append_log("Finished generating image z")
}

async function start_process(){
    append_log("This function has not yet been impemented")
}

async function clear_log(){
    let log = await document.getElementById('log')
    while (log.firstChild){
        log.removeChild(log.lastChild)
    }
}

function append_log(text, color='black'){
    let log = document.getElementById('log')
    let new_element = document.createElement('p')
    var today = new Date();

    new_element.innerHTML = today.getHours() +":"+today.getMinutes()+":"+today.getSeconds()+":"+today.getMilliseconds() + " - " + text
    new_element.style.color = color
    log.appendChild(new_element)
}

async function file_selector(id){
    let path = await eel.file_selector()()
    document.getElementById(id).innerHTML = path 
}
