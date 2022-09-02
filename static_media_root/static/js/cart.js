var updatecartbtn = document.getElementsByClassName('update_cart');

for (var i=0; i < updatecartbtn.length; i++) {
	updatecartbtn[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId: ', productId, 'action: ', action)

		console.log('user:', user)
		if(user=='AnonymousUser'){
			console.log('not logged in')
		}else{
			updateUserOrder(productId, action);
			//cartReload();
		}
	})
}


// add items to cart
function updateUserOrder(productId, action){
	console.log('sending data...')

	var url = '/update_cart/'

	fetch(url, {
		method:'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFTOKEN':csrf_token,
		},
		body:JSON.stringify({
			'productId':productId, 'action':action
		})		
	})
	.then((response) => {
		return response.json();
	})
	.then((data) =>{
		console.log('Data:', data)
	});
};



$(document).ready(function(){

	setInterval(function(){
		$.ajax({
			type:'GET',
			url: "/cartlist/",
			success: function(response){
				var cart1 = document.getElementById('cart1');
				var cart2 = document.getElementById('cart2');

				var json = response['get_cart_items'];

				console.log(json)

				cart1.innerHTML = json;

				cart2.innerHTML = cart1.innerHTML;

			},

		})

	}, 2000);
});


function cartResponse(){
	//console.log('Retreiving data...')
	var url = '/cart_response/'

	fetch(url, {
		method:'GET',
		headers:{
			'Content-Type':'application/json'
		}		
	})
	.then((response) => {
		return response.json();
	})
	.then((data) =>{
		//console.log('Data:', data)
		for (var i=0; i < data["item"].length; i++){
			console.log( data['item'][i].id)
			console.log( data['item'][i].product)
		}
		
	});
}