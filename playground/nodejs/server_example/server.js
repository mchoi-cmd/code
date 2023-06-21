const express = require('express')
const app = express()
const port = 3000

app.use(express.json())

// Example route that handles a GET request
app.get('/api/user/:id', (req, res) => {
  const userId = req.params.id

  // Simulating an error for demonstration purposes
  if (userId === 'error') {
    const error = new Error('User not found')
    error.status = 404
    throw error
  }

  // Simulating a successful response
  res.json({ id: userId, name: 'John Doe' })
})

app.get('/api/address/:id', (req, res) => {
  const addressId = req.params.id

  // Simulating an error for demonstration purposes
  if (addressId === 'error') {
    const error = new Error('Address not found')
    throw error
  }

  // Simulating a successful response
  res.json({ id: addressId, name: '123 Spring Ave' })
})

app.post('/api/address/:id', (req, res) => {
  const addressId = req.params.id

  // Simulating a successful response
  res.json({ id: addressId })
})

// Error handling middleware
app.use((err, req, res, next) => {
  // Default to 500 Internal Server Error if status code is not set
  const statusCode = err.status || 500

  // Log the error for debugging purposes
  console.error(err)
  console.log('Error Handling Middleware called')
  console.log('Path: ', req.path)

  // Send an error response
  res.status(statusCode).json({ error: err.message })
})

app.listen(port, () => {
  console.log(`Server listening on port ${port}`)
})
