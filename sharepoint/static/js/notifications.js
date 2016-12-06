
function url_fetch(url, onresponse, method='POST', async=false) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    onresponse(this)
  }
  xhttp.open(method, url, async);
  return xhttp;
}


reference = document.getElementById("dashboard");
var displayed_notifications = [];

function view_notification(message)
{
    var div = document.createElement("div");
    var span = document.createElement("span");
    var strong = document.createElement("strong");

    // strong attributes
    strong.innerHTML = message;
    
    // span attributes
    span.setAttribute('class', 'closebtn');
    span.setAttribute("onclick", "this.parentElement.style.display='none'");
    span.innerHTML = "&times";

    // div attributes
    div.setAttribute('class', 'alert info');
    div.style.setProperty("box-shadow", "0px 5px 5px #888888");

    // add child elements
    div.appendChild(strong);
    div.appendChild(span);
    document.body.insertBefore(div, document.getElementById("dashboard"));
    reference = div;
}

function get_notifications() {
    var req = url_fetch('/get_notifications',
    function(data) {
        if (data.status == 200 && data.response.length > 0) {
            var response = JSON.parse(data.response);
            if (response['any']) {
                var notifications = response['notifications'];
                for (i = 0; i < notifications.length; i++) {
                    if (!displayed_notifications.includes(notifications[i]['notification_id'])) {
                        view_notification(notifications[i]['message']);
                        displayed_notifications.push(notifications[i]['notification_id']);
                    }
                }
            }
    }
    }, 'GET', true);
    req.send();
}


setInterval(get_notifications, 1000);