# WebSocket Room Manager

This project implements a WebSocket-based Room Manager using FastAPI. It allows multiple clients to connect to a WebSocket endpoint and exchange data in real time.

## How It Works

1. **WebSocket Communication**: Clients connect to the WebSocket endpoint (`/`) and send JSON-formatted data.
2. **Room Management**: The `RoomManager` handles connecting users, broadcasting messages, and managing user disconnections.
3. **Real-Time Data**: All connected clients receive updates instantly.

---

## Video Explanation

We have created a detailed video explaining how this project works and showcasing its functionality. You can watch it here: [How It Works](https://www.youtube.com/watch?v=AOy7SsrzTCM).

---

## Project Structure

- **main.py**: The entry point of the application, containing the FastAPI WebSocket endpoint implementation.
- **space.py**: Defines the `RoomManager` class for managing connected users and broadcasting messages.

---

## Key Features

- **`@app.websocket("/")`**: Defines the WebSocket endpoint at the root path (`/`).
- **`RoomManager`**: Handles user connections, disconnections, and message broadcasting.
- **Exception Handling**: Ensures the server properly cleans up resources when a user disconnects.

---

## Running the Application

1. **Install Dependencies**:
   Make sure you have FastAPI and Uvicorn installed:
   ```bash
   pip install fastapi uvicorn
   ```

2. **Run the Server**:
   Start the FastAPI server using Uvicorn:
   ```bash
   uvicorn main:app --reload
   ```

3. **Connect to WebSocket**:
   Use a WebSocket client (e.g., a browser-based tool or a custom client) to connect to `ws://localhost:8000/`.

---

## Example Interaction

1. **Connect to WebSocket**:
   Open a WebSocket client and connect to the server.

2. **Send a Message**:
   ```json
   {"message": "Hello, World!"}
   ```

3. **Receive a Broadcast**:
   All connected clients will receive the message.

---

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a clear description of your changes.

---

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

