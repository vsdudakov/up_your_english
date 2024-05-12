export interface IMessage {
  id: string;
  user_name: string;
  message: string;
  // biome-ignore lint/suspicious/noExplicitAny: <explanation>
  render_message?: any; // eslint-disable-line
  timestamp: number;
}
