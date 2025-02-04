// Get the form element
const form = document.querySelector('form');

// Add a submit event listener to the form
form.addEventListener('submit', function(event) {
  // Get the input values
  const seats = parseInt(form.elements.seats.value);
  const kms_driven = parseFloat(form.elements.kms_driven.value);
  const power = parseFloat(form.elements.owner_type.value);
  const age = parseFloat(form.elements.age.value);
  const mileage = parseFloat(form.elements.mileage.value);
  const engine = parseFloat(form.elements.engine.value);

  // Get the select options
  const fuel_type = form.elements.fuel_type.value;
  const owner_type = form.elements.owner_type.value;
  const manufacturer = form.elements.manufacturer.value;
  const transmission = form.elements.transmission.value;



  // Check if the present price is a number
  if (isNaN(engine)) {
    alert('Please enter a valid positive Engine capacity(CC).');
    event.preventDefault();
    return false;
  }


  // Check if the mileage is a number
  if (isNaN(mileage)) {
    alert('Please enter a valid positive mileage(kmpl or km/kg).');
    event.preventDefault();
    return false;
  }


  // Check if the power is a number
  if (isNaN(power)) {
    alert('Please enter a valid positive Power(bhp).');
    event.preventDefault();
    return false;
  }


  // Check if the seats is a number
  if (isNaN(seats)) {
    alert('Please enter a valid positive number of seats.');
    event.preventDefault();
    return false;
  }



  // Check if the kilometers driven is a number
  if (isNaN(kms_driven)) {
    alert('Please enter a valid number of kilometers driven.');
    event.preventDefault();
    return false;
  }

  // Check if the past owners is a number
  if (owner_type == '') {
    alert('Please select an owner type.');
    event.preventDefault();
    return false;
  }

  // Check if the age is a number
  if (isNaN(age)) {
    alert('Please enter a valid age.');
    event.preventDefault();
    return false;
  }

  // Check if a seller type is selected
  if (manufacturer === '') {
    alert('Please select a Manufacturer.');
    event.preventDefault();
    return false;
  }

  // Check if a fuel type is selected
  if (fuel_type === '') {
    alert('Please select a fuel type.');
    event.preventDefault();
    return false;
  }

  // Check if a transmission is selected
  if (transmission === '') {
    alert('Please select a transmission.');
    event.preventDefault();
    return false;
  }
});
