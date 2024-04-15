function submitPrediction() {
    const symptomsInput = document.getElementById('symptomsInput').value;
    const symptomsList = symptomsInput.split(',').map(symptom => symptom.trim());
    const data = { symptoms: symptomsList };
    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        window.location.href = `/result_page?prediction=${encodeURIComponent(data.prediction)}`;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}


document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('predictionForm').addEventListener('submit', function(event) {
        event.preventDefault(); 
        submitPrediction();
    });
});

function initializeAutocomplete(symptomsList) {
    $('#symptomsInput').autocomplete({
        minLength: 0, 
        source: function(request, response) {
            const terms = splitTerms(request.term);
            const term = terms.pop().trim(); // Get the current term
            const filteredArray = symptomsList.filter(function(item) {
                return item.toLowerCase().indexOf(term.toLowerCase()) === 0;
            });
            response(filteredArray);
        },
        focus: function() {
            return false;
        },
        select: function(event, ui) {
            const terms = splitTerms(this.value);
            terms.pop();
            terms.push(ui.item.value);
            terms.push("");
            this.value = terms.join(", ");
            return false;
        }
    });
    
    function splitTerms(val) {
        return val.split(/,\s*/);
    }
}

fetch('/symptoms')
    .then(response => response.json())
    .then(symptomsList => initializeAutocomplete(symptomsList))
    .catch(error => console.error('Error fetching symptom names:', error));

