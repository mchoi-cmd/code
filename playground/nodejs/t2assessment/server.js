const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

app.use(bodyParser.json());

app.post('/cart', (req, res) => {
  // Validate the request body
  if (!req.body.items || !Array.isArray(req.body.items)) {
    return res.status(400).json({ error: 'Invalid request body' });
  }

  if (req.body.items.length === 0) {
    return res.status(400).json({ error: 'No item in cart' });
  }

  // Calculate the total price
  const cartItems = req.body.items.map(item => {
    if (!item.id || typeof item.unitPrice !== 'number' || typeof item.quantity !== 'number') {
      return res.status(400).json({ error: 'Invalid item in the request body' });
    }
    if (item.unitPrice < 0) {
      return res.status(400).json({ error: 'Unit Price is less than zero' });
    }
    if (item.quantity < 0) {
      return res.status(400).json({ error: 'Quantity is less than zero' });
    }
    return item;
  });
  const totalPrice = calculateTotalPrice(req.body.items);

  // Prepare the response
  const response = {
    items: cartItems,
    totalPrice: totalPrice
  };

  // Send the response
  res.json(response);
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

function calculateTotalPrice(items) {
  let totalPrice = 0;
  items.map(item => {
    totalPrice += item.unitPrice * item.quantity;
  });

  return totalPrice
}