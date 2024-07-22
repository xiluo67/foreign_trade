// script.js

// Function to populate the currency dropdown
function populateCurrencies() {
    const currencies = [
        { code: 'GBP'},
        { code: 'HKD'},
        { code: 'USD'},
        { code: 'CHF'},
        { code: 'SGD'},
        { code: 'PKR'},
        { code: 'SEK'},
        { code: 'DKK'},
        { code: 'NOK'},
        { code: 'JPY'},
        { code: 'CAD'},
        { code: 'AUD'},
        { code: 'MYR'},
        { code: 'EUR'},
        { code: 'RUB'},
        { code: 'MOP'},
        { code: 'THB'},
        { code: 'NZD'},
        { code: 'ZAR'},
        { code: 'KZT'},
        { code: 'KRW'}
    ];

    const dropdown = document.getElementById('currency');
    currencies.forEach(currency => {
        const option = document.createElement('option');
        option.value = currency.code;
        // option.textContent = `${currency.code} (Sell Rate: ${currency.sellRate}, Buy Rate: ${currency.buyRate})`;
        option.textContent = `${currency.code}`;
        dropdown.appendChild(option);
    });
}

// Call the function to populate the currencies when the page loads
document.addEventListener('DOMContentLoaded', populateCurrencies);

// Handle form submission
document.getElementById('tradingForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way
    
    // Get form data
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const currency = document.getElementById('currency').value;
    const threshold = document.getElementById('threshold').value;

    // Create a data object
    const data = {
        name: name,
        email: email,
        currency: currency,
        threshold: threshold
    };

    // Send the data to the server
    fetch('your-backend-endpoint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        console.log('Success:', result);
        alert('Your preferences have been submitted successfully.');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('There was an error submitting your preferences.');
    });
});
