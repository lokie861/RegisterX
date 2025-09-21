
   // Form submission
document.getElementById("convertForm").addEventListener("submit", function(e) {
e.preventDefault();
const plc = plcTypeSelect.value;
const address = document.getElementById("address").value;
const reg_type = document.getElementById("reg_type").value;

fetch(`api/convert?plc=${encodeURIComponent(plc)}&address=${encodeURIComponent(address)}&regtype=${encodeURIComponent(reg_type)}`)
    .then(resp => resp.json())
    .then(data => {
    document.getElementById("raw-address").innerText = data.raw;
    document.getElementById("modbus-address").innerText = data.converted;
    })
    .catch(err => {
    document.getElementById("raw-addressaw").innerText = "-";
    document.getElementById("modbus-address").innerText = "Error: " + err;
    });
});

function showNotification(message, type = "success") {
    const notification = document.getElementById("notification");
    notification.innerText = message;
    notification.className = `notification show ${type}`;
    
    // Hide after 3s
    setTimeout(() => {
        notification.className = "notification";
    }, 3000);
}


function copyToClipboard(id) {
    const text = document.getElementById(id).innerText;
    navigator.clipboard.writeText(text).then(() => {
        // alert('Copied to clipboard: ' + text);
        showNotification('Copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Failed to copy!', err);
    });
}