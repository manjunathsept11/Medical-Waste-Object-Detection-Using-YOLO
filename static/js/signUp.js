$(function(){
	$('#btnSignUp').click(function(){
		alert('Reached');
		var com = $("#inputTktId").val();
		alert(com);
		$.ajax({
			url: '/PredictInstance',
			type: 'POST',
			success: function(response){
				alert(response);
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
