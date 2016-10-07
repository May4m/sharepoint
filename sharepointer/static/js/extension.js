function validateRegisterForm()
{
  if (document.forms["registerForm"]["p2"].value == document.forms["registerForm"]["password"].value)
    return true;
  alert("Passwords don't match");
  return false;
}