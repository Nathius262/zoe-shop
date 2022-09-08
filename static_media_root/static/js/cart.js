//cart start

function cartResponse(){
	$(document).ready(function(){
	
		console.log('Retreiving data...')


		setInterval(function(){
			$.ajax({
				type:'GET',
				url: '/cart_response/',
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
						

						//display_image(img, 276, 110, temp.productName);
						var obj =
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


						$('#cartRep').append(obj)						
						
					}


					var	updatecartbtn = document.getElementsByClassName('update_cart')
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
							}
						})
					}
				},

			})
		}, 2000)

	

	})
}

//caet end


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

//}



$(document).ready(function(){

	setInterval(function(){
		$.ajax({
			type:'GET',
			url: "/cartlist/",
			success: function(response){
				var cart1 = document.getElementById('cart1');
				var cart2 = document.getElementById('cart2');

				var json = response['get_cart_items'];

				//console.log(json)

				cart1.innerHTML = json;

				cart2.innerHTML = cart1.innerHTML;

			},

		})

	}, 2000);

});


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