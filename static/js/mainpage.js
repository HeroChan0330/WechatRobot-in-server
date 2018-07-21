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
	$("#clearSelectedBtn").click(function(){
		var friends=$(".friendItem");
		var res='';
		for(var i=0;i<friends.length;i++){
				friends[i].checked=false;
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
		var btnArray = ['否', '是'];
		mui.confirm('确认群发消息？', '微信机器人', btnArray, function(e) {
			if (e.index == 1) {
				var msg=$("#groupMsgText")[0].value;
				groupMsg(msg);
			}
		});

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
	var base = new Base64();
	$.get('RobotCommand',{'command':'GroupMsg','msg':base.encode(msg)},function(data,status){
		
	});
}




/**
*
*  Base64 encode / decode
*
*  @author haitao.tu
*  @date   2010-04-26
*  @email  tuhaitao@foxmail.com
*
*/
 
function Base64() {
 
	// private property
	_keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
 
	// public method for encoding
	this.encode = function (input) {
		var output = "";
		var chr1, chr2, chr3, enc1, enc2, enc3, enc4;
		var i = 0;
		input = _utf8_encode(input);
		while (i < input.length) {
			chr1 = input.charCodeAt(i++);
			chr2 = input.charCodeAt(i++);
			chr3 = input.charCodeAt(i++);
			enc1 = chr1 >> 2;
			enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
			enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
			enc4 = chr3 & 63;
			if (isNaN(chr2)) {
				enc3 = enc4 = 64;
			} else if (isNaN(chr3)) {
				enc4 = 64;
			}
			output = output +
			_keyStr.charAt(enc1) + _keyStr.charAt(enc2) +
			_keyStr.charAt(enc3) + _keyStr.charAt(enc4);
		}
		return output;
	}
 
	// public method for decoding
	this.decode = function (input) {
		var output = "";
		var chr1, chr2, chr3;
		var enc1, enc2, enc3, enc4;
		var i = 0;
		input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");
		while (i < input.length) {
			enc1 = _keyStr.indexOf(input.charAt(i++));
			enc2 = _keyStr.indexOf(input.charAt(i++));
			enc3 = _keyStr.indexOf(input.charAt(i++));
			enc4 = _keyStr.indexOf(input.charAt(i++));
			chr1 = (enc1 << 2) | (enc2 >> 4);
			chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
			chr3 = ((enc3 & 3) << 6) | enc4;
			output = output + String.fromCharCode(chr1);
			if (enc3 != 64) {
				output = output + String.fromCharCode(chr2);
			}
			if (enc4 != 64) {
				output = output + String.fromCharCode(chr3);
			}
		}
		output = _utf8_decode(output);
		return output;
	}
 
	// private method for UTF-8 encoding
	_utf8_encode = function (string) {
		string = string.replace(/\r\n/g,"\n");
		var utftext = "";
		for (var n = 0; n < string.length; n++) {
			var c = string.charCodeAt(n);
			if (c < 128) {
				utftext += String.fromCharCode(c);
			} else if((c > 127) && (c < 2048)) {
				utftext += String.fromCharCode((c >> 6) | 192);
				utftext += String.fromCharCode((c & 63) | 128);
			} else {
				utftext += String.fromCharCode((c >> 12) | 224);
				utftext += String.fromCharCode(((c >> 6) & 63) | 128);
				utftext += String.fromCharCode((c & 63) | 128);
			}
 
		}
		return utftext;
	}
 
	// private method for UTF-8 decoding
	_utf8_decode = function (utftext) {
		var string = "";
		var i = 0;
		var c = c1 = c2 = 0;
		while ( i < utftext.length ) {
			c = utftext.charCodeAt(i);
			if (c < 128) {
				string += String.fromCharCode(c);
				i++;
			} else if((c > 191) && (c < 224)) {
				c2 = utftext.charCodeAt(i+1);
				string += String.fromCharCode(((c & 31) << 6) | (c2 & 63));
				i += 2;
			} else {
				c2 = utftext.charCodeAt(i+1);
				c3 = utftext.charCodeAt(i+2);
				string += String.fromCharCode(((c & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
				i += 3;
			}
		}
		return string;
	}
}
