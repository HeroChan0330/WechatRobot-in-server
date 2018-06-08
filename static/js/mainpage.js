var port='5005';
var logined=false;
var hasQRCode=false;

function init(){
	$.get('StartRobot',{},function(data,status){
		
	});
	$("#friendSelectedBtn").click(function(){
		var friends=$(".friendItem");
		var res='';
		for(var i=0;i<friends.length;i++){
			if(friends[i].checked){
				res+=friends.eq(i).attr("name")+'|';
			}
		}
		if(res.endsWith('|'))res=res.substring(0,res.length-1);
		$.get('RobotCommand',{'command':'Listen','value':res},function(data,status){
			
		});
	});
	$("#opositeSelectedBtn").click(function(){
		var friends=$(".friendItem");
		var res='';
		for(var i=0;i<friends.length;i++){
			if(friends[i].checked){
				friends[i].checked=false;
			}
			else{
				friends[i].checked=true;
			}
		}
	});
	$("#stopListenBtn").click(function(){
		$.get('RobotCommand',{'command':'Stop'},function(data,status){
		
		});
	});
	$("#exitBtn").click(function(){
		$.get('RobotCommand',{'command':'Exit'},function(data,status){
		
		});
	});
	$("#groupMsgBtn").click(function(){
		var msg=$("#groupMsgText")[0].value;
		groupMsg(msg);
	});
	//getList();
	setInterval("update()",5000);
	login();
}
function getList(){
	$.get('RobotCommand',{'command':'GetList'},function(data,status){
		//console.log(data);
		var list=JSON.parse(data);
		
		var content='<div class="title">好友</div>';
		for(var i=0;i<list['friend'].length;i++){
			var item=list['friend'][i];
			content+='<li class="mui-table-view-cell mui-radio mui-left"><input class="friendItem" name="'
			+item['index']+'" type="radio" '
			+(item['checked']?'checked':'')
			+'>'+item['name']+'</li>';
		}
		content+='<div class="title">群组</div>';
		for(var i=0;i<list['group'].length;i++){
			var item=list['group'][i];
			content+='<li class="mui-table-view-cell mui-radio mui-left"><input class="friendItem" name="'
			+item['index']+'" type="radio" '
			+(item['checked']?'checked':'')
			+'">'+item['name']+'</li>';
		}
		//console.log(content);
		$("#friendList").html(content);
	});
}

function setInfo(res){
	$(".selfName").html(res['name']);
	var content='';
	for(var i=0;i<res['listening'].length;i++){
		content+='<li class="mui-table-view-cell">'+res['listening'][i]+'</li>';
	}
	$(".registeredList").html(content);
}

function update(){
	$.get('RobotCommand',{'command':'GetState'},function(data,status){
		var res=JSON.parse(data);
		if(res['logined']=='1'){
			setInfo(res);
		}
		else if(res['logined']=='0'){
//			alert('已退出');
//			$(".qrCodeContainer").css("display",'block');
//			$(".qrCodeContainer").attr('src','');
//			$(".qrCodeContainer").html("已退出");
			$("#friendList").html('');
		}
	});
}

function login(){
	$.get('RobotCommand',{'command':'GetState'},function(data,status){
		var res=JSON.parse(data);
		if(res['logined']=='1'){
			setInfo(res);
			getList();
			logined=true;
			$(".qrCodeContainer").css("display",'none');
		}
		else if(res['hasQRCode']=='1'){
			//console.log(res['QRCodePath']);
			$(".qrCodeContainer").attr('src',res['QRCodePath']);
			hasQRCode=true;
		}
		else{
			//setTimeout(getState,1000);
		}
	});
	if(!logined) setTimeout(login,1000);
}

function groupMsg(msg){
	$.get('RobotCommand',{'command':'GroupMsg','msg':msg},function(data,status){
		
	});
}
