window.addEventListener('load', function () {
  Notification.requestPermission(function (status) {
    // This allows to use Notification.permission with Chrome/Safari
    if (Notification.permission !== status) {
      Notification.permission = status;
    }
  });
  // When we're using HTTPS, use WSS too.
  var ws_scheme = window.location.protocol == 'https:' ? 'wss' : 'ws';
  var notifications = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + '/notifications/' + language_code);

  notifications.onmessage = function (message) {
    var data = JSON.parse(message.data);
    addNotification(data);
  }
});


// Add new notifications
function addNotification(notification) {
  // If we have permission to show browser notifications
  // we can show the notification
  if (window.Notification && Notification.permission === 'granted') {
    data = {
      body: notification.message,
      icon: notification.icon,
      tag: 'notifications_' + language_code,
      url: notification.url
    };
    var note = new Notification(notification.title, data);
    note.onclick = function () {
      document.location = notification.url;
    }
  }
}
