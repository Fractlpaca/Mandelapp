function showSelection(num){
	var options=document.getElementsByClassName("options");
	var tabs=document.getElementsByClassName("tab");
	if(num==0){
		options[0].style.display="table";
		options[1].style.display="none";
		tabs[1].style.backgroundColor="";
		tabs[0].style.backgroundColor="#ffc24c";
	}else{
		options[1].style.display="table";
		options[0].style.display="none";
		tabs[0].style.backgroundColor="";
		tabs[1].style.backgroundColor="#ffc24c";
	}
}
