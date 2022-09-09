//gobal function

function cartResponse(obj_url){
	$(document).ready(function(){
	
		console.log('Retreiving data...')
		setInterval(function(){
			$.ajax({
				type:'GET',
				url: cart_response_url,
				success: function(response){

					var cartRep = document.getElementById('cartRep')
					var c_item = document.getElementById('c_item')
					var c_total = document.getElementById('c_total')

				

					var total = response.slice(-1)[0]

					c_item.innerHTML = total.quantityTotal
					c_total.innerHTML = total.priceTotal

					$('#cartRep').empty();
					for (var i=0; i < (response.length-1); i++){
						var temp = response[i];
						var img = temp.productImage
						var obj

						if (cart_url == obj_url){
							obj =
								`
									<div class="row align-items-center text-center mb-5 border">
										<div class="col col-lg-4 d-none d-md-flex">
											<img class="cart_item_img" src="`+img+`" alt="`+temp.productName+`">
										</div>						
										<h4 class="col">`+temp.productName+`</h4>
										<h4 class="col">$`+temp.productPrice+`</h4>
										<h4 class="col">
											<div class="d-flex justify-content-center align-items-center">
												`+temp.quantity+`
												<div class="d-grid">
													<button class="btn p-0 update_cart border-0" data-product="`+temp.productId+`" data-action="add"><img width="25" src=`+arrow_up+` alt=`+arrow_up+`></button>
													<button class="btn p-0 update_cart border-0" data-product="`+temp.productId+`" data-action="remove"><img width="25" src=`+arrow_down+` alt=`+arrow_down+`></button>
												</div>
											</div>
										</h4>
										<h4 class="col">$`+temp.price+`</h4>
									</div>
								`	
						}else if (checkout_url == obj_url){
							obj =
								`
									<div class="row align-items-center text-center mb-5">
										<div class="col col-lg-4 d-none d-md-flex">
											<img class="cart_item_img" src="`+img+`" alt="`+temp.productName+`">
										</div>						
										<h5 class="col">`+temp.productName+`</h5>
										<h5 class="col">$`+temp.productPrice+`</h5>
										<h5 class="col">`+temp.quantity+`</h5>
										<h5 class="col">$`+temp.price+`</h5>
									</div>
								`	
						}

						


						$('#cartRep').append(obj)						
						
					}


					var	updatecartbtn = document.getElementsByClassName('update_cart')
					updatecart();					
				},

			})
		}, 2000)

	

	})
}

var updatecartbtn = document.getElementsByClassName('update_cart');
updatecart();

// add items to cart
function updateUserOrder(productId, action){
	console.log('sending data...')

	var url = update_cart_url

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


function updatecart(){
	for (var i=0; i < updatecartbtn.length; i++) {
	updatecartbtn[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId: ', productId, 'action: ', action)

		console.log('user:', user)
		if(user=='AnonymousUser'){
			addCookieItem(productId, action);
		}else{
			updateUserOrder(productId, action);
		}
	})
}
}


// AnonymousUsers
function addCookieItem(productId, action){
	console.log('not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
			cart[productId] = {'quantity':1}
		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){ 
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('item deleted')
			delete cart[productId];
		}
	}

	
	document.cookie = 'cart='+JSON.stringify(cart) + ";domain=;path=/"
	console.log('Cart:', cart)
}

// AnonymousUsers end

//gobal function end

$(document).ready(function(){

	setInterval(function(){
		$.ajax({
			type:'GET',
			url: cartlist_url,
			success: function(response){
				var cart1 = document.getElementById('cart1');
				var cart2 = document.getElementById('cart2');

				var json = response['get_cart_items'];

				cart1.innerHTML = json;

				cart2.innerHTML = cart1.innerHTML;

			},

		})

	}, 2000);

});

// checkout start

function shippingData(shipping, total){

	if (shipping == 'False'){
		document.getElementById('shipping_items').innerHTML = ''
		console.log(shipping)
	}

	if (user != 'AnonymousUser'){
		document.getElementById('user_info').innerHTML = '';
	}

	if (shipping == 'False' && user != 'AnonymousUser'){
		document.getElementById('form_wrapper').style.display = "none";
		document.getElementById('paypalbtn').style.display = "block";
	}


	var form =document.getElementById('form')
	form.addEventListener('submit', function(e){
		e.preventDefault()
		console.log('form submitted...')
		document.getElementById('formbtn').style.display ='none'
		document.getElementById('paypalbtn').style.display = 'block'
	})

	document.getElementById('make_pay').addEventListener('click', function(e){
		submitFormData()
	})

	function submitFormData(){
		console.log('Your payment has been submitted ')

		var userFormInfo = {
			'name': null,
			'email':null,
			'total':total,
		}

		var shippingInfo = {
			'address':null,
			'city':null,
			'state':null,
			'zipcode':null,
		}

		if (shipping != 'False'){
			shippingInfo.address = form.address.value
			shippingInfo.city = form.city.value
			shippingInfo.state = form.state.value
			shippingInfo.zipcode = form.zipcode.value

		}

		if (user == 'AnonymousUser'){
			userFormInfo.name = form.name.value
			userFormInfo.email = form.email.value
		}

		url = process_order_url

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrf_token,
			},
			body:JSON.stringify({'form':userFormInfo, 'shipping':shippingInfo})
		})
		.then((response) => response.json())
		.then((data) => {
			console.log('Success: ', data)
			alert('Tansaction completed')
			window.location.href = home_url
		})
	}
}

//checkout end

//footer start

//Get the button
let mybutton = document.getElementById("btn-back-to-top");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function () {
	scrollFunction();
};

function scrollFunction() {
	if (
		document.body.scrollTop > 20 ||
		document.documentElement.scrollTop > 20
	) {
		mybutton.style.display = "block";
	} else {
		mybutton.style.display = "none";
	}
}
// When the user clicks on the button, scroll to the top of the document
mybutton.addEventListener("click", backToTop);

function backToTop() {
	document.body.scrollTop = 0;
	document.documentElement.scrollTop = 0;
}

//footer end