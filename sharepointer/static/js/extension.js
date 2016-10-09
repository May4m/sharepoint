
function url_fetch(url, onresponse, method='POST', async=false)
{
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function(){
    onresponse(this)
  }
  xhttp.open(method, url, async);
  return xhttp;
}

function validateRegisterForm() {
  var email = document.forms["registerForm"]["email"].value;
  var returnvalue = true;
  if (document.forms["registerForm"]["p2"].value == document.forms["registerForm"]["password"].value) {
    var fetch = url_fetch("/does_user_exist?email="+email, function(data){
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