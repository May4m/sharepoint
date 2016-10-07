function validateRegisterForm()
{
  if (document.forms["registerForm"]["password1"].value != document.forms["registerForm"]["password1"].value) {
    alert("Passwords don't match");
    return false;
  }
  return false;
}