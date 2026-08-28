# Frontend Engineering (Member 1)

## Overview
This document explains the DISASTERVIEW frontend built with React, Vite, and Tailwind CSS.

### Key Concepts
- **React Components:** We broke the UI into reusable components (`StatCard`, `DashboardLayout`).
- **State & Hooks:** We use `useState` to store the incidents array and `useEffect` to fetch data on load and open the WebSocket connection.
- **WebSockets:** Look at `CommandCenter.tsx`. We connect to `ws://localhost:8000/ws`. When the backend detects a fire (either via AI or sensors), it broadcasts a message. The frontend receives this and instantly re-fetches incidents without a page refresh.

### Possible Judge Questions for You
**Q: Why use React instead of standard HTML/JS?**
*Answer:* React allows us to manage complex state (like a live incident feed) efficiently. When a WebSocket message arrives, React only updates the specific component that changed, making the dashboard extremely fast.

**Q: How does the map update in real-time?**
*Answer:* The map component listens to the global state (updated by WebSockets). When a new incident is added to the state array, the map re-renders the marker layer instantly.
