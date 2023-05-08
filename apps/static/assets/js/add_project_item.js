// add_catalog_item.js
/*
document.getElementById('add-catalog-item-form').addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent form submission

  // Get form data
  var itemName = document.getElementById('item-name').value;
  var itemDescription = document.getElementById('item-description').value;

  // Create an AJAX request to send form data to the server
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/projects/add', true);
  xhr.setRequestHeader('Content-Type', 'application/json');

  // Handle the server response
  xhr.onload = function() {
    if (xhr.status === 200) {
      // Item added successfully, do something (e.g., show a success message)
      alert('Item added successfully!');
    } else {
      // Error occurred, handle it accordingly (e.g., show an error message)
      alert('Error: ' + xhr.responseText);
    }
  };

  // Send the form data as JSON to the server
  xhr.send(JSON.stringify({
    name: itemName,
    description: itemDescription
  }));
});
*/