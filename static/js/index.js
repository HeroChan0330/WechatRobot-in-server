
function init(){
	$("#submitBtn").click(function(){
		var user=$("#user")[0].value;
		var passwd=$("#passwd")[0].value;
		var salt=parseInt(Math.random()*66666666);
		passwd=user+passwd+salt.toString();
		passwd=hex_md5(passwd);
		$.post('login',{'user':user,'passwd':passwd,'salt':salt},function(data,status){
			if(data!='success')
				alert(data);
			else
				window.location='mainpage.html';
		});
	});
}
