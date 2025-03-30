
module.exports = {
  apps: [
    {
      name: 'treats-n-more-fastapi',
      script: 'main.py',
      interpreter: 'python3.12',
      watch: true,
      autorestart: true,
      env: {
        PORT: 7013, // Change this if needed
        HOST: '0.0.0.0',  // Ensure it binds to all interfaces
        NODE_ENV: 'production'
      }
    }
  ]
};
