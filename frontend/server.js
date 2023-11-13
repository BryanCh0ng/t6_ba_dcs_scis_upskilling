const express = require('express');
const history = require('connect-history-api-fallback');
const path = require('path');
const port = process.env.PORT || 3000; // Use the desired port
const host = '0.0.0.0';

const app = express();

// Define the subdirectory path using an environment variable
const subdirectoryPath = process.env.SUBDIRECTORY_PATH || '/t6_ba_dcs_scis_upskilling';

// Serve static assets from the "dist" folder created by Vue CLI with the subdirectory path
app.use(subdirectoryPath, express.static(path.join(__dirname, 'dist')));

// Use connect-history-api-fallback to handle client-side routing
app.use(history({ 
  verbose: true,
}));

app.get('/t6_ba_dcs_scis_upskilling/*', (_req, res) => {
  console.log("send1");
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

app.get('/*', (_req, res) => {
  console.log("send2");
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

// Error handling
app.use((err, _req, res, _next) => {
  console.error(err.stack); // Log the error
  res.status(500).send('Something went wrong!'); // Send a 500 status response
});

app.listen(port, host, () => {
  console.log(`Server is running on ${host}:${port}`);
});