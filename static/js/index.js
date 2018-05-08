function init(){
	$("#submitBtn").click(function(){
		var user=$("#user")[0].value;
		var passwd=$("#passwd")[0].value;
		$.post('login',{'user':user,'passwd':passwd},function(data,status){
			if(data!='success')
				alert(data);
			else
				window.location='mainpage.html';
		});
	});
}
