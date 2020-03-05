function hide(){
    var elements = document.getElementsByClassName("popupwindow");
    for(var element of elements){
        element.style.display="none";
    }
}

function showWindow(window_id){
    document.getElementById(window_id).style.display = "block";
}