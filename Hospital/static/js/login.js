const loginForm = document.getElementById('loginForm');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');

loginForm.addEventListener('submit', (event) => {
  event.preventDefault();

  // Check if the username and password are valid
  const username = usernameInput.value;
  const password = passwordInput.value;

  if (username === '' || password === '') {
    alert('من فضلك أدخل اسم المستخدم وكلمة المرور');
    return;
  }

  // Send the login request to the server
  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/login/', true);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = () => {
    if (xhr.status === 200) {
      // The login was successful
      window.location.href = '/home/';
    } else {
      // The login failed
      alert('اسم المستخدم أو كلمة المرور غير صحيحة');
    }
  };
  xhr.send(`username=${username}&password=${password}`);
});
