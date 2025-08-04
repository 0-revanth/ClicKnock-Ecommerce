let cartBtns = document.getElementsByClassName('cart-btn');

for (let i = 0; i < cartBtns.length; i++) {
  cartBtns[i].addEventListener('click', function () {
    let productId = this.dataset.product;
    let action = this.dataset.action;

    if (user !== 'AnonymousUser') {
      updateUserOrder(productId, action);
    } else {
      alert("Please log in to add items to the cart.");
    }
  });
}

function updateUserOrder(productId, action) {
  const url = '/update_item/';

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({ 'productId': productId, 'action': action })
  })
  .then((response) => response.json())
  .then((data) => {
    showPopup(action);

    if (action === 'add') {
      setTimeout(() => {
        location.reload();
      }, 600);
    }
  })
  .catch(error => console.error('Error:', error));
}

function showPopup(action) {
  if (action === 'add') {
    const popup = document.getElementById('popup');
    if (popup) {
      popup.style.display = 'block';
      setTimeout(() => {
        popup.style.display = 'none';
      }, 1500);
    }
  }
}
