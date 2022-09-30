var city_tag_names = document.querySelector("#city-tag-names");


function switchToggle_changeBgColor(toggle_id) {
    var toggle = document.querySelector("#" + toggle_id);
    toggle.classList.toggle("bg-switchToggle-brand");
}

function sidebarButtons_animation(icon_id) {
    var icon = document.querySelector("#" + icon_id);

    if (icon.style.transform == "rotateX(180deg)")
        icon.style.transform = "rotateX(0deg)";
    else
        icon.style.transform = "rotateX(180deg)";
}


function unchecked_checkboxes(checkbox_class) {
    let checkboxes = document.getElementsByClassName(checkbox_class);

    for (let i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = false;
    }
}




function clean_city_item()
{
    // this function delete all city item elements that contains before in document
    const cities = document.getElementsByClassName("city-item");

    for(let elm of cities){
        elm.remove();
    }
}

function clean_state_item()
{
    // this function delete all state item elements that contains before in document
    const states = document.getElementsByClassName("state-item");

    for(let elm of states){
        elm.remove();
    }
}

function hidden_state_item(){
    const states = document.getElementsByClassName("state-item");
    for(let state of states){
        state.classList.add("d-none");
    }
}
function hidden_city_item(){
    const cities = document.getElementsByClassName("city-item");
    for(let city of cities){
        city.classList.add("d-none");
    }
}


// when user clock on city location in navbar
const container_city = document.getElementById("container-city");
const open_city_btn = document.getElementById("city-icon-navbar");
const back_city_btn = document.getElementById("back-to-cities-btn");



open_city_btn.addEventListener("click", function(e) {
            // delete Pervouse city in html
            clean_city_item();
            clean_state_item();
            hidden_city_item();
            // back_city_btn.classList.add("d-none");


            // request to server to get all states 
            const xhr = new XMLHttpRequest();
            const formdata = new FormData();
        
            formdata.append("csrf_token", document.getElementById("csrf_token").value);
        
            xhr.open("GET", "/states/", true);

            xhr.onreadystatechange = function(){
                if (this.readyState == 4 && this.status == 200) {
                    const response_Server = JSON.parse(this.responseText);
                    
                    // add each state to modal
                    for(let city in response_Server)
                    {
                        container_city.innerHTML += `
                        <p class="cursor-pointer state-item w-100 d-flex justify-content-between align-items-center border-bottom py-2 my-3">
                           <span class="text-black ps-3 fs-6">${city}</span>
                            <i class="text-muted bi bi-caret-left pe-3"></i>
                            <input type="hidden" name="${city}" value="${response_Server[city]}">
                        </p>
                        `;
                    }

                    const cities = document.getElementsByClassName("state-item");
                    for(let city of cities) 
                    {
                        city.addEventListener("click", (e)=>{

                            current_city = (e.currentTarget);
                            const key_city = (current_city.childNodes[5].value)

                            const xhr = new XMLHttpRequest();
                            const formdata = new FormData();

                            formdata.append("csrf_token", document.getElementById("csrf_token").value);
                            formdata.append("cities", key_city);

                            xhr.open("POST", "/state/cities/", true);
                            
                            xhr.onreadystatechange = function () {
                                if (this.readyState == 4 && this.status == 200) {
                                    const response_Server = this.responseText;
                                    // convert to actuall value
                                    const array_response = JSON.parse(response_Server);

                                    hidden_state_item();
                                    
                                    //  show all cities btn
                                    // back_city_btn.classList.remove("d-none");

                                    // replace all cities related with selected state
                                    for(let i = 0 ; i < array_response.length ;i++)
                                    {
                                        container_city.innerHTML += `
                                        <p class="cursor-pointer hover-muted rounded transition-all-1s city-item w-100 d-flex justify-content-between align-items-center border-bottom py-2 my-3">
                                            <span class="text-black ps-3 fs-6">${array_response[i]}</span>
                                            <i class="bi bi-hand-index-thumb pe-3"></i>
                                            <input type="hidden" name="${array_response[i]}" value="${array_response[i]}">
                                        </p>
                                        `;
                                    }
                                    
                                    // after put all city in modal we should put event lisiner to them
                                    const city_item = document.getElementsByClassName("city-item");
                                    for(let city of city_item)
                                    {
                                        city.addEventListener("click", (e)=>{
                                            const current_click = e.currentTarget;
                                            const city_selected = (current_click.children[2].value);
                                            
                                            const xhr = new XMLHttpRequest();
                                            const formdata = new FormData();

                                            formdata.append("user_selected_city",city_selected)
                                            console.log(document.getElementById("csrf_token"));
                                            formdata.append("csrf_token",document.getElementById("csrf_token").value)

                                            xhr.open("POST", "/user/city/", true)
                                            
                                            xhr.onreadystatechange = function(){
                                                if (this.status ==  200 && this.readyState == 4)
                                                {
                                                    // user city changed
                                                    const current_user_city = document.getElementById("current_user_city");
                                                    current_user_city.innerHTML = city_selected.trim();
                                                    const btn_close_modal = document.getElementById("btn_close_modal_city");
                                                    btn_close_modal.click();    
                                                    
                                                }
                                            }

                                            xhr.send(formdata);
                                        })
                                    }


                                }
                            }
                            xhr.send(formdata);

                        })
                    }

            }}
            xhr.send(formdata);

});



