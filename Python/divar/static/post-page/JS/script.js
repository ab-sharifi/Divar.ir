
function show_contact(email){
    
let show = `
<div class="accordion" id="info-user">
    
<div class="d-flex justify-content-between align-items-center my-4">
  <div class="w-auto ">

    <div>
      <a href="" role="button" id="contact_btn" 
      data-bs-toggle="collapse" role="button" data-bs-target="#user-info-open" 
        class="responsive-btn btn btn-brand btn-cs px-lg-2 px-md-4 fs-11  px-4 text-white text-brand-hover">اطلاعات
        تماس
      </a>

      <a href=""
      class="responsive-btn btn btn-brand btn-cs px-lg-4 px-md-5 px-4 fs-11 text-brand bg-white btn-outline-brand">چت
      </a>
    </div>

  </div>
  <div class="w-auto pe-2">
    <a href="#" class="icon-save-share text-muted p-2 "><i class="fs-10 bi bi-share-fill"></i></a>
  </div>
</div>
  <div class="collapse" id="user-info-open" data-parent="#info-user">
    <div id="user-information">
      <div class="my-3 add-information d-flex justify-content-between align-items-center">
        <div>
        <span class="text-muted">
        ایمیل
        </span>
        </div>
        <div>
          <span id="call_number" class="text-brand">${email}</span>
          <i id="save-cliboard" class="text-muted bi bi-clipboard2 cursor-pointer icon-save-share"></i>
        </div>
      </div>
      <div class="bg-info-light px-1 py-2 my-3 rounded fs-8 text-muted ">
        <span>
          هشدار پلیس
        </span>
        <br>
        <br>
        <p>
        لطفاً پیش از انجام معامله و هر نوع پرداخت وجه، از صحت کالا یا خدمات ارائه‌شده، به‌صورت حضوری اطمینان حاصل نمایید.
        </p>
      </div>
    </div>
  </div>
</div>
`;
    document.getElementById("conatiner_accordion").innerHTML = show;
}

const contact_btn = document.getElementById("contact_btn");
if (contact_btn != null) 
{
contact_btn.addEventListener("click", (e)=>{
    const agree_btn = document.getElementById("agree_button");
    agree_btn.addEventListener("click", (e)=>{
        const xhr = new XMLHttpRequest();
        const formdata = new FormData();

        formdata.append("csrf_token", document.getElementById("csrf_token").value);
        formdata.append("agree","True");
        formdata.append("post-uuid",document.getElementById("post_uuid").value);
        formdata.append("post-title",document.getElementById("post-title").innerHTML);

        xhr.open("POST", "/api/divar/agree/");

        xhr.onreadystatechange = function(){
            if (this.readyState == 4 && this.status == 200)
            {
                const close =document.getElementById("close_modal_agreement");
                close.click();
                show_contact(JSON.parse(this.response)["email"]);
                
                document.getElementById("contact_btn").click();
                
                const copy_phone_number = document.getElementById("save-cliboard");
                copy_phone_number.addEventListener("click",(e)=>{
                navigator.clipboard.writeText(document.querySelector('#call_number').innerHTML);
                window.alert("متن کپی شد")
                })

            }
            // if request if failed
            if(this.readyState == 4 && this.status == 200)
             {
                // just close modal
                document.getElementById("contact_btn").click();
             }
        };

        xhr.send(formdata);

    })
})
}


const button_bookmark = document.getElementById("bookmark_button");
button_bookmark.addEventListener("click", (e)=>{
    const xhr = new XMLHttpRequest();
    const formdata = new FormData();

    formdata.append("csrf_token", document.getElementById("csrf_token").value)
    formdata.append("post-uuid", document.getElementById("post_uuid").value)
    xhr.open("POST", "/api/divar/bookmark/",true);
    xhr.onreadystatechange = function(e){
      if (this.readyState == 4 && this.status == 200)
      {
        document.getElementById("container_bookmark").innerHTML = "<i class='bi bi-bookmark-fill'></i>";
      }
    }
    xhr.send(formdata);
})



