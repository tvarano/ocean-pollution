function openNav() {
    let options = document.getElementById("options");
    options.style.width = "250px";
    options.style.paddingLeft = "5px"
    options.style.paddingRight = "5px"
  }
  
  /* Set the width of the side navigation to 0 */
  function closeNav() {
    document.getElementById("options").style.width = "0";
    options.style.paddingLeft = "0"
    options.style.paddingRight = "0"
  }

//   function submitData() {
//     let filters = $('#option-form').serializeArray()
//     console.log(filters)
//     $.post( "/", function(data) {
//         console.log(data)
//     });
//   }