document.addEventListener('DOMContentLoaded', function() {
    var checkPageButton = document.getElementById('clickIt');
    checkPageButton.addEventListener('click', function() {
      var inputUrl = document.getElementById("url").value;
      var baseUrl = "https://t0s06c7lui.execute-api.us-west-2.amazonaws.com/Prod/predict?url="
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