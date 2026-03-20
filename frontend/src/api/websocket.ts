type MessageHandler = (data: any) => void;

class GameWebSocket {
  private ws: WebSocket | null = null;
  private gameId: number | null = null;
  private handlers: Map<string, Set<MessageHandler>> = new Map();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 10;
  private reconnectTimeout: ReturnType<typeof setTimeout> | null = null;

  connect(gameId: number) {
    this.gameId = gameId;
    this.reconnectAttempts = 0;
    this._connect();
  }

  private _connect() {
    if (!this.gameId) return;

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = 'localhost:8000';
    this.ws = new WebSocket(`${protocol}//${host}/ws/games/${this.gameId}/`);

    this.ws.onopen = () => {
      console.log(`WebSocket connected to game ${this.gameId}`);
      this.reconnectAttempts = 0;
    };

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        const handlers = this.handlers.get(data.type);
        if (handlers) {
          handlers.forEach(handler => handler(data));
        }
        // Also fire a wildcard handler
        const wildcardHandlers = this.handlers.get('*');
        if (wildcardHandlers) {
          wildcardHandlers.forEach(handler => handler(data));
        }
      } catch (e) {
        console.error('WebSocket message parse error:', e);
      }
    };

    this.ws.onclose = () => {
      console.log('WebSocket disconnected');
      this._attemptReconnect();
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  private _attemptReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      return;
    }
    const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
    this.reconnectAttempts++;
    console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);
    this.reconnectTimeout = setTimeout(() => this._connect(), delay);
  }

  disconnect() {
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
    }
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.gameId = null;
    this.handlers.clear();
  }

  on(type: string, handler: MessageHandler) {
    if (!this.handlers.has(type)) {
      this.handlers.set(type, new Set());
    }
    this.handlers.get(type)!.add(handler);
    return () => {
      this.handlers.get(type)?.delete(handler);
    };
  }

  send(data: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }
}

export const gameWebSocket = new GameWebSocket();
export default gameWebSocket;
