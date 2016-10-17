
/*
functional wrapper for ajax calls 
*/
function url_fetch(url, onresponse, method='POST', async=false)
{
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function(){
    onresponse(this)
  }
  xhttp.open(method, url, async);
  return xhttp;
}


/*
Checks whether the entered details are fine and don't exist before
procceding with registration
*/
function validateRegisterForm() {
  var email = document.forms["registerForm"]["email"].value;
  var returnvalue = true;
  if (document.forms["registerForm"]["p2"].value == document.forms["registerForm"]["password"].value) {
    var fetch = url_fetch("/does_user_exist?email=" + email, function(data){
      if (data.status == 200){
          var response = JSON.parse(data.response);
          if (response['status'] != 1) {
            alert("Email account already exists");
            returnvalue = false;
          }
      }
    }, method="GET");
    fetch.send();
    return returnvalue;
  }
  return false;
}

/*
Checks whether the entered account is valid without errors, beforeLogin
procceding to login
*/
function beforeLogin() {
  var email = document.forms["loginForm"]["email"].value;
  var password = document.forms["loginForm"]["password"].value;
  var returnvalue = false;

  var fetch = url_fetch('/validate_login?email=' + email + "&password=" + password, function(data){
    if (data.status == 200) {
      var response = JSON.parse(data.response);
      if (response['status'] == 1)
        returnvalue = true;
      else
        alert(response['message']);
      console.info(response['message']);
    }
  }, "GET");
  fetch.send();
  return returnvalue;
}

var selected = "";


var options = document.getElementsByClassName("dropcon");
for (var i=0; i<options.length; i++){
  options[i].addEventListener("click", function(){
    selected = this.innerHTML;
    console.info(selected);
  });
}

function uploadfile()
{
  var data = {'file': document.getElementById("upload").value, 'recipient': selected};
  if (data['recipient'] == '')
    return alert("Please select member to send file");
  if (data['file'] == '')
    return alert("Please upload a file");
  $.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
  });
  $.ajax({
      url: '/sendfile',
      type: 'POST',
      data: data,
      async: false,
      success: function (data) {
        alert("File Sent!!");
      },
      cache: false,
      contentType: false,
      processData: false
    });
    window.location = "/home";
}