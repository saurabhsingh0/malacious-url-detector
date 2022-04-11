document.addEventListener('DOMContentLoaded', function() {
    var checkPageButton = document.getElementById('clickIt');
    checkPageButton.addEventListener('click', function() {
      var inputUrl = document.getElementById("url").value;
      var baseUrl = "https://cop6f5q7xk.execute-api.us-west-2.amazonaws.com/Prod/predict?url="
      inputUrl = baseUrl.concat(inputUrl);
      fetch(inputUrl)
      .then(response => response.json())
      .then(data => {
        console.log(data.message);
        document.getElementById("result").innerHTML = data.message;
      })
      .catch(error => console.log(error));

    }, false);
  }, false);
