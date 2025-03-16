<think>
The user wants to run the frontend locally instead of in a Docker container. I'll provide instructions for setting up and running the frontend directly on their local machine.
</think>

# Running the Frontend Locally

To run the frontend locally instead of in Docker, follow these steps:

## 1. Navigate to the frontend directory

```bash
cd src/front-end
```

## 2. Install dependencies

```bash
npm install
```

## 3. Start the development server

```bash
npm run dev
```

Or if you need to specify the port:

```bash
npm run dev -- --port 30001
```

## 4. For production testing locally

```bash
# Build first
npm run build

# Serve using a local server
npx serve -s dist -l 30001
```

## 5. Setup environment variables

Create a `.env` file in your frontend directory with any needed variables:

```
VITE_API_URL=http://localhost:30000
```

This will run your frontend directly on your local machine, which can be helpful for faster development and easier debugging compared to using Docker.
