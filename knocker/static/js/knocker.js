window.addEventListener('load', function () {
  Notification.requestPermission(function (status) {
    // This allows to use Notification.permission with Chrome/Safari
    if (Notification.permission !== status) {
      Notification.permission = status;
    }
  });
  // When we're using HTTPS, use WSS too.
  var ws_scheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
  var notifications = new channels.WebSocketBridge();
  notifications.connect(ws_scheme + '://' + window.location.host + knocker_url + knocker_language + '/');
  notifications.listen(function(message) {
    addNotification(JSON.parse(message));
  });
});


// Add new notifications
function addNotification(notification) {
  // If we have permission to show browser notifications
  // we can show the notification
  if (window.Notification && Notification.permission === 'granted') {
    var data = {
      body: notification.message,
      icon: notification.icon,
      tag: 'notifications_' + notification.language,
      url: notification.url
    };
    var note = new Notification(notification.title, data);
    note.onclick = function () {
      document.location = notification.url;
    }
  }
}
