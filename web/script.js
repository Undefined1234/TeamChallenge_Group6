
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

    if (dra_path == ""){
        append_log("No DRA file was given, please select a DRA file first", 'red')
        return 
    }

    append_log("Generating image x")
    // let image_x = await eel.show_view(dra_path, mask_path, "z")()
    let datax = await eel.show_image(dra_path, "z")()
    document.getElementById('imagex').src = datax.image
    document.getElementById('slider1').max = (datax.shape-1)
    append_log("Finished generating image x")
    append_log("Generating image y")
    // let image_y = await eel.show_view(dra_path, mask_path, "z")()
    let datay = await eel.show_image(dra_path, "x")()
    document.getElementById('imagey').src = datay.image
    document.getElementById('slider2').max = (datay.shape-1)
    append_log("Finished generating image y")
    append_log("Generating image z")
    // let image_z = await eel.show_view(dra_path, mask_path, "z")()
    let dataz = await eel.show_image(dra_path, "y")()
    document.getElementById('imagez').src = dataz.image
    document.getElementById('slider3').max = (dataz.shape-1)
    append_log("Finished generating image z") 

    append_log("Adjusting sliders")

}

async function update_view(self, id, axis){
    let dra_path = document.getElementById('dra_path').innerHTML;
    let value = self.target.value
    if (dra_path != ""){
        let image = await eel.show_image(dra_path,axis, value)()
        document.getElementById(id).src = image.image
        append_log(String(value))
    }
    else{
        append_log("No image loaded", "red")
    }
        

    
}

async function start_process(){
    if (document.getElementById("dra_path").innerHTML == "" & document.getElementById("model_parameters").innerHTML == ""){
        append_log("Both the parameter file and DRA file are missing, please add them first", 'red')
        return
    }
    if (document.getElementById("model_parameters").innerHTML == ""){
        append_log("No parameter file was given, please add a parameter file first", "red")
        return
    }
    if (document.getElementById("dra_path").innerHTML == ""){
        append_log("No DRA file was given, please select a DRA file first", 'red')
    }

    await eel.start_process()()
}

async function clear_log(){
    let log = await document.getElementById('log')
    while (log.firstChild){
        log.removeChild(log.lastChild)
    }
}

eel.expose(append_log)
function append_log(text, color='black', python=false){
    let log = document.getElementById('log')
    let new_element = document.createElement('tr')
    log.appendChild(new_element)
    let new_new_element = document.createElement('th')

    var today = new Date();
    if (python){
        text = "Python Message: "+text
    }
    new_new_element.innerHTML = today.getHours() +":"+today.getMinutes()+":"+today.getSeconds()+":"+today.getMilliseconds() + " - " + text
    new_new_element.style.color = color
    new_element.appendChild(new_new_element)
    
}

eel.expose(getinnerHTML)
function getinnerHTML(id){
    return document.getElementById(id).innerHTML
}
eel.expose(getangle)
function getangle(){
    return document.getElementById("angle").value
}

async function file_selector(self, id, parameters=false){
    let path
    if (parameters==true) {
        path = await eel.file_selector(parameters)()
    }
    else {
        path = await eel.file_selector()()
    }
    
    document.getElementById(id).innerHTML = path;

    if (path != ""){
        self.style.background = 'green'
        append_log("The following path was found and loaded: "+path)
    }
}

const sl1 = document.getElementById("slider1")
sl1.addEventListener('click', (evt) => {
    update_view(evt, "imagex", "z")
    
})
const sl2 = document.getElementById("slider2")
sl2.addEventListener('click', (evt) => {
    update_view(evt, "imagey", "x")
    
})
const sl3 = document.getElementById("slider3")
sl3.addEventListener('click', (evt) => {
    update_view(evt, "imagez", "y")
    
})
