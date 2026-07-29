document.addEventListener("DOMContentLoaded", function(){


const button=document.getElementById("toggle-btn");

const sidebar=document.querySelector(".sidebar");

const overlay=document.getElementById("overlay");



if(!button || !sidebar){

    return;

}



button.addEventListener("click",function(){



if(window.innerWidth <= 768){


sidebar.classList.toggle("show");


if(overlay){

overlay.classList.toggle("show");

}


}

else{


sidebar.classList.toggle("collapsed");


}



});




if(overlay){


overlay.addEventListener("click",function(){


sidebar.classList.remove("show");

overlay.classList.remove("show");


});


}



});