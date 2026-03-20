import { useNotificationStore } from '../store/notificationStore';

const BORDER_COLORS: Record<string, string> = {
  info: 'border-l-blue-500',
  success: 'border-l-green-500',
  warning: 'border-l-amber-500',
  error: 'border-l-red-500',
};

export default function Notifications() {
  const { notifications, removeNotification } = useNotificationStore();

  if (notifications.length === 0) return null;

  return (
    <div className="fixed bottom-4 right-4 z-50 space-y-2 max-w-sm">
      {notifications.map((notification) => (
        <div
          key={notification.id}
          className={`bg-[#1a1a1a] border border-[#2a2a2a] border-l-4 ${BORDER_COLORS[notification.type]} rounded-lg p-3 shadow-lg animate-slide-in`}
        >
          <div className="flex items-start justify-between gap-2">
            <p className="text-gray-200 text-sm">{notification.message}</p>
            <button
              onClick={() => removeNotification(notification.id)}
              className="text-gray-500 hover:text-gray-300 text-xs flex-shrink-0 cursor-pointer"
            >
              x
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
